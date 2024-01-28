<template>
  <div
    class="dark:bg-slate-800 dark:text-neutral-200 h-screen grid lg:grid-cols-5 grid-cols-4 relative"
  >
    <div
      class="col-span-1 lg:block hidden dark:bg-slate-800 bg-slate-200 sticky overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
      :style="{
        height: `${toastStore.height}px`,
        top: `${toastStore.navbarHeight}px`,
      }"
    >
      <div class="p-4">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold">Nhóm</h2>
          <Cog8ToothIcon
            class="w-10 p-2 dark:bg-slate-600 bg-slate-300 rounded-full cursor-pointer dark:hover:bg-slate-500 duration-75"
          />
        </div>
        <div class="relative">
          <MagnifyingGlassIcon
            class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
          />
          <!-- @keyup="getQuery" -->
          <input
            ref="input"
            type="text"
            placeholder="Tìm kiếm nhóm"
            class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
          />
        </div>
      </div>
      <div class="p-2">
        <ul class="">
          <li
            @click="getActiveTab(category.tab)"
            v-for="category in categories"
            :key="category.tab"
            class="flex gap-3 items-center hover:bg-slate-400 dark:hover:bg-slate-700 duration-75 px-4 py-2 rounded-lg cursor-pointer"
            :class="activeTab === category.tab ? 'bg-slate-700' : ''"
          >
            <NewspaperIcon
              class="w-10 p-2 bg-slate-200  rounded-full cursor-pointer duration-75"
              v-if="category.tab === 1"
              :class="activeTab === category.tab ? 'dark:bg-emerald-500' : 'dark:bg-slate-600'"
            />
            <MapIcon
              class="w-10 p-2 bg-slate-200 rounded-full cursor-pointer duration-75"
              v-if="category.tab === 2"
              :class="activeTab === category.tab ? 'dark:bg-emerald-500' : 'dark:bg-slate-600'"
            />
            <UserGroupIcon
              class="w-10 p-2 bg-slate-200 rounded-full cursor-pointer duration-75"
              v-if="category.tab === 3"
              :class="activeTab === category.tab ? 'dark:bg-emerald-500' : 'dark:bg-slate-600'"
            />
            <h3 class="font-semibold">{{ category.name }}</h3>
          </li>
        </ul>
      </div>
      <div class="p-4">
        <button
          class="px-4 py-2 w-full flex items-center justify-center gap-2 bg-slate-300 dark:bg-emerald-700/50 dark:hover:bg-emerald-400/50 rounded-lg duration-75"
        >
          <PlusIcon class="w-6 text-emerald-300" />
          <h4 class="font-semibold text-emerald-300">Tạo nhóm mới</h4>
        </button>
      </div>
      <hr class="border-slate-600 mx-4" />
      <div class="p-4">
        <h3 class="font-semibold text-lg">Nhóm do bạn quản lý</h3>
        <div
          v-for="n in 2"
          :key="n"
          class="my-2 space-y-1 py-2 px-1 dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
        >
          <div class="flex items-center gap-3">
            <img
              src="https://s3.amazonaws.com/intanibase/iad_screenshots/1951/3523/6thumb.jpg"
              alt=""
              class="h-12 w-12 rounded-xl"
            />
            <div class="space-y-2">
              <h4 class="font-semibold">Tom Group</h4>
              <h5 class="text-xs">Lần hoạt động gần nhất khoảng 1 giờ trước</h5>
            </div>
          </div>
        </div>
      </div>
      <hr class="border-slate-600 mx-4" />
      <div class="p-4">
        <div class="flex justify-between items-center">
          <h3 class="font-semibold text-lg">Nhóm bạn đã tham gia</h3>
          <h4
            class="p-2 text-emerald-500 rounded-md dark:hover:bg-slate-700 cursor-pointer duration-75"
          >
            Xem tất cả
          </h4>
        </div>
        <div
          v-for="n in 5"
          :key="n"
          class="my-2 space-y-1 py-2 px-1 dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
        >
          <div class="flex items-center gap-3">
            <img
              src="https://s3.amazonaws.com/intanibase/iad_screenshots/1951/3523/6thumb.jpg"
              alt=""
              class="h-12 w-12 rounded-xl"
            />
            <div class="space-y-2">
              <h4 class="font-semibold">Tom Group</h4>
              <h5 class="text-xs">Lần hoạt động gần nhất khoảng 1 giờ trước</h5>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="lg:col-span-4 md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative h-screen"
    >
      Hello
    </div>
  </div>
</template>

<script>
import { useToastStore } from "../stores/toast";
import { ref } from "vue";
import {
  Cog8ToothIcon,
  NewspaperIcon,
  MapIcon,
  UserGroupIcon,
  PlusIcon,
  MagnifyingGlassIcon,
} from "@heroicons/vue/20/solid";

export default {
  name: "GroupFeedView",
  components: {
    Cog8ToothIcon,
    NewspaperIcon,
    MapIcon,
    UserGroupIcon,
    PlusIcon,
    MagnifyingGlassIcon,
  },
  setup() {
    const toastStore = useToastStore();
    const categories = [
        {
          tab: 1,
          name: 'Bảng feed của bạn',
        },
        {
          tab: 2,
          name: 'Khám phá',
        },
        {
          tab: 3,
          name: 'Nhóm của bạn',
        }
      ]

    return {
      toastStore,
      categories,
    };
  },

  data(){
    return{
      activeTab: 1
    }
  },

  methods: {
    getActiveTab(tab){
      this.activeTab = tab
    }
  }
};
</script>

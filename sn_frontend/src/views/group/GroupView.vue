<template>
  <div>
    <div
      class="dark:bg-slate-800 dark:text-neutral-200 grid lg:grid-cols-5 grid-cols-4 relative"
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
                class="w-10 p-2 bg-slate-200 rounded-full cursor-pointer duration-75"
                v-if="category.tab === 1"
                :class="
                  activeTab === category.tab
                    ? 'dark:bg-emerald-500'
                    : 'dark:bg-slate-600'
                "
              />
              <MapIcon
                class="w-10 p-2 bg-slate-200 rounded-full cursor-pointer duration-75"
                v-if="category.tab === 2"
                :class="
                  activeTab === category.tab
                    ? 'dark:bg-emerald-500'
                    : 'dark:bg-slate-600'
                "
              />
              <UserGroupIcon
                class="w-10 p-2 bg-slate-200 rounded-full cursor-pointer duration-75"
                v-if="category.tab === 3"
                :class="
                  activeTab === category.tab
                    ? 'dark:bg-emerald-500'
                    : 'dark:bg-slate-600'
                "
              />
              <h3 class="font-semibold">{{ category.name }}</h3>
            </li>
          </ul>
        </div>
        <div class="p-4">
          <button
            @click="openCreateGroupModal"
            class="px-4 py-2 w-full flex items-center justify-center gap-2 bg-slate-300 dark:bg-emerald-700/50 dark:hover:bg-emerald-400/50 rounded-lg duration-75"
          >
            <PlusIcon class="w-6 text-emerald-300" />
            <h4 class="font-semibold text-emerald-300">Tạo nhóm mới</h4>
          </button>
          <CreateGroupModal
            @closeCreateGroupModal="closeCreateGroupModal"
            :show="isOpen"
          />
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
        class="lg:col-span-4 md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center pt-6 py-12 px-6"
      >
        <div v-if="activeTab === 1" class="w-[50%]">
          <div>
            <h3 class="font-semibold dark:text-neutral-400">Hoạt động gần đây</h3>
            <div v-for="n in 3" :key="n">
              <GroupPost />
            </div>
          </div>
        </div>
        <div v-if="activeTab === 2">
          <div class="mb-4">
            <h2 class="text-xl font-bold">Nhóm phổ biến ở gần bạn</h2>
            <h4>Nhóm mà mọi người tại khu vực của bạn tham gia</h4>
          </div>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="discoverGroup in discoverGroups" :key="discoverGroup.id">
              <DiscoverGroup :group="discoverGroup"/>
            </div>
          </div>
          <hr class="border-slate-600 my-8" />
          <h2 class="text-xl font-bold my-8">Gợi ý khác</h2>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="discoverGroup in discoverGroups" :key="discoverGroup.id">
              <DiscoverGroup :group="discoverGroup"/>
            </div>
          </div>
        </div>
        <div v-if="activeTab === 3" class="w-full px-12">
          <div class="mb-4">
            <h3 class="text-lg font-semibold mb-4">
              Tất cả các nhóm bạn đã tham gia ({{ yourGroups?.length }})
            </h3>
            <div class="grid grid-cols-3 gap-3 w-full">
              <div v-for="yourGroup in yourGroups" :key="yourGroup.id">
                <YourGroup :yourGroup="yourGroup"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "../../stores/toast";
import GroupPost from "../../components/items/group/GroupPost.vue";
import DiscoverGroup from "../../components/items/group/DiscoverGroup.vue";
import YourGroup from "../../components/items/group/YourGroup.vue";

import CreateGroupModal from "../../components/modals/group/createGroup/CreateGroupModal.vue";
import {
  Cog8ToothIcon,
  NewspaperIcon,
  MapIcon,
  UserGroupIcon,
  PlusIcon,
  MagnifyingGlassIcon,
} from "@heroicons/vue/20/solid";

export default {
  name: "group",
  components: {
    Cog8ToothIcon,
    NewspaperIcon,
    MapIcon,
    UserGroupIcon,
    PlusIcon,
    MagnifyingGlassIcon,
    GroupPost,
    DiscoverGroup,
    YourGroup,
    CreateGroupModal,
  },
  setup() {
    const toastStore = useToastStore();
    const categories = [
      {
        tab: 1,
        name: "Bảng feed của bạn",
      },
      {
        tab: 2,
        name: "Khám phá",
      },
      {
        tab: 3,
        name: "Nhóm của bạn",
      },
    ];

    return {
      toastStore,
      categories,
    };
  },

  data() {
    return {
      activeTab: 1,
      isOpen: false,
      yourGroups: [],
      discoverGroups: [],
    };
  },

  methods: {
    getActiveTab(tab) {
      this.activeTab = tab;
      if (this.activeTab === 2) {
        axios
          .get("/api/group/discover/")
          .then((res) => {
            if(!res.data.message){
              this.discoverGroups = res.data
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
      if (this.activeTab === 3) {
        axios
          .get("/api/group/your-groups/")
          .then((res) => {
            if(!res.data.message){
              this.yourGroups = res.data
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    openCreateGroupModal() {
      this.isOpen = true;
    },
    closeCreateGroupModal() {
      this.isOpen = false;
    },
  },
};
</script>

<template>
  <div class="flex flex-col">
    <div class="py-2 px-4">
      <div class="flex items-center gap-2">
        <div class="flex flex-col space-y-2">
          <h1 class="font-bold text-2xl">Kết quả tìm kiếm</h1>
          <div class="flex items-center gap-2">
            <h4 class="">trong {{ group.name }}</h4>
          </div>
        </div>
      </div>
    </div>
    <div
      class="p-2 space-y-1 w-full flex flex-col justify-center"
      v-if="isUserInGroup"
    >
      <div class="relative">
        <MagnifyingGlassIcon
          class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
        />
        <form v-on:submit.prevent="submitForm">
          <input
            v-model="query"
            ref="input"
            type="text"
            placeholder="Tìm kiếm trong nhóm này"
            class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
          />
        </form>
      </div>
    </div>
    <hr class="border dark:border-slate-700 mx-4" />
    <div class="p-4">
      <h3 class="font-semibold text-lg">Bộ lọc</h3>
      <div class="pl-12 py-4 flex flex-col gap-4">
        <div class="flex justify-between items-center">
          <h4>Bài viết bạn đã xem</h4>
          <Switch
            v-model="enabled"
            :class="enabled ? 'bg-emerald-500' : 'bg-slate-700'"
            class="relative inline-flex h-[24px] w-[48px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
          >
            <span class="sr-only">Use setting</span>
            <span
              aria-hidden="true"
              :class="enabled ? 'translate-x-6' : 'translate-x-[1px]'"
              class="pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
            />
          </Switch>
        </div>
        <div class="flex justify-between items-center">
          <h4>Gần đây nhất</h4>
          <Switch
            v-model="enabled"
            :class="enabled ? 'bg-emerald-500' : 'bg-slate-700'"
            class="relative inline-flex h-[24px] w-[48px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
          >
            <span class="sr-only">Use setting</span>
            <span
              aria-hidden="true"
              :class="enabled ? 'translate-x-6' : 'translate-x-[1px]'"
              class="pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
            />
          </Switch>
        </div>
        <div class="flex justify-between items-center">
          <h4>Người đăng</h4>
          <ChevronDownIcon class="w-8" />
        </div>
        <div class="flex justify-between items-center">
          <h4>Vị trí được gắn thẻ</h4>
          <ChevronDownIcon class="w-8" />
        </div>
        <div class="flex justify-between items-center">
          <h4>Ngày đăng</h4>
          <ChevronDownIcon class="w-8" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { RouterLink, useRoute } from "vue-router";
import axios from "axios";

import {
  ChevronUpIcon,
  MagnifyingGlassIcon,
  ChevronDownIcon,
} from "@heroicons/vue/20/solid";
import { Switch } from "@headlessui/vue";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  HomeIcon,
  TableCellsIcon,
} from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    HomeIcon,
    RouterLink,
    ChevronUpIcon,
    TableCellsIcon,
    MagnifyingGlassIcon,
    Switch,
    ChevronDownIcon,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const route = useRoute();

    return {
      userStore,
      toastStore,
      route,
    };
  },

  props: {
    group: Object,
    isUserInGroup: Boolean,
  },

  data() {
    return {
      enabled: false,
      query: "",
    };
  },

  mounted() {
    this.query = this.route.query.query;
  },

  methods: {
    submitForm() {
      axios
        .post(`/api/search/group/${this.group.id}/`, {
          query: this.query,
        })
        .then((res) => {
            
          this.$router.push(
            `/groups/${this.group.id}/search/?query=${this.query}`
          );
          console.log(res.data)
        })
        .catch((error) => {
          console.log("error:", error);
        });
    },
  },
});
</script>

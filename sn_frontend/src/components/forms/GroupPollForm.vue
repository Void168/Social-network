<template>
  <div class="w-full">
    <form v-on:submit.prevent="submitForm" method="post">
      <textarea
        v-model="title"
        class="p-4 w-full bg-gray-100 rounded-lg resize-none"
        cols="30"
        rows="3"
        placeholder="Bạn đang nghĩ gì?"
      ></textarea>
      <div
        class="p-4 border dark:border-slate-600 rounded-lg dark:bg-slate-800"
      >
        <h3 class="font-semibold">Thêm cuộc thăm dò ý kiến</h3>
        <div
          class="scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 overflow-auto max-h-72"
        >
          <div
            class="flex flex-col space-y-4 p-4 w-full"
            v-for="n in amount"
            :key="n"
          >
            <div class="flex gap-2 items-center">
              <MUILikedInput
                :placeholder="`Lựa chọn ${n}`"
                class="w-full"
                v-model="options[n - 1]"
              />
              <XMarkIcon
                v-if="amount > 2"
                class="w-8 p-1 dark:bg-slate-700 rounded-full dark:hover:bg-slate-600 duration-75 cursor-pointer"
                @click="removeOption(n)"
              />
            </div>
          </div>
        </div>
        <div class="flex xm:flex-row flex-col xm:items-center items-end gap-2 w-full">
          <div
            class="px-4 py-2 dark:bg-slate-700 font-semibold dark:hover:bg-slate-600 cursor-pointer rounded-lg justify-center flex xm:items-center w-full gap-2"
            @click="addOption"
          >
            <PlusIcon class="w-5" />
            Thêm lựa chọn
          </div>
          <div
            class="relative px-4 py-2 dark:bg-slate-700 dark:hover:bg-slate-600 cursor-pointer rounded-lg"
          >
            <Cog8ToothIcon class="w-6" @click="openSetting" />
            <div
              v-if="isSettingOpen"
              class="absolute xm:w-96 z-10 xm:left-[-305px] left-[-150px] top-10 dark:bg-slate-800 xm:p-4 p-2 space-y-2 rounded-lg shadow-md"
            >
              <div class="flex justify-between items-center">
                <h4 class="break-words xm:text-base text-sm">Cho phép mọi người chọn nhiều câu trả lời</h4>
                <div
                  @click="toggleMultipleOptions"
                  class="relative xm:w-6 w-[38px] h-6 border dark:border-slate-400 rounded-full"
                >
                  <span
                    v-if="isMultipleOptions"
                    class="absolute w-4 h-4 top-[3px] left-[3px] bg-emerald-400 z-20 rounded-full"
                  ></span>
                </div>
              </div>
              <div class="flex justify-between items-center">
                <h4 class="break-words xm:text-base text-sm">Cho phép mọi người thêm lựa chọn</h4>
                <div
                  @click="toggleAddOptions"
                  class="relative xm:w-6 w-8 h-6 border dark:border-slate-400 rounded-full"
                >
                  <span
                    v-if="isAddOptions"
                    class="absolute w-4 h-4 top-[3px] left-[3px] bg-emerald-400 z-20 rounded-full"
                  ></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    <button
      @click="submitForm"
      class="w-full my-4 font-semibold py-2 rounded-lg duration-75"
      :class="
        options.includes('') || !title
          ? 'dark:bg-slate-600 text-neutral-400'
          : 'dark:bg-emerald-400 text-slate-700'
      "
      :disabled="options.includes('') || !title"
    >
      Đăng bài viết
    </button>
  </div>
</template>
<script>
import axios from "axios";
import { usePageStore } from "../../stores/page";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";
import MUILikedInput from "../input/MUILikedInput.vue";
import {
  CheckIcon,
  ChevronUpDownIcon,
  Cog8ToothIcon,
  PlusIcon,
  XMarkIcon,
} from "@heroicons/vue/20/solid";

export default {
  components: {
    CheckIcon,
    ChevronUpDownIcon,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
    MUILikedInput,
    Cog8ToothIcon,
    PlusIcon,
    XMarkIcon,
  },
  setup() {
    const pageStore = usePageStore();

    return { pageStore };
  },
  props: {
    group: Object,
    isAnonymous: Boolean,
  },
  data() {
    return {
      title: "",
      options: [],
      amount: 2,
      isSettingOpen: false,
      isMultipleOptions: true,
      isAddOptions: true,
    };
  },

  methods: {
    addOption() {
      this.amount += 1;
    },
    removeOption(index) {
      this.amount -= 1;
      this.options.splice(index, 1);
    },
    openSetting() {
      this.isSettingOpen = !this.isSettingOpen;
    },
    toggleMultipleOptions() {
      this.isMultipleOptions = !this.isMultipleOptions;
    },
    toggleAddOptions() {
      this.isAddOptions = !this.isAddOptions;
    },
    submitForm() {
      axios
        .post(`/api/posts/create-poll/group/${this.group.id}/`, {
          body: this.title,
          options: this.options,
          allow_add_option: this.isAddOptions,
          multiple_options: this.isMultipleOptions,
          is_anonymous: this.isAnonymous
        })
        .then((res) => {
          // console.log("data", res.data);
          this.body = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

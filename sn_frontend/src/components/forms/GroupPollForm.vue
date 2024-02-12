<template>
  <div class="w-full">
    <form v-on:submit.prevent="submitForm" method="post">
      <textarea
        v-model="title"
        class="p-4 w-full bg-gray-100 rounded-lg resize-none"
        cols="30"
        rows="4"
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
                v-model="option[n - 1]"
              />
              <XMarkIcon
                v-if="amount > 2"
                class="w-8 p-1 dark:bg-slate-700 rounded-full dark:hover:bg-slate-600 duration-75 cursor-pointer"
                @click="removeOption(n)"
              />
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2 w-full">
          <div
            class="px-4 py-2 dark:bg-slate-700 font-semibold dark:hover:bg-slate-600 cursor-pointer rounded-lg justify-center flex items-center w-full gap-2"
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
              class="absolute w-96 z-10 left-[-386px] top-10 dark:bg-slate-800 p-4 space-y-2 rounded-lg shadow-md"
            >
              <div class="flex justify-between items-center">
                <h4>Cho phép mọi người chọn nhiều câu trả lời</h4>
                <div
                  @click="toggleMultipleOptions"
                  class="relative w-6 h-6 border dark:border-slate-400 rounded-full"
                >
                  <span
                    v-if="isMultipleOptions"
                    class="absolute w-4 h-4 top-[3px] left-[3px] bg-emerald-400 z-20 rounded-full"
                  ></span>
                </div>
              </div>
              <div class="flex justify-between items-center">
                <h4>Cho phép mọi người thêm lựa chọn</h4>
                <div
                  @click="toggleAddOptions"
                  class="relative w-6 h-6 border dark:border-slate-400 rounded-full"
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
        option.includes('') || !title
          ? 'dark:bg-slate-600 text-neutral-400'
          : 'dark:bg-emerald-400 text-slate-700'
      "
      :disabled="option.includes('') || !title"
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
  },
  data() {
    return {
      title: "",
      option: [],
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
      this.option.splice(index, 1);
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
      // console.log("submitForm", this.body);

      let formData = new FormData();
      formData.append("image", this.$refs.file.files[0]);
      formData.append("body", this.body);

      formData.append("is_private", this.is_private);
      formData.append("only_me", this.only_me);
      axios
        .post("/api/posts/create/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          // console.log("data", res.data);
          this.body = "";
          this.$refs.file.value = null;
          this.is_private = false;
          this.only_me = false;
          this.urlPost = null;

          if (this.user) {
            this.user.posts_count += 1;
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

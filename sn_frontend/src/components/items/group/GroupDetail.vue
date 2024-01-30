<template>
  <div class="w-full flex flex-col justify-center items-center">
    <GroupHeader :group="group" />
    <div class="flex w-[80%] my-4 gap-4 px-4">
      <div class="w-[60%]">
        <div class="dark:bg-slate-700 rounded-lg px-2">
          <div class="py-4 flex items-start gap-2 p-2 rounded-lg">
            <div>
              <img
                :src="group?.admin?.get_avatar"
                alt="admin-avatar"
                class="w-10 h-10 rounded-full"
              />
            </div>
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg resize-none"
              cols="30"
              rows="4"
              placeholder="Bạn đang nghĩ gì?"
            ></textarea>
          </div>
          <hr class="mx-4 border dark:border-slate-600" />
          <div class="flex justify-center items-center gap-2 px-4 py-2">
            <div
              class="flex items-center font-medium justify-center gap-2 py-2 w-full rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
            >
              <EyeSlashIcon class="w-6 text-sky-500" />
              Bài viết ẩn danh
            </div>
            <div
              class="flex items-center font-medium justify-center gap-2 py-2 w-full rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
            >
              <PhotoIcon class="w-6 text-emerald-500" />
              Ảnh/Video
            </div>
            <div
              class="flex items-center font-medium justify-center gap-2 py-2 w-full rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
            >
              <HandRaisedIcon class="w-6 text-amber-600" />
              Thăm dò ý kiến
            </div>
          </div>
        </div>
      </div>
      <div
        class="w-[40%] sticky space-y-4"
        :style="{
          height: `${toastStore.height}px`,
          top: `${toastStore.navbarHeight}px`,
        }"
      >
        <div class="dark:bg-slate-700 rounded-lg p-4 relative">
          <XMarkIcon class="w-6 top-4 right-4 absolute" />
          <h3 class="font-semibold text-lg">
            Hãy hoàn tất quy trình thiết lập nhóm
          </h3>
          <h4 class="font-semibold">
            Đã hoàn thành <span class="text-emerald-400">0/4</span> bước
          </h4>
          <h4 class="text-neutral-400">
            Tiếp tục thêm các thông tin chính và bắt đầu tương tác với cộng đồng
            của bạn.
          </h4>
          <hr class="border m-4 dark:border-slate-600"/>
          <div class="flex flex-col w-full">
            <div class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg">
              <UserIcon class="w-8 rounded-full p-1 bg-slate-600"/>
              <h3 class="text-lg">Mời mọi người tham gia</h3>
            </div>
            <div class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg">
              <PhotoIcon class="w-8 rounded-full p-1 bg-slate-600"/>
              <h3 class="text-lg">Thêm ảnh bìa</h3>
            </div>
            <div class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg">
              <PencilIcon class="w-8 rounded-full p-1 bg-slate-600"/>
              <h3 class="text-lg">Thêm phần mô tả</h3>
            </div>
            <div class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg">
              <PencilSquareIcon class="w-8 rounded-full p-1 bg-slate-600"/>
              <h3 class="text-lg">Tạo bài viết</h3>
            </div>
          </div>
        </div>
        <div class="dark:bg-slate-700 rounded-lg p-4">
          <h2 class="text-xl font-bold">Giới thiệu</h2>
          <div class="flex gap-2" v-if="group.is_privacy_group">
            <div class="flex flex-col justify-start">
                <GlobeAsiaAustraliaIcon class="w-6"/>
            </div>
            <div>
                <h3 class="font-semibold">Công khai</h3>
                <h4>Bất kỳ ai cũng có thể nhìn thấy mọi người trong nhóm và những gì họ đăng.</h4>
            </div>
          </div>
          <div class="flex gap-2" v-else>
            <div class="flex flex-col justify-start">
                <LockClosedIcon class="w-6"/>
            </div>
            <div>
                <h3 class="font-semibold">Riêng tư</h3>
                <h4>Chỉ thành viên mới nhìn thấy mọi người trong nhóm và những gì họ đăng.</h4>
            </div>
          </div>
          <div class="flex gap-2">
            <div class="flex flex-col justify-start" v-if="group.show_group">
                <EyeIcon class="w-6"/>
            </div>
            <div class="flex flex-col justify-start" v-else>
                <EyeSlashIcon class="w-6"/>
            </div>
            <div v-if="group.show_group">
                <h3 class="font-semibold">Hiển thị</h3>
                <h4>Ai cũng có thể tìm thấy nhóm này.</h4>
            </div>
            <div v-else>
                <h3 class="font-semibold">Ẩn</h3>
                <h4>Chỉ thành viên mới tìm thấy nhóm này.</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { RouterLink } from "vue-router";

import GroupHeader from "./GroupHeader.vue";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  EyeSlashIcon,
  PhotoIcon,
  HandRaisedIcon,
  XMarkIcon,
  UserIcon,
  PencilIcon,
  PencilSquareIcon,
  EyeIcon
} from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    GroupHeader,
    EyeSlashIcon,
    PhotoIcon,
    HandRaisedIcon,
    XMarkIcon,
    UserIcon,
    PencilIcon,
    PencilSquareIcon,
    EyeIcon
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  props: {
    group: Object,
  },
  data() {
    return {
      body: "",
      step: 0,
    };
  },
});
</script>

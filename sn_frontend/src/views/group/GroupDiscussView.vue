<template>
  <div class="w-full flex flex-col justify-center items-center">
    <div class="flex w-[80%] my-4 gap-4 px-4">
      <div class="w-[60%]">
        <div v-if="isUserInGroup" class="flex flex-col space-y-4">
          <div class="dark:bg-slate-700 rounded-lg px-4">
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
            <div
              v-if="urlPost"
              class="flex relative justify-center items-center w-full p-4 border-[1px] border-slate-400 rounded-lg my-2"
            >
              <img :src="urlPost" class="w-full rounded-lg" />
              <XCircleIcon
                class="absolute top-5 right-5 cursor-pointer w-10 h-10"
                @click="removeImage"
              >
              </XCircleIcon>
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
                <label for="doc">
                  <span class="xm:text-base text-xs flex gap-2"
                    ><PhotoIcon class="w-6 text-emerald-500" />Ảnh/Video</span
                  >
                  <input
                    type="file"
                    ref="file"
                    id="doc"
                    name="doc"
                    hidden
                    @change="onFileChange"
                  />
                </label>
              </div>
              <div
                class="flex items-center font-medium justify-center gap-2 py-2 w-full rounded-lg dark:hover:bg-slate-800 cursor-pointer duration-75"
              >
                <HandRaisedIcon class="w-6 text-amber-600" />
                Thăm dò ý kiến
              </div>
            </div>
            <button
              class="w-full mb-4 font-semibold"
              :class="
                !body
                  ? 'dark:bg-slate-600 text-neutral-400 py-2 rounded-lg  duration-75'
                  : 'btn'
              "
              :disabled="!body"
            >
              Đăng bài viết
            </button>
          </div>
          <div class="flex items-center gap-2 text-emerald-500 font-bold">
            Bài viết mới nhất
            <ChevronDownIcon class="w-5"/> 
          </div>
          <div class="dark:bg-slate-700 rounded-lg px-4 h-80 flex flex-col justify-center items-center" v-if="!groupPosts.length">
            <h2 class="text-xl font-semibold">Nhóm chưa có bài viết nào.</h2> 
            <h3 class="text-lg font-semibold">Hãy đăng bài để cùng nhau thảo luận nhé.</h3> 
          </div>
          <div class="dark:bg-slate-700 rounded-lg px-4" v-else>
            Hello
          </div>
        </div>
        <div
          v-else-if="!isUserInGroup && group.is_private_group"
          class="flex flex-col justify-center items-center dark:bg-slate-700 h-[500px] rounded-lg"
        >
          <img
            src="https://th.bing.com/th/id/R.0b658885df48a3649d297aa3cb9b701c?rik=O%2bnowdCCiEHMBw&riu=http%3a%2f%2fwww.freeiconspng.com%2fuploads%2fyellow-lock-icon-1.png&ehk=vmtKzvuDRyuDCuxWRt5bkcNNyst9WtJzTsByLmk4QOI%3d&risl=&pid=ImgRaw&r=0"
            alt="lock"
            class="w-40 h-40 shadow-none"
          />
          <h2 class="font-bold text-xl dark:text-neutral-300">
            Đây là nhóm riêng tư
          </h2>
          <h3 class="text-lg dark:text-neutral-400">
            Hãy tham gia nhóm này để xem hoặc cùng thảo luận nhé.
          </h3>
        </div>
        <div v-else-if="!isUserInGroup && !group.is_private_group">Hello</div>
      </div>
      <div
        class="w-[40%] sticky space-y-4"
        :style="{
          height: `${toastStore.height}px`,
          top: `${toastStore.navbarHeight}px`,
        }"
      >
        <div
          class="dark:bg-slate-700 rounded-lg p-4 relative"
          v-if="isUserInGroup"
        >
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
          <hr class="border m-4 dark:border-slate-600" />
          <div class="flex flex-col w-full">
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
            >
              <UserIcon class="w-8 rounded-full p-1 bg-slate-600" />
              <h3 class="text-lg">Mời mọi người tham gia</h3>
            </div>
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
            >
              <PhotoIcon class="w-8 rounded-full p-1 bg-slate-600" />
              <h3 class="text-lg">Thêm ảnh bìa</h3>
            </div>
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
            >
              <PencilIcon class="w-8 rounded-full p-1 bg-slate-600" />
              <h3 class="text-lg">Thêm phần mô tả</h3>
            </div>
            <div
              class="flex items-center gap-2 p-2 dark:hover:bg-slate-800 duration-75 cursor-pointer font-semibold rounded-lg"
            >
              <PencilSquareIcon class="w-8 rounded-full p-1 bg-slate-600" />
              <h3 class="text-lg">Tạo bài viết</h3>
            </div>
          </div>
        </div>
        <div class="dark:bg-slate-700 rounded-lg p-4">
          <h2 class="text-xl font-bold">Giới thiệu</h2>
          <div class="flex gap-2" v-if="group?.is_private_group">
            <div class="flex flex-col justify-start">
              <GlobeAsiaAustraliaIcon class="w-6" />
            </div>
            <div>
              <h3 class="font-semibold">Công khai</h3>
              <h4>
                Bất kỳ ai cũng có thể nhìn thấy mọi người trong nhóm và những gì
                họ đăng.
              </h4>
            </div>
          </div>
          <div class="flex gap-2" v-else>
            <div class="flex flex-col justify-start">
              <LockClosedIcon class="w-6" />
            </div>
            <div>
              <h3 class="font-semibold">Riêng tư</h3>
              <h4>
                Chỉ thành viên mới nhìn thấy mọi người trong nhóm và những gì họ
                đăng.
              </h4>
            </div>
          </div>
          <div class="flex gap-2">
            <div class="flex flex-col justify-start" v-if="group?.show_group">
              <EyeIcon class="w-6" />
            </div>
            <div class="flex flex-col justify-start" v-else>
              <EyeSlashIcon class="w-6" />
            </div>
            <div v-if="group?.show_group">
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
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { RouterLink } from "vue-router";

import GroupHeader from "../../components/items/group/GroupHeader.vue";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  EyeSlashIcon,
  PhotoIcon,
  HandRaisedIcon,
  XMarkIcon,
  XCircleIcon,
  UserIcon,
  PencilIcon,
  PencilSquareIcon,
  EyeIcon,
  ChevronDownIcon
} from "@heroicons/vue/24/solid";
export default {
  name: "groupdiscuss",
  components: {
    RouterLink,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    GroupHeader,
    EyeSlashIcon,
    PhotoIcon,
    HandRaisedIcon,
    XMarkIcon,
    XCircleIcon,
    UserIcon,
    PencilIcon,
    PencilSquareIcon,
    EyeIcon,
    ChevronDownIcon,
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
    isUserInGroup: Boolean,
  },
  data() {
    return {
      body: "",
      step: 0,
      urlPost: null,
      groupPosts: []
    };
  },

  methods: {
    removeImage() {
      this.urlPost = null;
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.urlPost = URL.createObjectURL(file);
    },
  },
};
</script>

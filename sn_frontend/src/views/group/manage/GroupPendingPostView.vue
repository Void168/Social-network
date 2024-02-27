<template>
  <div
    class="w-full flex flex-col justify-center items-center sticky"
    :style="{
      top: `${toastStore.navbarHeight}px`,
    }"
  >
    <div
      class="w-full flex flex-col justify-center items-center mx-auto dark:bg-slate-800 bg-white"
    >
      <div class="xl:w-[60%] w-full py-6 px-4">
        <div class="flex justify-between items-center sm:flex-nowrap flex-wrap">
          <h1 class="font-bold text-2xl">
            Bài viết đang chờ &middot; {{ pendingPosts.length }}
          </h1>
          <div
            class="flex px-4 py-2 gap-2 items-center"
          >
          <button
                :disabled="!isCheckAll"
              class="px-4 py-2 shadow-md  rounded-lg font-semibold max-w-max  duration-75 sm:text-base text-xs"
              :class="isCheckAll ? 'bg-emerald-500 hover:bg-emerald-400' : 'dark:bg-slate-500 text-neutral-400 bg-slate-100'"
            >
              Phê duyệt
            </button>
            <button
            :disabled="!isCheckAll"
              class="px-4 py-2 shadow-md rounded-lg font-semibold max-w-max duration-75 sm:text-base text-xs"
              :class="isCheckAll ? 'bg-rose-500 hover:bg-rose-400' : 'dark:bg-slate-500 text-neutral-400 bg-slate-100'"
            >
              Từ chối
            </button>
          </div>
        </div>
        <div class="flex items-center gap-2 my-2">
          <div class="relative w-full">
            <MagnifyingGlassIcon
              class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
            />
            <input
              ref="input"
              type="text"
              placeholder="Tìm kiếm"
              class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
            />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h3 class="font-semibold">Mới nhất trước</h3>
            <ChevronDownIcon class="w-4" />
          </div>
        </div>
        <div class="flex items-center flex-wrap gap-2">
            <div class="relative w-8 h-8 border dark:border-slate-500 cursor-pointer p-1 rounded-full dark:hover:bg-slate-600" @click="checkAll">
                <span class="absolute w-[30px] h-[30px] bg-emerald-500 rounded-full top-0 left-0" v-if="isCheckAll"></span>
            </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold text-sm">Xóa bộ lọc</h4>
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold text-sm">Liên kết</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold text-sm">Chọn ngày</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold text-sm">Tác giả</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold text-sm">Loại nội dung</h4>
            <ChevronDownIcon class="w-4" />
          </div>
        </div>
      </div>
    </div>
    <div class="xl:w-[50%] w-full my-12 space-y-4 dark:text-neutral-200 px-4">
      <div
        v-for="post in pendingPosts"
        :key="post.id"
        class="dark:bg-slate-700 bg-white rounded-lg p-4 flex flex-col gap-2"
      >
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-2">
            <img
            loading="lazy"
              :src="post?.created_by?.information?.get_avatar"
              alt="member-avatar"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <h4 class="font-semibold">
                {{ post?.created_by?.information?.name }}
              </h4>
              <div class="flex gap-1 items-center">
                <h5 class="text-xs">
                  {{ post?.created_at_formatted }} &middot;
                </h5>
                <UserGroupIcon class="w-4" />
              </div>
            </div>
          </div>
          <EllipsisHorizontalIcon
            class="w-8 p-1 rounded-lg dark:hover:bg-slate-600 duration-75 cursor-pointer"
          />
        </div>
        <h2 class="text-2xl font-medium my-4">
            {{ post.body }}
        </h2>
        <div class="flex justify-between items-start w-full">
          <div class="flex w-full gap-3">
            <button
              @click="
                handleRequest(
                  'accepted',
                  group?.id,
                  post?.id
                )
              "
              class="px-4 py-2 shadow-md bg-emerald-500 rounded-lg font-semibold w-full hover:bg-emerald-400 duration-75 sm:text-base text-sm"
            >
              Phê duyệt
            </button>
            <button
              @click="
                handleRequest(
                  'rejected',
                  group?.id,
                  post?.id
                )
              "
              class="px-4 py-2 shadow-md bg-rose-500 rounded-lg font-semibold w-full hover:bg-rose-400 duration-75 sm:text-base text-sm"
            >
              Từ chối
            </button>
            <EllipsisHorizontalIcon
              class="w-24 p-1 shadow-md dark:bg-slate-800 rounded-lg font-semibold dark:hover:bg-slate-600 duration-75 cursor-pointer"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { RouterLink } from "vue-router";
import {
  ClockIcon,
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  EllipsisHorizontalIcon,
  UserGroupIcon,
} from "@heroicons/vue/24/solid";
import GroupDetailNavigation from "../../../components/items/group/GroupDetailNavigation.vue";

export default {
  name: "groupjoinrequest",
  components: {
    ClockIcon,
    AdjustmentsHorizontalIcon,
    ChevronDownIcon,
    MagnifyingGlassIcon,
    EllipsisHorizontalIcon,
    RouterLink,
    GroupDetailNavigation,
    UserGroupIcon,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  data() {
    return {
      group: {},
      pendingPosts: [],
      isUserInGroup: false,
      isCheckAll: false,
    };
  },

  mounted() {
    this.checkUserInGroup();
  },

  methods: {
    checkAll(){
        this.isCheckAll = !this.isCheckAll
    },
    async checkUserInGroup() {
      await axios
        .get(`/api/group/check-user/${this.$route.params.id}`)
        .then((res) => {
          if (res.data.message === "User joined the group") {
            this.isUserInGroup = true;
          } else {
            this.isUserInGroup = false;
          }
          this.getGroupDetail();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupDetail() {
      await axios
        .get(`/api/group/${this.$route.params.id}/`)
        .then((res) => {
          this.group = res.data;
          // console.log(res.data);
          this.getPendingPosts();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getPendingPosts() {
      axios
        .get(`/api/posts/group/${this.group?.id}/pending-posts/`)
        .then((res) => {
          this.pendingPosts = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleRequest(status, pk, id) {
      axios
        .post(`/api/posts/group/${pk}/pending-post/${id}/${status}/`)
        .then((res) => {
          console.log(res.data);
          this.pendingPosts.filter((post) => post.id !== id)
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

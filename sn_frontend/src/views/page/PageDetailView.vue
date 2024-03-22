<template>
  <div class="col-span-3 grid grid-cols-3 gap-4 relative">
    <div class="col-span-1 lg:block hidden"></div>
    <div class="col-span-3 grid grid-cols-3 gap-4 relative">
      <div class="relative main-left top-0 lg:col-span-1 col-span-4">
        <div class="h-[88px] frame !shadow-none"></div>
        <div
          class="px-4 pb-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col rounded-lg shadow-md overflow-hidden lg:w-full w-[90%] mx-auto"
        >
          <div class="flex justify-center items-center flex-col">
            <div
              class="icon relative w-[200px] h-[100px] bg-gray-100 dark:bg-slate-700 rounded-bl-[100px] rounded-br-[100px] before:content-[''] after:content-[''] before:absolute after:absolute before:top-0 after:top-0 before:left-[-50px] before:w-[55px] before:h-[35px] before:bg-transparent before:rounded-tr-[50px] before:shadow-[20px_-20px_0_20px_rgba(243,244,246,1)] after:right-[-50px] after:w-[55px] after:h-[35px] after:bg-transparent after:rounded-tl-[50px] after:shadow-[-20px_-20px_0_20px_rgba(243,244,246,1)] before:dark:shadow-[20px_-20px_0_20px_rgba(51,65,85,1)] after:dark:shadow-[-20px_-20px_0_20px_rgba(51,65,85,1)]"
            >
              <span
                v-if="pageStore.pageId === page.id"
                @click="openAvatarModal"
                class="mb-6 rounded-full w-8 h-8 shadow-xl absolute flex justify-center items-center top-16 right-6 z-10 bg-neutral-200 dark:bg-slate-700 hover:ring-2 hover:ring-slate-300 dark:hover:ring-slate-500 transition cursor-pointer"
              >
                <CameraIcon
                  class="dark:text-neutral-200 w-5 h-5 dark:hover:text-neutral-300 hover:text-slate-700 transition"
                />
              </span>
            </div>
            <img
            loading="lazy"
              :src="page.get_avatar"
              alt=""
              class="rounded-full w-44 h-44 shadow-xl absolute top-2"
            />
            <AvatarModal
              v-if="pageStore.pageId === page.id"
              :show="avatarIsOpen"
              @closeAvatarModal="closeAvatarModal"
            />

            <p>
              <strong class="text-2xl">{{ page.name }}</strong>
            </p>
            <p class="sm:mt-6 font-semibold sm:text-lg">{{ page.biography }}</p>
          </div>
          <RouterLink
            :to="{ name: 'pageabout', params: { id: page.id } }"
            class="mt-6 flex space-x-8"
          >
            <ul class="flex flex-col !justify-start space-y-4 text-sm">
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <div class="flex gap-1 items-center">
                  <ExclamationCircleIcon class="h-6 w-6" />
                  <span>Trang</span>
                  <span>&middot;</span>
                  <span>{{ page.page_type }}</span>
                </div>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2 font-semibold"
              >
                <UserGroupIcon class="h-6 w-6" />
                <span>{{ page.followers_count }} người theo dõi</span>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2 font-semibold"
              >
                <HandThumbUpIcon class="h-6 w-6" />
                <span>{{ page.likes_count }} lượt thích</span>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <EnvelopeIcon class="h-6 w-6" />
                <span>{{ page.email }}</span>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <ClipboardDocumentListIcon class="h-6 w-6" />
                {{ page.posts_count }} bài đăng
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
                v-if="page.location"
              >
                <MapPinIcon class="w-6 h-6 dark:text-neutral-200" />
                <p class="break-words">{{ page.location }}</p>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <ClockIcon class="w-6 h-6 dark:text-neutral-200" />
                <p class="break-words">
                  Đã tạo vào Tháng {{ page?.created_at?.slice(5, 7) }} năm
                  {{ page?.created_at?.slice(0, 4) }}
                </p>
              </li>
            </ul>
          </RouterLink>
          <RouterLink
            to="/page/edit"
            class="flex justify-center items-center w-full"
            v-if="checkCurrentUserInPage && pageStore.pageId"
          >
            <button class="mt-4 btn lg:min-w-min xs:min-w-full">
              Chỉnh sửa chi tiết
            </button>
          </RouterLink>
        </div>
        <div
          class="lg:sticky !shadow-none"
          :style="{ top: `${toastStore.navbarHeight}px` }"
        >
          <div
            class="bg-white dark:bg-slate-600 dark:text-neutral-200 my-4 p-4"
          >
            <div class="flex justify-between items-center mb-4">
              <p class="font-bold xs:text-2xl text-xl">Ảnh</p>
              <RouterLink :to="{ name: 'pagephotos', params: { id: page.id } }">
                <p class="xs:text-lg hover:underline cursor-pointer">
                  Xem tất cả ảnh
                </p>
              </RouterLink>
            </div>
            <div class="grid grid-cols-3 gap-1">
              <div v-for="image in images" v-bind:key="image.id">
                <ImageShowcase v-bind:post="image" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="main-center lg:col-span-2 col-span-4 space-y-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 p-4"
        id="profile-frame"
      >
        <div
          v-if="checkCurrentUserInPage && pageStore.pageId"
          class="p-4 bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
        >
          <PostForm :user="user" :posts="posts" :page="page" />
        </div>
        <p class="font-semibold xm:text-2xl text-xl">Bài viết của {{ page.name }}</p>
        <div v-if="posts?.length">
          <div
            class="bg-white border border-gray-200 rounded-lg mt-4 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200"
            v-for="post in posts"
            v-bind:key="post.id"
          >
            <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
          </div>
          <SkeletonLoadingPost
            v-show="!loadMore"
            v-if="posts.length !== postsList.length"
          />
        </div>
        <p v-else class="text-center text-lg">
          {{ user.name }} Chưa có bài viết nào
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { usePageStore } from "../../stores/page";
import { defineAsyncComponent } from 'vue';

import {
  CameraIcon,
  ExclamationCircleIcon,
  UserGroupIcon,
  HandThumbUpIcon,
  EnvelopeIcon,
  ClipboardDocumentListIcon,
  MapPinIcon,
  ClockIcon,
} from "@heroicons/vue/24/solid";
import AvatarModal from "../../components/modals/profile/AvatarModal.vue";
import ImageShowcase from "../../components/items/profile/ImageShowcase.vue";
import FeedItem from "../../components/items/post/FeedItem.vue";
import SkeletonLoadingPost from "../../components/loadings/SkeletonLoadingPost.vue";
import PostForm from "../../components/forms/PostForm.vue";

export default {
  name: "pagedetail",
  components: {
    CameraIcon,
    ExclamationCircleIcon,
    UserGroupIcon,
    HandThumbUpIcon,
    EnvelopeIcon,
    ClipboardDocumentListIcon,
    MapPinIcon,
    ClockIcon,
    AvatarModal,
    ImageShowcase,
    FeedItem,
    SkeletonLoadingPost,
    PostForm,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore();

    return {
      userStore,
      toastStore,
      pageStore,
    };
  },

  props: {
    user: Object,
    page: Object,
    images: Array,
    posts: Array,
    postsList: Array,
    pageLikes: Array,
    pageFollowers: Array,
    PostToShow: Number,
  },

  data() {
    return {
      avatarIsOpen: false,
      loadMore: false,
    };
  },

  computed: {
    checkCurrentUserInPage() {
      return this.pageStore.pagesList
        .map((page) => page.id)
        .includes(this.$route.params.id);
    },
  },

  mounted(){
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  methods: {
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },
    openAvatarModal() {
      this.avatarIsOpen = true;
    },
    closeAvatarModal() {
      this.avatarIsOpen = false;
    },
    infinateScroll() {
      const frame = document.getElementById("profile-frame");
      let height = frame.scrollHeight;
      let scrollY = window.scrollY;
      if (height < scrollY + 800) {
        setTimeout(() => {
          this.loadMore = true;
        }, 1000);
        if (this.loadMore === true) {
          const newPosts = this.postsList.slice(
            this.posts.length,
            this.posts.length + this.PostToShow
          );
          this.posts.push(...newPosts);
        }
      } else {
        this.loadMore = false;
      }
    },
  },
};
</script>

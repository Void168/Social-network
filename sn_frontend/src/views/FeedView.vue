<template>
  <div
    class="grid lg:grid-cols-8 xs:grid-cols-3 gap-4 min-h-screen relative"
    id="feed-frame"
  >
    <div class="col-span-2 lg:block hidden">
      <Suspense>
        <div
          class="overflow-y-scroll sticky scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 dark:scrollbar-track-slate-800"
          :style="{
            height: `${toastStore.height}px`,
            top: `${toastStore.navbarHeight}px`,
          }"
        >
          <ul class="w-full">
            <div
              @click="redirectToProfile"
              class="flex gap-3 w-full items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl duration-75"
            >
              <img
                loading="lazy"
                :src="
                  pageStore.pageId
                    ? pageStore.pageActive.get_avatar
                    : userStore.user.avatar
                "
                alt=""
                class="w-12 h-12 rounded-full"
              />
              <h3 class="dark:text-white font-semibold">
                {{
                  pageStore.pageId
                    ? pageStore.pageActive.name
                    : userStore.user.name
                }}
              </h3>
            </div>
            <li
              v-for="nav in !pageStore?.pageId
                ? navigation.slice(0, navigationsShow)
                : navigation
                    .slice(0, navigationsShow)
                    .filter((nav) => nav.for === 'both')"
              :key="nav.icon"
            >
              <RouterLink
                :to="nav.url"
                class="flex gap-3 w-full items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
              >
                <img
                  loading="lazy"
                  :src="nav.icon"
                  alt=""
                  class="2xl:w-10 2xl:h-10 w-8 h-8 rounded-full"
                />
                <h3 class="dark:text-white font-semibold">{{ nav.name }}</h3>
              </RouterLink>
            </li>
            <li
              @click="clickLoadMoreNavigation"
              v-if="!loadMoreNavigation"
              class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
            >
              <ChevronDownIcon
                class="w-10 rounded-full p-1 bg-slate-300 dark:bg-slate-500"
              />
              <span class="font-semibold">Xem thêm</span>
            </li>
            <li
              @click="clickLoadMoreNavigation"
              v-else
              class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
            >
              <ChevronUpIcon
                class="w-10 rounded-full p-1 bg-slate-300 dark:bg-slate-500"
              />
              <span class="font-semibold">Ẩn bớt</span>
            </li>
          </ul>
          <hr class="mx-4 my-2" />
          <ul class="">
            <h2 class="mx-4 dark:text-slate-400 font-semibold text-lg">
              Lối tắt của bạn
            </h2>
            <RouterLink
              v-for="group in yourGroups"
              :key="group.id"
              :to="{
                name: 'groupdiscuss',
                params: {
                  id: group.id,
                },
              }"
              class="flex gap-3 w-full items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
            >
              <img
                loading="lazy"
                :src="group.get_cover_image"
                alt=""
                class="w-12 h-12 rounded-full"
              />
              <h3 class="dark:text-white font-semibold">
                {{ group.name }}
              </h3>
            </RouterLink>
            <li
              v-for="group in listGroups.slice(0, groupsShow)"
              :key="group.icon"
              class="flex gap-3 w-full items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
            >
              <img
                loading="lazy"
                :src="group.icon"
                alt=""
                class="2xl:w-10 2xl:h-10 w-8 h-8 rounded-full"
              />
              <h3 class="dark:text-white font-semibold">{{ group.name }}</h3>
            </li>
            <li
              @click="clickLoadMoreGroups"
              v-if="!loadMoreListGroups"
              class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
            >
              <ChevronDownIcon
                class="w-10 rounded-full p-1 bg-slate-300 dark:bg-slate-500"
              />
              <span class="font-semibold">Xem thêm</span>
            </li>
            <li
              @click="clickLoadMoreGroups"
              v-else
              class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 hover:bg-slate-300 cursor-pointer px-4 py-2 rounded-xl"
            >
              <ChevronUpIcon
                class="w-10 rounded-full p-1 bg-slate-300 dark:bg-slate-500"
              />
              <span class="font-semibold">Ẩn bớt</span>
            </li>
          </ul>
        </div>
        <template #fallback
          ><SkeletonLoadingContainer
            class="flex justify-center items-center w-full"
        /></template>
      </Suspense>
    </div>
    <div
      class="sm:ml-5 sm:mx-5 main-center !shadow-none lg:col-span-4 sm:col-span-2 col-span-3 space-y-4 xm:py-6"
    >
      <div
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 xm:rounded-lg overflow-x-hidden"
        :style="{maxWidth: `${toastStore.width}px`}"
      >
        <StoriesContainer />
      </div>
      <div
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
        :style="{maxWidth: toastStore.width < 320 ? `${toastStore.width}px` : '100%'}"
      >
        <PostForm v-bind:user="null" v-bind:posts="posts" @getNewPost="getNewPost"/>
        <SkeletonLoadingPostVue v-if="isLoading" />
        <div v-else>
          <div
            class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg mt-4 shadow-sm"
            v-for="post in posts"
            v-bind:key="post.id"
          >
            <FeedItem :post="post" v-on:deletePost="deletePost" />
          </div>

          <SkeletonLoadingPostVue
            v-show="!loadMore"
            v-if="posts.length !== postsList.length"
          />
          <div v-else class="flex justify-center items-center h-48">
            <p class="text-xl font-semibold">Đã tải hết bài viết</p>
          </div>
        </div>
      </div>
    </div>
    <div
      :style="{
        height: `${toastStore.height}px`,
        top: `${toastStore.navbarHeight}px`,
      }"
      class="main-right ml-auto lg:col-span-2 2xl:w-[80%] sm:col-span-1 sm:block vs:hidden space-y-4 sticky w-full"
    >
      <PeopleYouMayKnow v-if="!pageStore.pageId" />
      <Trends />
      <ChatContainer v-if="!pageStore.pageId" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { defineAsyncComponent } from "vue";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import ChatContainer from "../components/ChatContainer.vue";

import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/vue/24/solid";

import PostForm from "../components/forms/PostForm.vue";
import FeedItem from "../components/items/post/FeedItem.vue";
import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";
import { usePageStore } from "../stores/page";
import navigation from "../data/navigationBar";
import listGroups from "../data/listGroups";
import { RouterLink } from "vue-router";

import SkeletonLoadingContainer from "../components/loadings/SkeletonLoadingContainer.vue";
import SkeletonLoadingPostVue from "../components/loadings/SkeletonLoadingPost.vue";

const StoriesContainer = defineAsyncComponent({
  loader: () => import("../components/StoriesContainer.vue"),
  loadingComponent: SkeletonLoadingContainer,
  delay: 500,
  timeout: 3000,
});

export default {
  name: "FeedView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    PostForm,
    SkeletonLoadingPostVue,
    ChatContainer,
    StoriesContainer,
    ChevronUpIcon,
    ChevronDownIcon,
    RouterLink,
    SkeletonLoadingContainer,
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

  data() {
    return {
      newPost: {},
      posts: [],
      postsList: [],
      yourGroups: [],
      body: "",
      PostToShow: 5,
      loadMore: false,
      isLoading: false,
      navigation: navigation,
      listGroups: listGroups,
      loadMoreNavigation: false,
      loadMoreListGroups: false,
      navigationsShow: 7,
      groupsShow: 5,
    };
  },

  created() {
    this.getFeed();
    this.getYourGroups();
  },

  mounted() {
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  methods: {
    redirectToProfile() {
      if (this.pageStore.pageId) {
        this.$router.push(`/page/${this.pageStore.pageId}`);
      } else {
        this.$router.push(`/profile/${this.userStore.user.id}`);
      }
    },
    getNewPost(data){
      if(data.id){
        this.posts?.unshift(data)
      }
    },

    async getFeed() {
      this.isLoading = true;
      if (!this.pageStore?.pageId) {
        await axios
          .get("/api/posts/")
          .then((res) => {
            this.postsList = res.data.posts.concat(res.data.page_posts, res.data.share_posts);
            // console.log(res.data)
            this.postsList.sort(
              (a, b) => new Date(b.created_at) - new Date(a.created_at)
            );
            this.posts = this.postsList.slice(0, this.PostToShow);
            this.isLoading = false;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .get(`/api/posts/page/${this.pageStore.pageId}`)
          .then((res) => {
            const posts = res.data.posts;
            const pagePosts = res.data.page_posts;
            this.postsList = posts.concat(pagePosts);
            this.postsList.sort(
              (a, b) => new Date(b.created_at) - new Date(a.created_at)
            );
            this.posts = this.postsList.slice(0, this.PostToShow);
            this.isLoading = false;
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    async getYourGroups() {
      if (!this.pageStore?.pageId) {
        await axios
          .get("/api/group/your-groups/")
          .then((res) => {
            if (!res.data.message) {
              this.yourGroups = res.data;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },
    infinateScroll() {
      const frame = document.getElementById("feed-frame");
      let height = frame?.scrollHeight;
      let scrollY = window.scrollY;
      if (height < scrollY + 1000) {
        setTimeout(() => {
          this.loadMore = true;
        }, 1000);
        if (this.loadMore) {
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
    clickLoadMoreNavigation() {
      this.loadMoreNavigation = !this.loadMoreNavigation;
      if (this.loadMoreNavigation) {
        this.navigationsShow = this.navigation.length;
      } else {
        this.navigationsShow = 7;
      }
    },
    clickLoadMoreGroups() {
      this.loadMoreListGroups = !this.loadMoreListGroups;
      if (this.loadMoreListGroups) {
        this.groupsShow = this.listGroups.length;
      } else {
        this.groupsShow = 5;
      }
    },
  },
};
</script>

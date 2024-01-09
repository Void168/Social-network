<template>
  <div class="grid lg:grid-cols-8 xs:grid-cols-3 gap-4 min-h-screen" id="feed-frame">
    <div class="col-span-2 lg:block hidden">
      <div class="overflow-y-scroll h-[800px] sticky xl:top-[16%] md:top-[10%] z-10 scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800">
        <ul
          class="w-full"
        >
          <li
            class="flex gap-3 w-full items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <img
              :src="userStore.user.avatar"
              alt=""
              class="w-12 h-12 rounded-full"
            />
            <h3 class="dark:text-white font-semibold">
              {{ userStore.user.name }}
            </h3>
          </li>
          <li
            v-for="nav in navigation.slice(0, navigationsShow)"
            :key="nav.icon"
            class="flex gap-3 w-full items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <img :src="nav.icon" alt="" class="2xl:w-10 2xl:h-10 w-8 h-8 rounded-full" />
            <h3 class="dark:text-white font-semibold">{{ nav.name }}</h3>
          </li>
          <li
            @click="clickLoadMoreNavigation"
            v-if="!loadMoreNavigation"
            class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <ChevronDownIcon class="w-10  rounded-full p-1 bg-slate-500" />
            <span class="font-semibold">Xem thêm</span>
          </li>
          <li
            @click="clickLoadMoreNavigation"
            v-else
            class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <ChevronUpIcon class="w-10 rounded-full p-1 bg-slate-500" />
            <span class="font-semibold">Ẩn bớt</span>
          </li>
        </ul>
        <hr class="mx-4 my-2"/>
        <ul class="">
          <h2 class="mx-4 dark:text-slate-400 font-semibold text-lg">Lối tắt của bạn</h2>
          <li
            v-for="group in listGroups.slice(0, groupsShow)"
            :key="group.icon"
            class="flex gap-3 w-full items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <img :src="group.icon" alt="" class="2xl:w-10 2xl:h-10 w-8 h-8 rounded-full" />
            <h3 class="dark:text-white font-semibold">{{ group.name }}</h3>
          </li>
          <li
            @click="clickLoadMoreGroups"
            v-if="!loadMoreListGroups"
            class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <ChevronDownIcon class="w-10  rounded-full p-1 bg-slate-500" />
            <span class="font-semibold">Xem thêm</span>
          </li>
          <li
            @click="clickLoadMoreGroups"
            v-else
            class="flex gap-3 w-full dark:text-slate-200 items-center dark:hover:bg-slate-600 cursor-pointer px-4 py-2 rounded-xl"
          >
            <ChevronUpIcon class="w-10 rounded-full p-1 bg-slate-500" />
            <span class="font-semibold">Ẩn bớt</span>
          </li>
        </ul>
      </div>
    </div>
    <div class="lg:mx-auto sm:ml-5 mx-5 main-center lg:col-span-4 sm:col-span-2 col-span-3 space-y-4 py-6">
      <div
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
      >
        <StoriesContainer />
      </div>
      <div
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
      >
        <PostForm v-bind:user="null" v-bind:posts="posts" />
        <SkeletonLoadingPostVue v-if="isLoading" />
        <div v-else>
          <div
            class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg mt-4 shadow-sm"
            v-for="post in posts"
            v-bind:key="post.id"
          >
            <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
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
      class="main-right ml-auto lg:col-span-2 2xl:w-[80%] sm:col-span-1 sm:block xs:hidden space-y-4 sticky xl:top-[16%] sm:top-[10%] h-[800px] w-full"
    >
      <PeopleYouMayKnow />
      <Trends />
      <ChatContainer />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { defineAsyncComponent } from "vue";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import ChatContainer from "../components/ChatContainer.vue";
import StoriesContainer from "../components/StoriesContainer.vue";

import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/vue/24/solid";

import PostForm from "../components/forms/PostForm.vue";
import FeedItem from "../components/items/post/FeedItem.vue";
import SkeletonLoadingPostVue from "../components/loadings/SkeletonLoadingPost.vue";
import { useUserStore } from "../stores/user";
import navigation from "../data/navigationBar";
import listGroups from '../data/listGroups'

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
  },

  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      posts: [],
      postsList: [],
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

  mounted() {
    this.getFeed();
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  methods: {
    async getFeed() {
      this.isLoading = true;
      await axios
        .get("/api/posts/")
        .then((res) => {
          // console.log(res.data);
          this.postsList = res.data;
          this.posts = res.data.slice(0, this.PostToShow);
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },
    infinateScroll() {
      const frame = document.getElementById("feed-frame");
      let height = frame.scrollHeight;
      let scrollY = window.scrollY;
      if (height < scrollY + 1000) {
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

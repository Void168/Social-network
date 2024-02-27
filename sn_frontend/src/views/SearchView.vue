<template>
  <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4 min-h-screen">
    <div class="main-left sm:col-span-3 col-span-5 flex flex-col space-y-4">
      <div class="sm:hidden">
        <PeopleYouMayKnow />
        <Trends />
      </div>
      <div
        class="bg-white border border-gray-200 rounded-lg mb-4 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <form
          v-on:submit.prevent="submitForm"
          class="p-4 flex space-x-4 justify-between"
        >
          <input
            v-model="query"
            type="search"
            class="p-4 w-full bg-gray-100 dark:bg-slate-700 rounded-lg"
            placeholder="Bạn đang tìm gì?"
          />
          <div class="flex justify-center items-center">
            <button class="btn">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
                ></path>
              </svg>
            </button>
          </div>
        </form>
      </div>

      <div
        v-if="!query"
        class="bg-white border p-4 border-gray-200 rounded-lg mb-4 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <h3 class="text-lg font-semibold">Lịch sử tìm kiếm</h3>
        <div
          class="px-4 flex flex-col dark:text-neutral-200 py-2 rounded-lg dark:hover:bg-slate-700 duration-75 cursor-pointer my-4"
          v-for="keyword in keywords.slice(0, 6)"
          :key="keyword.id"
        >
          <div class="flex justify-between items-center">
            <div class="w-full">
              <div
                class="flex items-center gap-3 w-full"
                @click="searchByKeyWord(keyword)"
              >
                <ClockIcon class="w-8 p-1 dark:bg-slate-700 rounded-full" />
                <h3>{{ keyword.body }}</h3>
              </div>
            </div>
            <div @click="$emit('deleteKeyWord', keyword)">
              <XMarkIcon
                @click="deleteKeyWord(keyword)"
                class="w-8 p-1 dark:hover:bg-slate-600 rounded-full"
              />
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="users.length"
        class="p-4 bg-white border space-y-3 border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
      >
        <h1 class="text-xl font-bold">Mọi người</h1>
        <div
          class="grid xl:grid-cols-4 lg:grid-cols-3 sm:grid-cols-2 xs:grid-cols-1 gap-4"
        >
          <div
            v-for="user in users"
            v-bind:key="user.id"
            class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg shadow-md flex flex-col justify-center items-center"
          >
            <RouterLink
              :to="{ name: 'profile', params: { id: user.id } }"
              class="flex flex-col space-y-2 justify-center items-center"
            >
              <img
                loading="lazy"
                :src="user.get_avatar"
                alt=""
                class="mb-6 rounded-full w-32 h-32"
              />
              <p>
                <strong> {{ user.name }}</strong>
              </p>
              <div
                class="mt-6 flex 2xl:gap-2 justify-between gap-4 2xl:flex-col 2xl:justify-center"
              >
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.friends_count }} người bạn
                </p>
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.posts_count }} bài đăng
                </p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>

      <div
        v-if="pages.length"
        class="p-4 bg-white border space-y-3 border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
      >
        <h1 class="text-xl font-bold">Trang</h1>
        <div
          class="grid xl:grid-cols-4 lg:grid-cols-3 sm:grid-cols-2 xs:grid-cols-1 gap-4"
        >
          <div
            v-for="page in pages"
            v-bind:key="page.id"
            class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg shadow-md flex flex-col justify-center items-center"
          >
            <RouterLink
              :to="{ name: 'page', params: { id: page.id } }"
              class="flex flex-col space-y-2 justify-center items-center"
            >
              <img
                loading="lazy"
                :src="page.get_avatar"
                alt=""
                class="mb-6 rounded-full w-32 h-32"
              />
              <p>
                <strong> {{ page.name }}</strong>
              </p>
              <div
                class="mt-6 flex 2xl:gap-2 justify-between gap-4 2xl:flex-col 2xl:justify-center"
              >
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ page.followers_count }} người theo dõi
                </p>
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ page.posts_count }} bài đăng
                </p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>

      <div
        v-for="post in posts"
        v-bind:key="post.id"
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg mt-4"
      >
        <FeedItem v-bind:post="post" />
      </div>

      <div
        v-if="!users.length && !pages.length && !posts.length && isSearch"
        class="flex justify-center items-center p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg mt-4"
      >
        Không tìm thấy kết quả phù hợp
      </div>
    </div>
    <div class="main-right col-span-2 space-y-4 hidden sm:block">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import FeedItem from "../components/items/post/FeedItem.vue";

import { ClockIcon, XMarkIcon } from "@heroicons/vue/20/solid";

export default {
  name: "SearchView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    ClockIcon,
    XMarkIcon,
  },

  data() {
    return {
      query: "",
      users: [],
      posts: [],
      pages: [],
      keywords: [],
      isSearch: false
    };
  },

  watch: {
    "$route.params.id": {
      handler: function () {},
      deep: true,
      immediate: true,
    },
  },

  mounted() {
    this.getSearchKeywords();
  },

  methods: {
    async getSearchKeywords() {
      await axios
        .get("/api/search/get-key-words/")
        .then((res) => {
          this.keywords = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    createSearchKeyWord() {
      axios
        .post("/api/search/create-key-word/", {
          query: this.query,
        })
        .then((res) => {
          this.keywords = this.keywords.unshift(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    searchByKeyWord(keyword) {
      axios
        .post("/api/search/", {
          query: keyword.body,
        })
        .then((res) => {
          axios
            .post("/api/search/create-key-word/", {
              query: keyword.body,
            })
            .then((res) => {})
            .catch((error) => {
              console.log(error);
            });

          this.$router.push(`/search/?query=${keyword.body}`);
          this.users = res.data.users;
          const page_posts = res.data.page_posts;
          this.posts = res.data.posts.concat(page_posts);
          this.pages = res.data.pages;
          // console.log(page_posts)
        })
        .catch((error) => {
          console.log("error:", error);
        });
    },
    deleteKeyWord(keyword) {
      axios
        .delete(`/api/search/${keyword.id}/delete/`)
        .then((res) => {
          this.keywords = this.keywords.filter((kw) => kw.id !== keyword.id);
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitForm() {
      // console.log("submitForm", this.query);
      if (this.query) {
        axios
          .post("/api/search/", {
            query: this.query,
          })
          .then((res) => {
            this.createSearchKeyWord();
            this.isSearch = true
            this.$router.push(`/search/?query=${this.query}`);
            this.users = res.data.users;
            const page_posts = res.data.page_posts;
            this.posts = res.data.posts.concat(page_posts);
            this.pages = res.data.pages;
            // console.log(page_posts)
          })
          .catch((error) => {
            console.log("error:", error);
          });
      }
    },
  },
};
</script>

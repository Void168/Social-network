<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-3">
      <div class="bg-white border border-gray-200 rounded-lg mb-4 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200">
        <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4 justify-between">
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
        v-if="users.length"
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg grid grid-cols-4 gap-4"
      >
        <div
          v-for="user in users"
          v-bind:key="user.id"
          class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg shadow-md"
        >
          <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
            <img
              :src="user.get_avatar"
              alt=""
              class="mb-6 rounded-full w-48 h-48"
            />
            <p>
              <strong> {{ user.name }}</strong>
            </p>
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500 dark:text-neutral-200">{{user.friends_count}} người bạn</p>
              <p class="text-xs text-gray-500 dark:text-neutral-200">{{user.posts_count}} bài đăng</p>
            </div>
          </RouterLink>
        </div>
      </div>

      <div
        v-for="post in posts"
        v-bind:key="post.id"
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg mt-4"
      >
        <FeedItem v-bind:post="post" />
      </div>
    </div>
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import FeedItem from "../components/FeedItem.vue";

export default {
  name: "SearchView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
  },

  data() {
    return {
      query: "",
      users: [],
      posts: [],
    };
  },

  methods: {
    submitForm() {
      console.log("submitForm", this.query);

      axios
        .post("/api/search/", {
          query: this.query,
        })
        .then((res) => {
          console.log("response:", res.data);
          this.$router.push(`/search/?query=${this.query}`)
          this.users = res.data.users;
          this.posts = res.data.posts;
        })
        .catch((error) => {
          console.log("error:", error);
        });
    },
  },
};
</script>

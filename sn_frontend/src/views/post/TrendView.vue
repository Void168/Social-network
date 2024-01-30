<template>
  <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4 min-h-screen">
    <div class="main-center sm:col-span-3 col-span-5">
      <div class="sm:hidden">
        <PeopleYouMayKnow />
        <Trends />
      </div>
      <div class="p-4 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-500 rounded-b-lg">
        <h2 class="text-xl dark:text-slate-200">Xu hướng: #{{ $route.params.id }}</h2>
      </div>
      <div
        class="p-4 bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-500 dark:text-slate-200 rounded-lg mt-4"
        v-for="post in posts"
        v-bind:key="post.id"
      >
        <FeedItem v-bind:post="post" />
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
import PeopleYouMayKnow from "../../components/PeopleYouMayKnow.vue";
import Trends from "../../components/Trends.vue";
import FeedItem from "../../components/items/post/FeedItem.vue";

export default {
  name: "TrendView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
  },

  data() {
    return {
      posts: [],
    };
  },

  mounted() {
    this.getFeed();
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getFeed();
      },
      deep: true,
      immediate: true,
    },
  },

  methods: {
    getFeed() {
      axios
        .get(`/api/posts/posts-trend-list/?trend=${this.$route.params.id}`)
        .then((res) => {
          // console.log("data", res.data);

          this.posts = res.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

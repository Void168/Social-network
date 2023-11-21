<template>
  <div class="mr-5 p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg">
    <h3 class="mb-6 text-xl">Xu hướng</h3>

    <div class="space-y-4">
      <div
        v-for="trend in trends"
        v-bind:key="trend.id"
        class="flex items-center justify-between"
      >
        <div class="flex items-center space-x-2">
          <p class="text-xs">
            <strong>#{{ trend.hashtag }}</strong
            ><br />
            <span class="text-gray-500 dark:text-neutral-200">{{ trend.occurences }} bài viết</span>
          </p>
        </div>
        <RouterLink :to="{ name: 'trendview', params: { id: trend.hashtag } }"
          ><button type="button" class="btn btn-sm">Khám phá</button></RouterLink
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  data() {
    return {
      trends: [],
    };
  },
  mounted() {
    this.getTrends();
  },
  methods: {
    getTrends() {
      axios
        .get(`/api/posts/trends/`)
        .then((res) => {
          this.trends = res.data;
        })
        .catch((error) => console.log(error));
    },
  },
  components: { RouterLink },
});
</script>

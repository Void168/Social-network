<template>
  <div class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-l-lg">
    <h3 class="mb-6 xl:text-xl text-center">Xu hướng</h3>
    <SkeletionLoadingChatBox v-if="isLoading"/>
    <div class="space-y-4" v-else>
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
          ><button type="button" class="btn lg:py-1 lg:px-2 xl:py-2 xl:px-4">Khám phá</button></RouterLink
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { RouterLink } from "vue-router";
import SkeletionLoadingChatBox from "./loadings/SkeletionLoadingChatbox.vue"

export default (await import("vue")).defineComponent({
  data() {
    return {
      trends: [],
      isLoading: false
    };
  },
  mounted() {
    this.getTrends();
  },
  methods: {
    async getTrends() {
      await axios
        .get(`/api/posts/trends/`)
        .then((res) => {
          this.trends = res.data;
        })
        .catch((error) => console.log(error));
    },
  },
  components: { RouterLink, SkeletionLoadingChatBox },
});
</script>

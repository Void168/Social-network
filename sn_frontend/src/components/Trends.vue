<template>
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">Xu hướng</h3>

    <div class="space-y-4">
      <div
        v-for="trend in trends"
        v-bind:key="trend.id"
        class="flex items-center justify-between"
      >
        <div class="flex items-center space-x-2">
          <p class="text-xs">
            <strong>#{{ trend.hashtag }}</strong><br />
            <span class="text-gray-500">{{ trend.occurences }} bài viết</span>
          </p>
        </div>
        <a href="#"><button class="btn-sm">Khám phá</button></a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
        .get("/api/posts/trends/")
        .then((res) => {
          console.log(res.data);

          this.trends = res.data;
        })
        .catch((error) => console.log(error));
    },
  },
});
</script>

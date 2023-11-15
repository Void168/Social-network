<template>
  <div class="max-w-7xl mx-auto flex justify-center items-center gap-4">
    <div class="space-y-4 w-6/12">
      <div
        v-if="post.id"
        class="p-4 bg-white border border-gray-200 rounded-lg mt-4 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <FeedItem v-bind:post="post" />
      </div>
      <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200">
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              cols="30"
              rows="1"
              placeholder="Viết bình luận..."
            ></textarea>
          </div>

          <div class="px-4 py-2 border-t border-gray-100 flex justify-end dark:border-slate-400">
            <button class="btn">Bình luận</button>
          </div>
        </form>
      </div>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg ml-10 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <div
          v-if="!post.comments?.length"
          class="flex justify-center items-center"
        >
          Chưa có bình luận nào
        </div>
        <div
          v-else
          class="bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
          v-for="comment in post.comments.slice(0, lastComment)"
          v-bind:key="comment.id"
        >
          <CommentItem v-bind:comment="comment" />
        </div>
        <div class="flex justify-end">
          <button
            class="hover:underline transition"
            @click="loadMore"
            v-if="lastComment < post.comments.length"
          >
            Tải thêm bình luận
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import FeedItem from "../components/items/FeedItem.vue";
import CommentItem from "../components/items/CommentItem.vue";

export default {
  name: "PostView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    CommentItem,
  },

  data() {
    return {
      post: {
        id: null,
        comments: [],
      },
      lastComment: 5,
      body: "",
    };
  },

  mounted() {
    this.getPost();
  },

  methods: {
    getPost() {
      axios
        .get(`/api/posts/${this.$route.params.id}`)
        .then((res) => {
          console.log("data", res.data);

          this.post = res.data.post;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    loadMore() {
      this.lastComment = this.lastComment + 10;
      if (this.post.comments.length < this.lastComment) {
        this.lastComment = this.post.comments.length;
      }
    },

    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post(`/api/posts/${this.$route.params.id}/comment/`, {
          body: this.body,
        })
        .then((res) => {
          console.log("data", res.data);

          this.post.comments.unshift(res.data);
          this.post.comments_count += 1;
          this.body = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

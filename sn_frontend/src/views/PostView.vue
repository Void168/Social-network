<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div
        v-if="post.id"
        class="p-4 bg-white border border-gray-200 rounded-lg mt-4"
      >
        <FeedItem v-bind:post="post" />
      </div>

      <div class="p-4 bg-white border border-gray-200 rounded-lg ml-10">
        <div v-if="!post.comments?.length" class="flex justify-center items-center">Chưa có bình luận nào</div>
        <div
          v-else
          class="bg-white rounded-lg"
          v-for="comment in post.comments.reverse()"
          v-bind:key="comment.id"
        >
          <CommentItem v-bind:comment="comment" />
        </div>
      </div>
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              cols="30"
              rows="4"
              placeholder="Viết bình luận..."
            ></textarea>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-end">
            <button class="btn">Bình luận</button>
          </div>
        </form>
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
import CommentItem from "../components/CommentItem.vue";

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

    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post(`/api/posts/${this.$route.params.id}/comment/`, {
          body: this.body,
        })
        .then((res) => {
          console.log("data", res.data);

          this.post.comments.unshift(res.data);
          this.post.comments_count += 1
          this.body = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

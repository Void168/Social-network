<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <img
          src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
          alt=""
          class="mb-6 rounded-full"
        />
        <p>
          <strong class="text-2xl">{{ user.name }}</strong>
        </p>
        <div class="mt-6 flex space-x-8 justify-around">
          <p class="text-xs text-gray-500">229 người bạn</p>
          <p class="text-xs text-gray-500">168 bài đăng</p>
        </div>
      </div>
    </div>

    <div class="main-center col-span-2 space-y-4">
      <div
        v-if="userStore.user.id === user.id"
        class="p-4 bg-white border border-gray-200 rounded-lg"
      >
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              cols="30"
              rows="4"
              placeholder="Bạn đang nghĩ gì?"
            ></textarea>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <a
              href="#"
              class="inline-block py-3 px-6 bg-gray-600 text-white rounded-lg"
              >Đăng ảnh</a
            >
            <button>Đăng bài viết</button>
          </div>
        </form>

        <div
          class="p-4 bg-white border border-gray-200 rounded-lg mt-4"
          v-for="post in posts"
          v-bind:key="post.id"
        >
          <div class="mb-6 flex items-center justify-between">
            <div class="flex items-center space-x-6">
              <img
                src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
                class="w-[40px] rounded-full"
              />

              <p>
                <strong>{{ post.created_by.name }}</strong>
              </p>
            </div>

            <p class="text-gray-600">{{ post.created_at_formatted }} trước</p>
          </div>

          <p>
            {{ post.body }}
          </p>

          <!-- <img
              src="https://th.bing.com/th/id/OIP.5SOFKPjL7kQyUxxyYEk26wHaE9?pid=ImgDet&rs=1"
              class="w-full rounded-lg mt-6"
            /> -->
          <div class="my-6 flex justify-between">
            <div class="flex space-x-6">
              <div class="flex items-center space-x-2">
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
                    d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
                  />
                </svg>

                <span class="text-gray-500 text-xs">82 lượt thích</span>
              </div>

              <div class="flex items-center space-x-2">
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
                    d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"
                  />
                </svg>

                <span class="text-gray-500 text-xs">0 bình luận</span>
              </div>
            </div>

            <div>
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
                  d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"
                />
              </svg>
            </div>
          </div>
        </div>
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
import { useUserStore } from "../stores/user";

export default {
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  name: "FeedView",
  components: {
    PeopleYouMayKnow,
    Trends,
  },

  data() {
    return {
      posts: [],
      user: {},
      body: "",
    };
  },

  mounted() {
    this.getFeed();
  },

  methods: {
    async getFeed() {
      await axios
        .get(`/api/posts/profile/${this.$route.params.id}/`)
        .then((res) => {
          this.posts = res.data.posts;
          this.user = res.data.user;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post("/api/posts/create/", {
          body: this.body,
        })
        .then((res) => {
          console.log("data", res.data);

          this.posts.unshift(res.data);
          this.body = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

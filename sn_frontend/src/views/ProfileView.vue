<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        class="p-4 bg-white border border-gray-200 flex flex-col justify-center items-center rounded-lg shadow-md"
      >
        <img
          :src="user.get_avatar"
          alt=""
          class="mb-6 rounded-full w-64 h-64 shadow-md"
        />
        <p>
          <strong class="text-2xl">{{ user.name }}</strong>
        </p>
        <div class="mt-6 flex space-x-8 justify-around">
          <div>
            <p class="text-xs text-gray-500">
              {{ user.friends_count }} người bạn
            </p>
            <router-link
              :to="{ name: 'friends', params: { id: user.id } }"
              v-if="userStore.user.id === user.id"
              ><p class="text-sm mt-4">
                <span
                  class="bg-rose-400 py-1 px-[0.7rem] rounded-full font-semibold"
                  >{{ friendshipRequest.length }}</span
                >
                lời mời kết bạn mới
              </p></router-link
            >
          </div>

          <p class="text-xs text-gray-500">{{ user.posts_count }} bài đăng</p>
        </div>
        <div class="flex flex-col mt-4">
          <div v-if="userStore.user.id !== user.id" class="mt-6">
            <button
              v-if="status === 'request already sent'"
              @click="sendFriendshipRequest"
            >
              Đã gửi lời mời kết bạn
            </button>
            <button v-else @click="sendFriendshipRequest">Thêm bạn bè</button>
          </div>
          <RouterLink v-else to="/profile/edit">
            <button @click="edit">Sửa thông tin</button>
          </RouterLink>
        </div>

        <button
          v-if="userStore.user.id !== user.id"
          @click="sendDirectMessage"
          class="mt-6 bg-violet-400 hover:bg-violet-600"
        >
          Nhắn tin
        </button>
        <button
          v-else
          @click="logout"
          class="mt-6 bg-gray-400 hover:bg-gray-600"
        >
          Đăng xuất
        </button>
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
            <div
              id="preview"
              v-if="url"
              class="flex relative justify-center items-center w-full p-4 border-[1px] rounded-lg"
            >
              <img :src="url" class="w-full rounded-lg" />
              <span class="absolute top-5 right-5 cursor-pointer" @click="removeImage"
                ><svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="w-8 h-8"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </span>
            </div>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <label for="doc">
              <div
                class="py-3 px-6 text-black bg-gray-400 font-semibold rounded-lg transition-colors hover:bg-gray-600 hover:text-white cursor-pointer"
              >
                <span>Chọn ảnh</span>
              </div>
              <input
                type="file"
                ref="file"
                id="doc"
                name="doc"
                hidden
                @change="onFileChange"
              />
            </label>

            <button>Đăng bài viết</button>
          </div>
        </form>

        <div
          class="p-4 bg-white border border-gray-200 rounded-lg mt-4"
          v-for="post in posts"
          v-bind:key="post.id"
        >
          <FeedItem v-bind:post="post" />
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
import FeedItem from "../components/FeedItem.vue";
import { RouterLink } from "vue-router";

import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";

export default {
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  name: "FeedView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    RouterLink,
  },

  data() {
    return {
      posts: [],
      user: {
        id: null,
      },
      body: "",
      friendshipRequest: [],
      status: "",
      url: null,
    };
  },

  mounted() {
    this.getFeed();
    this.getFriends();
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
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },

    removeImage() {
      this.url = null
    },

    sendDirectMessage() {
      axios
        .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
        .then((res) => {
          this.$router.push("/chat");
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    sendFriendshipRequest() {
      axios
        .post(`/api/friends/${this.$route.params.id}/request/`)
        .then((res) => {
          this.status = res.data.message;

          if (this.status === "request already sent") {
            this.toastStore.showToast(
              5000,
              "Không thể gửi lần 2",
              "bg-rose-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Đã gửi lời mời kết bạn",
              "bg-emerald-400 text-white"
            );
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getFeed() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/`)
        .then((response) => {
          console.log("data", response.data);

          this.posts = response.data.posts;
          this.user = response.data.user;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    getFriends() {
      axios
        .get(`/api/friends/${this.$route.params.id}/`)
        .then((res) => {
          this.friendshipRequest = res.data.requests;
          this.user = res.data.user;

          console.log(this.user);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      console.log("submitForm", this.body);

      let formData = new FormData();
      formData.append("image", this.$refs.file.files[0]);
      formData.append("body", this.body);

      axios
        .post("/api/posts/create/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("data", response.data);

          this.posts.unshift(response.data);
          this.body = "";
          this.$refs.file.value = null;
          this.url = null;

          if (this.user) {
            this.user.posts_count += 1;
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    logout() {
      console.log("log out");

      this.userStore.removeToken();

      this.$router.push("/login");
    },
  },
};
</script>

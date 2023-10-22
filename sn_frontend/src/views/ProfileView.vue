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
            <div v-if="can_send_friendship_request === false">
              <button v-if="friends.includes(this.userStore.user.id) === false">
                Đã gửi lời mời kết bạn
              </button>
              <button v-else>Bạn bè</button>
            </div>
            <div v-else>
              <button @click="sendFriendshipRequest">Thêm bạn bè</button>
            </div>
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
        <PostForm v-bind:user="user" v-bind:posts="posts" />
      </div>
      <p class="font-semibold text-2xl">Bài viết của {{ user.name }}</p>
      <div v-if="posts?.length">
        <div
          class="p-4 bg-white border border-gray-200 rounded-lg mt-4"
          v-for="post in posts"
          v-bind:key="post.id"
        >
          <FeedItem v-bind:post="post" />
        </div>
      </div>
      <p v-else class="text-center text-lg">
        {{ user.name }} Chưa có bài viết nào
      </p>
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
import PostForm from "../components/PostForm.vue";
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
    PostForm,
  },

  data() {
    return {
      posts: [],
      user: {
        id: null,
      },
      can_send_friendship_request: null,
      friendshipRequest: [],
      status: "",
      friends: [],
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
          console.log(res.data);
          this.status = res.data.message;
          if (this.status === "request already sent") {
            this.toastStore.showToast(
              5000,
              "Không thể gửi lần 2",
              "bg-rose-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              3000,
              "Đã gửi lời mời kết bạn",
              "bg-emerald-400 text-white"
            );
          }
          setTimeout(() => {
            this.$router.go();
          }, 3500);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getFeed() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/`)
        .then((res) => {
          this.posts = res.data.posts;
          this.user = res.data.user;
          this.can_send_friendship_request =
            res.data.can_send_friendship_request;

          console.log(res.data);
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
          this.friends = res.data.friends;
          console.log(res.data.friends);
        })
        .catch((error) => {
          console.log(error);
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

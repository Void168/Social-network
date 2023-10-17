<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        class="flex flex-col justify-center items-center p-4 bg-white border border-gray-200 text-center rounded-lg"
      >
        <img
          :src="user.get_avatar"
          alt=""
          class="w-64 h-64 mb-6 rounded-full"
        />
        <p>
          <strong class="text-2xl">{{ user.name }}</strong>
        </p>
        <div class="mt-6 flex space-x-8 justify-around">
          <p class="text-xs text-gray-500">
            {{ user.friends_count }} người bạn
          </p>
          <p class="text-xs text-gray-500">{{ user.posts_count }} bài đăng</p>
        </div>
      </div>
    </div>

    <div class="main-center col-span-2 space-y-4">
      <div
        v-if="friendshipRequests.length"
        class="p-4 bg-white border border-gray-200 rounded-lg"
      >
        <h2 class="mb-6 text-xl">Lời mời kết bạn</h2>
        <div
          v-for="friendshipRequest in friendshipRequests"
          v-bind:key="friendshipRequest.id"
          class="p-4 bg-gray-100 text-center rounded-lg mb-4"
        >
          <RouterLink
            :to="{
              name: 'profile',
              params: { id: friendshipRequest.created_by.id },
            }"
          >
            <img
              :src="user.get_avatar"
              alt=""
              class="mb-6 rounded-full mx-auto"
            />

            <p>
              <strong> {{ friendshipRequest.created_by.name }}</strong>
            </p>
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500">
                {{ user.friends_count }} người bạn
              </p>
              <p class="text-xs text-gray-500">
                {{ user.posts_count }} bài đăng
              </p>
            </div>
          </RouterLink>
          <div class="mt-6 space-x-4">
            <button
              @click="
                handleRequest('accepted', friendshipRequest.created_by.id)
              "
            >
              Đồng ý
            </button>
            <button
              @click="
                handleRequest('rejected', friendshipRequest.created_by.id)
              "
              class="bg-rose-400 hover:bg-rose-600"
            >
              Từ chối
            </button>
          </div>
        </div>

        <hr />
      </div>
      <div
        v-if="friends.length"
        class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4"
      >
        <div
          v-for="friend in friends"
          v-bind:key="friend.id"
          class="p-4 bg-gray-200 text-center rounded-lg"
        >
          <RouterLink :to="{ name: 'profile', params: { id: friend.id } }">
            <img :src="friend.get_avatar" alt="" class="w-64 h-64 mb-6 rounded-full" />
            <p>
              <strong> {{ friend.name }}</strong>
            </p>
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500">
                {{ user.friends_count }} người bạn
              </p>
              <p class="text-xs text-gray-500">
                {{ user.posts_count }} bài đăng
              </p>
            </div>
          </RouterLink>
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
  name: "FriendsView",
  components: {
    PeopleYouMayKnow,
    Trends,
  },

  data() {
    return {
      user: {},
      friendshipRequests: [],
      friends: [],
    };
  },

  mounted() {
    this.getFriends();
  },

  methods: {
    getFriends() {
      axios
        .get(`/api/friends/${this.$route.params.id}/`)
        .then((res) => {
          console.log(res.data);

          this.friendshipRequests = res.data.requests;
          this.friends = res.data.friends;
          this.user = res.data.user;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    handleRequest(status, pk) {
      console.log("handleRequest", status);

      axios
        .post(`/api/friends/${pk}/${status}/`)
        .then((res) => {
          console.log("data", res.data);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

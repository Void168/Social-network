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
      <h2 class="mb-6 text-xl">Lời mời kết bạn</h2>
      <div
        v-if="friendshipRequests.length"
        class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"
      >
        <div
          v-for="friendshipRequest in friendshipRequests"
          v-bind:key="friendshipRequest.id"
          class="p-4 bg-gray-100 text-center rounded-lg"
        >
          <RouterLink
            :to="{
              name: 'profile',
              params: { id: friendshipRequest.created_by.id },
            }"
          >
            <img
              src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
              alt=""
              class="mb-6 rounded-full"
            />

            <p>
              <strong> {{ friendshipRequest.created_by.name }}</strong>
            </p>
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500">229 người bạn</p>
              <p class="text-xs text-gray-500">168 bài đăng</p>
            </div>
          </RouterLink>
        </div>
      </div>
      <div
        v-if="friends.length"
        class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"
      >
        <div
          v-for="friend in friends"
          v-bind:key="friend.id"
          class="p-4 bg-gray-200 text-center rounded-lg"
        >
          <RouterLink :to="{ name: 'profile', params: { id: friend.id } }">
            <img
              src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
              alt=""
              class="mb-6 rounded-full"
            />
            <p>
              <strong> {{ user.name }}</strong>
            </p>
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500">229 người bạn</p>
              <p class="text-xs text-gray-500">168 bài đăng</p>
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
  },
};
</script>

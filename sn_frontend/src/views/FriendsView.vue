<template>
  <div class="max-w-7xl mx-auto gap-4 min-h-screen">
    <div class="main-center space-y-4" id="feed-frame">
      <div class="sticky py-2 top-0 h-16 dark:bg-slate-700" :style="{top: `${toastStore.navbarHeight}px`}">
        <RouterLink
            :to="{
              name: 'profile',
              params: { id: userStore.user.id },
            }"
            class="flex items-center gap-3"
          >
          <img :src="userStore.user.avatar" class="w-10 h-10 rounded-full">
          <h3 class="dark:text-slate-200 font-bold">{{ userStore.user.name }}</h3>
        </RouterLink>
      </div>
      <div
        v-if="friendshipRequests.length"
        class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
      >
        <h2 class="mb-6 text-xl">Lời mời kết bạn</h2>
        <div
          v-for="friendshipRequest in friendshipRequests"
          v-bind:key="friendshipRequest.id"
          class="p-4 bg-gray-100 dark:bg-slate-500 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg mb-4"
        >
          <RouterLink
            :to="{
              name: 'profile',
              params: { id: friendshipRequest.created_by.id },
            }"
          >
            <img
              :src="friendshipRequest.created_by.get_avatar"
              alt=""
              class="mb-6 rounded-full mx-auto w-32 h-32"
            />

            <p>
              <strong> {{ friendshipRequest.created_by.name }}</strong>
            </p>
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500 dark:text-neutral-200">
                {{ friendshipRequest.created_by.friends_count }} người bạn
              </p>
              <p class="text-xs text-gray-500 dark:text-neutral-200">
                {{ friendshipRequest.created_by.posts_count }} bài đăng
              </p>
            </div>
          </RouterLink>
          <div class="mt-6 space-x-4">
            <button
              @click="
                handleRequest('rejected', friendshipRequest.created_by.id)
              "
              class="bg-rose-400 hover:bg-rose-600 btn"
            >
              Từ chối
            </button>
            <button
              @click="
                handleRequest('accepted', friendshipRequest.created_by.id)
              "
              class="btn"
            >
              Đồng ý
            </button>
          </div>
        </div>
      </div>
      <TabGroup>
      <TabList class="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
        <Tab
          v-for="category in categories"
          as="template"
          :key="category"
          v-slot="{ selected }"
        >
          <button
            :class="[
              'w-full rounded-lg py-2.5 xm:text-sm text-xs font-medium leading-5',
              'ring-white/60 ring-offset-2 ring-offset-blue-200 focus:outline-none focus:ring-2',
              selected
                ? 'bg-white dark:bg-slate-800 dark:text-slate-200 text-blue-700 shadow'
                : 'text-blue-100 hover:bg-white/[0.12] hover:text-white',
            ]"
          >
            <span>{{ category.name }}</span>
            <span v-if="category.name === 'Tất cả bạn bè'"> ({{ friends.length }})</span>
            <span v-if="category.name === 'Người theo dõi'"> ({{ followers.length }})</span>
            <span v-if="category.name === 'Đang theo dõi'"> ({{ following.length }})</span>
          </button>
        </Tab>
      </TabList>

      <TabPanels class="mt-2">
        <TabPanel
          v-for="n in categories.length"
          :key="n"
          :class="[
            'xl:rounded-xl rounded-none p-3',
            'focus:outline-none',
          ]"
          class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
        >
        <div v-if="friends.length && n === 1" class="grid sm:grid-cols-2 grid-cols-1 gap-4">
          <div
            v-for="friend in friends"
            v-bind:key="friend.id"
            class="p-4 bg-gray-200 dark:bg-slate-500 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
          >
            <RouterLink :to="{ name: 'profile', params: { id: friend.id } }" class="flex flex-col items-center">
              <img
                :src="friend.get_avatar"
                alt=""
                class="w-32 h-32 mb-6 rounded-full"
              />
              <p>
                <strong> {{ friend.name }}</strong>
              </p>
              <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.friends_count }} người bạn
                </p>
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.posts_count }} bài đăng
                </p>
              </div>
            </RouterLink>
          </div>
        </div>
        <div v-if="friends.length && n === 2" class="grid sm:grid-cols-2 grid-cols-1 gap-4">
          <div
            v-for="follower in followers"
            v-bind:key="follower.id"
            class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
          >
            <RouterLink :to="{ name: 'profile', params: { id: follower.id } }" class="flex flex-col items-center">
              <img
                :src="follower.get_avatar"
                alt=""
                class="w-32 h-32 mb-6 rounded-full"
              />
              <p>
                <strong> {{ follower.name }}</strong>
              </p>
              <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.friends_count }} người bạn
                </p>
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.posts_count }} bài đăng
                </p>
              </div>
            </RouterLink>
          </div>
        </div>
        <div v-if="friends.length && n === 3" class="grid sm:grid-cols-2 grid-cols-1 gap-4">
          <div
            v-for="following in following"
            v-bind:key="following.id"
            class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
          >
            <RouterLink :to="{ name: 'profile', params: { id: following.id } }" class="flex flex-col items-center">
              <img
                :src="following.get_avatar"
                alt=""
                class="w-32 h-32 mb-6 rounded-full"
              />
              <p>
                <strong> {{ following.name }}</strong>
              </p>
              <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.friends_count }} người bạn
                </p>
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ user.posts_count }} bài đăng
                </p>
              </div>
            </RouterLink>
          </div>
        </div>
        </TabPanel>
      </TabPanels>
    </TabGroup>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'

import { useUserStore } from "../stores/user";

export default {
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  name: "FriendsView",
  components: {
    TabGroup, TabList, Tab, TabPanels, TabPanel
  },

  data() {
    return {
      user: {},
      friendshipRequests: [],
      friends: [],
      followers: [],
      following: [],
      categories: [
        {
          'name': 'Tất cả bạn bè'
        },
        {
          'name': 'Người theo dõi'
        },
        {
          'name': 'Đang theo dõi'
        }
      ],
      activeTab: 0,
    };
  },

  mounted() {
    this.getFriends();
  },

  methods: {
    async getFriends() {
      await axios
        .get(`/api/friends/${this.$route.params.id}/`)
        .then((res) => {
          console.log(res.data);
          
          this.friendshipRequests = res.data.requests;
          this.friends = res.data.friends;
          this.followers = res.data.followers;
          this.following =res.data.following
          this.user = res.data.user;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    handleRequest(status, pk) {
      axios
        .post(`/api/friends/${pk}/${status}/`)
        .then((res) => {
          console.log(status === "accepted");

          if (status === "accepted") {
            this.toastStore.showToast(
              5000,
              "Đã đồng ý lời mời kết bạn",
              "bg-emerald-500 text-white"
            );
            // setTimeout(() => {
            //   this.$router.go();
            // }, 5500);
          } else if (status === "rejected") {
            this.toastStore.showToast(
              5000,
              "Đã từ chối lời mời kết bạn",
              "bg-amber-500 text-white"
            );
            setTimeout(() => {
              this.$router.go();
            }, 5500);
          } else {
            this.toastStore.showToast(
              5000,
              "Chấp nhận lời mời thất bại",
              "bg-red-500 text-white"
            );
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

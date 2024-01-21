<template>
  <div class="max-w-7xl mx-auto gap-4 min-h-screen">
    <div class="main-center space-y-4" id="feed-frame">
      <div
        class="sticky py-2 top-0 h-16 dark:bg-slate-700 dark:text-neutral-200"
        :style="{ top: `${toastStore.navbarHeight}px` }"
      >
        <RouterLink
          :to="{
            name: 'page',
            params: { id: page.id },
          }"
          class="flex items-center gap-3 max-w-max"
        >
          <img :src="page.get_avatar" class="w-10 h-10 rounded-full" />
          <h3 class="dark:text-slate-200 font-bold">
            {{ page.name }}
          </h3>
        </RouterLink>
      </div>
      <div
        class="dark:text-neutral-200 space-y-4 p-4 dark:bg-slate-800/50 rounded-lg"
      >
      <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold">Người theo dõi</h2>
          <div class="relative">
          <MagnifyingGlassIcon
            class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
          />
          <input
            @keyup="getQuery"
            ref="searchInput"
            type="text"
            placeholder="Tìm kiếm"
            class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
          />
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
                <span v-if="category.name === 'Người theo dõi'">
                  ({{ page.followers?.length }})</span
                >
                <span v-if="category.name === 'Đang theo dõi'">
                  ({{ page.following?.length }})</span
                >
                <span v-if="category.name === 'Lượt thích'">
                  ({{ page?.likes_count }})</span
                >
              </button>
            </Tab>
          </TabList>

          <TabPanels class="mt-2">
            <TabPanel
              v-for="n in categories.length"
              :key="n"
              :class="['xl:rounded-xl rounded-none p-3', 'focus:outline-none']"
              class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
            >
              <div
                v-if="page?.followers?.length && n === 1"
                class="grid sm:grid-cols-2 grid-cols-1 gap-4"
              >
                <div
                  v-for="follower in page?.followers"
                  v-bind:key="follower.id"
                  class="p-4 bg-gray-200 dark:bg-slate-500 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
                >
                  <RouterLink
                    :to="{ name: 'profile', params: { id: follower.id } }"
                    class="flex flex-col items-center"
                  >
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
                        {{ follower.friends_count }} người bạn
                      </p>
                      <p class="text-xs text-gray-500 dark:text-neutral-200">
                        {{ follower.posts_count }} bài đăng
                      </p>
                    </div>
                  </RouterLink>
                </div>
              </div>
              <div
                v-else-if="!page?.followers?.length && n === 1"
                class="h-48 flex justify-center items-center"
              >
                <h1 class="text-2xl font-semibold dark:text-neutral-400">
                  Chưa có ai theo dõi
                </h1>
              </div>
              <div
                v-if="page.following?.length && n === 2"
                class="grid sm:grid-cols-2 grid-cols-1 gap-4"
              >
                <div
                  v-for="following in page.following"
                  v-bind:key="following.id"
                  class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
                >
                  <RouterLink
                    :to="{ name: 'profile', params: { id: following.id } }"
                    class="flex flex-col items-center"
                  >
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
                        {{ following.friends_count }} người bạn
                      </p>
                      <p class="text-xs text-gray-500 dark:text-neutral-200">
                        {{ following.posts_count }} bài đăng
                      </p>
                    </div>
                  </RouterLink>
                </div>
              </div>
              <div
                v-else-if="!page?.following?.length && n === 2"
                class="h-48 flex justify-center items-center"
              >
                <h1 class="text-2xl font-semibold dark:text-neutral-400">
                  Chưa theo dõi ai
                </h1>
              </div>
              <div
                v-if="page?.likes?.length && n === 3"
                class="grid sm:grid-cols-2 grid-cols-1 gap-4"
              >
                <div
                  v-for="user in page.likes"
                  v-bind:key="user.id"
                  class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
                >
                  <RouterLink
                    :to="{ name: 'profile', params: { id: user.id } }"
                    class="flex flex-col items-center"
                  >
                    <img
                      :src="user.get_avatar"
                      alt=""
                      class="w-32 h-32 mb-6 rounded-full"
                    />
                    <p>
                      <strong> {{ user.name }}</strong>
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
              <div
                v-else-if="!page?.likes?.length && n === 3"
                class="h-48 flex justify-center items-center"
              >
                <h1 class="text-2xl font-semibold dark:text-neutral-400">
                  Chưa ai thích
                </h1>
              </div>
            </TabPanel>
          </TabPanels>
        </TabGroup>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";

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
  name: "PageUsersView",
  components: {
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    MagnifyingGlassIcon,
  },

  data() {
    return {
      page: {},
      categories: [
        {
          name: "Người theo dõi",
        },
        {
          name: "Đang theo dõi",
        },
        {
          name: "Lượt thích",
        },
      ],
      activeTab: 0,
    };
  },

  mounted() {
    this.getUsers();
  },

  methods: {
    async getUsers() {
      await axios
        .get(`/api/page/get-page/${this.$route.params.id}`)
        .then((res) => {
          this.page = res.data;
        })
        .catch((error) => console.log(error));
      console.log("hello");
    },
    getQuery() {
      this.query = this.$refs.searchInput.value;
    },
  },
};
</script>

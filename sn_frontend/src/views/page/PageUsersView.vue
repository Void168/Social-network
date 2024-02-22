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
          <h2 class="sm:text-2xl xm:text-lg text-sm font-bold">Người theo dõi</h2>
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
          <TabList class="flex sm:flex-row flex-col space-x-1 rounded-xl bg-blue-900/20 p-1">
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
                  ({{ allFollowers?.length }})</span
                >
                <span v-if="category.name === 'Đang theo dõi'">
                  ({{ page?.followings_count }})</span
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
                v-if="allFollowers?.length && n === 1"
                class="grid sm:grid-cols-2 grid-cols-1 gap-4"
              >
                <div
                  v-for="follower in allFollowers"
                  v-bind:key="follower.id"
                  class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
                >
                <UserItem :user="follower" v-if="!follower.is_page"/>
                <PageItem :page="follower" v-else/>
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
                v-if="allFollowings?.length && n === 2"
                class="grid sm:grid-cols-2 grid-cols-1 gap-4"
              >
                <div
                  v-for="following in allFollowings"
                  v-bind:key="following.id"
                  class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
                >
                <UserItem :user="following" v-if="!following.is_page"/>
                <PageItem :page="following" v-else/>
                </div>
              </div>
              <div
                v-else-if="!allFollowings?.length && n === 2"
                class="h-48 flex justify-center items-center"
              >
                <h1 class="text-2xl font-semibold dark:text-neutral-400">
                  Chưa theo dõi ai
                </h1>
              </div>
              <div
                v-if="allLikes?.length && n === 3"
                class="grid sm:grid-cols-2 grid-cols-1 gap-4"
              >
                <div
                  v-for="like in allLikes"
                  v-bind:key="like.id"
                  class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg"
                >
                <UserItem :user="like" v-if="!like.is_page"/>
                <PageItem :page="like" v-else/>
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

import { useUserStore } from "../../stores/user";

import UserItem from "../../components/items/profile/UserItem.vue";
import PageItem from '../../components/items/page/PageItem.vue';
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
    UserItem,
    PageItem
  },

  data() {
    return {
      page: {},
      other_page_followers: [],
      other_page_likes: [],
      other_page_following: [],
      // allFollowers: [],
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

  computed: {
    allFollowers() {
      return this.page?.followers
        ?.concat(this.other_page_followers)
        .sort((a, b) => {
          const nameA = a.name.toUpperCase();
          const nameB = b.name.toUpperCase();
          if (nameA < nameB) {
            return -1;
          }
          if (nameA > nameB) {
            return 1;
          }

          return 0;
        });
    },
    allLikes(){
      return this.page?.likes
        ?.concat(this.other_page_likes)
        .sort((a, b) => {
          const nameA = a.name.toUpperCase();
          const nameB = b.name.toUpperCase();
          if (nameA < nameB) {
            return -1;
          }
          if (nameA > nameB) {
            return 1;
          }

          return 0;
        });
    },
    allFollowings(){
      return this.page?.following
        ?.concat(this.other_page_following)
        .sort((a, b) => {
          const nameA = a.name.toUpperCase();
          const nameB = b.name.toUpperCase();
          if (nameA < nameB) {
            return -1;
          }
          if (nameA > nameB) {
            return 1;
          }

          return 0;
        });
    }
  },

  mounted() {
    this.getUsers();
  },

  methods: {
    async getUsers() {
      await axios
        .get(`/api/page/get-page/${this.$route.params.id}`)
        .then((res) => {
          this.page = res.data.data;
          this.other_page_followers = res.data.other_page_followers;
          this.other_page_likes = res.data.other_page_likes
          this.other_page_following = res.data.other_page_following
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

<template>
  <div class="min-h-screen" :class="isExpand ? 'requires-no-scroll' : ''">
    <GroupViewNavigation @getActiveTab="getActiveTab" :activeTab="activeTab" v-if="isExpand" class="block fixed"/>
    <div v-if="isExpand" class="w-full h-full absolute bg-slate-700/50 z-10 duration-100" @click="expandGroupNavigation"></div>
    <div
      class="dark:bg-slate-800 dark:text-neutral-200 grid md:grid-cols-5 grid-cols-4 relative"
    >
      <div
        @click="expandGroupNavigation"
        class="fixed flex md:hidden left-0 z-20 inset-y-2/4 w-5 h-20 bg-slate-700 rounded-r-2xl"
        :class="isExpand ? 'translate-x-[332px]' : 'translate-x-0'"
      >
        <ChevronRightIcon class="dark:text-slate-200" v-if="!isExpand" />
        <ChevronLeftIcon class="dark:text-slate-200" v-else />
      </div>
      <GroupViewNavigation @getActiveTab="getActiveTab" :activeTab="activeTab" v-if="!isExpand" class="hidden sticky"/>

      <div
        class="xl:col-span-4 min-h-screen md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center pt-6 py-12 px-6"
      >
        <div v-if="activeTab === 1" class="xl:w-[50%]">
          <div class="py-12">
            <h3 class="font-semibold dark:text-neutral-400">
              Hoạt động gần đây
            </h3>
            <div v-for="groupPost in groupPosts" :key="groupPost.id">
              <GroupPost :post="groupPost" :group="groupPost.group" />
            </div>
          </div>
        </div>
        <div v-if="activeTab === 2">
          <div class="py-8">
            <h2 class="text-xl font-bold">Nhóm phổ biến ở gần bạn</h2>
            <h4>Nhóm mà mọi người tại khu vực của bạn tham gia</h4>
          </div>
          <div class="grid xl:grid-cols-4 md:grid-cols-2 grid-cols-1 gap-3">
            <div
              v-for="discoverGroup in discoverGroups"
              :key="discoverGroup.id"
            >
              <DiscoverGroup :group="discoverGroup" />
            </div>
          </div>
          <hr class="border-slate-600 my-8" />
          <h2 class="text-xl font-bold my-8">Gợi ý khác</h2>
          <div class="grid xl:grid-cols-4 md:grid-cols-2 grid-cols-1 gap-3">
            <div
              v-for="discoverGroup in discoverGroups"
              :key="discoverGroup.id"
            >
              <DiscoverGroup :group="discoverGroup" />
            </div>
          </div>
        </div>
        <div v-if="activeTab === 3" class="w-full md:px-12">
          <div class="mb-4">
            <h3 class="text-lg font-semibold mb-4">
              Tất cả các nhóm bạn đã tham gia ({{ yourGroups?.length }})
            </h3>
            <div class="grid xl:grid-cols-3 grid-cols-1 gap-3 w-full">
              <div v-for="yourGroup in yourGroups" :key="yourGroup.id">
                <YourGroup :yourGroup="yourGroup" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "../../stores/toast";
import GroupPost from "../../components/items/group/post/GroupPost.vue";
import DiscoverGroup from "../../components/items/group/DiscoverGroup.vue";
import YourGroup from "../../components/items/group/YourGroup.vue";
import GroupViewNavigation from '../../components/items/group/GroupViewNavigation.vue';

import CreateGroupModal from "../../components/modals/group/createGroup/CreateGroupModal.vue";
import {
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/vue/20/solid";

export default {
  name: "group",
  components: {
    ChevronLeftIcon,
    ChevronRightIcon,
    GroupViewNavigation,
    GroupPost,
    DiscoverGroup,
    YourGroup,
    CreateGroupModal,
  },
  setup() {
    const toastStore = useToastStore();
    const categories = [
      {
        tab: 1,
        name: "Bảng feed của bạn",
      },
      {
        tab: 2,
        name: "Khám phá",
      },
      {
        tab: 3,
        name: "Nhóm của bạn",
      },
    ];

    return {
      toastStore,
      categories,
    };
  },

  data() {
    return {
      activeTab: 1,
      isOpen: false,
      yourGroups: [],
      discoverGroups: [],
      groupPosts: [],
      isExpand: false,
    };
  },

  mounted() {
    this.getYourGroupPosts();
  },

  methods: {
    getActiveTab(tab) {
      this.isExpand = false
      this.activeTab = tab;
      if (this.activeTab === 2) {
        axios
          .get("/api/group/discover/")
          .then((res) => {
            if (!res.data.message) {
              this.discoverGroups = res.data;
            }
            // console.log(res.data)
          })
          .catch((error) => {
            console.log(error);
          });
      }
      if (this.activeTab === 3) {
        axios
          .get("/api/group/your-groups/")
          .then((res) => {
            if (!res.data.message) {
              this.yourGroups = res.data;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    async getYourGroupPosts() {
      axios
        .get("/api/posts/group/your-group/")
        .then((res) => {
          this.groupPosts = res.data.data;
          // console.log(res.data.data)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    expandGroupNavigation() {
      this.isExpand = !this.isExpand;
      console.log('hello')
    },
  },
};
</script>

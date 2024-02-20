<template>
  <div
    class="dark:bg-slate-800 dark:text-neutral-200 grid md:grid-cols-3 xl:grid-cols-5 lg:grid-cols-7 grid-cols-4 relative min-h-screen"
    :class="isExpand ? 'requires-no-scroll' : ''"
  >
  <div v-if="isExpand" class="w-full h-full absolute bg-slate-700/50 z-10 duration-100" @click="expandGroupNavigation"></div>
    <div
      @click="expandGroupNavigation"
      class="fixed flex md:hidden left-0 z-20 inset-y-2/4 w-5 h-20 bg-slate-600 rounded-r-2xl"
      :class="isExpand ? 'translate-x-[274px]' : 'translate-x-0'"
    >
      <ChevronRightIcon class="dark:text-slate-200" v-if="!isExpand" />
      <ChevronLeftIcon class="dark:text-slate-200" v-else />
    </div>
    <div
      class="xl:col-span-1 md:col-span-1 lg:col-span-2 md:block border-r dark:border-slate-600 dark:bg-slate-800 bg-slate-200 md:sticky fixed overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 z-50"
      :style="{
        height: `${toastStore.height}px`,
        top: `${toastStore.navbarHeight}px`,
      }"
      :class="isExpand ? 'block' : 'hidden'"
    >
      <GroupSearchNavigation
        v-if="route.name === 'groupsearch'"
        :group="group"
        :isUserInGroup="isUserInGroup"
        @getQuery="getQuery"
      />
      <GroupDetailNavigation
        :group="group"
        :isUserInGroup="isUserInGroup"
        v-else
      />
    </div>
    <div
      class="xl:col-span-4 lg:col-span-5 md:col-span-2 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center"
    >
      <GroupHeader
        :group="group"
        :isUserInGroup="isUserInGroup"
        @openModal="openModal"
        v-if="
          route.name === 'groupdiscuss' ||
          route.name === 'groupabout' ||
          route.name === 'groupmembers' ||
          route.name === 'groupmedia' ||
          route.name === 'groupfile'
        "
      />
      <SearchModal
        :show="isOpen"
        @closeModal="closeModal"
        :group="group"
        :keywords="keywords"
        @getQuery="getQuery"
        @deleteKeyWord="deleteKeyWord"
      />
      <router-view
        :isUserInGroup="isUserInGroup"
        :group="group"
        :currentMember="currentMember"
        :query="query"
      ></router-view>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { RouterLink, useRoute } from "vue-router";
import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  HomeIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
} from "@heroicons/vue/24/solid";
import GroupDetailNavigation from "../../components/items/group/GroupDetailNavigation.vue";
import GroupSearchNavigation from "../../components/items/group/GroupSearchNavigation.vue";
import GroupHeader from "../../components/items/group/GroupHeader.vue";
import SearchModal from "../../components/modals/group/SearchModal.vue";
export default {
  name: "groupdetail",
  components: {
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    HomeIcon,
    ChevronRightIcon,
    ChevronLeftIcon,
    RouterLink,
    GroupDetailNavigation,
    GroupSearchNavigation,
    GroupHeader,
    SearchModal,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const route = useRoute();

    return {
      userStore,
      toastStore,
      route,
    };
  },
  data() {
    return {
      group: {},
      isUserInGroup: false,
      currentMember: {},
      query: "",
      isOpen: false,
      keywords: [],
      isExpand: false,
    };
  },

  computed: {
    check() {
      return this.group.members
        .map((member) => member.information)
        .map((info) => info.id)
        .includes(this.userStore.user.id);
    },
  },

  created() {
    this.checkUserInGroup();
  },

  methods: {
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
      this.getKeyWords();
    },
    expandGroupNavigation() {
      this.isExpand = !this.isExpand;
    },
    async checkUserInGroup() {
      await axios
        .get(`/api/group/check-user/${this.$route.params.id}/`)
        .then((res) => {
          // console.log(res.data);
          if (res.data.message === "User joined the group") {
            this.isUserInGroup = true;
          } else {
            this.isUserInGroup = false;
          }
          this.getGroupDetail();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupDetail() {
      await axios
        .get(`/api/group/${this.$route.params.id}/`)
        .then((res) => {
          this.group = res.data;
          this.getCurrentMember();
          // console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getCurrentMember() {
      await axios
        .get(`/api/group/get-current-member/${this.$route.params.id}/`)
        .then((res) => {
          this.currentMember = res.data;
          // console.log(res.data)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getKeyWords() {
      await axios
        .get(`/api/search/group/${this.group.id}/get-key-words/`)
        .then((res) => {
          this.keywords = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getQuery(query) {
      this.query = query;
    },
    deleteKeyWord(keyword) {
      this.keywords = this.keywords.filter((kw) => kw.id !== keyword.id);
    },
  },
};
</script>

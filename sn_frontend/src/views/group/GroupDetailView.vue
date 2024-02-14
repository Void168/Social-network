<template>
  <div
    class="dark:bg-slate-800 dark:text-neutral-200 grid lg:grid-cols-5 grid-cols-4 relative"
  >
    <div
      class="col-span-1 lg:block hidden dark:bg-slate-800 bg-slate-200 sticky overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
      :style="{
        height: `${toastStore.height}px`,
        top: `${toastStore.navbarHeight}px`,
      }"
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
      class="lg:col-span-4 md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center"
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
        @getQuery="getQuery"
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
      axios
        .get(`/api/group/get-current-member/${this.$route.params.id}/`)
        .then((res) => {
          this.currentMember = res.data;
          // console.log(res.data)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getQuery(query) {
      this.query = query;
    },
  },
};
</script>

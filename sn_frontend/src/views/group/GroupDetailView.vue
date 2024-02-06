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
      <GroupDetailNavigation :group="group" :isUserInGroup="isUserInGroup" />
    </div>
    <div
      class="lg:col-span-4 md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center"
    >
      <GroupHeader
        :group="group"
        :isUserInGroup="isUserInGroup"
        v-if="
          route.name === 'groupdiscuss' ||
          route.name === 'groupabout' ||
          route.name === 'groupmembers' ||
          route.name === 'groupmedia' ||
          route.name === 'groupfile'
        "
      />
      <router-view
        :isUserInGroup="isUserInGroup"
        :group="group"
        :currentMember="currentMember"
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
import GroupHeader from "../../components/items/group/GroupHeader.vue";
export default {
  name: "groupdetail",
  components: {
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    HomeIcon,
    RouterLink,
    GroupDetailNavigation,
    GroupHeader,
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

  beforeMount() {
    this.getGroupDetail();
  },

  // watch: {
  //   group: {
  //     handler: function () {
  //       this.getGroupDetail();
  //     },
  //     deep: true,
  //   },
  // },

  methods: {
    async checkUserInGroup() {
      await axios
        .get(`/api/group/check-user/${this.group.id}`)
        .then((res) => {
          if (res.data.message === "User joined the group") {
            this.isUserInGroup = true;
            this.getCurrentMember();
          } else {
            this.isUserInGroup = false;
          }
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
          this.checkUserInGroup()
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
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

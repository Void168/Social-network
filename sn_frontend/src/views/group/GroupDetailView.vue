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
      <GroupDetailNavigation :group="group" :isUserInGroup="isUserInGroup"/>
    </div>
    <div
      class="lg:col-span-4 md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center"
    >
      <GroupDetail :group="group" :isUserInGroup="isUserInGroup"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { RouterLink } from "vue-router";
import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  HomeIcon,
} from "@heroicons/vue/24/solid";
import GroupDetailNavigation from "../../components/items/group/GroupDetailNavigation.vue";
import GroupDetail from "../../components/items/group/GroupDetail.vue";

export default {
  name: "groupdetail",
  components: {
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    HomeIcon,
    RouterLink,
    GroupDetailNavigation,
    GroupDetail,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  data() {
    return {
      group: {},
      isUserInGroup: false,
    };
  },

  mounted() {
    this.checkUserInGroup();
  },

  methods: {
    async checkUserInGroup() {
      await axios
        .get(`/api/group/check-user/${this.$route.params.id}`)
        .then((res) => {
          if(res.data.message === 'User joined the group'){
            this.isUserInGroup = true
          } else {
            this.isUserInGroup = false
          }
          this.getGroupDetail()
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
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<template>
  <div
    class="dark:bg-slate-900 bg-slate-200 pt-6 py-12 px-6 md:w-[70%] lg:w-[50%]"
  >
  <div class="flex flex-col gap-4 relative items-center" v-if="members?.length || groupPosts?.length">
    <div
      v-for="member in members"
      :key="member.id"
      class="w-full"
    >
      <GroupMember :member="member"/>
    </div>
    <div
      v-for="groupPost in groupPosts"
      :key="groupPost.id"
      class="dark:bg-slate-700 rounded-lg px-4 w-full"
    >
      <GroupPost
        :post="groupPost"
        :group="group"
        :currentMember="currentMember"
      />
    </div>
  </div>
  <div class="flex justify-center items-center" v-else>
    Không tìm thấy kết quả phù hợp
  </div>
  </div>
</template>

<script>
import axios from "axios";
import GroupPost from "../../components/items/post/GroupPost.vue";
import GroupMember from "../../components/items/group/GroupMember.vue";
import { useUserStore } from "../../stores/user";
import { useRoute } from 'vue-router';


export default {
  name: "groupsearch",
  components: {
    GroupPost,
    GroupMember,
  },

  setup() {
    const userStore = useUserStore();
    const route = useRoute()

    return {
      userStore,
      route
    };
  },

  props: {
    group: Object,
    currentMember: Object,
    query: String
  },

  data() {
    return {
      members: [],
      groupPosts: [],
    };
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getQuerySearch();
      },
      deep: true,
      immediate: true,
    },
  },

  mounted() {
    this.getQuerySearch();
  },

  methods: {
    async getQuerySearch() {
      if(this.route.query.query){
        await axios
          .post(`/api/search/group/${this.$route.params.id}/`, {
            query: this.route.query.query,
          })
          .then((res) => {
            this.members = res.data.members;
            this.groupPosts = res.data?.groupPosts?.concat(res.data?.anonymousPosts);
            this.groupPosts?.sort(
              (a, b) => new Date(b.created_at) - new Date(a.created_at)
            );
            // console.log(this.route.query.query);
          })
          .catch((error) => {
            console.log("error:", error);
          });
      }
    },
  },
};
</script>

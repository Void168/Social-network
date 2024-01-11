<template>
  <div class="max-h-[200px] p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-bl-lg overflow-y-auto">
    <h3 class="mb-6 xl:text-xl text-center">Người bạn có thể biết</h3>
    <SkeletionLoadingChatBox v-if="isLoading"/>
    <div class="space-y-4" v-else>
      <div
        v-for="user in users"
        v-bind:key="user.id"
        class="flex items-center justify-between"
      >
        <div class="flex items-center space-x-2">
          <img :src="user.get_avatar" class="w-10 h-10 rounded-full" />

          <p class="text-xs">
            <strong>{{ user.name }}</strong>
          </p>
        </div>

        <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
          ><button class="btn btn-sm">Xem</button></RouterLink
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SkeletionLoadingChatBox from "./loadings/SkeletionLoadingChatbox.vue"

export default (await import("vue")).defineComponent({
  components: {
    SkeletionLoadingChatBox,
  },

  data() {
    return {
      users: [],
      isLoading: false
    };
  },

  mounted() {
    this.getFriendSuggestions();
  },

  methods: {
    async getFriendSuggestions() {
      this.isLoading = true
      await axios
        .get("/api/friends/suggested/")
        .then((res) => {
          this.users = res.data;
          this.isLoading = false
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

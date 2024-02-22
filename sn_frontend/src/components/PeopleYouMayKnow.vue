<template>
  <div
    ref="peopleContainer"
    class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-bl-lg overflow-y-auto"
  >
    <h3 class="mb-6 xl:text-xl text-center">Người bạn có thể biết</h3>
    <SkeletionLoadingChatBox v-if="isLoading" />
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
import { useToastStore } from "../stores/toast";
import SkeletionLoadingChatBox from "./loadings/SkeletionLoadingChatBox.vue";
export default (await import("vue")).defineComponent({
  components: {
    SkeletionLoadingChatBox,
  },
  setup(){
    const toastStore = useToastStore()

    return {
      toastStore
    }
  },
  data() {
    return {
      users: [],
      isLoading: false,
    };
  },

  mounted() {
    this.getFriendSuggestions();
    window.addEventListener("setHeight", this.setHeight);
  },
  unmounted() {
    window.removeEventListener("setHeight", this.setHeight);
  },

  methods: {
    async getFriendSuggestions() {
      this.isLoading = true;
      await axios
        .get("/api/friends/suggested/")
        .then((res) => {
          this.users = res.data;
          this.isLoading = false;
          this.setHeight()
        })
        .catch((error) => {
          console.log(error);
        });
    },
    setHeight() {
      this.toastStore.resetPeopleHeight()
      this.toastStore.setPeopleHeight(
        this.$refs.peopleContainer.clientHeight
      );
    },
  },
});
</script>

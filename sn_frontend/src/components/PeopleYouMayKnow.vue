<template>
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">Người bạn có thể biết</h3>
    <div class="space-y-4">
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
          ><button class="btn-sm">Xem</button></RouterLink
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default (await import("vue")).defineComponent({
  data() {
    return {
      users: [],
    };
  },

  mounted() {
    this.getFriendSuggestions();
  },

  methods: {
    getFriendSuggestions() {
      axios
        .get("/api/friends/suggested/")
        .then((res) => {
          this.users = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

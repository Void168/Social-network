<template>
  <div class="w-full">
    <p class="my-1">{{ option.poll_option_name }}</p>
    <div class="flex gap-3 justify-between items-center">
      <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
        <div
          class="h-2.5 rounded-full"
          style="width: 45%"
          :class="[selectedTheme.background]"
        ></div>
      </div>
      <div @click="vote">
        <div
          @click="submitVote(option)"
          class="relative w-[14px] h-[14px] rounded-full bg-white cursor-pointer"
        >
          <span
            v-if="isVote"
            class="absolute top-[3px] left-[3px] w-2 h-2 rounded-full"
            :class="[selectedTheme.background]"
          ></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import themes from "../../data/themes";
import { useUserStore } from "../../stores/user";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    option: Object,
    activeConversation: Object,
  },

  data() {
    return {
      themes: themes,
      isVote: false,
      user: {},
    };
  },

  computed: {
    selectedTheme() {
      return this.themes.filter(
        (theme) => theme.name === this.activeConversation.theme
      )[0];
    },
    filteredUser() {
      return this.option.users_vote
        .map((user) => user.id)
        .includes(this.user.id);
    },
  },

  mounted() {
    this.getUserInfo();
  },

  methods: {
    setIsVote() {
      if (this.filteredUser) {
        this.isVote = true;
      } else {
        this.isVote = false;
      }
    },
    getUserInfo() {
      axios
        .get(`/api/user-info/${this.userStore.user.id}`)
        .then((res) => {
          this.user = res.data.user;
          this.setIsVote()
        })
        .catch((error) => {
          console.log(error);
        });
    },
    vote() {
      this.isVote = !this.isVote;
    },
    submitVote(option) {
      axios
        .post(`/api/chat/group/${option.id}/vote-poll/`)
        .then((res) => {
          console.log(res.data);
        //   Toast
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

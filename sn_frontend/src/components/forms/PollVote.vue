<template>
  <div class="w-full">
    <div class="flex gap-3 justify-between items-end">
      <div class="flex flex-col w-full">
        <div class="flex justify-between items-center">
          <p class="my-1">{{ option.poll_option_name }}</p>
          <div
            class="flex items-center gap-1 cursor-pointer"
            @click="openUsersVoteModal"
          >
            <VotesListModal
              :option="option"
              :show="isOpen"
              @closeModal="closeModal"
            />
            <span
              v-if="usersVote.length > 3"
              class="bg-neutral-500 dark:text-neutral-200 rounded-full text-sm px-1"
              >+{{ usersVote.length - 3 }}</span
            >
            <div v-for="user in usersVote.slice(0, 3)" :key="user.id">
              <img
                :src="user.get_avatar"
                alt="avatar-vote"
                class="w-4 h-4 rounded-full"
              />
            </div>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
          <div
            class="h-2.5 rounded-full"
            :style="{ width: width }"
            :class="[selectedTheme.background]"
          ></div>
        </div>
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
import VotesListModal from "../modals/VotesListModal.vue";

export default (await import("vue")).defineComponent({
  components: {
    VotesListModal
  },
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
      isOpen: false,
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
    usersVote() {
      return this.option.users_vote.map((user) => user);
    },
    width() {
      return `${parseFloat(
        (this.option.users_vote.length / this.activeConversation.users.length) *
          100
      ).toFixed(2)}%`;
    },
    date() {
      return new Date().getTime();
    },
  },

  mounted() {
    this.getUserInfo();
  },

  methods: {
    closeModal(){
      this.isOpen = false
    },
    openUsersVoteModal() {
      this.isOpen = true
    },
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
          this.setIsVote();
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
        .post(
          `/api/chat/group/${this.$route.params.id}/vote-poll/${option.id}/`
        )
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

<template>
  <div class="relative rounded-lg border dark:border-slate-500 cursor-pointer">
    <div @click="$emit('voteOption', option)">
      <div class="relative flex items-center gap-4 p-4 w-full" @click="vote">
        <div
          class="absolute z-10 bg-emerald-500/20 h-full left-0"
          :style="{
            width: `${
              totalVote > 0 ? Math.round((voteCount / totalVote) * 100, 0) : 0
            }%`,
          }"
        />
        <div class="relative w-6 h-6 border dark:border-slate-500 rounded-md">
          <CheckIcon
            v-if="isVote"
            class="w-6 absolute top-[-1px] left-[-1px] bg-emerald-500 rounded-md"
          />
        </div>
        <h3 class="text-lg font-semibold">{{ option.body }}</h3>
        <div class="flex items-center">
          <div v-for="user in option?.vote_by?.slice(0, 3)" :key="user?.id">
            <img
              :src="user?.information?.get_avatar || userStore.user.avatar"
              alt="vote-avatar"
              class="w-6 h-6 rounded-full"
            />
          </div>
          <div v-if="option?.vote_by?.length > 1" class="ml-2">
            <h4 class="font-semibold text-emerald-400 text-sm">
              {{ option?.vote_by[0].information?.name }} và
              {{ option?.vote_by?.length - 1 }} người nữa đã bình chọn
            </h4>
          </div>
        </div>
      </div>
    </div>
    <div
      class="absolute right-1 top-4 flex gap-2 items-center"
      @click="openListVoteModal"
    >
      <h3 class="text-emerald-500 font-semibold">
        {{ totalVote > 0 ? Math.round((voteCount / totalVote) * 100, 0) : 0 }}%
      </h3>
      <ChevronRightIcon class="w-4" />
      <ListMemberVoteModal
        :show="isListVoteOpen"
        :option="option"
        @closeListVoteModal="closeListVoteModal"
        :totalVote="totalVote"
        :voteCount="voteCount"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { CheckIcon, ChevronRightIcon } from "@heroicons/vue/24/solid";
import { useUserStore } from "../../../../stores/user";
import ListMemberVoteModal from "../../../modals/group/ListMemberVoteModal.vue";
export default (await import("vue")).defineComponent({
  components: {
    CheckIcon,
    ChevronRightIcon,
    ListMemberVoteModal
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    option: Object,
    totalVote: Number,
    voteCount: Number,
  },

  data() {
    return {
      isVote: null,
      isListVoteOpen: false,
    };
  },

  mounted() {
    this.checkVote();
  },

  beforeUpdate() {
    this.checkVote();
  },

  methods: {
    openListVoteModal() {
      this.isListVoteOpen = true;
    },
    closeListVoteModal() {
      this.isListVoteOpen = false;
    },
    vote() {
      this.isVote = !this.isVote;
    },
    async checkVote() {
      await axios
        .get(`/api/posts/group/poll/option/${this.option.id}/check-vote/`)
        .then((res) => {
          console.log(res.data);
          if (res.data.message === "voted") {
            this.isVote = true;
          } else {
            this.isVote = false;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

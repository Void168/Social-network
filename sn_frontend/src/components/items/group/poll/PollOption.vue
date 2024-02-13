<template>
  <div class="relative rounded-lg border dark:border-slate-500 cursor-pointer">
    <div @click="$emit('voteOption', option)">
      <div class="relative flex items-center gap-4 p-4 w-full" @click="vote">
        <div
          class="absolute z-10 bg-emerald-500/20 h-full left-0"
          :style="{
            width: `${
              totalVote > 0
                ? Math.round((voteCount / totalVote) * 100, 0)
                : 0
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
      </div>
    </div>
    <div class="absolute right-1 top-4 flex gap-2 items-center">
      <h3 class="text-emerald-500 font-semibold">
        {{
          totalVote > 0
            ? Math.round((voteCount / totalVote) * 100, 0)
            : 0
        }}%
      </h3>
      <ChevronRightIcon class="w-4" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { CheckIcon, ChevronRightIcon } from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    CheckIcon,
    ChevronRightIcon,
  },
  props: {
    option: Object,
    totalVote: Number,
    voteCount: Number
  },

  data() {
    return {
      isVote: null,
    };
  },

  mounted() {
    this.checkVote();
  },

  updated() {
    this.checkVote();
  },

  methods: {
    vote() {
      this.isVote = !this.isVote;
    },
    async checkVote() {
      await axios
        .get(`/api/posts/group/poll/option/${this.option.id}/check-vote/`)
        .then((res) => {
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

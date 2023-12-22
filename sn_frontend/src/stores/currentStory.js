import { defineStore } from "pinia";
import router from "../router";

export const useCurrentStoryStore = defineStore({
  id: "currentUserStory",

  state: () => ({
    currentStory: [],
    userId: null,
  }),

  actions: {
    getCurrentUserStory(data) {
      data.forEach((story) => {
        if (!this.currentStory.map((s) => s.id).includes(story.id)) {
          this.currentStory.unshift(story);
          this.currentStory.reverse()

        }
      });
      console.log(this.currentStory)
      this.userId = data[0]?.created_by?.id;
    },
    resetCurrentStory() {
      this.currentStory = [];
    },
  },
});

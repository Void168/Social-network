import { defineStore } from "pinia";


export const useCurrentStoryStore = defineStore({
  id: "currentUserStory",

  state: () => ({
    currentStory: [],
  }),

  actions: {
    getCurrentUserStory(data) {
      this.currentStory = data
    },
  },
});

import { defineStore } from "pinia";


export const useCurrentStoryStore = defineStore({
  id: "currentUserStory",

  state: () => ({
    currentStory: [],
    userId: null
  }),

  actions: {
    getCurrentUserStory(data) {
      this.currentStory = data
      this.userId = data[0].created_by.id
    },
  },
});

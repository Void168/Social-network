import { defineStore } from "pinia";

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
          this.currentStory
            .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
        }
      });
      this.userId = data[0]?.created_by?.id;
    },
  },
});

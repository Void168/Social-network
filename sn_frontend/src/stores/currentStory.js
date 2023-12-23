import { defineStore } from "pinia";

export const useCurrentStoryStore = defineStore({
  id: "currentUserStory",

  state: () => ({
    currentStory: [],
    userId: null,
    currentUserId: null,
    listId: [],
  }),

  actions: {
    getCurrentUserId(data) {
      this.currentUserId = data;
    },
    getCurrentUserStory(data) {
      data.forEach((story) => {
        if (!this.currentStory.map((s) => s.id).includes(story.id)) {
          this.currentStory.unshift(story);
          this.currentStory.reverse();
        }
      });
      this.userId = data[0]?.created_by?.id;
    },
    getUserIdList(data) {
      data.forEach((id) => {
        this.listId.unshift(id);
      });

      if(!this.listId.includes(this.currentUserId)){
        this.listId.unshift(this.currentUserId)
      }

      if(this.listId.includes(this.userId)){
        this.listId.filter((id) => id === this.userId)
        if(this.listId.includes(this.currentUserId)){
          this.listId.splice(1, 0, this.userId)
        } else {
          this.listId.unshift(this.listId)
        }
      }
      this.listId = [... new Set(this.listId)]

      console.log(this.listId)
    },
    resetCurrentStory() {
      this.currentStory = [];
    },
    resetListId() {
      this.listId = [];
    },
  },
});

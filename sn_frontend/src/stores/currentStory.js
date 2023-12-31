import { defineStore } from "pinia";

export const useCurrentStoryStore = defineStore({
  id: "currentUserStory",

  state: () => ({
    currentStory: [],
    userId: null,
    currentUserId: null,
    activeStory: null,
    listId: [],
    activeSlide: 0,
  }),

  actions: {
    getCurrentUserId(data) {
      this.currentUserId = data;
    },
    getCurrentUserStory(data) {
      data.forEach((story) => {
        if (!this.currentStory.map((s) => s.id).includes(story.id)) {
          this.currentStory.unshift(story);
          this.currentStory.sort(
            (a, b) => new Date(a.created_at) - new Date(b.created_at)
          );
        }
      });
      this.userId = data[0]?.created_by?.id;
      if(this.listId.includes(this.userId)){
        this.listId.filter((id) => id === this.userId)
        if(this.listId.includes(this.currentUserId)){
          this.listId.splice(1, 0, this.userId)
        } else {
          this.listId.unshift(this.listId)
        }
      }
      this.listId = [... new Set(this.listId)]
    },
    getActiveSlide(data){
      this.activeSlide = data
    },
    getActiveStory(data){
      this.activeStory = data
    },
    getUserIdList(data) {
      data.forEach((id) => {
        this.listId.unshift(id);
        this.listId.reverse()
      });
      if(!this.listId.includes(this.currentUserId)){
        this.listId.unshift(this.currentUserId)
      }
    },
    resetCurrentStory() {
      this.currentStory = [];
    },
    resetListId() {
      this.listId = [];
    },
    resetActiveStory(){
      this.activeStory = null
    }
  },
});

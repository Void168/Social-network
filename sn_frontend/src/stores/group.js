import { defineStore } from "pinia";

export const useGroupStore = defineStore({
  id: "group",

  state: () => ({
    groupQuery: localStorage.getItem("groupQuery"),
  }),

  actions: {
    setQuery(query) {
        this.groupQuery = localStorage.setItem('groupQuery', query)
    },
  },
});

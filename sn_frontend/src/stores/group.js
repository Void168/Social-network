import { defineStore } from "pinia";

export const useGroupStore = defineStore({
  id: "group",

  state: () => ({
    groupQuery: localStorage.getItem("groupQuery"),
    defaultTab: 1
  }),

  actions: {
    setQuery(query) {
        this.groupQuery = localStorage.setItem('groupQuery', query)
    },
    setDefaultTab(tab) {
        this.tab = tab
    },
  },
});

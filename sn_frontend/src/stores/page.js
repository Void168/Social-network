import { defineStore } from "pinia";

import axios from "axios";

export const usePageStore = defineStore({
  id: "page",

  state: () => ({
    pagesList: [],
    pageActive: {},
    pageId: localStorage.getItem("pageId"),
  }),

  actions: {
    setActivePage(pageId) {
      const listPageId = this.pagesList.map((page) => page.id);
      const pagePosition = listPageId.indexOf(pageId);
      this.pageActive = this.pagesList[pagePosition];
      this.pageId = localStorage.setItem("pageId", this.pageActive.id);
    },
    async getActivePage() {
      if(this.pageId){
        await axios
          .get(`/api/page/get-page/${this.pageId}/`)
          .then((res) => {
            this.pageActive = res.data.data;
          })
          .catch((erorr) => {
  
          });
      }
    },
    async getPagesList(data) {
      await axios
        .get(`/api/page/get-pages/${data}/`)
        .then((res) => {
          this.pagesList = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    outPage() {
      localStorage.setItem("pageId", "");
    },
  },
});

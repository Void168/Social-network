import { defineStore } from "pinia";

import axios from "axios";

export const usePageStore = defineStore({
  id: "page",

  state: () => ({
    pageActive: {
      id: null,
      name: null,
      email: null,
      avatar: null,
      cover_image: null,
    },
  }),

  actions: {
    async initPageStore(id) {
      await axios
        .get(`/api/page/get-page/${id}/`)
        .then((res) => {
          this.pageActive.id = res.data.id;
          this.pageActive.name = res.data.name;
          this.pageActive.email = res.data.email;
          this.pageActive.avatar = res.data.get_avatar;
          this.pageActive.cover_image = res.data.get_cover_image;
          console.log(this.pageActive)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    outPage() {
      this.pageActive.id = null;
      this.pageActive.name = null;
      this.pageActive.email = null;
      this.pageActive.avatar = null;
      this.pageActive.cover_image = null;
    },
  },
});

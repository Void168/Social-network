import { defineStore } from "pinia";

import axios from "axios";

export const useNotificationStore = defineStore({
  id: "notification",

  state: () => ({
    length: 0,
  }),

  actions: {
    getNotifications() {
      axios
        .get("/api/notifications/")
        .then((res) => {
            this.length = res.data.filter((noti) => !noti.is_read).length;

        })
        .catch((error) => {
            console.log(error);
        });
        
        return this.length
    },
  },
});

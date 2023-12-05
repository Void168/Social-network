import { defineStore } from "pinia";

import axios from "axios";
import Pusher from "pusher-js";
import { useUserStore } from '../stores/user'

export const useNotificationStore = defineStore({
  id: "notification",

  state: () => ({
    length: 0,
    allNotifications: [],
    userStore: useUserStore()
  }),

  actions: {
    getNotifications() {
      axios
        .get("/api/notifications/")
        .then((res) => {
          this.allNotifications = res.data;
          Pusher.logToConsole = false;

          const pusher = new Pusher(`${import.meta.env.VITE_PUSHER_KEY}`, {
            cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
          });
          const channel = pusher.subscribe(
            `${this.userStore.user.id}-notification`
          );
          channel.bind("like-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          channel.bind("comment-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          channel.bind("relationship-request-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          channel.bind("accepted-relationship-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          channel.bind("send-friendship-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          channel.bind("accept-friendship-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          channel.bind("tag-comment-notification:new", (data) => {
            this.allNotifications.push(JSON.parse(data.notification));
          });
          this.length = this.allNotifications.filter(
            (noti) => !noti.is_read
          ).length;
          console.log(this.length)
        })
        .catch((error) => {
          console.log(error);
        });

        return this.length;
      },
  },
});

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <div v-if="notifications?.length">
          <div
            v-for="notification in notifications.slice(0, lastNoti)"
            v-bind:key="notification.id"
            @click="readNotification(notification)"
          >
            <div
              class="p-4 bg-white border border-gray-200 rounded-lg mt-4 cursor-pointer dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-400"
              v-if="notification.is_read"
            >
              <div class="flex flex-col gap-2">
                <p>{{ notification.body }}</p>
                <p>{{ formatTime(notification.created_at) }} trước</p>
              </div>
            </div>
            <div
              class="flex justify-between items-center font-semibold text-emerald-600 p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 border rounded-lg mt-4 cursor-pointer"
              v-else
            >
              <div class="flex flex-col gap-2">
                <p>{{ notification.body }}</p>
                <p>{{ formatTime(notification.created_at) }} trước</p>
              </div>
              <span class="w-5 h-5 bg-emerald-600 rounded-full"></span>
            </div>
          </div>
          <div class="flex justify-center items-center mt-4">
            <button
              class="btn"
              @click="loadMore"
              v-if="lastNoti < notifications.length"
            >
              Tải thêm thông báo
            </button>
          </div>
        </div>
        <div v-else>
          <p>Bạn không có thông báo nào</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Pusher from "pusher-js";
import { useUserStore } from "../stores/user";

import vi from "date-fns/locale/vi";
import formatDistanceToNow from "date-fns/formatDistanceToNow";

export default (await import("vue")).defineComponent({
  name: "notifications",
  setup() {
    const userStore = useUserStore()

    return {
      userStore
    }
  },
  data() {
    return {
      notifications: [],
      lastNoti: 5,
    };
  },

  mounted() {
    this.getNotifications();
  },

  methods: {
    getPusher() {
      Pusher.logToConsole = false;

      const pusher = new Pusher(`${import.meta.env.VITE_PUSHER_KEY}`, {
        cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
      });
      const channel = pusher.subscribe(`${this.userStore.user.id}-notification`);
      channel.bind("like-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
      channel.bind("comment-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
      channel.bind("relationship-request-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
      channel.bind("accepted-relationship-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
      channel.bind("send-friendship-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
      channel.bind("accepted-friendship-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
      channel.bind("tag-comment-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
      });
    },
    formatTime(t) {
      const d1 = new Date(t);
      const result = d1.getTime();
      return formatDistanceToNow(result, { locale: vi });
    },
    getNotifications() {
      axios
        .get("/api/notifications/")
        .then((res) => {
          this.notifications = res.data;
          this.getPusher();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    loadMore() {
      this.lastNoti = this.lastNoti + 10;
      if (this.notifications.length < this.lastNoti) {
        this.lastNoti = this.post.comments.length;
      }
    },

    async readNotification(notification) {
      await axios
        .post(`/api/notifications/read/${notification.id}/`)
        .then((res) => {
          if (
            notification.type_of_notification === "post_like" ||
            notification.type_of_notification === "post_comment" ||
            notification.type_of_notification === "tag_comment"
          ) {
            this.$router.push({
              name: "postview",
              params: { id: notification.post.id },
            });
          }
          if (
            notification.type_of_notification === "new_relationship_request" ||
            notification.type_of_notification === "accepted_relationship_request"
          ) {
            this.$router.push({
              name: "profile",
              params: {
                id: notification.created_for.id,
              },
            });
          }
          if (
            notification.type_of_notification === "accepted_friend_request" ||
            notification.type_of_notification === "new_friend_request"
          ) {
            this.$router.push({
              name: "friends",
              params: {
                id: notification.created_for.id,
              },
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

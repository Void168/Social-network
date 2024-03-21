<template>
  <div class="max-w-7xl mx-auto gap-4">
    <div class="main-center shadow-none mx-auto md:py-12 md:w-[80%] space-y-4 min-h-screen">
      <div
        class="p-4 bg-white border shadow-md border-gray-200 md:rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <div class="flex gap-2 items-center">
          <div
            @click="getAllNotifications"
            :class="unRead ? 'dark:bg-slate-700 bg-slate-200' : 'bg-emerald-400'"
            class="px-4 py-2 font-semibold rounded-lg duration-75 dark:hover:bg-emerald-500 cursor-pointer shadow-md"
          >
            Tất cả
          </div>
          <div
            @click="getUnreadNotifications"
            :class="unRead ? 'bg-emerald-400' : 'dark:bg-slate-700 bg-slate-200'"
            class="px-4 py-2 font-semibold rounded-lg duration-75 dark:hover:bg-emerald-500 cursor-pointer shadow-md"
          >
            Chưa đọc
          </div>
        </div>
        <div v-if="allNotifications?.length">
          <div
            v-for="notification in allNotifications.slice(0, lastNoti)"
            v-bind:key="notification.id"
            @click="readNotification(notification)"
          >
            <div
              class="p-4 bg-white border border-gray-200 rounded-lg mt-4 cursor-pointer dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-400"
              v-if="notification.is_read"
            >
              <div class="flex flex-col gap-2 xs:text-base vs:text-sm">
                <p>{{ notification.body }}</p>
                <p>{{ formatTime(notification.created_at) }} trước</p>
              </div>
            </div>
            <div
              class="flex justify-between items-center font-semibold text-emerald-600 p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 border rounded-lg mt-4 cursor-pointer"
              v-else
            >
              <div class="flex flex-col gap-2 xs:text-base vs:text-sm">
                <p>{{ notification.body }}</p>
                <p>{{ formatTime(notification.created_at) }} trước</p>
              </div>
              <span class="xm:w-5 xm:h-5 vs:w-3 vs:h-3 bg-emerald-600 rounded-full"></span>
            </div>
          </div>
          <div class="flex justify-center items-center mt-4">
            <button
              class="btn"
              @click="loadMore"
              v-if="lastNoti < allNotifications.length"
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
import { usePageStore } from "../stores/page";

import vi from "date-fns/locale/vi";
import formatDistanceToNow from "date-fns/formatDistanceToNow";

export default (await import("vue")).defineComponent({
  name: "notifications",
  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore();

    return {
      userStore,
      pageStore,
    };
  },
  data() {
    return {
      notifications: [],
      lastNoti: 5,
      unRead: false,
    };
  },

  computed:{
    allNotifications(){
      return !this.unRead ? this.notifications : 
      this.notifications.filter((noti) => !noti.is_read)
    }
  },

  mounted() {
    this.getNotifications();
  },

  updated() {
    this.getPusher();
  },

  methods: {
    getPusher() {
      Pusher.logToConsole = false;

      const pusher = new Pusher(`${import.meta.env.VITE_PUSHER_KEY}`, {
        cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
      });
      const channel = pusher.subscribe(
        `${this.userStore.user.id}-notification`
      );
      channel.bind("like-notification:new", (data) => {
        this.notifications.push(JSON.parse(data.notification));
        console.log(JSON.parse(data.notification));
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
    async getNotifications() {
      if (!this.pageStore.pageId) {
        await axios
          .get("/api/notifications/")
          .then((res) => {
            this.notifications = res.data;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .get(`/api/notifications/page/${this.pageStore.pageId}/`)
          .then((res) => {
            this.notifications = res.data;
          })
          .catch((error) => {
            console.log(error);
          });
      }
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
            notification.type_of_notification ===
              "accepted_relationship_request"
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

    getAllNotifications() {
      this.unRead = false;
    },
    getUnreadNotifications() {
      this.unRead = true;
    },
  },
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <div v-if="notifications?.length">
          <div
            v-for="notification in notifications"
            v-bind:key="notification.id"
            @click="readNotification(notification)"
          >
            <div
              class="p-4 bg-white border border-gray-200 rounded-lg mt-4 cursor-pointer"
              v-if="notification.is_read"
            >
              <div class="flex flex-col gap-2">
                <p>{{ notification.body }}</p>
                <p>{{ formatTime(notification.created_at) }} trước</p>
              </div>
            </div>
            <div
              class="flex justify-between items-center font-semibold text-emerald-600 p-4 bg-gray-200 border rounded-lg mt-4 cursor-pointer"
              v-else
            >
              <div class="flex flex-col gap-2">
                <p>{{ notification.body }}</p>
                <p>{{ formatTime(notification.created_at) }} trước</p>
              </div>
              <span class="w-5 h-5 bg-emerald-600 rounded-full"></span>
            </div>
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
import vi from "date-fns/locale/vi";
import formatDistanceToNow from "date-fns/formatDistanceToNow";

export default (await import("vue")).defineComponent({
  name: "notifications",

  data() {
    return {
      notifications: [],
    };
  },

  mounted() {
    this.getNotifications();
  },

  methods: {
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
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async readNotification(notification) {
      console.log("readNotification", notification.id);

      await axios
        .post(`/api/notifications/read/${notification.id}/`)
        .then((res) => {
          console.log(res.data);

          if (
            notification.type_of_notification === "post_like" ||
            notification.type_of_notification === "post_comment"
          ) {
            this.$router.push({
              name: "postview",
              params: { id: notification.post_id },
            });
          } else {
            this.$router.push({
              name: "friends",
              params: {
                id: notification.created_for_id,
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

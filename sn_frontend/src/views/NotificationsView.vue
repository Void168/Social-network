<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <div
          class="p-4 bg-white border border-gray-200 rounded-lg mt-4"
          v-for="notification in notifications"
          v-bind:key="notification.id"
        >
          <div v-if="notifications.length">
            <p>{{ notification.body }}</p>
            <button @click="readNotification(notification)">Xem thêm</button>
          </div>
          <div v-else>
            <p>Bạn không có thông báo nào</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
    getNotifications() {
      axios
        .get("/api/notifications/")
        .then((res) => {
          console.log(res.data);

          this.notifications = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    readNotification(notification) {
      console.log("readNotification", notification.id);
    },
  },
});
</script>

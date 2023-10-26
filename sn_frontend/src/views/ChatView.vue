<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="bg-white border border-gray-200 rounded-lg h-[500px]">
        <h3 class="text-xl p-3">Đoạn hội thoại ({{ conversations.length }})</h3>
        <div>
          <ConversationBox
            v-bind:conversations="conversations"
            v-on:getConversations="getConversations"
          />
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <div
        class="bg-white h-[500px] border-gray-200 rounded-lg flex justify-center items-center"
      >
        Chưa chọn đoạn hội thoại nào
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";
import ConversationBox from "../components/ConversationBox.vue";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      conversations: [],
      body: "",
      lastMessage: {},
    };
  },
  mounted() {
    this.getConversations();
    this.getLastMessage();
  },

  methods: {
    getConversations() {
      axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getLastMessage() {
      axios
        .get(`/api/chat/${this.conversations.id}/get_last_message/`)
        .then((res) => {
          console.log(res.data);
          this.lastMessage = res.data;
        })
        .catch((error) => console.log(error));
    },
  },
});
</script>

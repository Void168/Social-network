<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        class="bg-white border border-gray-200 rounded-lg h-[750px] px-2"
      >
        <h3 class="text-xl p-3">Đoạn hội thoại ({{ conversations.length }})</h3>

        <ConversationBox v-bind:conversations="conversations" />
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <ChatBox v-bind:chats="conversations" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ConversationBox from "../components/ConversationBox.vue";
import ChatBox from "../components/ChatBox.vue";
import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  name: "chat",
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
  },
  data() {
    return {
      conversations: [],
      activeConversation: {},
      body: "",
      listMessages: [],
      lastMessage: {},
    };
  },
  watch: {
    "$route.params.id": {
      handler: function () {
        this.getMessages();
      },
      deep: true,
      immediate: true,
    },
  },
  mounted() {
    this.getConversations();
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
    getMessages() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
        .then((res) => {
          this.activeConversation = res.data;
          this.listMessages = this.activeConversation.messages;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      axios
        .post(`/api/chat/${this.activeConversation.id}/send/`, {
          body: this.body,
        })
        .then((res) => {
          this.activeConversation.messages.push(res.data);
          this.body = "";
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  components: { RouterLink, ConversationBox, ChatBox },
});
</script>

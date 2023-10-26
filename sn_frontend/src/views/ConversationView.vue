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
      <ChatBox
        v-bind:chats="conversations"
      />
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
      receivedUser: {},
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
            console.log(this.conversations)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getActiveConversation() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
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
          let users = [];
          for (let i = 0; i < this.activeConversation.users.length; i++) {
            users.push(this.activeConversation.users[i]);
          }
          const filteredUser = users?.filter(
            (id) => id !== this.userStore.user.id
          );
          const allowed = ["created_by", "sent_to"];
          const messages = this.activeConversation.messages
            .filter(
              (data) =>
                JSON.stringify(data).indexOf(this.userStore.user.id) !== -1
            )
            .find((createdby) => createdby.id !== this.userStore.user.id);
          const filtered = Object.keys(messages)
            .filter((key) => allowed.includes(key))
            .reduce((obj, key) => {
              return {
                ...obj,
                [key]: messages[key],
              };
            }, {});
          this.receivedUser = Object.values(filtered).filter(
            (data) =>
              JSON.stringify(data).toLowerCase().indexOf(filteredUser) !== -1
          )[0];
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getLastMessage(id) {
      this.conversations = this.conversations.filter(
        (conversation) => conversation.id === id
      );
    },

    submitForm() {
      axios
        .post(`/api/chat/${this.activeConversation.id}/send/`, {
          body: this.body,
        })
        .then((res) => {
          console.log(res.data);
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

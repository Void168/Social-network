<template>
  <div class="grid grid-cols-4 gap-4 h-screen">
    <div class="main-left col-span-1">
      <div
        class="bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg h-screen px-2"
      >
        <h3 class="text-xl p-3">Đoạn hội thoại ({{ conversations.length }})</h3>
        <div v-for="conversation in conversations" :key="conversation.id">
          <ConversationBox
            v-bind:conversations="conversations"
            v-bind:conversation="conversation"
            @seenMessage="seenMessage"
          />
        </div>
        <div
          class="flex flex-col bg-white dark:bg-slate-600 dark:text-neutral-200 rounded-lg px-2"
        >
          <h3 class="text-xl p-3">Đoạn hội thoại nhóm ({{ groupConversations.length }})</h3>
          <div
            @click="openModal"
            class="flex gap-2 items-center justify-center px-4 py-2 bg-neutral-200 hover:bg-neutral-300 dark:bg-slate-700 dark:hover:bg-slate-800 transition duration-100 rounded-md shadow-md cursor-pointer"
          >
            <PlusCircleIcon class="w-8 h-8" />
            <span>Tạo đoạn chat nhóm</span>
          </div>
          <div
            v-for="groupConversation in groupConversations"
            v-bind:key="groupConversation.id"
          >
            <GroupConversationBox v-bind:groupConversation="groupConversation" @seenGroupMessage="seenGroupMessage"/>
          </div>
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <ChatBox v-bind:chats="conversations" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ConversationBox from "../components/items/ConversationBox.vue";
import GroupConversationBox from "../components/items/GroupConversationBox.vue";
import ChatBox from "../components/items/ChatBox.vue";

import { useUserStore } from "../stores/user";
import { PlusCircleIcon } from "@heroicons/vue/24/outline";

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
      groupConversations: [],
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
    this.getGroupConversations();
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
    getGroupConversations() {
      axios
        .get("/api/chat/group/")
        .then((res) => {
          this.groupConversations = res.data
          // console.log(this.groupConversations);
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
          this.seenMessage();
          // console.log(this.activeConversation)
          this.listMessages = this.activeConversation.messages;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    seenMessage() {
      this.$emit("seenMessage", this.activeConversation.id);

      axios
        .post(`/api/chat/${this.activeConversation.id}/set_seen/`)
        .then((res) => {
          // console.log(res.data);
        })
        .catch((error) => console.log(error));
    },
    seenGroupMessage() {
      this.$emit("seenMessage", this.activeConversation.id);

      axios
        .post(`/api/chat/${this.activeConversation.id}/group_set_seen/`)
        .then((res) => {
          // console.log(res.data);
        })
        .catch((error) => console.log(error));
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
  components: { RouterLink, ConversationBox, ChatBox, PlusCircleIcon, GroupConversationBox },
});
</script>

<template>
  <div class="grid sm:grid-cols-4 grid-cols-3 max-h-screen" :class="isExpand ? 'requires-no-scroll' : ''">
    <div
      @click="expandChatNavigation"
      class="fixed flex md:hidden z-20 inset-y-2/4 w-5 h-20 dark:bg-slate-700 bg-white rounded-r-2xl"
      :class="isExpand ? 'left-[90%]' : 'left-0'"
    >
      <ChevronRightIcon class="dark:text-slate-200" v-if="!isExpand" />
      <ChevronLeftIcon class="dark:text-slate-200" v-else />
    </div>
    <div
      v-if="isExpand"
      class="w-full h-full absolute bg-slate-700/50 z-10 duration-100"
      @click="expandChatNavigation"
    ></div>
    <div
      class="main-left xl:col-span-1 sm:col-span-2 sm:sticky sm:block vs:z-10 sm:w-full vs:w-[90%] bottom-0"
      :class="isExpand ? 'vs:fixed' : 'hidden'"
    >
      <div
        :style="{ height: `${toastStore.height}px` }"
        class="bg-white overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 sm:rounded-lg h-screen px-2"
      >
        <h3 class="sm:text-xl p-3 sm:text-left text-center">
          Đoạn hội thoại ({{ conversations.length }})
        </h3>
        <div v-for="conversation in conversations" :key="conversation.id">
          <ConversationBox
            v-bind:conversations="conversations"
            v-bind:conversation="conversation"
            @seenMessage="seenMessage"
            @click="expandChatNavigation"
          />
        </div>
        <div
          class="flex flex-col bg-white dark:bg-slate-600 dark:text-neutral-200 rounded-lg px-2"
        >
          <h3 class="sm:text-xl p-3 sm:text-left text-center">
            Đoạn hội thoại nhóm ({{ groupConversations.length }})
          </h3>
          <div
            @click="openModal"
            class="flex gap-2 items-center justify-center px-4 py-2 bg-neutral-200 hover:bg-neutral-300 dark:bg-slate-700 dark:hover:bg-slate-800 transition duration-100 rounded-md shadow-md cursor-pointer"
          >
            <PlusCircleIcon class="w-8 h-8" />
            <span @click="getFriends"
              >Tạo đoạn chat nhóm</span
            >
          </div>
          <div
            v-for="groupConversation in groupConversations"
            v-bind:key="groupConversation.id"
          >
            <GroupConversationBox
              v-bind:groupConversation="groupConversation"
              @seenGroupMessage="seenGroupMessage"
            />
          </div>
          <h3 class="sm:text-xl p-3 sm:text-left text-center">
            Đoạn hội thoại trang ({{ pageConversations.length }})
          </h3>

          <div
            v-for="pageConversation in pageConversations"
            v-bind:key="pageConversation.id"
          >
            <PageConversationBox :pageConversation="pageConversation" />
          </div>
        </div>
      </div>
    </div>

    <div
      :style="{ minHeight: `${toastStore.height}px` }"
      class="main-center xl:col-span-3 sm:col-span-2 vs:col-span-3 space-y-4"
    >
      <ChatBox v-bind:chats="conversations" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ConversationBox from "../../components/items/chat/ConversationBox.vue";
import GroupConversationBox from "../../components/items/chat/GroupConversationBox.vue";
import ChatBox from "../../components/items/chat/ChatBox.vue";
import PageConversationBox from "../../components/items/chat/PageConversationBox.vue";

import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";

import { PlusCircleIcon } from "@heroicons/vue/24/outline";
import {
  UserIcon,
  UserGroupIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
} from "@heroicons/vue/24/solid";

import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  name: "conversation",
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  data() {
    return {
      conversations: [],
      groupConversations: [],
      pageConversations: [],
      activeConversation: {},
      body: "",
      listMessages: [],
      lastMessage: {},
      isExpand: false,
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
    expandChatNavigation() {
      this.isExpand = !this.isExpand;
    },
    async getConversations() {
      await axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data.conversations;
          this.pageConversations = res.data.page_conversations;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupConversations() {
      await axios
        .get("/api/chat/group/")
        .then((res) => {
          this.groupConversations = res.data;
          // console.log(this.groupConversations);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getMessages() {
      await axios
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
    async seenMessage() {
      this.$emit("seenMessage", this.activeConversation.id);

      await axios
        .post(`/api/chat/${this.activeConversation.id}/set_seen/`)
        .then((res) => {
          // console.log(res.data);
        })
        .catch((error) => console.log(error));
    },
    async seenGroupMessage() {
      this.$emit("seenMessage", this.activeConversation.id);

      await axios
        .post(`/api/chat/${this.activeConversation.id}/group_set_seen/`)
        .then((res) => {
          // console.log(res.data);
        })
        .catch((error) => console.log(error));
    },
  },
  components: {
    RouterLink,
    ConversationBox,
    ChatBox,
    PlusCircleIcon,
    GroupConversationBox,
    PageConversationBox,
    UserIcon,
    UserGroupIcon,
    ChevronRightIcon,
    ChevronLeftIcon,
  },
});
</script>

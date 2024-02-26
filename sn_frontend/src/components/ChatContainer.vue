<template>
  <div
    class="relative scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-l-lg overflow-y-scroll"
    :style="{height: `${toastStore.height - toastStore.peopleYouMayKnowHeight - toastStore.trendsHeight + 35}px`}"
  >
    <h3 class="xl:text-xl p-4 text-center">Người liên hệ</h3>
    <SkeletionLoadingChatBoxVue v-if="isLoading" />
    <div class="flex flex-col" v-else>
      <div v-for="friend in friends" :key="friend.id">
        <div
          @click="getFriendId(friend)"
          class="px-4 py-2 cursor-pointer hover:bg-slate-300 dark:hover:bg-slate-700"
        >
          <div @click="seenMessage">
            <div class="flex gap-2 items-center">
              <div class="relative">
                <img :src="friend.get_avatar" class="w-10 h-10 rounded-full" />
                <!-- v-if="connectionStore.isConnected" -->
                <span
                  class="w-3 h-3 bg-emerald-400 shadow-md absolute top-0 right-0 ring-4 dark:ring-slate-600 rounded-full"
                ></span>
              </div>
              <span class="font-semibold lg:text-sm sm:text-base">{{ friend.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <h3 class="xl:text-xl p-4 text-center">Đoạn chat nhóm</h3>
    <div
      v-for="groupConversation in groupConversations"
      v-bind:key="groupConversation.id"
      class="hover:bg-slate-300 dark:hover:bg-slate-700"
    >
      <RouterLink
        :to="{
          name: 'groupConversation',
          params: { id: groupConversation.id },
        }"
        class="flex items-center gap-2 px-4 py-2 cursor-pointer"
      >
        <img
          v-if="groupConversation.get_avatar"
          :src="groupConversation.get_avatar"
          alt=""
          class="h-10 w-10 rounded-full"
        />
        <img
          v-else
          :src="groupConversation.admin.get_avatar"
          alt=""
          class="h-10 w-10 rounded-full"
        />
        <p class="font-semibold truncate">{{ groupConversation.group_name }}</p>
      </RouterLink>
    </div>
    <div class="fixed flex gap-1 justify-end bottom-0 right-32 max-w-[1220px] z-50">
      <div v-for="friend in friendsChat" :key="friend.id">
        <ChatWindow
          :friend="friend"
          :conversation="conversation"
          @removeFriendChat="removeFriendChat(friend)"
          @miniatureChat="miniatureChat(friend)"
        />
      </div>
    </div>
    <div class="absolute bottom-3 right-1">
      <div class="flex flex-col" v-for="friend in chats" :key="friend.id">
        <ChatBubble :friend="friend" @openChatWindow="openChatWindow(friend)" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
// import { useConnectionStore } from "../stores/connection";

import { RouterLink } from "vue-router";
import GroupConversationBox from "./items/chat/GroupConversationBox.vue";

import ChatWindow from "./items/chat/ChatWindow.vue";
import ChatBubble from "./items/chat/ChatBubble.vue";

import {
  XMarkIcon,
  MinusIcon,
  PhoneIcon,
  VideoCameraIcon,
  ChevronDownIcon,
  PaperAirplaneIcon,
  PlusCircleIcon,
  PhotoIcon,
  GifIcon,
  FaceSmileIcon,
} from "@heroicons/vue/24/solid";

import "emoji-picker-element";

import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import SkeletionLoadingChatBoxVue from "./loadings/SkeletionLoadingChatBox.vue";
import { useToastStore } from "../stores/toast";
import { th } from "date-fns/locale";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    RouterLink,
    Popover,
    PopoverButton,
    PopoverPanel,
    ChatWindow,
    ChatBubble,
    GroupConversationBox,
    SkeletionLoadingChatBoxVue,
    XMarkIcon,
    MinusIcon,
    PhoneIcon,
    VideoCameraIcon,
    ChevronDownIcon,
    PaperAirplaneIcon,
    PlusCircleIcon,
    PhotoIcon,
    GifIcon,
    FaceSmileIcon,
  },
  setup() {
    const userStore = useUserStore();
    // const connectionStore = useConnectionStore();
    const toastStore = useToastStore()

    return {
      userStore,
      toastStore,
      // connectionStore,
    };
  },

  data() {
    return {
      conversations: [],
      groupConversations: [],
      friendsChat: [],
      bubbleChats: [],
      body: "",
      friends: [],
      isMini: false,
      conversation: {},
      isLoading: false,
    };
  },

  computed: {
    chats() {
      return this.bubbleChats.reverse();
    },
  },

  mounted() {
    this.getFriends();
    this.getConversations();
    this.getGroupConversations();
  },

  methods: {
    async getFriends() {
      this.isLoading = true;
      await axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          this.friendshipRequests = res.data.requests;
          this.friends = res.data.friends;
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getConversations() {
      await axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data;
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
    miniatureChat(friend) {
      this.friendsChat = this.friendsChat?.filter((fc) => fc !== friend);
      if (!this.bubbleChats?.includes(friend)) {
        this.bubbleChats?.reverse().push(friend);
      }
    },
    getFriendId(friend) {
      if (!this.friendsChat?.includes(friend)) {
        this.friendsChat?.push(friend);
      }
      if (this.bubbleChats?.includes(friend)) {
        this.bubbleChats = this.bubbleChats
          ?.filter((bbc) => bbc !== friend)
          .reverse();
      }
      if (
        this.friendsChat.length > 3 &&
        !this.bubbleChats?.includes(this.friendsChat[0]) && this.toastStore.width > 1380
      ) {
        this.bubbleChats?.reverse().push(this.friendsChat[0]);
        this.friendsChat?.reverse().pop();
      }
      if (
        this.friendsChat.length > 2 &&
        !this.bubbleChats?.includes(this.friendsChat[0]) && this.toastStore.width > 990 && this.toastStore.width < 1380
      ) {
        this.bubbleChats?.reverse().push(this.friendsChat[0]);
        this.friendsChat?.reverse().pop();
      }
      if (
        this.friendsChat.length > 1 &&
        !this.bubbleChats?.includes(this.friendsChat[0]) && this.toastStore.width > 640 && this.toastStore.width < 990
      ) {
        this.bubbleChats?.reverse().push(this.friendsChat[0]);
        this.friendsChat?.reverse().pop();
      }
    },
    openChatWindow(friend) {
      if (!this.friendsChat?.includes(friend)) {
        this.friendsChat?.push(friend);
      }
      if (this.bubbleChats?.includes(friend)) {
        this.bubbleChats = this.bubbleChats
          ?.filter((bbc) => bbc !== friend)
          .reverse();
      }
      if (
        this.friendsChat.length > 3 &&
        !this.bubbleChats?.includes(this.friendsChat[0]) && this.toastStore.width > 1380
      ) {
        this.bubbleChats?.reverse().push(this.friendsChat[0]);
        this.friendsChat?.reverse().pop();
      }
      if (
        this.friendsChat.length > 2 &&
        !this.bubbleChats?.includes(this.friendsChat[0]) && this.toastStore.width > 990 && this.toastStore.width < 1380
      ) {
        this.bubbleChats?.reverse().push(this.friendsChat[0]);
        this.friendsChat?.reverse().pop();
      }
      if (
        this.friendsChat.length > 1 &&
        !this.bubbleChats?.includes(this.friendsChat[0]) && this.toastStore.width > 640 && this.toastStore.width < 990
      ) {
        this.bubbleChats?.reverse().push(this.friendsChat[0]);
        this.friendsChat?.reverse().pop();
      }
    },
    removeFriendChat(friend) {
      this.friendsChat = this.friendsChat?.filter((fc) => fc !== friend);
      this.bubbleChats = this.bubbleChats?.filter((bbc) => bbc !== friend);
    },
    removeBubbleChat(friend) {
      this.bubbleChats = this.bubbleChats?.filter((bbc) => bbc !== friend);
    },
    Pick() {
      document
        .querySelector("emoji-picker")
        .addEventListener("emoji-click", (event) => {
          this.body = this.body + event.detail.unicode;

          return this.body;
        });
    },
    seenMessage() {
      this.$emit("seenMessage", this.conversation?.id);
      if (this.conversation?.id) {
        axios
          .post(`/api/chat/${this.conversation?.id}/set_seen/`)
          .then((res) => {
            // console.log(res.data);
          })
          .catch((error) => console.log(error));
      }
    },
  },
});
</script>

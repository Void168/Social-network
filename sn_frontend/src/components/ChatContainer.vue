<template>
  <div
    class="mr-5 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg h-[630px]"
  >
    <h3 class="text-xl p-4">Người liên hệ</h3>
    <div class="flex flex-col">
      <div v-for="friend in friends" :key="friend.id">
        <div
          @click="getFriendId(friend)"
          class="flex gap-2 px-4 py-2 items-center cursor-pointer hover:bg-slate-300 dark:hover:bg-slate-700"
        >
          <img :src="friend.get_avatar" class="w-10 h-10 rounded-full" />
          <span class="font-semibold">{{ friend.name }}</span>
        </div>
      </div>
    </div>
    <div class="fixed flex gap-1 justify-end bottom-0 right-32 max-w-[1220px]">
      <div v-for="friend in friendsChat" :key="friend.id">
        <ChatWindow
          :friend="friend"
          :conversation="conversation"
          @removeFriendChat="removeFriendChat(friend)"
          @miniatureChat="miniatureChat(friend)"
        />
      </div>
    </div>
    <div class="absolute bottom-0 right-0">
      <div class="flex flex-col" v-for="friend in chats" :key="friend.id">
        <ChatBubble :friend="friend" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";
import ConversationBox from "../components/items/ConversationBox.vue";
import ChatWindow from "../components/items/ChatWindow.vue";
import ChatBubble from "../components/items/ChatBubble.vue";

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

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
    Popover,
    PopoverButton,
    PopoverPanel,
    ChatWindow,
    ChatBubble,
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

    return {
      userStore,
    };
  },

  data() {
    return {
      conversations: [],
      friendsChat: [],
      bubbleChats: [],
      body: "",
      friends: [],
      isMini: false,
      userAvatar: "",
      conversation: {},
    };
  },

  computed: {
    chats() {
      return this.bubbleChats.reverse();
    },
  },

  mounted() {
    this.getFriends();
  },

  methods: {
    getFriends() {
      axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          console.log(res.data);

          this.friendshipRequests = res.data.requests;
          this.friends = res.data.friends;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    miniatureChat(friend) {
        this.friendsChat = this.friendsChat?.filter((bbc) => bbc !== friend);
      if (!this.bubbleChats?.includes(friend)) {
        this.bubbleChats?.push(friend);
      }

      this.userAvatar = friend.get_avatar;
      console.log(this.bubbleChats);
      console.log(this.friendsChat);
    },
    getFriendId(friend) {
      axios
        .get(`/api/user-info/${friend.id}`)
        .then((res) => {
          this.getConversation();
        })
        .catch((error) => console.log(error));
      if (!this.friendsChat?.includes(friend)) {
        this.friendsChat?.push(friend);
      }
      if (this.bubbleChats?.includes(friend)) {
        this.bubbleChats = this.bubbleChats?.filter((bbc) => bbc !== friend);
      }
      console.log(this.bubbleChats); //all
      console.log(this.friendsChat); //null
    },
    removeFriendChat(friend) {
      this.friendsChat = this.friendsChat?.filter((bbc) => bbc !== friend);
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
    getConversation() {
      console.log("hello");
    },
  },
});
</script>

<template>
  <div
    class="grid 2xl:grid-cols-5 sm:grid-cols-4 grid-cols-3 max-h-screen overflow-x-hidden"
    :style="{ maxWidth: `${toastStore.width}px` }"
  >
    <div
      class="main-left xl:col-span-1 sm:col-span-2 xs:col-span-1 sticky bottom-0"
    >
      <div
        :style="{ height: `${toastStore.height}px` }"
        class="bg-white overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg px-2"
      >
        <h3 class="sm:text-xl p-3 xm:block hidden sm:text-left text-center">
          Đoạn hội thoại ({{ conversations.length }})
        </h3>
        <div class="flex justify-center items-center xm:hidden p-3">
          <UserIcon class="w-6" /> ({{ conversations.length }})
        </div>
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
          <h3 class="text-xl p-3 sm:block hidden">
            Đoạn hội thoại nhóm ({{ groupConversations.length }})
          </h3>
          <h3 class="p-3 sm:hidden text-center xs:hidden xm:block">
            Chat nhóm ({{ groupConversations.length }})
          </h3>
          <div class="flex justify-center items-center xm:hidden p-3">
            <UserGroupIcon class="w-6" /> ({{ conversations.length }})
          </div>
          <div
            @click="openModal"
            class="flex gap-2 items-center justify-center px-4 py-2 bg-neutral-200 hover:bg-neutral-300 dark:bg-slate-700 dark:hover:bg-slate-800 transition duration-100 rounded-md shadow-md cursor-pointer"
          >
            <PlusCircleIcon class="w-8 h-8" />
            <span @click="getFriends" class="sm:block hidden"
              >Tạo đoạn chat nhóm</span
            >
            <span
              @click="getFriends"
              class="sm:hidden block sm:text-base xs:hidden"
              >Tạo nhóm</span
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
        </div>
      </div>
    </div>
    <div
      @click="expandInfomation"
      class="absolute flex 2xl:hidden right-0 z-20 inset-y-2/4 w-5 h-20 bg-slate-800 rounded-l-2xl"
      :class="isExpand ? '-translate-x-[320px]' : '-translate-x-0'"
    >
      <ChevronLeftIcon class="dark:text-slate-200" v-if="!isExpand" />
      <ChevronRightIcon class="dark:text-slate-200" v-else />
    </div>
    <div
      class="main-center xl:col-span-3 sm:col-span-2 xs:col-span-2 space-y-4"
    >
      <GroupChatBox />
    </div>
    <div
      :style="{ height: `${toastStore.height}px` }"
      class="absolute z-10 right-0 translate-x-[320px] 2xl:hidden bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-l-lg overflow-y-auto scrollbar-thin scrollbar-corner-slate-200 scrollbar-thumb-slate-400 scrollbar-track-slate-800 w-[320px]"
      :class="
        isExpand
          ? '-translate-x-0 ease-in-out transition duration-200'
          : '-translate-x-[-320px] ease-in-out transition duration-200 hidden'
      "
    >
      <GroupChatInfo v-bind:activeConversation="activeConversation" />
    </div>
    <div
      :style="{ height: `${toastStore.height}px` }"
      class="2xl:col-span-1 2xl:block hidden overflow-y-auto scrollbar-thin scrollbar-corner-slate-200 scrollbar-thumb-slate-400 scrollbar-track-slate-800 space-y-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
    >
      <GroupChatInfo v-bind:activeConversation="activeConversation" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import GroupConversationBox from "../components/items/chat/GroupConversationBox.vue";
import GroupChatBox from "../components/items/chat/GroupChatBox.vue";
import GroupChatInfo from "../components/items/chat/GroupChatInfo.vue";

import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";

import { PlusCircleIcon } from "@heroicons/vue/24/outline";
import {
  UserIcon,
  UserGroupIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/vue/24/solid";

import { RouterLink } from "vue-router";
import { defineAsyncComponent } from "vue";
import SkeletonLoadingPost from "../components/loadings/SkeletonLoadingPost.vue";

const ConversationBox = defineAsyncComponent({
  loader: () => import("../components/items/chat/ConversationBox.vue"),
  loadingComponent: SkeletonLoadingPost,
});

export default (await import("vue")).defineComponent({
  name: "groupchat",
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
          this.groupConversations = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getMessages() {
      setTimeout(() => {
        axios
          .get(`/api/chat/group/${this.$route.params.id}/`)
          .then((res) => {
            this.activeConversation = res.data;
            this.seenMessage();
            // console.log(this.activeConversation)
            this.listMessages = this.activeConversation?.group_messages;
          })
          .catch((error) => {
            console.log(error);
          });
      }, 1500);
    },
    seenMessage() {
      setTimeout(() => {
        this.$emit("seenMessage", this.activeConversation?.id);

        axios
          .post(`/api/chat/${this.activeConversation?.id}/group_set_seen/`)
          .then((res) => {
            // console.log(res.data);
          })
          .catch((error) => console.log(error));
      }, 2500);
    },
    expandInfomation() {
      this.isExpand = !this.isExpand;
    },
    seenGroupMessage() {
      setTimeout(() => {
        this.$emit("seenMessage", this.activeConversation?.id);

        axios
          .post(`/api/chat/${this.activeConversation?.id}/group_set_seen/`)
          .then((res) => {
            // console.log(res.data);
          })
          .catch((error) => console.log(error));
      }, 1500);
    },
    submitForm() {
      axios
        .post(`/api/chat/${this.activeConversation.id}/send_group/`, {
          body: this.body,
        })
        .then((res) => {
          this.activeConversation.group_messages.push(res.data);
          this.body = "";
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  components: {
    RouterLink,
    ConversationBox,
    PlusCircleIcon,
    GroupConversationBox,
    GroupChatInfo,
    GroupChatBox,
    SkeletonLoadingPost,
    UserIcon,
    UserGroupIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
  },
});
</script>

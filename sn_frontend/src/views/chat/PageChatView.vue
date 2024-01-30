<template>
  <div class="grid sm:grid-cols-4 grid-cols-3 max-h-screen">
    <div
      class="main-left xl:col-span-1 sm:col-span-2 xs:col-span-1 sticky bottom-0"
    >
      <div
        :style="{ height: `${toastStore.height}px` }"
        class="bg-white overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg h-screen px-2"
      >
        <h3 class="sm:text-xl p-3 xm:block hidden sm:text-left text-center">
          Đoạn hội thoại ({{
            !pageStore.pageId
              ? conversations?.length
              : pageConversations?.length
          }})
        </h3>
        <div class="flex justify-center items-center xm:hidden p-3">
          <UserIcon class="w-6" /> ({{ conversations?.length }})
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
          <h3 class="text-xl p-3 sm:block hidden" v-if="!pageStore.pageId">
            Đoạn hội thoại nhóm ({{ groupConversations.length }})
          </h3>
          <h3
            class="p-3 sm:hidden text-center xs:hidden xm:block"
            v-if="!pageStore.pageId"
          >
            Chat nhóm ({{ groupConversations.length }})
          </h3>
          <div
            class="flex justify-center items-center xm:hidden p-3"
            v-if="!pageStore.pageId"
          >
            <UserGroupIcon class="w-6" /> ({{ conversations.length }})
          </div>
          <div
            v-if="!pageStore.pageId"
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
          <h3
            class="sm:text-xl p-3 xm:block hidden sm:text-left text-center"
            v-if="!pageStore.pageId"
          >
            Đoạn hội thoại trang ({{ pageConversations.length }})
          </h3>
          <div
            class="flex justify-center items-center xm:hidden p-3"
            v-if="!pageStore.pageId"
          >
            <UserIcon class="w-6" /> ({{ conversations.length }})
          </div>
          <div
            v-for="pageConversation in pageConversations"
            v-bind:key="pageConversation.id"
          >
            <PageConversationBox
              :pageConversation="pageConversation"
              @seenPageMessage="seenPageMessage"
            />
          </div>
        </div>
      </div>
    </div>

    <div
      :style="{ minHeight: `${toastStore.height}px` }"
      class="main-center xl:col-span-3 sm:col-span-2 xs:col-span-2 space-y-4"
    >
      <PageChatBox />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ConversationBox from "../../components/items/chat/ConversationBox.vue";
import GroupConversationBox from "../../components/items/chat/GroupConversationBox.vue";
import PageChatBox from "../../components/items/chat/PageChatBox.vue";
import PageConversationBox from "../../components/items/chat/PageConversationBox.vue";

import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { usePageStore } from "../../stores/page";

import { PlusCircleIcon } from "@heroicons/vue/24/outline";
import { UserIcon, UserGroupIcon } from "@heroicons/vue/24/solid";

import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  name: "pageConversation",
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore();

    return {
      userStore,
      toastStore,
      pageStore,
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
    async getConversations() {
      if (!this.pageStore.pageId) {
        await axios
          .get("/api/chat/")
          .then((res) => {
            this.conversations = res.data.conversations;
            this.pageConversations = res.data.page_conversations;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        await axios
          .get(`/api/chat/page/${this.pageStore.pageId}/`)
          .then((res) => {
            this.pageConversations = res.data;
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    async getGroupConversations() {
      if (!this.pageStore.pageId)
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
        .get(`/api/chat/page/${this.$route.params.id}/detail/`)
        .then((res) => {
          this.activeConversation = res.data;
          this.seenPageMessage();
          // console.log(this.activeConversation)
          this.listMessages = this.activeConversation.messages;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async seenMessage() {
      if(!this.pageStore.pageId){
        this.$emit("seenMessage", this.activeConversation.id);
        await axios
          .post(`/api/chat/${this.activeConversation.id}/set_seen/`)
          .then((res) => {
            // console.log(res.data);
          })
          .catch((error) => console.log(error));
      }
    },
    async seenGroupMessage() {
      if(!this.pageStore.pageId){
        this.$emit("seenGroupMessage", this.activeConversation.id);
  
        await axios
          .post(`/api/chat/${this.activeConversation.id}/group_set_seen/`)
          .then((res) => {
            // console.log(res.data);
          })
          .catch((error) => console.log(error));
      }
    },
    async seenPageMessage() {
      this.$emit("seenPageMessage", this.activeConversation.id);
      if (!this.pageStore.pageId) {
        await axios
          .post(`/api/chat/page/${this.activeConversation.id}/set_seen/`)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => console.log(error));
      } else {
        await axios
          .post(
            `/api/chat/page/${this.pageStore.pageId}/set_seen/${this.activeConversation.id}/`
          )
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => console.log(error));
      }
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
  components: {
    RouterLink,
    ConversationBox,
    PageChatBox,
    PlusCircleIcon,
    GroupConversationBox,
    PageConversationBox,
    UserIcon,
    UserGroupIcon,
  },
});
</script>

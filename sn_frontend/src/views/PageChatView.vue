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
            <h3 class="sm:text-xl p-3 xm:block hidden sm:text-left text-center">
            Đoạn hội thoại trang ({{ pageConversations.length }})
          </h3>
          <div class="flex justify-center items-center xm:hidden p-3">
            <UserIcon class="w-6" /> ({{ conversations.length }})
          </div>
  
          <div
            v-for="pageConversation in pageConversations"
            v-bind:key="pageConversation.id"
          >
            <PageConversationBox :pageConversation="pageConversation"/>
          </div>
          </div>
        </div>
      </div>
  
      <div
        :style="{ minHeight: `${toastStore.height}px` }"
        class="main-center xl:col-span-3 sm:col-span-2 xs:col-span-2 space-y-4"
      >
        <PageChatBox  />
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import ConversationBox from "../components/items/chat/ConversationBox.vue";
  import GroupConversationBox from "../components/items/chat/GroupConversationBox.vue";
  import PageChatBox from "../components/items/chat/PageChatBox.vue";
  import PageConversationBox from "../components/items/chat/PageConversationBox.vue";
  
  import { useUserStore } from "../stores/user";
  import { useToastStore } from "../stores/toast";
  
  import { PlusCircleIcon } from "@heroicons/vue/24/outline";
  import { UserIcon, UserGroupIcon } from "@heroicons/vue/24/solid";
  
  import { RouterLink } from "vue-router";
  
  export default (await import("vue")).defineComponent({
    name: "pageConversation",
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
        await axios
          .get("/api/chat/")
          .then((res) => {
            this.conversations = res.data.conversations;
            this.pageConversations = res.data.page_conversations
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
          .get(`/api/chat/page/${this.$route.params.id}/`)
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
        // this.$emit("seenMessage", this.activeConversation.id);
  
        // await axios
        //   .post(`/api/chat/${this.activeConversation.id}/set_seen/`)
        //   .then((res) => {
        //     // console.log(res.data);
        //   })
        //   .catch((error) => console.log(error));
        console.log('hello')
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
  
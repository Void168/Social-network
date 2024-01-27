<template>
  <div class="grid sm:grid-cols-4 grid-cols-3 gap-4">
    <div
      class="main-left xl:col-span-1 sm:col-span-2 xs:col-span-1 sticky bottom-0"
    >
      <div
        :style="{ height: `${toastStore.height}px` }"
        class="bg-white border overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border-b border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg px-2"
      >
        <h3 class="sm:text-xl p-3 xm:block hidden sm:text-left text-center">
          Đoạn hội thoại ({{ pageStore.pageId ? pageConversations.length : conversations.length }})
        </h3>
        <div class="flex justify-center items-center xm:hidden p-3">
          <UserIcon class="w-6" /> ({{ pageStore.pageId ? pageConversations.length : conversations.length }})
        </div>

        <div class="relative">
          <MagnifyingGlassIcon
            class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
          />
          <input
            @keyup="getQuery"
            ref="input"
            type="text"
            placeholder="Tìm kiếm đoạn hội thoại"
            class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
          />
        </div>
        <div class="flex flex-col bg-white dark:bg-slate-600 dark:text-neutral-200 rounded-lg px-2" v-if="!pageStore.pageId">
          <div
            v-for="conversation in conversations"
            v-bind:key="conversation.id"
          >
            <ConversationBox :conversation="conversation" v-if="!pageStore.pageId"/>
          </div>
        </div>
        <div
          v-if="!pageStore.pageId"
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
            />
          </div>
        </div>
        <div
          class="flex flex-col bg-white dark:bg-slate-600 dark:text-neutral-200 rounded-lg px-2">
          <h3 class="sm:text-xl p-3 xm:block hidden sm:text-left text-center" v-if="!pageStore.pageId">
            Đoạn hội thoại trang ({{ pageConversations.length }})
          </h3>
          <div class="flex justify-center items-center xm:hidden p-3">
            <UserIcon class="w-6" /> ({{ pageConversations.length }})
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
      class="main-center xl:col-span-3 sm:col-span-2 xs:col-span-2 space-y-4"
    >
      <div
        :style="{ minHeight: `${toastStore.height}px` }"
        class="bg-white border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex justify-center items-center"
      >
        Chưa chọn đoạn hội thoại nào
      </div>
    </div>
    <CreateGroupChatModal
      :show="isCreateGroupOpen"
      @closeModal="closeModal"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";
import { usePageStore } from "../stores/page";
import { RouterLink } from "vue-router";

import ConversationBox from "../components/items/chat/ConversationBox.vue";
import CreateGroupChatModal from "../components/modals/chat/CreateGroupChatModal.vue";
import GroupConversationBox from "../components/items/chat/GroupConversationBox.vue";
import PageConversationBox from "../components/items/chat/PageConversationBox.vue";

import { MagnifyingGlassIcon, PlusCircleIcon } from "@heroicons/vue/24/outline";
import { UserIcon, UserGroupIcon } from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
    CreateGroupChatModal,
    GroupConversationBox,
    PageConversationBox,
    MagnifyingGlassIcon,
    PlusCircleIcon,
    UserIcon,
    UserGroupIcon,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore()

    return {
      userStore,
      toastStore,
      pageStore,
    };
  },

  data() {
    return {
      conversations: [],
      pageConversations: [],
      groupConversations: [],
      body: "",
      query: "",
      isCreateGroupOpen: false,
      options: [],
    };
  },

  computed: {
    filteredConversation() {
      return this.query === ""
        ? this.conversations
        : this.conversations?.filter((conversation) =>
            conversation?.users
              .map((user) => user?.name?.toLowerCase())
              .filter((name) => name !== this.userStore.user.name.toLowerCase())
              .includes(this.query)
          );
    },
  },

  mounted() {
    this.getConversations();
    this.getGroupConversations();
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getConversations();
      },
      deep: true,
      immediate: true,
    },
  },

  methods: {
    async getConversations() {
      if(!this.pageStore.pageId){
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
    async getFriends() {
      if(!this.pageStore.pageId){
        await axios
          .get(`/api/friends/${this.userStore.user.id}/`)
          .then((res) => {
            // console.log(res.data)
            res.data.friends?.forEach((friend) => {
              const obj = {};
              obj["label"] = friend.name;
              obj["value"] = friend.id;
              this.options.push(obj);
            });
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    async getGroupConversations() {
      if(!this.pageStore.pageId){
        await axios
          .get("/api/chat/group/")
          .then((res) => {
            this.groupConversations = res.data;
            console.log(this.groupConversations);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    getQuery() {
      this.query = this.$refs.input.value;
    },
    closeModal() {
      this.isCreateGroupOpen = false;
    },
    openModal() {
      this.isCreateGroupOpen = true;
    },
  },
});
</script>

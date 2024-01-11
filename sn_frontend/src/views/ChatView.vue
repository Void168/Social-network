<template>
  <div class="grid sm:grid-cols-4 grid-cols-3 gap-4 max-h-screen">
    <div
      class="main-left xl:col-span-1 sm:col-span-2 xs:col-span-1 sticky bottom-0"
    >
      <div
        :style="{ height: `${toastStore.height}px` }"
        class="bg-white border overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border-b border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg px-2"
      >
        <h3 class="sm:text-xl p-3 xm:block hidden sm:text-left text-center">
          Đoạn hội thoại ({{ conversations.length }})
        </h3>
        <div class="flex justify-center items-center xm:hidden p-3">
          <UserIcon class="w-6" /> ({{ conversations.length }})
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
        <div
          v-for="conversation in filteredConversation"
          v-bind:key="conversation.id"
        >
          <ConversationBox v-bind:conversation="conversation" />
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
            />
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
      :show="isOpen"
      @closeModal="closeModal"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";
import { RouterLink } from "vue-router";

import ConversationBox from "../components/items/chat/ConversationBox.vue";
import CreateGroupChatModal from "../components/modals/chat/CreateGroupChatModal.vue";
import GroupConversationBox from "../components/items/chat/GroupConversationBox.vue";

import { MagnifyingGlassIcon, PlusCircleIcon } from "@heroicons/vue/24/outline";
import { UserIcon, UserGroupIcon } from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
    CreateGroupChatModal,
    GroupConversationBox,
    MagnifyingGlassIcon,
    PlusCircleIcon,
    UserIcon,
    UserGroupIcon,
  },
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
      body: "",
      query: "",
      isOpen: false,
      options: [],
    };
  },

  computed: {
    filteredConversation() {
      return this.query === ""
        ? this.conversations
        : this.conversations.filter((conversation) =>
            conversation.users
              .map((user) => user.name.toLowerCase())
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
    getConversations() {
      setTimeout(() => {
        axios
          .get("/api/chat/")
          .then((res) => {
            this.conversations = res.data;
            // console.log(this.conversations);
          })
          .catch((error) => {
            console.log(error);
          });
      }, 500);
    },
    getFriends() {
      setTimeout(() => {
        axios
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
      }, 2000);
    },
    getGroupConversations() {
      setTimeout(() => {
        axios
          .get("/api/chat/group/")
          .then((res) => {
            this.groupConversations = res.data;
            console.log(this.groupConversations);
          })
          .catch((error) => {
            console.log(error);
          });
      }, 1000);
    },
    getQuery() {
      this.query = this.$refs.input.value;
    },
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
});
</script>

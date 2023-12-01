<template>
  <div class=" grid grid-cols-4 gap-4">
    <div class="main-left col-span-1 sticky bottom-0">
      <div
        class="bg-white border overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border-b border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg container px-2"
      >
        <h3 class="text-xl p-3">Đoạn hội thoại ({{ conversations.length }})</h3>

        <div class="relative">
          <MagnifyingGlassIcon
            class="absolute top-[18px] left-2 w-6 h-6 dark:text-neutral-400"
          />
          <input
            @keyup="getQuery"
            ref="input"
            type="text"
            placeholder="Tìm kiếm đoạn hội thoại"
            class="w-full my-2 py-2 px-8 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl"
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
          <h3 class="text-xl p-3">Đoạn hội thoại nhóm ({{ groupConversations.length }})</h3>
          <div
            @click="openModal"
            class="flex gap-2 items-center justify-center px-4 py-2 bg-neutral-200 hover:bg-neutral-300 dark:bg-slate-700 dark:hover:bg-slate-800 transition duration-100 rounded-md shadow-md cursor-pointer"
          >
            <PlusCircleIcon class="w-8 h-8" />
            <span @click="getFriends">Tạo đoạn chat nhóm</span>
          </div>
          <div
            v-for="groupConversation in groupConversations"
            v-bind:key="groupConversation.id"
          >
            <GroupConversationBox v-bind:groupConversation="groupConversation" />
          </div>
        </div>
      </div>
    </div>
    <div class="main-center col-span-3 space-y-4">
      <div
        class="container bg-white border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg flex justify-center items-center"
      >
        Chưa chọn đoạn hội thoại nào
      </div>
    </div>
    <CreateGroupChatModal :show="isOpen" @closeModal="closeModal" :options="options"/>
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";

import ConversationBox from "../components/items/ConversationBox.vue";
import CreateGroupChatModal from "../components/modals/CreateGroupChatModal.vue";
import GroupConversationBox from "../components/items/GroupConversationBox.vue";

import { MagnifyingGlassIcon, PlusCircleIcon } from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
    CreateGroupChatModal,
    GroupConversationBox,
    MagnifyingGlassIcon,
    PlusCircleIcon,
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
      groupConversations: [],
      body: "",
      query: "",
      isOpen: false,
      options: []
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
      axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data;
          // console.log(this.conversations);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getFriends() {
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
    },
    getGroupConversations() {
      axios
        .get("/api/chat/group/")
        .then((res) => {
          this.groupConversations = res.data
          console.log(this.groupConversations);
        })
        .catch((error) => {
          console.log(error);
        });
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

<style scoped>
.container {
  min-height: calc(100vh - 100vh*0.1);
}
</style>
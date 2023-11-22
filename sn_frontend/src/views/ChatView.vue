<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        class="bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg h-[750px] px-2"
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
      </div>
    </div>
    <div class="main-center col-span-3 space-y-4">
      <div
        class="bg-white h-[750px] border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg flex justify-center items-center"
      >
        Chưa chọn đoạn hội thoại nào
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";
import ConversationBox from "../components/items/ConversationBox.vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
    MagnifyingGlassIcon,
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
      body: "",
      query: "",
    };
  },

  computed: {
    filteredConversation() {
      return this.query === ""
        ? this.conversations
        : this.conversations.filter((conversation) =>
            conversation.users.filter((user) =>
              user.name
            ).includes(this.query.toLowerCase().replace(/\s+/g, ''))
          );
    },
  },

  mounted() {
    this.getConversations();
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
    getQuery() {
      this.query = this.$refs.input.value;
      console.log(this.conversations.filter((conversation) => conversation.users))
    },
  },
});
</script>

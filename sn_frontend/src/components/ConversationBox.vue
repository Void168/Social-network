<template>
  <div>
    <RouterLink
      class="flex items-center justify-between cursor-pointer px-3 py-2 hover:bg-gray-200"
      :to="{ name: 'conversation', params: { id: conversation.id } }"
      v-for="conversation in conversations"
      v-bind:key="conversation.id"
    >
      <div class="flex items-center flex-col justify-center">
        <div
          v-for="user in conversation.users"
          v-bind:key="user.id"
          class="flex justify-center items-center gap-3"
        >
          <img
            v-if="user.id !== userStore.user.id"
            :src="user.get_avatar"
            alt=""
            class="w-10 h-10 rounded-full"
          />
          <p class="text-xs font-bold" v-if="user.id !== userStore.user.id">
            {{ user.name }}
          </p>
        </div>
        <div>
          <!-- <p v-if="getLastMessage(conversation.id)">
            {{ lastMessage.body }}
          </p> -->
        </div>
      </div>
      <span class="text-xs text-gray-600"
        >{{ conversation.modified_at_formatted }} trước</span
      >
    </RouterLink>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";

export default (await import("vue")).defineComponent({
  props: {
    conversations: Array,
    // lastMessage: Object,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
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
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // getLastMessage() {
    //   this.$emit("getLastMessage", this.conversation.id);

    //   axios
    //     .get(`/api/chat/${this.conversation.id}/get_last_message/`)
    //     .then((res) => {
    //       console.log(res.data);
    //       this.lastMessage = res.data;
    //     })
    //     .catch((error) => console.log(error));
    // },
  },
});
</script>

<template>
  <div>
    <RouterLink
      class="flex justify-between cursor-pointer"
      :to="{ name: 'conversation', params: { id: conversation.id } }"
      v-for="conversation in conversations"
      v-bind:key="conversation.id"
    >
      <div
        class="flex flex-col w-full gap-1 px-3 py-2 rounded-lg hover:bg-gray-200 duration-100"
      >
        <div class="flex justify-between items-center">
          <div
            v-for="user in conversation.users"
            v-bind:key="user.id"
            class="flex justify-center items-center gap-3"
          >
            <img
              v-if="user.id !== userStore.user.id"
              :src="user.get_avatar"
              alt="avatar"
              class="w-10 h-10 rounded-full"
            />
            <p class="text-xs font-bold" v-if="user.id !== userStore.user.id">
              {{ user.name }}
            </p>
          </div>

          <span
            v-if="conversation.messages.length"
            class="text-xs text-gray-600"
            >{{
              conversation.messages[conversation.messages.length - 1]
                .created_at_formatted
            }}
            trước</span
          >
          <span v-else></span>
        </div>

        <div class="text-sm">
          <div v-if="conversation.messages.length" class="flex gap-1">
            <span
              class="font-semibold"
              v-if="
                conversation.messages[conversation.messages.length - 1]
                  .created_by.id === userStore.user.id
              "
              >Bạn:
            </span>
            <span v-else>{{
              conversation.messages[conversation.messages.length - 1].created_by
                .name
            }}</span>
            <p class="truncate">{{
              conversation.messages[conversation.messages.length - 1].body
            }}</p>
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";

export default (await import("vue")).defineComponent({
  data() {
    return {
      conversations: [],
    };
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
  },
});
</script>

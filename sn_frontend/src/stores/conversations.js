import { defineStore } from "pinia";

import axios from "axios";
import { useUserStore } from "./user";

export const useUnseenConversationsStore = defineStore({
  id: "conversations",

  state: () => ({
    length: 0,
  }),

  actions: {
    getUnseenConversations() {
      axios
        .get("/api/chat/")
        .then((res) => {
          const userStore = useUserStore();
          
          if (res.data.conversations.length > 0) {
            this.length = res.data?.conversations.filter(
              (conversation) =>
                !conversation?.messages[
                  conversation?.messages?.length - 1
                ]?.seen_by
                  .map((user) => user?.created_by?.name)
                  .includes(userStore.user.name)
            )?.length;
          }
        })
        .catch((error) => {
          console.log(error);
        });

      return this.length;
    },
  },
});

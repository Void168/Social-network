<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="bg-white border border-gray-200 rounded-lg">
        <h3 class="text-xl p-3">
          Đoạn hội thoại ({{ conversations.length }})
        </h3>
        <div>
          <div
            v-for="conversation in conversations"
            v-bind:key="conversation.id"
            class="flex items-center justify-between cursor-pointer px-3 py-2 hover:bg-gray-200"
            v-on:click="setActiveConversation(conversation.id)"
          >
            <div class="flex items-center space-x-2">
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
                <p
                  class="text-xs font-bold"
                  v-if="user.id !== userStore.user.id"
                >
                  {{ user.name }}
                </p>
              </div>
            </div>
            <span class="text-xs text-gray-600"
              >{{ conversation.modified_at_formatted }} trước</span
            >
          </div>
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <div>
          <div class="p-4 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <img :src="receivedUser.get_avatar" alt="" class="w-10 h-10 rounded-full" />
              <span
                class="font-bold"
                >{{ receivedUser.name }}</span
              >
            </div>

            <span>Đang hoạt động</span>
          </div>
        </div>

        <hr />
        <div class="flex flex-col flex-grow p-4">
          <div
            v-for="message in activeConversation.messages"
            v-bind:key="message.id"
          >
            <div
              class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div>
                <div
                  class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg"
                >
                  <p class="text-sm">
                    {{ message.body }}
                  </p>
                </div>
                <span class="text-xs text-gray-500 leading-none"
                  >{{ message.created_at_formatted }} trước</span
                >
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  alt=""
                  class="w-10 h-10 rounded-full"
                />
              </div>
            </div>
            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  alt=""
                  class="w-10 h-10 rounded-full"
                />
              </div>
              <div>
                <div
                  v-if="
                    activeConversation.messages.filter(
                      (user) => user.sent_to.id === userStore.user.id
                    )
                  "
                  v-bind:key="message.id"
                  class="mb-4"
                >
                  <div
                    class="bg-gray-200 p-3 rounded-r-lg rounded-bl-lg"
                    v-if="
                      message.created_by !== conversations[0]?.users[0].name
                    "
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                  <span class="text-xs text-gray-500 leading-none"
                    >{{ message.created_at_formatted }} trước</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-white border border-gray-200 rounded-lg">
        <form v-on:submit.prevent="submitForm">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              name=""
              id=""
              cols="30"
              rows="1"
              placeholder="Bạn muốn nói điều gì?"
            ></textarea>
          </div>
          <div class="p-4 border-t border-gray-100 flex justify-end">
            <button>Gửi</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";

export default (await import("vue")).defineComponent({
  name: "chat",
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      conversations: [],
      activeConversation: {},
      body: "",
      receivedUser: {},
    };
  },

  mounted() {
    this.getConversations();
  },

  methods: {
    setActiveConversation(id) {
      this.activeConversation = id;
      this.getMessages();
    },
    getConversations() {
      axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data;

          if (this.conversations.length) {
            this.activeConversation = this.conversations[0].id;
          }
          this.getMessages();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getMessages() {
      axios
        .get(`/api/chat/${this.activeConversation}/`)
        .then((res) => {
          this.activeConversation = res.data;
          let users = [];
          for (let i = 0; i < this.activeConversation.users.length; i++) {
            users.push(this.activeConversation.users[i]);
          }
          const filteredUser = users.filter(
            (id) => id !== this.userStore.user.id
          );

          const allowed = ["created_by", "sent_to"];
          const messages = this.activeConversation.messages
            .filter(
              (data) =>
                JSON.stringify(data).indexOf(this.userStore.user.id) !== -1
            )
            .find((createdby) => createdby.id !== this.userStore.user.id);

          const filtered = Object.keys(messages)
            .filter((key) => allowed.includes(key))
            .reduce((obj, key) => {
              return {
                ...obj,
                [key]: messages[key],
              };
            }, {});
          this.receivedUser = Object.values(filtered).filter(
            (data) =>
              JSON.stringify(data).toLowerCase().indexOf(filteredUser) !== -1
          )[0];
        })

        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      axios
        .post(`/api/chat/${this.activeConversation.id}/send/`, {
          body: this.body,
        })
        .then((res) => {
          console.log(res.data);

          this.activeConversation.messages.push(res.data);
          this.body = "";
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

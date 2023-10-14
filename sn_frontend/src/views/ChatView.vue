<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">Đoạn hội thoại</h3>
        <div class="space-y-4">
          <div
            v-for="conversation in conversations"
            v-bind:key="conversation.id"
            class="flex items-center justify-between"
          >
            <div class="flex items-center space-x-2">
              <img
                src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
                alt=""
                class="w-[40px] rounded-full"
              />
              <div v-for="user in conversation.users" v-bind:key="user.id">
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
        <div v-for="user in activeConversation.users" v-bind:key="user.id">
          <div
            v-if="user.id !== userStore.user.id"
            class="p-4 flex justify-between items-center"
          >
            <div class="flex items-center gap-2">
              <img
                src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
                alt=""
                class="w-[40px] rounded-full"
              />
              <p class="font-bold">{{ user.name }}</p>
            </div>

            <span>Hoạt động bây giờ</span>
          </div>
        </div>

        <hr />
        <div class="flex flex-col flex-grow p-4">
          <div
            v-for="message in activeConversation.messages"
            v-bind:key="message.id"
            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
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
                src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
                alt=""
                class="w-[40px] rounded-full"
              />
            </div>
          </div>
          <div class="flex w-full mt-2 space-x-3 max-w-md">
            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
              <img
                src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
                alt=""
                class="w-[40px] rounded-full"
              />
            </div>
            <div>
              <div
                v-for="message in activeConversation.messages"
                v-bind:key="message.id"
                class="bg-gray-200 p-3 rounded-r-lg rounded-bl-lg"
              >
                <p class="text-sm">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum,
                  accusantium illum modi doloremque inventore consequuntur enim
                  optio fuga repellat quo corporis amet voluptas totam non id
                  doloribus rerum tempore accusamus!
                </p>
              </div>
              <!-- {{
                message.created_at_formatted
              }} -->
              <span class="text-xs text-gray-500 leading-none"></span>
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
          console.log(res.data);

          this.conversations = res.data;

          if (this.conversations.length) {
            this.activeConversation = this.conversations[0];
          }

          this.getMessages();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getMessages() {
      axios
        .get(`/api/chat/${this.activeConversation.id}/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post(`/api/chat/${this.activeConversation.id}/send/`, {
          body: this.body,
        })
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

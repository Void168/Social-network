<template>
  <div>
    <div class="bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg">
      <div>
        <div class="p-4 flex justify-between items-center">
          <div class="flex items-center gap-2">
            <img
              :src="receivedUser.get_avatar"
              alt=""
              class="w-10 h-10 rounded-full"
            />
            <span class="font-bold">{{ receivedUser.name }}</span>
          </div>

          <span>Đang hoạt động</span>
        </div>
      </div>

      <hr />
      <div class="flex flex-col flex-grow p-4 overflow-y-auto h-[500px]">
        <div v-if="recentConversation?.messages?.length > 0">
          <div
            v-for="message in listMessages"
            v-bind:key="message.id"
            :id="message.id"
          >
            <div
              class="flex flex-col w-full mt-2 space-x-3 items-end max-w-md ml-auto justify-end gap-2"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div class="flex gap-2">
                <div>
                  <div
                    class="bg-blue-600 dark:bg-blue-500 text-white p-3 shadow-md rounded-l-lg rounded-br-lg"
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                </div>
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                  <img
                    :src="message.created_by.get_avatar"
                    alt=""
                    class="w-10 h-10 rounded-full"
                  />
                </div>
              </div>
              <span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id === listMessages[listMessages.length - 1].id &&
                  listMessages[listMessages.length - 1].seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === true
                "
                >Đã gửi
                {{ listMessages[listMessages.length - 1].created_at_formatted }}
                trước</span
              ><span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id === listMessages[listMessages.length - 1].id &&
                  listMessages[listMessages.length - 1].seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === false
                "
                >Đã xem
                {{ listMessages[listMessages.length - 1].created_at_formatted }}
                trước</span
              >
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
                    recentConversation?.messages?.filter(
                      (user) => user.sent_to.id === userStore.user.id
                    )
                  "
                  v-bind:key="message.id"
                  class="mb-4"
                >
                  <div
                    class="bg-gray-200 p-3 rounded-r-lg rounded-bl-lg dark:bg-slate-500 dark:border-slate-600 dark:text-neutral-200"
                    v-if="message.created_by !== chats[0]?.users[0].name"
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                  <span
                    class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                    v-if="
                      message.id === listMessages[listMessages.length - 1].id
                    "
                    >Đã gửi
                    {{
                      listMessages[listMessages.length - 1].created_at_formatted
                    }}
                    trước</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 h-[500px] flex justify-center items-center">
          Hãy bắt đầu nói chuyện với nhau
        </div>
      </div>
    </div>
    <div class="bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg relative">
      <form v-on:submit.prevent="submitForm" @keyup.enter="submitForm">
        <div class="p-4 relative">
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
        <div class="p-4 border-t border-slate-400 flex justify-end">
          <button class="btn" type="submit">Gửi</button>
        </div>
      </form>
      <div class="absolute right-3 p-4 top-4">
        <Popover class="relative">
          <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-y-1 opacity-0"
            enter-to-class="translate-y-0 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 opacity-100"
            leave-to-class="translate-y-1 opacity-0"
            ><PopoverPanel
              class="absolute z-10 bottom-10 right-0 shadow-2xl rounded-lg"
              @click="Pick"
            >
              <emoji-picker></emoji-picker>
            </PopoverPanel>
          </transition>

          <PopoverButton>
            <FaceSmileIcon class="w-6 h-6" />
          </PopoverButton>
        </Popover>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ConversationBox from "./ConversationBox.vue";
import { useUserStore } from "../../stores/user";
import { RouterLink } from "vue-router";

import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import "emoji-picker-element";
import { FaceSmileIcon } from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  props: {
    chats: Array,
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
  },

  data() {
    return {
      receivedUser: {},
      listMessages: [],
      recentConversation: {},
      body: "",
      isOpen: false,
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
    this.getActiveConversation();
    this.getMessages();
  },
  methods: {
    getActiveConversation() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
        .then((res) => {
          this.recentConversation = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getMessages() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
        .then((res) => {
          this.recentConversation = res.data;
          this.listMessages = this.recentConversation.messages;
          let users = [];
          for (let i = 0; i < this.recentConversation.users.length; i++) {
            users.push(this.recentConversation.users[i]);
          }
          const filteredUser = users
            ?.map((user) => user.id)
            .filter((id) => id !== this.userStore.user.id);
          this.receivedUser = users.filter(
            (user) => user.id === filteredUser[0]
          )[0];
        })
        .catch((error) => {
          console.log(error);
        });
    },

    Pick() {
      document
        .querySelector("emoji-picker")
        .addEventListener("emoji-click", (event) => {
          this.body = this.body + event.detail.unicode;

          return this.body;
        });
    },

    submitForm() {
      axios
        .post(`/api/chat/${this.recentConversation.id}/send/`, {
          body: this.body,
        })
        .then((res) => {
          this.recentConversation.messages.push(res.data);
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
    Popover,
    PopoverButton,
    PopoverPanel,
    FaceSmileIcon,
  },
});
</script>

<style>
@media screen and (max-width: 320px) {
  emoji-picker {
    --num-columns: 6;
    --category-emoji-size: 1.125rem;
  }
}
</style>

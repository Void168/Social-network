<template>
  <div
    v-if="isOpen"
    class="relative flex flex-col h-[480px] w-[400px] bg-slate-200 dark:bg-slate-500 rounded-t-lg"
  >
    <div
      v-if="isOpenSettings"
      class="absolute top-8 left-10 w-64 bg-white dark:bg-slate-800 shadow-lg rounded-lg open-settings"
    >
      <ul>
        <li
          class="px-4 py-2 text-lg font-semibold hover:bg-slate-100 dark:hover:bg-slate-900 hover:rounded-t-lg cursor-pointer"
        >
          <p v-if="conversation?.id">
            <RouterLink
              :to="{
                name: 'conversation',
                params: { id: conversation?.id },
              }"
            >
              Mở trong tin nhắn
            </RouterLink>
          </p>
          <p v-else>Mở trong tin nhắn</p>
        </li>
        <hr />
        <li
          class="px-4 py-2 text-lg font-semibold hover:bg-slate-100 dark:hover:bg-slate-900 cursor-pointer transition"
        >
          <RouterLink :to="{ name: 'profile', params: { id: friend.id } }">
            Xem trang cá nhân
          </RouterLink>
        </li>
        <li
          @click="openConversationThemeModal"
          class="px-4 py-2 text-lg font-semibold hover:bg-slate-100 dark:hover:bg-slate-900 cursor-pointer transition"
        >
          Chủ đề
        </li>
        <ConversationThemeModal
          :currentTheme="conversation"
          :show="isConversationThemeModalOpen"
          @closeConversationThemeModal="closeConversationThemeModal"
        />
        <li
          class="px-4 py-2 text-lg font-semibold hover:bg-slate-100 dark:hover:bg-slate-900 cursor-pointer transition"
        >
          Tìm kiếm tin nhắn
        </li>
        <li
          @click="openModal"
          class="px-4 py-2 text-lg font-semibold hover:bg-slate-100 dark:hover:bg-slate-900 hover:rounded-b-lg cursor-pointer"
        >
          Xóa cuộc hội thoại
        </li>
        <DeleteConversationModal
          :show="isDeleteOpen"
          @closeModal="closeModal"
          @deleteConversation="deleteConversation"
        />
      </ul>
    </div>
    <div
      class="h-16 flex justify-between shadow-xl rounded-t-lg"
      :class="[selectedTheme?.background, selectedTheme?.textColor]"
    >
      <div
        @click="openSettings"
        class="flex p-4 gap-2 items-center hover:rounded-tl-lg cursor-pointer transition duration-[25ms]"
        :class="[selectedTheme?.hover]"
      >
        <img :src="friend.get_avatar" class="rounded-full h-10 w-10" />
        <span class="font-bold">{{ friend.name }}</span>
        <ChevronDownIcon class="w-6 h-6 rounded-full p-1" />
      </div>
      <div class="flex gap-1 p-4">
        <VideoCameraIcon
          class="w-8 h-8 rounded-full p-1 transition cursor-pointer"
          :class="[selectedTheme?.hover]"
        />
        <PhoneIcon
          class="w-8 h-8 rounded-full p-1 transition cursor-pointer"
          :class="[selectedTheme?.hover]"
        />
        <MinusIcon
          @click="$emit('miniatureChat')"
          class="w-8 h-8 rounded-full p-1 transition cursor-pointer"
          :class="[selectedTheme?.hover]"
        />
        <div @click="$emit('removeFriendChat')">
          <!-- v-on:click="closeConversationBubble" -->
          <XMarkIcon
            class="w-8 h-8 rounded-full p-1 transition cursor-pointer"
            :class="[selectedTheme?.hover]"
          />
        </div>
      </div>
    </div>
    <div
      ref="chatContainer"
      class="h-[346px] px-4 overflow-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border-b border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
    >
      <div class="flex flex-col flex-grow p-4">
        <div v-if="conversation?.messages?.length > 0 && conversation">
          <div
            v-for="message in conversation?.messages"
            v-bind:key="message.id"
            :id="message.id"
          >
            <div
              class="flex flex-col mt-2 space-x-3 items-end max-w-md ml-auto justify-end gap-2"
              v-if="message.created_by.id == userStore.user.id"
            >
              <p
                v-if="
                  message.body && !message.attachments.length && selectedTheme
                "
                class="p-3 text-sm shadow-md rounded-3xl max-w-[200px] px-4 font-semibold"
                :class="[selectedTheme?.background, selectedTheme?.textColor]"
              >
                <span class="block whitespace-normal break-words">{{
                  message.body
                }}</span>
              </p>
              <div v-if="message.attachments.length > 0">
                <p
                  v-if="message.body"
                  class="p-3 shadow-md max-w-[200px] rounded-t-lg font-semibold"
                  :class="[selectedTheme?.background, selectedTheme?.textColor]"
                >
                  <span class="block whitespace-normal break-words">
                    {{ message.body }}
                  </span>
                </p>
                <img
                  v-if="message.attachments.length > 0"
                  :src="message?.attachments[0]?.get_image"
                  :class="
                    message.body ? 'w-48 h-40 rounded-t-none' : 'w-48 h-40'
                  "
                />
              </div>

              <span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id === lastMessage?.id &&
                  !lastMessage?.seen_by
                    .map((obj) => obj.created_by.id)
                    .includes(receivedUser.id)
                "
                >Đã gửi
                {{ lastMessage?.created_at_formatted }}
                trước</span
              ><span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id === lastMessage?.id &&
                  lastMessage?.seen_by
                    .map((obj) => obj.created_by.id)
                    .includes(receivedUser.id)
                "
                >Đã xem</span
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
              <div class="flex flex-col w-full space-x-3 items-start max-w-md ml-auto justify-end gap-2">
                <div
                  v-if="
                    conversation?.messages?.filter(
                      (user) => user.sent_to.id === userStore.user.id
                    )
                  "
                  v-bind:key="message.id"

                >
                  <p
                    class="bg-gray-200 max-w-[200px] p-3 rounded-3xl dark:bg-slate-500 dark:border-slate-600 dark:text-neutral-200"
                  >
                    <span class="block whitespace-normal break-words">
                      {{ message.body }}
                    </span>
                  </p>
                </div>
                <span
                  class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                  v-if="message.id === lastMessage?.id"
                  >Đã gửi
                  {{ lastMessage?.created_at_formatted }}
                  trước</span
                >
              </div>
            </div>
          </div>
        </div>

        <div
          v-else
          class="bg-slate-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col justify-center items-center"
        >
          <img
            :src="friend.get_avatar"
            alt="non_conversation_avatar"
            class="w-16 h-16 rounded-full"
          />
          <p>{{ friend.name }}</p>
          <p>Hãy bắt đầu nói chuyện với nhau</p>
        </div>
      </div>
    </div>
    <div
      id="preview"
      v-if="url"
      class="flex relative items-center p-4 shadow-md rounded-b-md bg-slate-100 dark:bg-slate-700"
    >
      <img
        :src="url"
        class="w-20 h-20 rounded-lg border-[1px] border-slate-200 bg-slate-300 dark:border-slate-500 p-1"
      />
      <span class="absolute top-5 right-5 cursor-pointer" @click="removeImage"
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-8 h-8"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </span>
    </div>
    <div
      class="relative max-h-48 p-4 border-t-2 border-slate-400 dark:border-slate-300"
    >
      <span class="absolute right-12 p-4 bottom-0 z-10">
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
            <FaceSmileIcon
              class="w-6 h-6"
              :class="[selectedTheme?.iconColor]"
            />
          </PopoverButton>
        </Popover>
      </span>
      <form
        v-on:submit.prevent="submitForm"
        @keyup.enter="submitForm"
        class="flex items-end justify-between gap-1"
      >
        <div class="flex gap-1 items-end">
          <PlusCircleIcon
            class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-600 transition p-1"
            :class="[selectedTheme?.iconColor]"
          />
          <div class="relative cursor-pointer">
            <label for="image">
              <PhotoIcon
                class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-600 transition p-1"
                :class="[selectedTheme?.iconColor]"
              />

              <input
                type="file"
                ref="fileMessage"
                id="image"
                name="image"
                hidden
                @change="onFileChange"
              />
            </label>
          </div>
          <GifIcon
            class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-600 transition p-1"
            :class="[selectedTheme?.iconColor]"
          />
        </div>
        <div class="relative flex items-end gap-2">
          <textarea
            v-model="body"
            class="w-full py-2 pl-4 pr-8 bg-gray-100 rounded-xl resize-none overflow-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
            :class="rows > 5 ? 'overflow-y-auto' : ''"
            name=""
            id=""
            :rows="rows || 1"
            cols="30"
            placeholder="Bạn muốn nói điều gì?"
          ></textarea>
          <button
            type="submit"
            :disabled="(body.length < 1 && url === '') || body.length < 1"
          >
            <PaperAirplaneIcon
              class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-600 transition p-1"
              :class="[selectedTheme?.iconColor]"
            />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Pusher from "pusher-js";

import { RouterLink } from "vue-router";
import themes from "../../data/themes";

import {
  XMarkIcon,
  MinusIcon,
  PhoneIcon,
  VideoCameraIcon,
  ChevronDownIcon,
  PaperAirplaneIcon,
  PlusCircleIcon,
  PhotoIcon,
  GifIcon,
  FaceSmileIcon,
} from "@heroicons/vue/24/solid";

import "emoji-picker-element";

import ConversationThemeModal from "../modals/ConversationThemeModal.vue";
import DeleteConversationModal from "../modals/DeleteConversationModal.vue";

import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    RouterLink,
    Popover,
    PopoverButton,
    PopoverPanel,
    XMarkIcon,
    MinusIcon,
    PhoneIcon,
    VideoCameraIcon,
    ChevronDownIcon,
    PaperAirplaneIcon,
    PlusCircleIcon,
    PhotoIcon,
    GifIcon,
    FaceSmileIcon,
    ConversationThemeModal,
    DeleteConversationModal,
  },

  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },

  props: {
    friend: Object,
  },

  data() {
    return {
      conversation: {},
      friendsChat: [],
      body: "",
      isOpen: true,
      isDeleteOpen: false,
      url: null,
      isOpenSettings: false,
      isConversationThemeModalOpen: false,
      themes: themes,
    };
  },

  computed: {
    selectedTheme() {
      return this.themes.filter(
        (theme) => theme.name === this.conversation?.theme
      )[0];
    },
    rows() {
      return Math.ceil(this.body.length / 30) < 6
        ? Math.ceil(this.body.length / 30)
        : 5;
    },
    lastMessage() {
      return this.conversation?.messages[
        this.conversation.messages?.length - 1
      ];
    },
    seen() {
      return this.lastMessage?.seen_by
        ?.map((user) => user.created_by.id)
        .includes(this.friend.id);
    },
    receivedUser() {
      return this.conversation.users.filter(
        (user) => user.id !== this.userStore.user.id
      )[0];
    },
  },

  mounted() {
    document.addEventListener("click", this.clickOutside);
    this.getConversation();
    this.getPusher();
  },
  
  beforeUnmount() {
    document.removeEventListener("click", this.clickOutside);
  },
  
  updated() {
    this.scrollToBottom();
    this.seenMessage()
  },

  methods: {
    getPusher() {
      Pusher.logToConsole = false;

      const pusher = new Pusher(`${import.meta.env.VITE_PUSHER_KEY}`, {
        cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
      });
      const channel = pusher.subscribe(`${this.conversation?.id}`);
      channel.bind("message:new", (data) => {
        this.listMessages.push(JSON.parse(data.message));
      });
    },
    scrollToBottom() {
      const objDiv = this.$refs.chatContainer;
      objDiv.scrollTop = objDiv.scrollHeight;
    },
    getConversation() {
      axios
        .get(`/api/chat/${this.friend?.id}/get-chat-window/`)
        .then((res) => {
          this.conversation = res.data.conversation;
          console.log(this.conversation);
        })
        .catch((error) => console.log(error));
    },
    seenMessage() {
      setTimeout(() => {
        axios
          .post(`/api/chat/${this.conversation?.id}/set_seen/`)
          .then((res) => {
            // console.log(res.data);
          })
          .catch((error) => console.log(error));
      }, 2000)
    },
    Pick() {
      document
        .querySelector("emoji-picker")
        .addEventListener("emoji-click", (event) => {
          this.body = this.body + event.detail.unicode;

          return this.body;
        });
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },
    closeConversationThemeModal() {
      this.isConversationThemeModalOpen = false;
    },
    closeModal() {
      this.isDeleteOpen = false;
    },
    openModal() {
      this.isDeleteOpen = true;
    },
    openConversationThemeModal() {
      this.isConversationThemeModalOpen = true;
    },
    removeImage() {
      this.url = null;
    },
    openSettings() {
      this.isOpenSettings = !this.isOpenSettings;
    },
    clickOutside() {
      const modalContainer = document.querySelector(".open-settings");

      if (modalContainer && !modalContainer.contains(event.target.parentNode)) {
        this.autoComplete = false;
      }
    },
    submitForm() {
      // console.log(this.conversation);
      if (this.conversation?.id === undefined) {
        axios
          .post(`/api/chat/${this.friend.id}/create/`)
          .then((res) => {
            this.conversation = res.data;
            let formData = new FormData();
            if (this.$refs.fileMessage.files[0]) {
              formData.append("image", this.$refs.fileMessage.files[0]);
            }
            formData.append("body", this.body);
            axios
              .post(`/api/chat/${res.data.id}/send/`, formData, {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              })
              .then((res) => {
                // console.log(res.data);
                this.scrollToBottom();
                res.data.messages?.push(res.data);
                this.$refs.fileMessage.value = null;
                this.url = null;
                this.body = "";
              })
              .catch((error) => {
                console.log(error);
              });
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        // console.log("submitForm", this.body);
        let formData = new FormData();
        if (this.$refs.fileMessage.files[0]) {
          formData.append("image", this.$refs.fileMessage.files[0]);
        }
        formData.append("body", this.body);

        axios
          .post(`/api/chat/${this.conversation.id}/send/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            // console.log(res.data);
            this.scrollToBottom();
            this.conversation?.messages?.push(res.data);
            this.$refs.fileMessage.value = null;
            this.url = null;
            this.body = "";
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    deleteConversation() {
      this.$emit("deleteConversation", this.conversation.id);

      axios
        .delete(`/api/chat/${this.conversation.id}/delete/`)
        .then((res) => {
          setTimeout(() => {
            this.closeModal();
          }, 500);
          this.toastStore.showToast(
            5000,
            "Đã xóa đoạn hội thoại",
            "bg-emerald-500 text-white"
          );
          setTimeout(() => {
            this.$router.go(0);
          }, 6000);
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            5000,
            "Xóa đoạn hội thoại thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
  },
});
</script>

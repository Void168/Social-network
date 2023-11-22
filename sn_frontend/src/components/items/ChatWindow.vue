<template>
  <div
    v-if="isOpen"
    class="flex flex-col h-[480px] w-[400px] bg-slate-200 dark:bg-slate-500 rounded-t-lg"
  >
    <div
      class="h-16 border-b-2 border-slate-400 dark:border-slate-300 flex justify-between"
    >
      <div
        class="flex p-4 gap-2 items-center hover:bg-slate-600 hover:rounded-lg transition duration-75 cursor-pointer"
      >
        <img :src="friend.get_avatar" class="rounded-full h-10 w-10" />
        <span class="font-bold">{{ friend.name }}</span>
        <ChevronDownIcon class="w-6 h-6 rounded-full hover:bg-slate-600 p-1" />
      </div>
      <div class="flex gap-1 p-4">
        <VideoCameraIcon
          class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
        />
        <PhoneIcon
          class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
        />
        <MinusIcon
          @click="$emit('miniatureChat')"
          class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
        />
        <div @click="$emit('removeFriendChat')">
          <!-- v-on:click="closeConversationBubble" -->
          <XMarkIcon
            class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
          />
        </div>
      </div>
    </div>
    <div
      class="h-[346px] p-4 overflow-y-scroll scrollbar-none scrollbar scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
    >
      <div class="flex flex-col flex-grow p-4 overflow-y-auto">
        <div v-if="activeConversation.messages?.length > 0">
          <div
            v-for="message in activeConversation.messages"
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
                    class="bg-blue-600 dark:bg-blue-500 text-white p-3 shadow-md rounded-full px-4"
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                </div>
              </div>
              <span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id ===
                    activeConversation.messages[
                      activeConversation.messages.length - 1
                    ].id &&
                  activeConversation.messages[
                    activeConversation.messages.length - 1
                  ].seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === true
                "
                >Đã gửi
                {{
                  activeConversation.messages[
                    activeConversation.messages.length - 1
                  ].created_at_formatted
                }}
                trước</span
              ><span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id ===
                    activeConversation.messages[
                      activeConversation.messages.length - 1
                    ].id &&
                  activeConversation.messages[
                    activeConversation.messages.length - 1
                  ].seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === false
                "
                >Đã xem
                {{
                  activeConversation.messages[
                    activeConversation.messages.length - 1
                  ].created_at_formatted
                }}
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
                    activeConversation?.messages?.filter(
                      (user) => user.sent_to.id === userStore.user.id
                    )
                  "
                  v-bind:key="message.id"
                  class="mb-4"
                >
                  <div
                    class="bg-gray-200 p-3 rounded-3xl dark:bg-slate-500 dark:border-slate-600 dark:text-neutral-200"
                  >
                    <!-- v-if="message.created_by !== chats[0]?.users[0].name" -->
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                  <span
                    class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                    v-if="
                      message.id ===
                      activeConversation.messages[
                        activeConversation.messages.length - 1
                      ].id
                    "
                    >Đã gửi
                    {{
                      activeConversation.messages[
                        activeConversation.messages.length - 1
                      ].created_at_formatted
                    }}
                    trước</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          v-else
          class="bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col justify-center items-center"
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
      class="relative h-16 p-4 border-t-2 border-slate-400 dark:border-slate-300"
    >
      <span class="absolute right-12 p-4 top-2 z-10">
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
      </span>
      <form
        v-on:submit.prevent="submitForm"
        @keyup.enter="submitForm"
        class="flex items-center justify-between gap-1"
      >
        <div class="flex gap-1">
          <PlusCircleIcon
            class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
          />
          <PhotoIcon
            class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
          />
          <GifIcon
            class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
          />
        </div>
        <div class="relative flex items-center gap-2">
          <textarea
            v-model="body"
            class="w-full py-2 px-4 bg-gray-100 rounded-3xl resize-none"
            name=""
            id=""
            cols="30"
            rows="1"
            placeholder="Bạn muốn nói điều gì?"
          ></textarea>
          <button class="" type="submit">
            <PaperAirplaneIcon
              class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
            />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { RouterLink } from "vue-router";

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

import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { useUserStore } from "../../stores/user";
import { fr } from "date-fns/locale";

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
  },

  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  props: {
    friend: Object,
    conversation: Object,
  },

  data() {
    return {
      friendsChat: [],
      body: "",
      isOpen: true,
      activeConversation: {},
    };
  },

  mounted() {
    this.getConversation();
  },

  methods: {
    Pick() {
      document
        .querySelector("emoji-picker")
        .addEventListener("emoji-click", (event) => {
          this.body = this.body + event.detail.unicode;

          return this.body;
        });
    },
    getConversation() {
      axios
        .get(`/api/chat/${this.friend.id}/get/`)
        .then((res) => {
          this.activeConversation = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    submitForm() {
        console.log(this.activeConversation)
      if (!this.activeConversation.messages?.length) {
        axios
          .post(`/api/chat/${this.friend.id}/create/`)
          .then((res) => {
            // console.log(res.data);
            axios
              .post(`/api/chat/${res.data.id}/send/`, {
                body: this.body,
              })
              .then((res) => {
                this.activeConversation.messages?.push(res.data);
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
        axios
          .post(`/api/chat/${this.activeConversation.id}/send/`, {
            body: this.body,
          })
          .then((res) => {
            this.activeConversation?.messages?.push(res.data);
            this.body = "";
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
});
</script>

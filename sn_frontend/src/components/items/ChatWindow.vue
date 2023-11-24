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
      id="chat-container"
      class="h-[346px] px-4 overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border-b border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
    >
      <div class="flex flex-col flex-grow p-4 overflow-y-auto">
        <div v-if="conversation?.messages?.length > 0">
          <div
            v-for="message in conversation?.messages"
            v-bind:key="message.id"
            :id="message.id"
          >
            <div
              class="flex flex-col mt-2 space-x-3 items-end max-w-md ml-auto justify-end gap-2"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div class="flex gap-2">
                <div>
                  <div
                    v-if="
                      message.body &&
                      !message.attachments.length &&
                      selectedTheme
                    "
                    class="p-3 shadow-md rounded-full px-4 font-semibold"
                    :class="[
                      selectedTheme?.background,
                      selectedTheme?.textColor,
                    ]"
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                  <div v-if="message.attachments.length > 0">
                    <div
                      v-if="message.body"
                      class="p-3 shadow-md rounded-t-lg font-semibold"
                      :class="[
                        selectedTheme?.background,
                        selectedTheme?.textColor,
                      ]"
                    >
                      <p class="text-sm">
                        {{ message.body }}
                      </p>
                    </div>
                    <img
                      v-if="message.attachments.length > 0"
                      :src="message?.attachments[0]?.get_image"
                      :class="
                        message.body ? 'w-48 h-40 rounded-t-none' : 'w-48 h-40'
                      "
                    />
                  </div>
                </div>
              </div>
              <span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id ===
                    conversation.messages[conversation.messages.length - 1]
                      .id &&
                  conversation.messages[
                    conversation.messages.length - 1
                  ].seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === true
                "
                >Đã gửi
                {{
                  conversation.messages[conversation.messages.length - 1]
                    .created_at_formatted
                }}
                trước</span
              ><span
                class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                v-if="
                  message.id ===
                    conversation.messages[conversation.messages.length - 1]
                      .id &&
                  conversation.messages[
                    conversation.messages.length - 1
                  ].seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === false
                "
                >Đã xem
                {{
                  conversation.messages[conversation.messages.length - 1]
                    .created_at_formatted
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
                    conversation?.messages?.filter(
                      (user) => user.sent_to.id === userStore.user.id
                    )
                  "
                  v-bind:key="message.id"
                  class="mb-4"
                >
                  <div
                    class="bg-gray-200 max-w-min p-3 rounded-3xl dark:bg-slate-500 dark:border-slate-600 dark:text-neutral-200"
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                  <span
                    class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                    v-if="
                      message.id ===
                      conversation.messages[conversation.messages.length - 1].id
                    "
                    >Đã gửi
                    {{
                      conversation.messages[conversation.messages.length - 1]
                        .created_at_formatted
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
        class="flex items-center justify-between gap-1"
      >
        <div class="flex gap-1">
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
        <div class="relative flex items-center gap-2">
          <textarea
            v-model="body"
            @keyup="getContent"
            class="w-full py-2 px-4 bg-gray-100 rounded-3xl resize-none"
            name=""
            id=""
            cols="30"
            rows="1"
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
    conversation: Object,
  },

  data() {
    return {
      friendsChat: [],
      body: "",
      isOpen: true,
      isDeleteOpen: false,
      url: null,
      isOpenSettings: false,
      isConversationThemeModalOpen: false,
      themes: [
        {
          name: "Ngân hà",
          background:
            "bg-gradient-to-r from-blue-800 via-indigo-800 to-violet-800",
          textColor: "text-neutral-200",
          hover: "hover:bg-violet-500",
          iconColor: "text-violet-500 dark:text-violet-400",
        },
        {
          name: "Hoàng hôn",
          background:
            "bg-gradient-to-r from-orange-700 via-pink-700 to-blue-700",
          textColor: "text-neutral-100",
          hover: "hover:bg-pink-600",
          iconColor: "text-pink-500 dark:text-pink-400",
        },
        {
          name: "Bãi biển",
          background: "bg-gradient-to-r from-blue-500 via-sky-500 to-amber-500",
          textColor: "text-neutral-100",
          hover: "hover:bg-sky-400",
          iconColor: "text-amber-500 dark:text-amber-400",
        },
        {
          name: "Giáng sinh",
          background:
            "bg-gradient-to-r from-neutral-100 via-emerald-400 to-rose-400",
          textColor: "text-slate-800",
          hover: "hover:bg-emerald-400",
          iconColor: "text-emerald-500 dark:text-emerald-400",
        },
        {
          name: "Mùa xuân",
          background:
            "bg-gradient-to-r from-neutral-200 via-rose-400 to-amber-300",
          textColor: "text-slate-700",
          hover: "hover:bg-rose-400",
          iconColor: "text-amber-500 dark:text-amber-400",
        },
        {
          name: "Mùa hè",
          background:
            "bg-gradient-to-r from-amber-300 via-cyan-300 to-emerald-400",
          textColor: "text-slate-700",
          hover: "hover:bg-emerald-500 hover:text-neutral-200",
          iconColor: "text-emerald-500 dark:text-emerald-400",
        },
        {
          name: "Mùa thu",
          background:
            "bg-gradient-to-r from-rose-600 via-amber-700 to-orange-700",
          textColor: "text-neutral-200",
          hover: "hover:bg-amber-600",
          iconColor: "text-orange-700 dark:text-orange-600",
        },
        {
          name: "Mùa đông",
          background: "bg-gradient-to-r from-white via-neutral-200 to-cyan-200",
          textColor: "text-slate-700",
          hover: "hover:bg-slate-300",
          iconColor: "text-cyan-500 dark:text-cyan-400",
        },
        {
          name: "Tình nhân",
          background: "bg-gradient-to-r from-white via-rose-400 to-red-500",
          textColor: "text-slate-800",
          hover: "hover:bg-rose-300",
          iconColor: "text-red-500 dark:text-red-400",
        },
        {
          name: "Cà phê",
          background:
            "bg-gradient-to-r from-yellow-700 via-amber-700 to-orange-900",
          textColor: "text-neutral-200",
          hover: "hover:bg-amber-600",
          iconColor: "text-amber-800 dark:text-amber-700",
        },
        {
          name: "Bóng đá",
          background:
            "bg-gradient-to-r from-neutral-300 via-emerald-500 to-slate-600",
          textColor: "text-neutral-100",
          hover: "hover:bg-emerald-400",
          iconColor: "text-slate-700 dark:text-slate-200",
        },
        {
          name: "Cổ điển",
          background: "bg-emerald-500",
          textColor: "text-neutral-200",
          hover: "hover:bg-emerald-400",
          iconColor: "text-emerald-500 dark:text-emerald-400",
        },
      ],
    };
  },

  computed: {
    selectedTheme() {
      return this.themes.filter(
        (theme) => theme.name === this.conversation?.theme
      )[0];
    },
  },

  mounted() {
    document.addEventListener("click", this.clickOutside);
    this.scrollToBottom();
  },

  beforeUnmount() {
    document.removeEventListener("click", this.clickOutside);
  },

  methods: {
    scrollToBottom() {
      const objDiv = document.getElementById("chat-container");
      objDiv.scrollTop = objDiv.scrollHeight;
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
      console.log(this.conversation);
      if (this.conversation?.id === undefined) {
        axios
          .post(`/api/chat/${this.friend.id}/create/`)
          .then((res) => {
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
        console.log("submitForm", this.body);
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

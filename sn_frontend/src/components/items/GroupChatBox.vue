<template>
  <div>
    <div class="rounded-lg relative">
      <div>
        <div
          class="p-4 flex justify-between items-center rounded-t-lg"
          :class="[selectedTheme?.background, selectedTheme?.textColor]"
        >
          <div class="flex items-center gap-2">
            <div
              class="h-14 w-16 relative"
              v-if="!activeConversation.get_avatar"
            >
              <img
                :src="avatar2"
                alt="avatar-1"
                class="w-9 h-9 rounded-full absolute top-0 z-9 right-1"
              />
              <img
                :src="avatar1"
                alt="avatar-0"
                class="w-9 h-9 rounded-full ring-4 absolute bottom-0 z-9"
                :class="[selectedTheme?.ringAvatar]"
              />
            </div>
            <img
              v-else
              :src="activeConversation.get_avatar"
              alt="avatar-group"
              class="w-14 h-14 rounded-full"
            />
            <span class="font-bold">{{ activeConversation.group_name }}</span>
          </div>
          <div
            class="font-semibold cursor-pointer p-4 bg-transparent shadow-md rounded-lg hover:bg-white/30 transition"
            @click="openPollsListModal"
          >
            <p>Cuộc thảo luận</p>
            <PollsListModal
              :show="isPollsListOpen"
              @closeModal="closePollsListModal"
              :pollslist="pollslist"
              :activeConversation="activeConversation"
            />
          </div>
          <span class="font-semibold">Đang hoạt động</span>
        </div>
      </div>
      <div
        id="chatview-container"
        class="overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 h-[750px]"
      >
        <div class="flex flex-col flex-grow p-4 overflow-y-auto">
          <div v-if="activeConversation?.group_messages?.length > 0">
            <div
              v-for="message in allMessages"
              v-bind:key="message.id"
              :id="message.id"
            >
              <div
                class="flex flex-col w-full mt-2 space-x-3 items-end max-w-md ml-auto justify-end gap-2"
                v-if="message.created_by?.id === userStore.user.id"
              >
                <div class="flex gap-2">
                  <div>
                    <div
                      v-if="
                        message?.body &&
                        !message?.attachments.length &&
                        selectedTheme
                      "
                      class="p-3 shadow-md rounded-l-lg rounded-br-lg"
                      :class="[
                        selectedTheme.background,
                        selectedTheme.textColor,
                      ]"
                    >
                      <p class="text-sm font-semibold">
                        {{ message?.body }}
                      </p>
                    </div>
                    <div v-if="message?.attachments.length > 0">
                      <div
                        v-if="message?.body"
                        class="p-3 shadow-md rounded-t-lg"
                        :class="[
                          selectedTheme.background,
                          selectedTheme.textColor,
                        ]"
                      >
                        <p class="text-sm font-semibold">
                          {{ message?.body }}
                        </p>
                      </div>
                      <img
                        v-if="message?.attachments.length > 0"
                        :src="message?.attachments[0]?.get_image"
                        :class="
                          message?.body
                            ? 'w-48 h-40 rounded-t-none'
                            : 'w-48 h-40'
                        "
                      />
                    </div>
                  </div>
                  <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                    <img
                      :src="message?.created_by?.get_avatar"
                      alt=""
                      class="w-10 h-10 rounded-full"
                    />
                  </div>
                </div>
                <div
                  class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                  v-if="
                    !message?.content &&
                    message.id === lastMessage?.id &&
                    lastMessage?.seen_by
                      .map((obj) => obj.created_by?.email)
                      .includes(userStore.user.email) === true
                  "
                >
                  <p>
                    Đã gửi
                    {{ lastMessage?.created_at_formatted }}
                    trước
                  </p>
                  <div
                    @click="openSeenUsersModal"
                    v-if="lastMessage?.seen_by?.length"
                    class="relative flex items-center justify-end mt-2 gap-1 cursor-pointer"
                  >
                    <SeenUsersModal
                      :show="isOpen"
                      @closeModal="closeSeenUsersModal"
                      :lastMessage="getSeenBy"
                    />
                    <span
                      v-if="getSeenBy.length > 3"
                      class="mr-1 bg-slate-400 px-1 rounded-full text-sm cursor-pointer"
                      >+{{ getSeenBy.length - 3 }}</span
                    >
                    <span
                      v-for="seen_by in getSeenBy.slice(0, 3)"
                      :key="seen_by.id"
                      class="text-sm text-gray-500 dark:text-neutral-200 leading-none relative group cursor-pointer"
                    >
                      <span
                        class="absolute z-50 w-56 px-4 py-2 rounded-lg leading-4 text-neutral-200 dark:text-slate-700 dark:bg-white bg-slate-700 top-[-60px] left-[-200px] hidden group-hover:block bg-opacity-80"
                      >
                        {{ seen_by.created_by.name }} đã xem lúc
                        {{ seen_by.created_at.slice(11, 19) }} ngày
                        {{
                          seen_by.created_at
                            .slice(0, 10)
                            .split("-")
                            .reverse()
                            .join("-")
                        }}
                      </span>
                      <img
                        :src="seen_by.created_by.get_avatar"
                        alt="seen-avatar"
                        class="w-4 h-4"
                      />
                    </span>
                  </div>
                </div>
                <div
                  class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                  v-if="
                    message.id === lastMessage?.id &&
                    lastMessage?.seen_by
                      .map((obj) => obj.created_by?.email)
                      .includes(userStore.user.email) === false
                  "
                >
                  Đã xem
                  {{ lastMessage?.created_at_formatted }}
                  trước
                </div>
              </div>
              <div
                v-if="message.content"
                class="flex justify-center items-center my-2"
              >
                {{ message.content }}
              </div>
              <div
                class="flex w-full mt-2 space-x-3 max-w-md"
                v-if="
                  message.created_by?.id !== userStore.user.id &&
                  !message?.content
                "
              >
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                  <img
                    :src="message?.created_by?.get_avatar"
                    alt=""
                    class="w-10 h-10 rounded-full"
                  />
                </div>
                <div>
                  <div
                    v-if="
                      activeConversation?.group_messages?.filter(
                        (user) => user.sent_to?.id === userStore.user.id
                      )
                    "
                    v-bind:key="message.id"
                    class="mb-4"
                  >
                    <div
                      class="bg-gray-200 p-3 rounded-r-lg rounded-bl-lg dark:bg-slate-500 dark:border-slate-600 dark:text-neutral-200"
                    >
                      <p class="text-sm font-semibold">
                        {{ message?.body }}
                      </p>
                    </div>
                    <span
                      class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                      v-if="
                        message.id === lastMessage?.id &&
                        lastMessage?.seen_by.length
                      "
                      >Đã gửi
                      {{ lastMessage?.created_at_formatted }}
                      trước</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            v-else
            class="bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 h-[500px] flex justify-center items-center"
          >
            Hãy bắt đầu nói chuyện với nhau
          </div>
        </div>
        <div
          id="preview"
          v-if="url"
          class="flex absolute bottom-0 w-full items-center p-4 shadow-md rounded-b-md bg-slate-100 dark:bg-slate-700"
        >
          <img
            :src="url"
            class="w-20 h-20 rounded-lg border-[1px] border-slate-200 bg-slate-300 dark:border-slate-500 p-1"
          />
          <span
            class="absolute top-5 right-5 cursor-pointer"
            @click="removeImage"
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
      </div>
    </div>
    <div
      class="bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg relative"
    >
      <form
        v-on:submit.prevent="submitForm"
        @keyup.enter="submitForm"
        class="flex items-center px-4"
      >
        <div class="flex gap-1">
          <PlusCircleIcon
            class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-700 transition p-1"
            :class="[selectedTheme?.iconColor]"
          />
          <div class="relative cursor-pointer">
            <label for="doc">
              <PhotoIcon
                class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-700 transition p-1"
                :class="[selectedTheme?.iconColor]"
              />

              <input
                type="file"
                ref="file"
                id="doc"
                name="doc"
                hidden
                @change="onFileChange"
              />
            </label>
          </div>
          <GifIcon
            class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-700 transition p-1"
            :class="[selectedTheme?.iconColor]"
          />
        </div>
        <div class="p-4 relative w-full flex items-center">
          <textarea
            v-model="body"
            class="p-4 w-full bg-gray-100 rounded-lg resize-none"
            name=""
            id=""
            cols="30"
            rows="1"
            placeholder="Bạn muốn nói điều gì?"
          ></textarea>
          <div class="absolute right-3 p-4 top-3">
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
                  class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-700 transition p-1"
                  :class="[selectedTheme?.iconColor]"
                />
              </PopoverButton>
            </Popover>
          </div>
        </div>
        <div class="flex justify-end">
          <button
            type="submit"
            :disabled="(body.length < 1 && url === '') || body.length < 1"
          >
            <PaperAirplaneIcon
              class="w-8 h-8 cursor-pointer rounded-full hover:bg-slate-300 dark:hover:bg-slate-700 transition p-1"
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
import ConversationBox from "./ConversationBox.vue";
import { useUserStore } from "../../stores/user";
import { RouterLink } from "vue-router";

import SeenUsersModal from "../modals/SeenUsersModal.vue";
import PollsListModal from "../modals/PollsListModal.vue";

import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import "emoji-picker-element";
import {
  FaceSmileIcon,
  PlusCircleIcon,
  PaperAirplaneIcon,
  PhotoIcon,
  GifIcon,
} from "@heroicons/vue/24/outline";

import themes from "../../data/themes";

export default (await import("vue")).defineComponent({
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
      pollslist: [],
      activeConversation: {},
      body: "",
      isOpen: false,
      isPollsListOpen: false,
      url: null,
      themes: themes,
      notifications: [],
    };
  },
  computed: {
    selectedTheme() {
      return this.themes.filter(
        (theme) => theme.name === this.activeConversation.theme
      )[0];
    },
    avatar1() {
      return this.activeConversation?.users
        ?.filter((user) => this.userStore.user.id !== user.id)
        .map((user) => user?.get_avatar)[0];
    },
    avatar2() {
      return this.activeConversation?.users
        ?.filter((user) => this.userStore.user.id !== user.id)
        .map((user) => user?.get_avatar)[1];
    },
    lastMessage() {
      return this.listMessages[this.listMessages?.length - 1];
    },
    getSeenBy() {
      return this.listMessages[this.listMessages.length - 1].seen_by.filter(
        (seen) => seen.created_by.id !== this.userStore.user.id
      );
    },
    allMessages() {
      return this.listMessages.concat(this.notifications).sort((a, b) => {
        if (a.created_at < b.created_at) {
          return -1;
        }
        if (a.created_at > b.created_at) {
          return 1;
        }

        return 0;
      });
    },
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
    this.getMessages();
    this.scrollToBottom();
    this.getGroupNotifications();
    this.getPusher();
  },
  methods: {
    getPusher() {
      Pusher.logToConsole = false;

      const pusher = new Pusher(import.meta.env.VITE_PUSHER_KEY, {
        cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
      });
      const channel = pusher.subscribe(`${this.$route.params.id}`);
      channel.bind("group_message:new", (data) => {
        this.listMessages.push(JSON.parse(data.message));
      });
    },
    getGroupNotifications() {
      axios
        .get(`/api/chat/group/${this.$route.params.id}/get-notifications/`)
        .then((res) => {
          this.notifications = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    scrollToBottom() {
      const objDiv = document.querySelector("#chatview-container");
      objDiv.scrollTop = objDiv.scrollHeight;
    },
    closeSeenUsersModal() {
      this.isOpen = false;
    },
    openSeenUsersModal() {
      this.isOpen = true;
    },
    closePollsListModal() {
      this.isPollsListOpen = false;
    },
    openPollsListModal() {
      this.isPollsListOpen = true;
      axios
        .get(`/api/chat/group/${this.activeConversation?.id}/get-polls/`)
        .then((res) => {
          this.pollslist = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getMessages() {
      axios
        .get(`/api/chat/group/${this.$route.params.id}/`)
        .then((res) => {
          this.scrollToBottom();
          this.activeConversation = res.data;
          this.listMessages = res.data.group_messages;
          let users = [];
          for (let i = 0; i < this.activeConversation.users.length; i++) {
            users.push(this.activeConversation.users[i]);
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

    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },

    removeImage() {
      this.url = null;
    },

    submitForm() {
      // console.log("submitForm", this.body);

      let formData = new FormData();
      if (this.$refs.file.files[0]) {
        formData.append("image", this.$refs.file.files[0]);
      }
      formData.append("body", this.body);

      axios
        .post(`/api/chat/${this.activeConversation.id}/send_group/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          this.scrollToBottom();
          this.$refs.file.value = null;
          this.url = null;
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
    PlusCircleIcon,
    PhotoIcon,
    GifIcon,
    PaperAirplaneIcon,
    SeenUsersModal,
    PollsListModal,
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

<template>
    <div>
      <div class="rounded-lg relative">
        <div>
          <div
            class="p-4 flex justify-between items-center rounded-t-lg"
            :class="[selectedTheme?.background, selectedTheme?.textColor]"
          >
            <div class="flex items-center gap-2">
              <img
                :src="receivedUser.get_avatar"
                alt=""
                class="w-10 h-10 rounded-full"
              />
              <span class="font-bold">{{ receivedUser.name }}</span>
            </div>
  
            <span class="font-semibold">Đang hoạt động</span>
          </div>
        </div>
        <div
          id="chatview-container"
          class="overflow-y-scroll scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 h-[589px]"
        >
          <div class="flex flex-col flex-grow p-4 overflow-y-auto">
            <div v-if="recentConversation?.group_messages?.length > 0">
              <div
                v-for="message in listMessages"
                v-bind:key="message.id"
                :id="message.id"
              >
                <div
                  class="flex flex-col w-full mt-2 space-x-3 items-end max-w-md ml-auto justify-end gap-2"
                  v-if="message.created_by?.id == userStore.user.id"
                >
                  <div class="flex gap-2">
                    <div>
                      <div
                        v-if="
                          message.body &&
                          !message.attachments.length &&
                          selectedTheme
                        "
                        class="p-3 shadow-md rounded-l-lg rounded-br-lg"
                        :class="[
                          selectedTheme.background,
                          selectedTheme.textColor,
                        ]"
                      >
                        <p class="text-sm">
                          {{ message.body }}
                        </p>
                      </div>
                      <div v-if="message.attachments.length > 0">
                        <div
                          v-if="message.body"
                          class="p-3 shadow-md rounded-t-lg"
                          :class="[
                            selectedTheme.background,
                            selectedTheme.textColor,
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
                            message.body
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
                  <span
                    class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                    v-if="
                      message.id === listMessages[listMessages.length - 1].id &&
                      listMessages[listMessages.length - 1].seen_by
                        .map((obj) => obj.created_by?.email)
                        .includes(userStore.user.email) === true
                    "
                    >Đã gửi
                    {{
                      listMessages[listMessages.length - 1].created_at_formatted
                    }}
                    trước</span
                  ><span
                    class="text-xs text-gray-500 dark:text-neutral-200 leading-none"
                    v-if="
                      message.id === listMessages[listMessages.length - 1].id &&
                      listMessages[listMessages.length - 1].seen_by
                        .map((obj) => obj.created_by?.email)
                        .includes(userStore.user.email) === false
                    "
                    >Đã xem
                    {{
                      listMessages[listMessages.length - 1].created_at_formatted
                    }}
                    trước</span
                  >
                </div>
                <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
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
                        recentConversation?.group_messages?.filter(
                          (user) => user.sent_to?.id === userStore.user.id
                        )
                      "
                      v-bind:key="message.id"
                      class="mb-4"
                    >
                      <div
                        class="bg-gray-200 p-3 rounded-r-lg rounded-bl-lg dark:bg-slate-500 dark:border-slate-600 dark:text-neutral-200"
                        v-if="message?.created_by !== chats[0]?.users[0].name"
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
                          listMessages[listMessages.length - 1]
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
            <img :src="url" class="w-20 h-20 rounded-lg border-[1px] border-slate-200 bg-slate-300 dark:border-slate-500 p-1" />
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
  import ConversationBox from "./ConversationBox.vue";
  import { useUserStore } from "../../stores/user";
  import { RouterLink } from "vue-router";
  
  import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
  import "emoji-picker-element";
  import {
    FaceSmileIcon,
    PlusCircleIcon,
    PaperAirplaneIcon,
    PhotoIcon,
    GifIcon,
  } from "@heroicons/vue/24/outline";
  
  import themes from '../../data/themes'
  
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
        url: null,
        themes: themes
      };
    },
    computed: {
      selectedTheme() {
        return this.themes.filter(
          (theme) => theme.name === this.recentConversation.theme
        )[0];
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
      this.getActiveConversation();
      this.getMessages();
      this.scrollToBottom();
    },
    methods: {
      scrollToBottom() {
        const objDiv = document.getElementById("chatview-container");
        objDiv.scrollTop = objDiv.scrollHeight;
      },
      getActiveConversation() {
        axios
          .get(`/api/chat/group/${this.$route.params.id}/`)
          .then((res) => {
            this.recentConversation = res.data;
          })
          .catch((error) => {
            console.log(error);
          });
      },
      getMessages() {
        axios
          .get(`/api/chat/group/${this.$route.params.id}/`)
          .then((res) => {
            this.recentConversation = res.data;
            this.listMessages = this.recentConversation.group_messages;
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
          .post(`/api/chat/${this.recentConversation.id}/send_group/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            // console.log(res.data);
            this.scrollToBottom();
            this.recentConversation.group_messages?.push(res.data);
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
  
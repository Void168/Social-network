<template>
  <div @click="$emit('seenMessage')">
    <RouterLink
      class="flex justify-between cursor-pointer"
      :to="{ name: 'conversation', params: { id: conversation.id } }"
    >
      <div
        class="w-full group relative flex flex-col gap-1 px-3 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-slate-500 duration-100"
      >
        <div class="absolute right-3 bottom-2">
          <Menu
            as="div"
            class="hidden relative group-hover:inline-block text-left"
          >
            <div>
              <MenuButton
                class="btn inline-flex w-full justify-center rounded-full bg-white dark:bg-slate-300 dark:border-slate-400 dark:text-neutral-800 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 hover:text-gray-900"
              >
                <EllipsisHorizontalIcon class="w-3 h-3" />
              </MenuButton>
            </div>

            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems
                class="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              >
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <div
                      :class="[
                        active ? 'bg-gray-100 text-gray-700' : 'text-gray-700',
                        'block px-4 py-2 text-sm cursor-pointer',
                      ]"
                    >
                      <RouterLink
                        :to="{
                          name: 'profile',
                          params: {
                            id: conversation.users?.filter(
                              (user) => this.userStore.user.id !== user.id
                            )[0].id,
                          },
                        }"
                      >
                        <span class="flex items-center gap-3"
                          ><UserIcon class="w-5 h-5" />Đến trang cá nhân</span
                        >
                      </RouterLink>
                    </div>
                  </MenuItem>
                  <hr />
                  <MenuItem v-slot="{ active }" @click="openModal">
                    <div
                      :class="[
                        active ? 'bg-gray-100 text-rose-700' : 'text-rose-700',
                        'block px-4 py-2 text-sm cursor-pointer',
                      ]"
                    >
                      <span class="flex items-center gap-3"
                        ><TrashIcon class="w-5 h-5" />Xóa đoạn hội thoại</span
                      >
                    </div>
                  </MenuItem>
                </div>
              </MenuItems>
            </transition>
          </Menu>
          <DeleteConversationModal
            :show="isOpen"
            @closeModal="closeModal"
            @deleteConversation="deleteConversation"
          />
        </div>
        <div class="flex sm:justify-between justify-center items-center">
          <div class="flex justify-center items-center gap-3">
            <img
            loading="lazy"
              :src="friend?.get_avatar"
              alt="avatar"
              class="xm:w-14 xm:h-14 h-10 w-10 rounded-full shadow-lg"
            />
            <p
              class="text-xs font-bold dark:text-neutral-300 sm:block hidden"
              v-if="
              lastMessage &&
                lastMessage?.seen_by
                  .map((obj) => obj.created_by.email)
                  .includes(userStore.user.email) === false
              "
            >
              {{ friend?.name }}
            </p>
            <p
              v-else-if="friend?.id !== userStore.user.id"
              class="text-sm dark:text-neutral-300 font-semibold sm:block hidden"
            >
              {{ friend?.name }}
            </p>
          </div>

          <span
            v-if="conversation?.messages?.length && lastMessage"
            class="text-xs text-gray-600 dark:text-neutral-300 sm:block hidden"
            >{{ lastMessage?.created_at_formatted }} trước</span
          >
        </div>

        <div class="text-sm sm:block hidden">
          <div
            v-if="conversation?.messages?.length"
            class="flex gap-1 justify-between"
          >
            <div class="flex gap-2 px-2 py-1 w-[50%]">
              <span
                class="font-semibold"
                v-if="lastMessage?.created_by?.id === userStore.user.id && lastMessage"
                >Bạn:
              </span>
              <span
                v-else-if="
                  lastMessage?.created_by?.id !== userStore.user.id &&
                  lastMessage?.seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === false && lastMessage
                "
                class="font-bold text-emerald-500 dark:text-neutral-200"
                >{{ lastMessage?.created_by?.name }}:
              </span>
              <span class="dark:text-neutral-300" v-else
                >{{ lastMessage?.created_by?.name }}:
              </span>
              <div class="flex justify-between w-full">
                <p
                  class="truncate font-bold text-emerald-500 dark:text-neutral-200"
                  v-if="
                    conversation.messages[
                      conversation.messages.length - 1
                    ]?.seen_by
                      .map((obj) => obj.created_by.email)
                      .includes(userStore.user.email) === false
                  "
                >
                  {{ lastMessage?.body }}
                </p>
                <p class="truncate dark:text-neutral-300" v-else>
                  {{ lastMessage?.body }}
                </p>
              </div>
            </div>
            <span
              class="bg-emerald-500 w-3 h-3 rounded-full shadow-md"
              v-if="
                conversation.messages[conversation.messages.length - 1]?.seen_by
                  .map((obj) => obj.created_by.email)
                  .includes(userStore.user.email) === false 
              "
            ></span>
            <span v-if="seen && lastMessage?.created_by?.id === userStore.user.id && lastMessage">
              <img
              loading="lazy"
                :src="friend.get_avatar"
                class="w-4 h-4 rounded-full"
                alt="seen-avatar"
              />
            </span>
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script>
import axios from "axios";
import Pusher from "pusher-js";
import { useUserStore } from "../../../stores/user";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  EllipsisHorizontalIcon,
  UserIcon,
  TrashIcon,
} from "@heroicons/vue/24/solid";
import { useToastStore } from "../../../stores/toast";
import DeleteConversationModal from "../../modals/chat/DeleteConversationModal.vue";

export default (await import("vue")).defineComponent({
  name: "ConversationBox",
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    DeleteConversationModal,
    EllipsisHorizontalIcon,
    TrashIcon,
    UserIcon,
  },
  data() {
    return {
      isOpen: false,
    };
  },
  props: {
    conversation: Object,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },

  computed: {
    getOtherUserId() {
      return this.conversation?.users?.filter(
        (user) => this.userStore.user.id !== user.id
      )[0];
    },
    lastMessage() {
      return this.conversation ? this.conversation?.messages[
        this.conversation?.messages?.length - 1
      ] : null;
    },
    friend() {
      return this.conversation?.users?.filter(
        (user) => user.id !== this.userStore.user.id
      )[0];
    },
    seen() {
      return this.lastMessage?.seen_by
        ?.map((user) => user?.created_by?.id)
        .includes(this.friend?.id);
    },
  },

  mounted() {
    this.getPusher();
  },

  methods: {
    getPusher() {
      Pusher.logToConsole = false;

      const pusher = new Pusher(import.meta.env.VITE_PUSHER_KEY, {
        cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
      });
      const channel = pusher.subscribe(`${this.conversation.id}`);
      channel.bind("message:new", (data) => {
        this.conversation?.messages.push(JSON.parse(data.message));
      });
      // channel.bind("seen_message", (data) => {
      //   this.lastMessage = JSON.parse(data.message);
      // });
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
            this.$router.push("/chat");
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
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
});
</script>

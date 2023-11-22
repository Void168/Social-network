<template>
  <div @click="$emit('seenMessage')">
    <RouterLink
      class="flex justify-between cursor-pointer"
      :to="{ name: 'conversation', params: { id: conversation.id } }"
    >
      <div
        class="group relative flex flex-col w-full gap-1 px-3 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-slate-500 duration-100"
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
        <div class="flex justify-between items-center">
          <div
            v-for="user in conversation.users"
            v-bind:key="user.id"
            class="flex justify-center items-center gap-3"
          >
            <img
              v-if="user.id !== userStore.user.id"
              :src="user.get_avatar"
              alt="avatar"
              class="w-10 h-10 rounded-full"
            />
            <p
              class="text-xs font-bold dark:text-neutral-300"
              v-if="
                user.id !== userStore.user.id &&
                conversation.messages[conversation.messages.length - 1]?.seen_by
                  .map((obj) => obj.created_by.email)
                  .includes(userStore.user.email) === false
              "
            >
              {{ user.name }}
            </p>
            <p
              v-else-if="user.id !== userStore.user.id"
              class="text-xs dark:text-neutral-300"
            >
              {{ user.name }}
            </p>
          </div>

          <span
            v-if="conversation.messages.length"
            class="text-xs text-gray-600 dark:text-neutral-300"
            >{{
              conversation.messages[conversation.messages.length - 1]
                .created_at_formatted
            }}
            trước</span
          >
        </div>

        <div class="text-sm">
          <div
            v-if="conversation.messages.length"
            class="flex gap-1 justify-between"
          >
            <div class="flex gap-2">
              <span
                class="font-semibold"
                v-if="
                  conversation.messages[conversation.messages.length - 1]
                    .created_by.id === userStore.user.id
                "
                >Bạn:
              </span>
              <span
                v-else-if="
                  conversation.messages[conversation.messages.length - 1]
                    .created_by.id !== userStore.user.id &&
                  conversation.messages[
                    conversation.messages.length - 1
                  ]?.seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === false
                "
                class="font-bold text-emerald-500 dark:text-neutral-200"
                >{{
                  conversation.messages[conversation.messages.length - 1]
                    .created_by.name
                }}:
              </span>
              <span class="dark:text-neutral-300" v-else
                >{{
                  conversation.messages[conversation.messages.length - 1]
                    .created_by.name
                }}:
              </span>
              <div class="flex justify-between">
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
                  {{
                    conversation?.messages[conversation.messages?.length - 1]
                      .body
                  }}
                </p>
                <p class="truncate dark:text-neutral-300" v-else>
                  {{
                    conversation?.messages[conversation.messages?.length - 1]
                      .body
                  }}
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
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../stores/user";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  EllipsisHorizontalIcon,
  UserIcon,
  TrashIcon,
} from "@heroicons/vue/24/solid";
import { useToastStore } from "../../stores/toast";
import DeleteConversationModal from "../modals/DeleteConversationModal.vue";

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
      conversations: [],
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
      return this.conversation.users?.filter(
        (user) => this.userStore.user.id !== user.id
      )[0];
    },
  },
  mounted() {
    this.getConversations();
  },

  methods: {
    getConversations() {
      axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
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

<template>
  <div @click="$emit('seenGroupMessage')">
    <RouterLink
      class="flex justify-between cursor-pointer my-2"
      :to="{ name: 'groupConversation', params: { id: groupConversation.id } }"
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
                  <hr />
                  <MenuItem v-slot="{ active }">
                    <div
                      :class="[
                        active ? 'bg-gray-100 text-gray-700' : 'text-gray-700',
                        'block px-4 py-2 text-sm cursor-pointer',
                      ]"
                    >
                      <span class="flex items-center gap-3"
                        ><UserIcon class="w-5 h-5" />Rời nhóm</span
                      >
                    </div>
                  </MenuItem>
                  <MenuItem
                    v-slot="{ active }"
                    @click="openModal"
                    v-if="groupConversation.admin.name === userStore.user.name"
                  >
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
          <div class="flex justify-center items-center gap-4 w-full">
            <div class="h-14 w-16 relative" v-if="!groupConversation.get_avatar">
              <img
              loading="lazy"
                :src="getAvatars[1]"
                alt="avatar-1"
                class="w-9 h-9 rounded-full absolute top-0 z-10 right-0"
              />
              <img
              loading="lazy"
                :src="getAvatars[0]"
                alt="avatar-0"
                class="w-9 h-9 rounded-full ring-4 ring-white dark:ring-slate-600 absolute bottom-0 z-20"
              />
            </div>
            <img
            loading="lazy"
              v-else
              :src="groupConversation.get_avatar"
              alt="avatar-group"
              class="xm:w-14 xm:h-14 h-10 w-10 rounded-full"
            />
            <p class="text-sm font-bold dark:text-neutral-300 w-full truncate sm:block hidden">
              {{ groupConversation.group_name }}
            </p>
          </div>
        </div>

        <div class="text-sm gap-2 items-center sm:flex hidden">
          <div
            v-if="groupConversation?.group_messages?.length"
            class="flex gap-1 justify-between items-center w-full"
          >
            <div class="flex justify-between px-2 py-1 w-full">
              <div class="flex gap-2 w-full items-center">
                <span
                  class="font-semibold"
                  v-if="
                    groupConversation.group_messages[
                      groupConversation.group_messages?.length - 1
                    ]?.created_by.id === userStore.user.id
                  "
                  >Bạn:
                </span>
                <span
                  v-else-if="
                    groupConversation.group_messages[
                      groupConversation.group_messages?.length - 1
                    ]?.created_by.id !== userStore.user.id &&
                    groupConversation.group_messages[
                      groupConversation.group_messages?.length - 1
                    ]?.seen_by
                      .map((obj) => obj.created_by.email)
                      .includes(userStore.user.email) === false
                  "
                  class="font-bold text-emerald-500 dark:text-neutral-200 truncate"
                  >{{
                    groupConversation.group_messages[
                      groupConversation.group_messages?.length - 1
                    ]?.created_by.name
                  }}:
                </span>
                <span class="dark:text-neutral-300 truncate" v-else
                  >{{
                    groupConversation.group_messages[
                      groupConversation.group_messages?.length - 1
                    ]?.created_by.name
                  }}:
                </span>
                <div class="flex justify-between w-[40%]">
                  <p
                    class="truncate font-bold text-emerald-500 dark:text-neutral-200"
                    v-if="
                      groupConversation.group_messages[
                        groupConversation.group_messages?.length - 1
                      ]?.seen_by
                        .map((obj) => obj.created_by.email)
                        .includes(userStore.user.email) === false
                    "
                  >
                    {{
                      groupConversation?.group_messages[
                        groupConversation.group_messages?.length - 1
                      ]?.body
                    }}
                  </p>
                  <p class="truncate dark:text-neutral-300" v-else>
                    {{
                      groupConversation?.group_messages[
                        groupConversation.group_messages?.length - 1
                      ]?.body
                    }}
                  </p>
                </div>
                <span
                  v-if="groupConversation?.group_messages?.length"
                  class="text-xs text-gray-600 dark:text-neutral-300"
                  >{{
                    groupConversation.group_messages[
                      groupConversation.group_messages?.length - 1
                    ]?.created_at_formatted
                  }}
                  trước</span
                >
              </div>
              <span
                class="bg-emerald-500 w-3 h-3 rounded-full shadow-md flex-end"
                v-if="
                  groupConversation.group_messages[
                    groupConversation.group_messages.length - 1
                  ]?.seen_by
                    .map((obj) => obj.created_by.email)
                    .includes(userStore.user.email) === false
                "
              ></span>
            </div>
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
    groupConversation: Object,
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
      return this.groupConversation.users?.filter(
        (user) => this.userStore.user.id !== user.id
      )[0];
    },
    getAvatars() {
      return this.groupConversation?.users
        ?.filter((user) => this.userStore.user.id !== user.id)
        .map((user) => user?.get_avatar)
        .slice(0, 2);
    },
  },
  mounted() {
    this.getPusher()
  },
  methods: {
    getPusher() {
      Pusher.logToConsole = false;

      const pusher = new Pusher(import.meta.env.VITE_PUSHER_KEY, {
        cluster: `${import.meta.env.VITE_PUSHER_CLUSTER}`,
      });
      const channel = pusher.subscribe(`${this.groupConversation.id}`);
      channel.bind("group_message:new", (data) => {
        this.groupConversation?.group_messages.push(JSON.parse(data.message));
      });
    },
    deleteConversation() {
      this.$emit("deleteConversation", this.groupConversation.id);

      axios
        .delete(`/api/chat/group/${this.groupConversation.id}/delete/`)
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

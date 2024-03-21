<template>
  <div @click="$emit('seenPageMessage')">
    <RouterLink
      class="flex justify-between cursor-pointer"
      :to="{ name: 'pageConversation', params: { id: pageConversation?.id } }"
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
                          name: pageStore.pageId ? 'page' : 'profile',
                          params: {
                            id: pageStore.pageId
                              ? pageConversation?.user?.id
                              : pageConversation?.page?.id,
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
          <!-- <DeleteConversationModal
            :show="isOpen"
            @closeModal="closeModal"
            @deleteConversation="deleteConversation"
          /> -->
        </div>
        <div class="flex sm:justify-between items-center gap-2">
          <div class="flex justify-center items-center gap-3">
            <img
            loading="lazy"
              :src="
                pageStore.pageId
                  ? pageConversation?.user?.get_avatar
                  : pageConversation?.page?.get_avatar
              "
              alt="avatar"
              class="xm:w-14 xm:h-14 h-10 w-10 rounded-full shadow-lg"
            />
            <div class="flex sm:flex-row flex-col sm:gap-3">
              <p
                class="text-sm font-bold dark:text-neutral-300 truncate"
              >
                {{
                  pageStore.pageId
                    ? pageConversation?.user?.name
                    : pageConversation?.page?.name
                }}
              </p>
              <span
                v-if="pageMessages?.length"
                class="text-xs text-gray-600 dark:text-neutral-300"
                >{{ lastMessage?.created_at_formatted }} trước</span
              >
            </div>
          </div>
        </div>

        <div class="text-sm">
          <div v-if="pageMessages?.length" class="flex gap-1 justify-between items-center">
            <div class="flex gap-2 px-2 py-1 w-full">
              <span
                class="font-semibold"
                v-if="
                  lastMessage?.created_by?.id === userStore.user.id &&
                  !pageStore.pageId
                "
                >Bạn:
              </span>
              <span
                class="font-semibold"
                v-else-if="
                  lastMessage?.created_by_page?.id === pageStore.pageId &&
                  pageStore.pageId
                "
                >Bạn:
              </span>
              <span
                v-else-if="checkUserSeen"
                class="font-bold text-emerald-500 dark:text-neutral-200 min-w-max"
                >{{ lastMessage?.created_by_page ? lastMessage?.created_by_page?.name : lastMessage?.created_by?.name }}:
              </span>
              <span class="text-emerald-500 dark:text-neutral-300 min-w-max" v-else
                >{{ lastMessage?.created_by_page ? lastMessage?.created_by_page?.name : lastMessage?.created_by?.name }}:
              </span>
              <div
                class="flex justify-between w-full"
                v-if="pageMessages?.length"
              >
                <p
                  class="truncate text-emerald-500 dark:text-neutral-200"
                  :class="!checkPageSeen && !pageStore.pageId || !checkUserSeen && pageStore.pageId ? 'font-bold' : ''"
                >
                  {{ lastMessage?.body }}
                </p>
              </div>
            </div>
            <span
              class="bg-emerald-500 w-3 h-3 rounded-full shadow-md"
              v-if="!checkUserSeen && pageStore.pageId"
            ></span>
            <span
              class="bg-emerald-500 w-3 h-3 rounded-full shadow-md"
              v-if="!checkPageSeen && !pageStore.pageId"
            ></span>
            <span
              v-if="
                checkPageSeen && !pageStore.pageId
              "
            >
              <img
              loading="lazy"
                :src="pageConversation?.page?.get_avatar"
                class="w-4 h-4 rounded-full"
                alt="seen-avatar"
              />
            </span>
            <span
              v-if="
                checkUserSeen && pageStore.pageId
              "
            >
              <img
              loading="lazy"
                :src="pageConversation?.user?.get_avatar"
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
import { usePageStore } from "../../../stores/page";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  EllipsisHorizontalIcon,
  UserIcon,
  TrashIcon,
} from "@heroicons/vue/24/solid";
import { useToastStore } from "../../../stores/toast";
import DeleteConversationModal from "../../modals/chat/DeleteConversationModal.vue";

export default (await import("vue")).defineComponent({
  name: "PageConversationBox",
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
    pageConversation: Object,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore();

    return {
      userStore,
      toastStore,
      pageStore,
    };
  },

  data() {
    return {
      pageMessages: this.pageConversation?.page_messages,
    };
  },

  computed: {
    lastMessage() {
      return this.pageConversation?.page_messages?.length
        ? this.pageConversation?.page_messages[
            this.pageConversation?.page_messages?.length - 1
          ]
        : {};
    },
    checkUserSeen() {
      return this.lastMessage?.seen_by?.created_by?.id === this.pageConversation?.user?.id;
    },
    checkPageSeen(){
      return this.lastMessage?.seen_by_page?.created_by?.id === this.pageConversation?.page?.id
    }
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
      const channel = pusher.subscribe(`${this.pageConversation?.id}`);
      channel.bind("message:new", (data) => {
        this.pageMessages?.push(JSON.parse(data.message));
      });
      channel.bind("seen_message", (data) => {
        this.lastMessage = JSON.parse(data.message);
      });
    },
    deleteConversation() {
      this.$emit("deleteConversation", this.pageConversation?.id);

      axios
        .delete(`/api/chat/${this.pageConversation?.id}/delete/`)
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

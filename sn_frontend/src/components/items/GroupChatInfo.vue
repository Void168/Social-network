<template>
  <div class="py-4">
    <div class="flex flex-col items-center justify-center">
      <div class="h-14 w-16 relative" v-if="!activeConversation.get_avatar">
        <img
          :src="avatar1"
          alt="avatar-1"
          class="w-9 h-9 rounded-full absolute top-0 z-10 right-0"
        />
        <img
          :src="avatar2"
          alt="avatar-0"
          class="w-9 h-9 rounded-full ring-4 ring-white dark:ring-slate-600 absolute bottom-0 z-20"
        />
      </div>
      <img
        v-else
        :src="activeConversation.get_avatar"
        alt="avatar-group"
        class="w-20 h-20 rounded-full shadow-md"
      />
      <p class="text-center font-semibold my-4 p-2">
        {{ activeConversation?.group_name }}
      </p>
      <div class="flex gap-3">
        <div class="flex flex-col items-center mb-4">
          <BellIcon
            class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
          />
          <span>Tắt thông báo</span>
        </div>
        <div class="flex flex-col items-center">
          <MagnifyingGlassIcon
            class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
          />
          <span>Tìm kiếm</span>
        </div>
      </div>
      <div class="w-full">
        <div class="w-full rounded-xl bg-white dark:bg-slate-600 p-2">
          <Disclosure v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg dark:bg-slate-600 px-4 py-2 text-left text-sm font-medium dark:text-neutral-200"
            >
              <span class="text-lg">Thông tin về đoạn chat</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <EyeDropperIcon class="h-8 w-8 dark:text-neutral-200 font-bold" />
              <span class="text-lg">Xem tin nhắn đã ghim</span>
            </DisclosurePanel>
          </Disclosure>
          <Disclosure as="div" class="mt-2" v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg dark:bg-slate-600 px-4 py-2 text-left text-sm font-medium dark:text-neutral-200"
            >
              <span class="text-lg">Tùy chỉnh đoạn chat</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              @click="openChangeGroupChatNameModal"
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <PencilIcon class="w-8 h-8 p-1 dark:text-neutral-200" />
              <span class="text-lg">Thay đổi tên nhóm</span>
              <ChangeGroupChatNameModal
                :activeConversation="activeConversation"
                :show="isChangeNameOpen"
                @closeModal="closeChangeGroupChatNameModal"
                @changeGroupChatName="changeGroupChatName"
              />
            </DisclosurePanel>
            <DisclosurePanel
              @click="openChangeGroupChatAvatarModal"
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <PhotoIcon class="w-8 h-8 p-1 dark:text-neutral-200" />
              <span class="text-lg">Thay đổi ảnh nhóm</span>
              <ChangeGroupChatAvatarModal
                :activeConversation="activeConversation"
                :show="isChangeAvatarOpen"
                @closeModal="closeChangeGroupChatAvatarModal"
                @changeGroupChatAvatar="changeGroupChatAvatar"
              />
            </DisclosurePanel>
            <DisclosurePanel
              @click="openGroupConversationThemeModal"
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <span
                class="h-8 w-8 rounded-full shadow-md relative"
                :class="[selectedTheme.background]"
              >
                <span
                  class="h-4 w-4 rounded-full absolute z-20 top-2 left-2 bg-white dark:bg-slate-600"
                ></span>
              </span>
              <span class="text-lg">Đổi chủ đề</span>
              <GroupConversationThemeModal
                :currentTheme="activeConversation"
                :show="isGroupConversationThemeModalOpen"
                @closeGroupConversationThemeModal="
                  closeGroupConversationThemeModal
                "
              />
            </DisclosurePanel>
          </Disclosure>
          <Disclosure as="div" class="mt-2" v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg dark:bg-slate-600 px-4 py-2 text-left text-sm font-medium dark:text-neutral-200"
            >
              <span class="text-lg">Thành viên trong đoạn chat</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>

            <DisclosurePanel
              class="px-4 pb-2 pt-4 text-sm dark:text-neutral-200 font-semibold"
            >
              <div
                class="flex flex-col items-center mb-4"
                v-if="(activeConversation.admin.id = userStore.user.id)"
              >
                <PlusCircleIcon
                  @click="openAddUsersModal"
                  class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                />
                <span>Thêm thành viên</span>
              </div>
              <AddUsersGroupConversationModalVue
                :show="isAddUsersOpen"
                @closeModal="closeAddUsersModal"
                @addUsers="addUsers"
              />
              <div v-for="user in activeConversation?.users" :key="user.id">
                <div class="flex items-center justify-between gap-3 space-y-4">
                  <div class="flex gap-3 items-center">
                    <img
                      :src="user.get_avatar"
                      alt=""
                      class="w-10 h-10 rounded-full"
                    />
                    <span class="font-bold">{{ user.name }}</span>
                    <span
                      class="font-bold ml-4"
                      v-if="activeConversation.admin.name === user.name"
                      >Trưởng nhóm</span
                    >
                  </div>
                  <Menu as="div" class="relative inline-block text-left">
                    <div>
                      <MenuButton>
                        <EllipsisHorizontalIcon
                          class="w-10 h-10 p-1 hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-full cursor-pointer transition"
                        />
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
                        class="absolute right-0 z-10 mt-2 w-80 origin-top-right divide-y divide-gray-100 rounded-md bg-white dark:bg-slate-700 shadow-lg ring-1 ring-black/5 focus:outline-none"
                      >
                        <div class="px-1 py-1">
                          <MenuItem v-slot="{ active }">
                            <button
                              :class="[
                                active
                                  ? 'bg-slate-200 dark:bg-slate-500 dark:text-neutral-200'
                                  : 'text-gray-900 dark:text-neutral-200',
                                'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                              ]"
                            >
                              <ChatBubbleOvalLeftIcon
                                :active="active"
                                class="mr-2 h-5 w-5 dark:text-neutral-200"
                                aria-hidden="true"
                              />
                              Nhắn tin
                            </button>
                          </MenuItem>
                          <MenuItem v-slot="{ active }">
                            <RouterLink
                              :to="{ name: 'profile', params: { id: user.id } }"
                            >
                              <button
                                :class="[
                                  active
                                    ? 'bg-slate-200 dark:bg-slate-500 dark:text-neutral-200'
                                    : 'text-gray-900 dark:text-neutral-200',
                                  'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                                ]"
                              >
                                <UserCircleIcon
                                  :active="active"
                                  class="mr-2 h-5 w-5 dark:text-neutral-200"
                                  aria-hidden="true"
                                />
                                Trang cá nhân
                              </button>
                            </RouterLink>
                          </MenuItem>
                        </div>

                        <div
                          class="px-1 py-1"
                          v-if="
                            activeConversation.admin.id === userStore.user.id &&
                            activeConversation.admin.id !== user.id
                          "
                          @click="kickUser(user)"
                        >
                          <MenuItem v-slot="{ active }">
                            <button
                              :class="[
                                active
                                  ? 'bg-slate-200 dark:bg-slate-500 dark:text-neutral-200'
                                  : 'text-gray-900 dark:text-neutral-200',
                                'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                              ]"
                            >
                              <ArrowLeftOnRectangleIcon
                                :active="active"
                                class="mr-2 h-5 w-5 dark:text-neutral-200"
                                aria-hidden="true"
                              />
                              Đá khỏi nhóm
                            </button>
                          </MenuItem>
                        </div>
                      </MenuItems>
                    </transition>
                  </Menu>
                </div>
              </div>
            </DisclosurePanel>
          </Disclosure>
          <Disclosure as="div" class="mt-2" v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg dark:bg-slate-600 px-4 py-2 text-left text-sm font-medium dark:text-neutral-200"
            >
              <span class="text-lg">File phương tiện</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="px-4 pb-2 pt-4 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              No.
            </DisclosurePanel>
          </Disclosure>
          <Disclosure as="div" class="mt-2" v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg dark:bg-slate-600 px-4 py-2 text-left text-sm font-medium dark:text-neutral-200"
            >
              <span class="text-lg">Quyền riêng tư & hỗ trợ</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="px-8 pb-2 pt-2 text-lg dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <div class="flex gap-2 items-center">
                <BellSlashIcon
                  class="w-8 h-8 p-1 shadow-md rounded-full cursor-pointer"
                />
                <span class="text-lg">Tắt thông báo</span>
              </div>
            </DisclosurePanel>
            <DisclosurePanel
              class="px-8 pb-2 pt-2 text-lg dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <div class="flex gap-2 items-center">
                <ExclamationTriangleIcon
                  class="w-8 h-8 p-1 shadow-md rounded-full cursor-pointer"
                />
                <span class="text-lg">Báo cáo</span>
              </div>
            </DisclosurePanel>
            <DisclosurePanel
              class="px-8 pb-2 pt-2 text-lg dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <div class="flex gap-2 items-center">
                <ArrowLeftOnRectangleIcon
                  class="w-8 h-8 p-1 shadow-md rounded-full cursor-pointer"
                />
                <span class="text-lg">Rời nhóm</span>
              </div>
            </DisclosurePanel>
          </Disclosure>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import themes from "../../data/themes";

import AddUsersGroupConversationModalVue from "../modals/AddUsersGroupConversationModal.vue";
import ChangeGroupChatNameModal from "../modals/ChangeGroupChatNameModal.vue";
import ChangeGroupChatAvatarModal from "../modals/ChangeGroupChatAvatarModal.vue";
import GroupConversationThemeModal from "../modals/GroupConversationThemeModal.vue";

import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/vue";
import {
  EllipsisHorizontalIcon,
  UserIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  BellIcon,
  ChevronUpIcon,
  EyeDropperIcon,
  ArrowLeftOnRectangleIcon,
  BellSlashIcon,
  ExclamationTriangleIcon,
  PhotoIcon,
  PencilIcon,
} from "@heroicons/vue/24/solid";
import {
  ChatBubbleOvalLeftIcon,
  UserCircleIcon,
  PlusCircleIcon,
} from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  props: {
    activeConversation: Object,
  },
  data() {
    return {
      isAddUsersOpen: false,
      isChangeNameOpen: false,
      isChangeAvatarOpen: false,
      isGroupConversationThemeModalOpen: false,
      themes: themes,
    };
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
    // getOtherUserId() {
    //   return this.activeConversation?.users?.filter(
    //     (user) => this.userStore.user.id !== user.id
    //   )[0];
    // },
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
  },
  methods: {
    closeAddUsersModal() {
      this.isAddUsersOpen = false;
    },
    openAddUsersModal() {
      this.isAddUsersOpen = true;
    },
    closeChangeGroupChatNameModal() {
      this.isChangeNameOpen = false;
    },
    openChangeGroupChatNameModal() {
      this.isChangeNameOpen = true;
    },
    closeChangeGroupChatAvatarModal() {
      this.isChangeAvatarOpen = false;
    },
    openChangeGroupChatAvatarModal() {
      this.isChangeAvatarOpen = true;
    },
    closeGroupConversationThemeModal() {
      this.isGroupConversationThemeModalOpen = false;
    },
    openGroupConversationThemeModal() {
      this.isGroupConversationThemeModalOpen = true;
    },
    addUsers() {
      console.log("hello");
    },
    kickUser(user) {
      axios
        .post(
          `/api/chat/group/${this.activeConversation.id}/kick-user/${user.id}/`
        )
        .then((res) => console.log(res.data))
        .catch((error) => console.log(error));
    },
  },
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    AddUsersGroupConversationModalVue,
    ChangeGroupChatNameModal,
    ChangeGroupChatAvatarModal,
    GroupConversationThemeModal,
    EllipsisHorizontalIcon,
    TrashIcon,
    UserIcon,
    MagnifyingGlassIcon,
    BellIcon,
    ChevronUpIcon,
    EyeDropperIcon,
    ChatBubbleOvalLeftIcon,
    UserCircleIcon,
    ArrowLeftOnRectangleIcon,
    BellSlashIcon,
    ExclamationTriangleIcon,
    PlusCircleIcon,
    PhotoIcon,
    PencilIcon,
  },
});
</script>

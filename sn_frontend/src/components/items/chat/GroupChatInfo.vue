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
        class="2xl:w-20 2xl:h-20 w-16 h-16 rounded-full shadow-md"
      />
      <p class="text-center font-semibold my-4 p-2">
        {{ activeConversation?.group_name }}
      </p>
      <div class="flex gap-3">
        <div class="flex flex-col items-center mb-4 2xl:text-base text-sm">
          <BellIcon
            class="2xl:w-8 2xl:h-8 w-6 h-6 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
          />
          <span>Tắt thông báo</span>
        </div>
        <div class="flex flex-col items-center 2xl:text-base text-sm">
          <MagnifyingGlassIcon
            class="2xl:w-8 2xl:h-8 w-6 h-6 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
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
              <span class="2xl:text-lg">Thông tin về đoạn chat</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <EyeDropperIcon class="2xl:h-8 2xl:w-8 w-6 h-6 dark:text-neutral-200 font-bold" />
              <span class="2xl:text-lg">Xem tin nhắn đã ghim</span>
            </DisclosurePanel>
          </Disclosure>
          <Disclosure as="div" class="mt-2" v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg dark:bg-slate-600 px-4 py-2 text-left text-sm font-medium dark:text-neutral-200"
            >
              <span class="2xl:text-lg">Tùy chỉnh đoạn chat</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              @click="openChangeGroupChatNameModal"
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <PencilIcon class="2xl:h-8 2xl:w-8 w-6 h-6 p-1 dark:text-neutral-200" />
              <span class="2xl:text-lg">Thay đổi tên nhóm</span>
              <ChangeGroupChatNameModal
                :activeConversation="activeConversation"
                :show="isChangeNameOpen"
                @closeModal="closeChangeGroupChatNameModal"
              />
            </DisclosurePanel>
            <DisclosurePanel
              @click="openChangeGroupChatAvatarModal"
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <PhotoIcon class="2xl:h-8 2xl:w-8 w-6 h-6 p-1 dark:text-neutral-200" />
              <span class="2xl:text-lg">Thay đổi ảnh nhóm</span>
              <ChangeGroupChatAvatarModal
                :activeConversation="activeConversation"
                :show="isChangeAvatarOpen"
                @closeModal="closeChangeGroupChatAvatarModal"
              />
            </DisclosurePanel>
            <DisclosurePanel
              @click="openGroupConversationThemeModal"
              class="flex gap-2 items-center pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <span
                class="2xl:h-8 2xl:w-8 w-6 h-6 rounded-full shadow-md relative"
                :class="[selectedTheme.background]"
              >
                <span
                  class="2xl:h-4 2xl:w-4 w-2 h-2 rounded-full absolute z-20 top-2 left-2 bg-white dark:bg-slate-600"
                ></span>
              </span>
              <span class="2xl:text-lg">Đổi chủ đề</span>
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
              <span class="2xl:text-lg">Thành viên trong đoạn chat</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>

            <DisclosurePanel
              class="px-4 pb-2 pt-4 text-sm dark:text-neutral-200 font-semibold"
            >
              <div class="flex justify-center flex-wrap items-center gap-4 mb-4">
                <div
                  v-if="activeConversation.admin.id === userStore.user.id"
                  class="flex flex-col items-center"
                >
                  <PlusCircleIcon
                    @click="openAddUsersModal"
                    class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                  />
                  <span class="2xl:text-base text-sm">Thêm thành viên</span>
                </div>
                <div class="flex flex-col items-center">
                  <PlusCircleIcon
                    @click="openCreatePollModal"
                    class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                  />
                  <span>Cuộc thăm dò ý kiến</span>
                </div>
              </div>
              <CreatePollModal
                :show="isCreatePollOpen"
                @closeModal="closeCreatePollModal"
                :activeConversation="activeConversation"
              />
              <AddUsersGroupConversationModalVue
                :options="options"
                :show="isAddUsersOpen"
                @closeModal="closeAddUsersModal"
              />
              <div v-for="user in activeConversation?.users" :key="user.id">
                <div class="flex items-center justify-between gap-3 space-y-4">
                  <div class="flex gap-3 items-center">
                    <img
                      :src="user.get_avatar"
                      alt=""
                      class="w-10 h-10 rounded-full"
                    />
                    <div class="flex flex-col">
                      <span class="font-bold">{{ user.name }}</span>
                      <span
                        class="font-bold"
                        v-if="activeConversation.admin.name === user.name"
                        >Trưởng nhóm</span
                      >
                      <span
                        class="font-bold"
                        v-if="getModeratorsIds.includes(user.id)"
                        >Quản trị viên</span
                      >
                    </div>
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
                        class="absolute right-[-10px] z-50 mt-2 w-64 origin-top-right divide-y divide-gray-100 rounded-md bg-white dark:bg-slate-700 shadow-lg ring-1 ring-black/5 focus:outline-none"
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
                          <MenuItem
                            v-slot="{ active }"
                            v-if="
                              activeConversation.admin.id ===
                                userStore.user.id &&
                              activeConversation.admin.id !== user.id
                            "
                          >
                            <button
                              @click="setModerator(user)"
                              :class="[
                                active
                                  ? 'bg-slate-200 dark:bg-slate-500 dark:text-neutral-200'
                                  : 'text-gray-900 dark:text-neutral-200',
                                'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                              ]"
                            >
                              <ShieldExclamationIcon
                                :active="active"
                                class="mr-2 h-5 w-5 dark:text-neutral-200"
                                aria-hidden="true"
                              />
                              Đặt làm quản trị viên
                            </button>
                          </MenuItem>
                        </div>

                        <div
                          class="px-1 py-1"
                          v-if="
                            (activeConversation.admin.id ===
                              userStore.user.id &&
                              activeConversation.admin.id !== user.id) ||
                            getModeratorsIds.includes(userStore.user.id)
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
              <span class="2xl:text-lg">File phương tiện</span>
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
              <span class="2xl:text-lg">Quyền riêng tư & hỗ trợ</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 dark:text-neutral-200 font-bold"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="px-8 pb-2 pt-2 dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <div class="flex gap-2 items-center">
                <BellSlashIcon
                  class="2xl:w-8 2xl:h-8 w-6 h-6 p-1 shadow-md rounded-full cursor-pointer"
                />
                <span class="2xl:text-lg">Tắt thông báo</span>
              </div>
            </DisclosurePanel>
            <DisclosurePanel
              class="px-8 pb-2 pt-2 dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <div class="flex gap-2 items-center">
                <ExclamationTriangleIcon
                  class="2xl:w-8 2xl:h-8 w-6 h-6 p-1 shadow-md rounded-full cursor-pointer"
                />
                <span class="2xl:text-lg">Báo cáo</span>
              </div>
            </DisclosurePanel>
            <DisclosurePanel
              @click="leaveGroup"
              class="px-8 pb-2 pt-2 dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <div class="flex gap-2 items-center">
                <ArrowLeftOnRectangleIcon
                  class="2xl:w-8 2xl:h-8 w-6 h-6 p-1 shadow-md rounded-full cursor-pointer"
                />
                <span class="2xl:text-lg">Rời nhóm</span>
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
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import themes from "../../../data/themes";

import AddUsersGroupConversationModalVue from "../../modals/chat/AddUsersGroupConversationModal.vue";
import ChangeGroupChatNameModal from "../../modals/chat/ChangeGroupChatNameModal.vue";
import ChangeGroupChatAvatarModal from "../../modals/chat/ChangeGroupChatAvatarModal.vue";
import GroupConversationThemeModal from "../../modals/chat/GroupConversationThemeModal.vue";
import CreatePollModal from "../../modals/chat/CreatePollModal.vue";

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
  ShieldExclamationIcon,
  QuestionMarkCircleIcon,
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
      isCreatePollOpen: false,
      options: [],
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
    getModeratorsIds() {
      return this.activeConversation?.moderators.map(
        (moderator) => moderator.id
      );
    },
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
      axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          const usersId = this.activeConversation.users.map((user) => user.id);
          const filteredFiends = res.data.friends.filter(
            (friend) => !usersId.includes(friend.id)
          );
          filteredFiends.forEach((friend) => {
            const obj = {};
            obj["label"] = friend.name;
            obj["value"] = friend.id;
            this.options.push(obj);
          });
        })
        .catch((error) => {
          console.log(error);
        });
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
    closeCreatePollModal() {
      this.isCreatePollOpen = false;
    },
    openCreatePollModal() {
      this.isCreatePollOpen = true;
    },

    setModerator(user) {
      axios
        .post(
          `/api/chat/group/${this.activeConversation.id}/set_moderator/${user.id}/`
        )
        .then((res) => {
          if (res.data.message === "Successful") {
            this.toastStore.showToast(
              3000,
              `Đặt ${user.name} làm quản trị viên thành công.`,
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 3500);
          } else {
            this.toastStore.showToast(
              3000,
              `Đặt ${user.name} làm quản trị viên thất bại.`,
              "bg-rose-400 text-white"
            );
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    kickUser(user) {
      if (user.id !== this.activeConversation.admin.id) {
        axios
          .post(
            `/api/chat/group/${this.activeConversation.id}/kick-user/${user.id}/`
          )
          .then((res) => {
            if (res.data.message === "kick user successfully") {
              this.toastStore.showToast(
                3000,
                `Đã đá ${user.name} ra khỏi nhóm.`,
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 3500);
            } else {
              this.toastStore.showToast(
                3000,
                `Đá ${user.name} thất bại.`,
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => console.log(error));
      } else {
        this.toastStore.showToast(
          3000,
          "Bạn không thể đá trưởng nhóm.",
          "bg-rose-400 text-white"
        );
      }
    },
    leaveGroup() {
      axios
        .post(
          `/api/chat/group/${this.activeConversation.id}/leave-group/${this.userStore.user.id}/`
        )
        .then((res) => {
          if (res.data.message === "Left group") {
            this.toastStore.showToast(
              3000,
              `Đã rời khỏi nhóm.`,
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.push("/chat");
            }, 3500);
          } else {
            this.toastStore.showToast(
              3000,
              `Rời nhóm thất bại.`,
              "bg-rose-400 text-white"
            );
          }
        })
        .catch((error) => console.log(error));
    },
    createPoll() {
      console.log("hello");
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
    CreatePollModal,
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
    ShieldExclamationIcon,
    QuestionMarkCircleIcon,
  },
});
</script>

<template>
  <div class="py-4">
    <div class="flex flex-col items-center justify-center">
      <div class="h-14 w-16 relative">
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
      <p class="text-center font-semibold my-4 p-2">
        {{ activeConversation?.name }}
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
              class="flex items-center gap-2 px-8 pb-2 pt-2 dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <EyeDropperIcon class="h-5 w-5 dark:text-neutral-200 font-bold" />
              <span>Xem tin nhắn đã ghim</span>
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
              class="pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <span class="text-lg">Thay đổi ảnh nhóm</span>
            </DisclosurePanel>
            <DisclosurePanel
              class="pb-2 pt-2 px-8 text-sm dark:text-neutral-200 font-semibold hover:bg-neutral-300 dark:hover:bg-slate-700 rounded-md cursor-pointer transition duration-100"
            >
              <span class="text-lg">Đổi chủ đề</span>
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
              v-for="user in activeConversation?.users"
              :key="user.id"
              class="px-4 pb-2 pt-4 text-sm dark:text-neutral-200 font-semibold"
            >
              <div class="flex items-center justify-between gap-3">
                <div class="flex gap-3 items-center">
                  <img
                    :src="user.get_avatar"
                    alt=""
                    class="w-10 h-10 rounded-full"
                  />
                  <span class="font-bold">{{ user.name }}</span>
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
                        v-if="activeConversation.admin.id === userStore.user.id"
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
} from "@heroicons/vue/24/solid";
import {
  ChatBubbleOvalLeftIcon,
  UserCircleIcon,
} from "@heroicons/vue/24/outline";
import { useToastStore } from "../../stores/toast";

export default (await import("vue")).defineComponent({
  props: {
    activeConversation: Object,
  },
  data() {
    return {
      isOpen: false,
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
  //   methods: {
  //     closeModal() {
  //       this.isOpen = false;
  //     },
  //     openModal() {
  //       this.isOpen = true;
  //     },
  //   },
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
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
  },
});
</script>

<template>
  <div>
    <template v-if="userStore.user.isAuthenticated && userStore.user.id && !route.path.includes('auth')">
      <div class="flex flex-row items-center gap-3">
        <img
          loading="lazy"
          :src="
            pageStore.pageActive.id
              ? pageStore.pageActive.get_avatar
              : userStore.user.avatar
          "
          class="rounded-full w-12 h-12 vs:hidden sm:block"
          alt="avatar"
        />
        <Popover v-slot="{ open }" class="relative">
          <PopoverButton
            :class="open ? 'text-white' : 'text-white/90'"
            class="group inline-flex items-center rounded-md px-3 py-2 text-base font-medium hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
            @click="outListPage"
          >
            <span
              class="text-slate-700 dark:text-neutral-200 vs:hidden sm:block"
              >{{
                pageStore.pageActive.id
                  ? pageStore.pageActive.name
                  : userStore.user.name
              }}</span
            >
            <img
              loading="lazy"
              :src="
            pageStore.pageActive.id
              ? pageStore.pageActive.get_avatar
              : userStore.user.avatar
          "
              class="rounded-full w-8 h-8 sm:hidden vs:block"
              alt="avatar"
            />
            <ChevronDownIcon
              :class="
                open
                  ? 'text-slate-700 dark:text-neutral-200'
                  : 'text-slate-700 dark:text-neutral-200/70'
              "
              class="ml-2 h-5 w-5 transition duration-150 ease-in-out group-hover:text-neutral-300/80"
              aria-hidden="true"
            />
          </PopoverButton>

          <PopoverOverlay
            class="fixed inset-0 opacity-30"
            @click="outListPage"
          />
          <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-y-1 opacity-0"
            enter-to-class="translate-y-0 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 opacity-100"
            leave-to-class="translate-y-1 opacity-0"
          >
            <PopoverPanel
              v-slot="{ close }"
              class="absolute z-50 xs:left-[-90px] xm:left-[-70px] vs:left-[-20px] mt-3 w-screen max-w-xs -translate-x-1/2 transform px-4 sm:px-0"
            >
              <div
                v-if="isBack"
                class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5"
              >
                <div class="bg-gray-50 dark:bg-slate-800 p-4">
                  <RouterLink
                    :to="{
                      name: pageStore.pageId ? 'page' : 'profile',
                      params: {
                        id: pageStore.pageId
                          ? pageStore.pageId
                          : userStore.user.id,
                      },
                    }"
                  >
                    <div
                      @click="accept(close)"
                      class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-600 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 cursor-pointer"
                    >
                      <span class="flex items-center">
                        <span
                          class="text-sm font-medium text-gray-900 dark:text-neutral-200"
                        >
                          Trang cá nhân
                        </span>
                      </span>
                    </div>
                  </RouterLink>
                  <hr class="my-1 border-slate-500" />
                  <div
                    class="flow-root mt-4 mb-2 rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:bg-slate-600 dark:hover:bg-slate-500 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 cursor-pointer"
                  >
                    <span
                      class="flex items-center justify-center"
                      @click="toPageList"
                    >
                      <span
                        class="text-sm font-medium text-gray-900 dark:text-neutral-200"
                      >
                        Xem tất cả trang cá nhân
                      </span>
                    </span>
                  </div>
                  <RouterLink @click="accept(close)" to="/notifications" class="group xs:hidden flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 text-sm font-medium text-gray-900 dark:text-neutral-200">
                    Thông báo
                  </RouterLink>
                  <RouterLink @click="accept(close)" to="/groups" class="group xs:hidden flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 text-sm font-medium text-gray-900 dark:text-neutral-200">
                    Nhóm
                  </RouterLink>
                  <div
                    class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50"
                  >
                    <span class="flex items-center justify-between">
                      <span
                        class="text-sm font-medium text-gray-900 dark:text-neutral-200"
                      >
                        Chế độ màn hình
                      </span>
                      <Switch
                        @click="toggleDark()"
                        v-model="enabled"
                        :class="isDark ? 'bg-neutral-900' : 'bg-neutral-200'"
                        class="relative inline-flex justify-between items-center h-[23px] w-[48px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
                      >
                        <SunIcon class="w-5 h-5" />
                        <MoonIcon class="w-5 h-5" />

                        <span
                          aria-hidden="true"
                          :class="isDark ? 'translate-x-[-2px]' : 'translate-x-[23px]'"
                          class="absolute top-[-1] left-[2px] z-10 pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
                        />
                      </Switch>
                    </span>
                  </div>
                  <div
                    @click="accept(close)"
                    class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-600 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 cursor-pointer"
                  >
                    <RouterLink
                      :to="pageStore.pageId ? '/page/edit' : '/profile/edit'"
                    >
                      <span class="flex items-center">
                        <span
                          class="text-sm font-medium text-gray-900 dark:text-neutral-200"
                        >
                          Chỉnh sửa thông tin
                        </span>
                      </span>
                    </RouterLink>
                  </div>
                  <div
                    @click="accept(close)"
                    class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-600 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 cursor-pointer"
                  >
                    <span class="flex items-center" @click="logout">
                      <span
                        class="text-sm font-medium text-gray-900 dark:text-neutral-200"
                      >
                        Đăng xuất
                      </span>
                    </span>
                  </div>
                </div>
              </div>
              <div
                v-else
                class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5 dark:bg-slate-800 bg-white py-4"
              >
                <div class="bg-gray-50 dark:bg-slate-800 px-4 py-2">
                  <div
                    class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50"
                  >
                    <div class="flex gap-3 items-center">
                      <ArrowLeftIcon
                        class="w-8 cursor-pointer p-1 rounded-full dark:bg-slate-700 hover:dark:bg-slate-600 transition"
                        @click="outListPage"
                      />
                      <h1 class="text-2xl font-bold">Chọn trang cá nhân</h1>
                    </div>
                  </div>
                  <hr class="my-1 border-slate-500" />
                </div>
                <div
                  class="px-4"
                  @click="
                    accept(close);
                    outPage();
                  "
                >
                  <div
                    class="flex justify-between items-center dark:hover:bg-slate-700 p-2 rounded-xl cursor-pointer transition duration-100"
                  >
                    <div class="flex gap-3 items-center">
                      <img
                        loading="lazy"
                        :src="userStore.user.avatar"
                        alt="user-avatar"
                        class="w-10 h-10 rounded-full"
                      />
                      <h3 class="font-semibold">{{ userStore.user.name }}</h3>
                    </div>
                    <span
                      class="w-6 h-6 px-[6px] py-[6px] dark:bg-slate-500 bg-slate-200 rounded-full"
                    >
                      <span
                        v-if="!pageStore.pageActive.id"
                        class="w-3 h-3 bg-emerald-500 absolute rounded-full"
                      ></span>
                    </span>
                  </div>
                </div>
                <div
                  @click="
                    accept(close);
                    goToPage(page);
                  "
                  v-for="page in pages"
                  :key="page.id"
                  class="px-4"
                >
                  <div
                    class="flex justify-between items-center dark:hover:bg-slate-700 dark:bg-slate-800 bg-white hover:bg-slate-200 p-2 rounded-xl cursor-pointer transition duration-100"
                  >
                    <div class="flex gap-3 items-center">
                      <img
                        loading="lazy"
                        :src="page.get_avatar"
                        alt="page-avatar"
                        class="w-10 h-10 rounded-full"
                      />
                      <h3 class="font-semibold">{{ page.name }}</h3>
                    </div>
                    <span
                      class="w-6 h-6 px-[6px] py-[6px] dark:bg-slate-500 bg-slate-200 rounded-full"
                    >
                      <span
                        v-if="pageStore.pageActive.id === page.id"
                        class="w-3 h-3 bg-emerald-500 absolute rounded-full"
                      ></span>
                    </span>
                  </div>
                </div>
                <div @click="accept(close)">
                  <div class="px-4" @click="openCreatePageModal">
                    <div
                      class="flex gap-2 items-center dark:hover:bg-slate-700 dark:bg-slate-800 bg-white hover:bg-slate-200 p-2 rounded-xl cursor-pointer transition duration-100"
                    >
                      <PlusIcon
                        class="w-8 dark:text-slate-200 dark:bg-slate-500 bg-slate-100 hover:bg-slate-200 rounded-full p-1"
                      />
                      <h2 class="font-semibold">Tạo trang mới</h2>
                    </div>
                  </div>
                </div>

                <div class="px-4 my-2" @click="accept(close)">
                  <div
                    class="flex gap-2 items-center justify-center bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 p-2 rounded-xl cursor-pointer transition duration-100"
                  >
                    <h3>Xem tất cả các trang</h3>
                  </div>
                </div>
              </div>
            </PopoverPanel>
          </transition>
        </Popover>
        <CreatePageModal
          :show="isCreatePageOpen"
          @closeCreatePageModal="closeCreatePageModal"
          :isCreatePageOpen="isCreatePageOpen"
        />
      </div>
    </template>

    <template v-else>
      <div class="flex justify-between items-center gap-3 py-[6px]">
        <RouterLink :to="{ name: 'login' }"
          ><button class="px-4 py-2 rounded-lg font-semibold">
            Đăng nhập
          </button></RouterLink
        >
        <RouterLink :to="{ name: 'signup' }"
          ><button class="px-4 py-2 rounded-lg font-semibold">
            Đăng ký
          </button></RouterLink
        >
      </div>
    </template>
  </div>
</template>

<script>
import axios from "axios";
import { useDark, useToggle } from "@vueuse/core";
import {
  Popover,
  PopoverButton,
  PopoverPanel,
  PopoverOverlay,
} from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import {
  SunIcon,
  MoonIcon,
  ArrowLeftIcon,
  PlusIcon,
} from "@heroicons/vue/24/solid";
import { Switch } from "@headlessui/vue";
import { ref } from "vue";
import { useUserStore } from "../../stores/user";
import { usePageStore } from "../../stores/page";
import { RouterLink } from "vue-router";
import { useRoute } from "vue-router";

import CreatePageModal from "../modals/page/createPage/CreatePageModal.vue";

export default {
  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore();
    const isDark = useDark();
    const toggleDark = useToggle(isDark);
    const enabled = ref(false);
    const route = useRoute();
    return {
      userStore,
      toggleDark,
      isDark,
      enabled,
      pageStore,
      route,
    };
  },

  components: {
    RouterLink,
    Switch,
    Popover,
    PopoverButton,
    PopoverOverlay,
    PopoverPanel,
    CreatePageModal,
    ChevronDownIcon,
    SunIcon,
    MoonIcon,
    ArrowLeftIcon,
    PlusIcon,
  },

  data() {
    return {
      isBack: false,
      isCreatePageOpen: false,
      pages: [],
    };
  },

  methods: {
    async toPageList() {
      this.isBack = false;

      await axios
        .get(`/api/page/get-pages/${this.userStore.user.id}/`)
        .then((res) => {
          this.pages = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    goToPage(data) {
      if (data) {
        setTimeout(() => {
          this.pageStore.setActivePage(data?.id);
          if (this.route.name === "profileedit") {
            window.location = "/page/edit";
          } else if (this.route.name === "pageEdit") {
            window.location = "/profile/edit";
          } else {
            window.location = "/";
          }
        }, 3000);
      }
    },
    outPage() {
      setTimeout(() => {
        this.pageStore.outPage();
        window.location = "/";
      }, 3000);
    },
    outListPage() {
      this.isBack = true;
    },
    openCreatePageModal() {
      this.isCreatePageOpen = true;
    },
    closeCreatePageModal() {
      this.isCreatePageOpen = false;
    },
    async accept(close) {
      await fetch("/accept-terms", { method: "POST" });
      close();
    },
    logout() {
      this.userStore.removeToken();
      this.pageStore.outPage();
      this.$router.push("/auth/login");
    },
  },
};
</script>

<style scoped>
.router-link-active {
  --tw-text-opacity: 1;
  --tw-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --tw-shadow-colored: 0 4px 6px -1px var(--tw-shadow-color),
    0 2px 4px -2px var(--tw-shadow-color);
  background-color: rgb(16 185 129);
  border-radius: 0.5rem;
  box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),
    var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);
}
</style>

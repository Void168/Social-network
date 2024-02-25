<template>
  <div class="relative">
    <nav
      ref="navbar"
      v-if="path !== '/stories'"
      class="xl:py-10 xl:px-8 p-4 border-b border-gray-200 bg-white dark:bg-slate-700 dark:border-slate-500 dark:text-neutral-200 sticky w-full z-50 top-0 shadow-md"
    >
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center sm:justify-between justify-center">
          <div class="menu-left sm:block hidden">
            <a href="/" class="text-xl">SN</a>
          </div>
          <div
            class="menu-center flex sm:space-x-12 xm:space-x-5 xs:space-x-1"
            v-if="userStore.user.isAuthenticated"
          >
            <RouterLink to="/" class="group">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6 m-3 group-hover:text-emerald-600 duration-100"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
                />
              </svg>
            </RouterLink>

            <RouterLink to="/chat" class="group">
              <span class="relative">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="w-6 h-6 m-3 group-hover:text-emerald-600 duration-100"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"
                  ></path>
                </svg>
                <span
                  class="text-white text-center w-6 h-6 absolute top-0 right-0 rounded-full bg-rose-400"
                  v-if="pageStore.pageId"
                >
                  {{
                    userUnseenConversationsStore.getUnseenConversations()
                  }}</span
                >
              </span>
            </RouterLink>

            <RouterLink to="/notifications" class="group">
              <span class="relative">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="w-6 h-6 m-3 group-hover:text-emerald-600"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
                  ></path>
                </svg>
                <span
                  class="text-white text-center w-6 h-6 absolute top-0 right-0 rounded-full bg-rose-400"
                  >{{ userNotificationStore.getNotifications() }}</span
                >
              </span>
            </RouterLink>
            <RouterLink to="/search" class="group">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6 m-3 group-hover:text-emerald-600 duration-100"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
                ></path>
              </svg>
            </RouterLink>
            <RouterLink to="/groups" class="group">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6 m-3 group-hover:text-emerald-600 duration-100"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z"
                />
              </svg>
            </RouterLink>
          </div>

          <div class="menu-right">
            <ProfileDropdown />
          </div>
        </div>
      </div>
    </nav>

    <main
      class="bg-gray-200 dark:bg-slate-700 relative"
      :class="path === '/stories' ? 'h-screen p-0' : 'min-h-screen'"
    >
      <RouterView />
    </main>

    <toast />
  </div>
</template>

<script>
import Toast from "@/components/Toast.vue";
import { useUserStore } from "./stores/user";
import { useNotificationStore } from "./stores/notification";
import { useUnseenConversationsStore } from "./stores/conversations";
// import { useConnectionStore } from "./stores/connection";
import { useCurrentStoryStore } from "./stores/currentStory";
import { useToastStore } from "./stores/toast";
import { usePageStore } from "./stores/page";
// import { socket } from "./socket";
import { useRoute } from "vue-router";
import { computed } from "vue";

import axios from "axios";
import { RouterLink } from "vue-router";
import { useDark, useToggle } from "@vueuse/core";
import { ref } from "vue";
import NavBarDropdownVue from "./components/dropdown/ProfileDropdown.vue";
import ProfileDropdown from "./components/dropdown/ProfileDropdown.vue";

export default {
  setup() {
    // const connectionStore = useConnectionStore();
    const currentStoryStore = useCurrentStoryStore();
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore();
    const userNotificationStore = useNotificationStore();
    const userUnseenConversationsStore = useUnseenConversationsStore();
    const isDark = useDark();
    const toggleDark = useToggle(isDark);
    const enabled = ref(false);
    const route = useRoute();

    const path = computed(() => route.path);

    return {
      // connectionStore,
      currentStoryStore,
      userStore,
      toastStore,
      pageStore,
      userNotificationStore,
      userUnseenConversationsStore,
      toggleDark,
      isDark,
      enabled,
      path,
    };
  },

  data() {
    return {
      height: document.documentElement.clientHeight,
      width: document.documentElement.clientWidth,
    };
  },

  components: {
    toast: Toast,
    RouterLink,
    NavBarDropdownVue,
    ProfileDropdown,
  },

  beforeCreate() {
    this.userStore.initStore();
    // socket.off();
    // this.connectionStore.bindEvents();

    const token = this.userStore.user.access;

    if (token) {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  },

  mounted() {
    window.addEventListener("resize", this.getDimensions);
    this.getDimensions();
    this.pageStore.getPagesList(this.userStore.user.id);
    this.pageStore.getActivePage();
  },

  unmounted() {
    window.removeEventListener("resize", this.getDimensions);
  },

  methods: {
    getDimensions() {
      this.height = document.documentElement.clientHeight;
      this.width = document.documentElement.clientWidth;
      this.toastStore.setHeight(
        this.height - this.$refs.navbar.clientHeight - 1
      );
      this.toastStore.setWidth(this.width);
      this.toastStore.setNavbarHeight(this.$refs.navbar.clientHeight + 1);
    },
  },
};
</script>

<style scoped>
html.dark {
  color-scheme: dark;
}

.router-link-active {
  --tw-text-opacity: 1;
  color: rgb(16 185 129 / var(--tw-text-opacity));
}

main {
  min-height: calc(100vh - 129px);
}
</style>

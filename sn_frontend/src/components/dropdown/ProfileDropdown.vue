<template>
  <div>
    <template v-if="userStore.user.isAuthenticated && userStore.user.id">
      <div class="flex flex-row items-center gap-3">
        <img
          :src="userStore.user.avatar"
          class="rounded-full w-12 h-12"
          alt="avatar"
        />
        <Popover v-slot="{ open }" class="relative">
          <PopoverButton
            :class="open ? 'text-white' : 'text-white/90'"
            class="group inline-flex items-center rounded-md px-3 py-2 text-base font-medium hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75"
          >
            <span class="text-slate-700 dark:text-neutral-200">{{
              userStore.user.name
            }}</span>
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

          <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-y-1 opacity-0"
            enter-to-class="translate-y-0 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 opacity-100"
            leave-to-class="translate-y-1 opacity-0"
          >
            <PopoverPanel
              class="absolute z-[100] left-[-70px] mt-3 w-screen max-w-xs -translate-x-1/2 transform px-4 sm:px-0"
            >
              <div
                class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5"
              >
                <div class="bg-gray-50 dark:bg-slate-800 p-4">
                  <div
                    class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-600 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 cursor-pointer"
                  >
                    <RouterLink
                      :to="{
                        name: 'profile',
                        params: { id: userStore.user.id },
                      }"
                    >
                      <span class="flex items-center">
                        <span
                          class="text-sm font-medium text-gray-900 dark:text-neutral-200"
                        >
                          Trang cá nhân
                        </span>
                      </span>
                    </RouterLink>
                  </div>
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
                          :class="
                            isDark
                              ? 'translate-x-0'
                              : 'translate-x-6'
                          "
                          class="absolute top-0 left-[2px] z-10 pointer-events-none inline-block h-[20px] w-[20px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
                        />
                      </Switch>
                    </span>
                  </div>
                  <div
                    class="flow-root rounded-md px-2 py-2 transition duration-150 ease-in-out hover:bg-gray-100 dark:hover:bg-slate-600 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50 cursor-pointer"
                  >
                    <RouterLink to="/profile/edit">
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
            </PopoverPanel>
          </transition>
        </Popover>
      </div>
    </template>

    <template v-else>
      <div class="flex justify-between items-center gap-3">
        <RouterLink to="/login"
          ><button class="btn">Đăng nhập</button></RouterLink
        >
        <RouterLink to="/signup"
          ><button class="bg-gray-300 btn">Đăng ký</button></RouterLink
        >
      </div>
    </template>
  </div>
</template>

<script>
import { useDark, useToggle } from "@vueuse/core";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { SunIcon, MoonIcon } from "@heroicons/vue/24/solid";
import { Switch } from "@headlessui/vue";
import { ref } from "vue";
import { useUserStore } from "../../stores/user";
import { RouterLink } from "vue-router";

export default {
  setup() {
    const userStore = useUserStore();
    const isDark = useDark();
    const toggleDark = useToggle(isDark);
    const enabled = ref(false);

    return {
      userStore,
      toggleDark,
      isDark,
      enabled,
    };
  },

  components: {
    RouterLink,
    Switch,
    Popover,
    PopoverButton,
    PopoverPanel,
    ChevronDownIcon,
    SunIcon,
    MoonIcon,
  },

  methods: {
    logout() {
      this.userStore.removeToken();

      this.$router.push("/login");
    },
  },
};
</script>

<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton class="btn flex gap-2 items-center">
        <HandThumbUpIcon class="w-5" />
        <span>Đã thích</span>
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
        class="absolute left-0 z-[10000] mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
      >
        <div class="py-1">
          <MenuItem
            v-slot="{ active }"
            v-if="checkFollowers"
            @click="$emit('unfollowPage')"
          >
            <div
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><EyeSlashIcon class="w-5 h-5" />Hủy theo dõi</span
              >
            </div>
          </MenuItem>
          <MenuItem v-slot="{ active }" @click="$emit('followPage')" v-else>
            <div
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><EyeSlashIcon class="w-5 h-5" />Theo dõi</span
              >
            </div>
          </MenuItem>
        </div>
        <div class="py-1">
          <MenuItem v-slot="{ active }" @click="$emit('dislikePage')">
            <div
              href="#"
              :class="[
                active ? 'bg-gray-100 text-rose-700' : 'text-rose-700',

                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><UserMinusIcon class="w-5 h-5" />Bỏ thích</span
              >
            </div>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>

<script>
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  ShieldCheckIcon,
  TrashIcon,
  UsersIcon,
  EyeSlashIcon,
  UserMinusIcon,
  HandThumbUpIcon,
} from "@heroicons/vue/24/solid";
import { useUserStore } from "../../stores/user";
import { usePageStore } from "../../stores/page";
export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ShieldCheckIcon,
    TrashIcon,
    UsersIcon,
    EyeSlashIcon,
    UserMinusIcon,
    HandThumbUpIcon,
  },

  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore();

    return {
      userStore,
      pageStore,
    };
  },

  props: {
    followers: Array,
    likes: Array,
  },

  computed: {
    checkFollowers() {
      return this.followers
        ?.map((fl) => fl.id)
        .includes(
          this.pageStore.pageId ? this.pageStore.pageId : this.userStore.user.id
        );
    },
  },
};
</script>

<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton
        class="inline-flex w-full justify-center py-2"
      >
        <EllipsisHorizontalIcon class="w-8"/>
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
        <div class="py-1" v-if="yourStory?.created_by?.id === userStore.user.id">
          <MenuItem v-slot="{ active }" @click="$emit('openModal')">
            <div
              :class="[
                active ? 'bg-gray-100 text-rose-700' : 'text-rose-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><TrashIcon class="w-5 h-5" />Xóa tin</span
              >
            </div>
          </MenuItem>
        </div>
        <div class="py-1">
          <MenuItem v-slot="{ active }">
            <div
              href="#"
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><ShieldCheckIcon class="w-5 h-5" />Báo cáo tin</span
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
import { ShieldCheckIcon, TrashIcon, EllipsisHorizontalIcon } from "@heroicons/vue/24/solid";
import { useUserStore } from "../../stores/user";

export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ShieldCheckIcon,
    TrashIcon,
    EllipsisHorizontalIcon
  },

  setup() {
    const userStore = useUserStore()

    return {
        userStore
    }
  },

  props: {
    yourStory: Object
  }
};
</script>

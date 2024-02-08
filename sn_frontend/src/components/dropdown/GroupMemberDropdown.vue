<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton
        class="flex gap-2 items-center dark:bg-slate-700 rounded-lg dark:hover:bg-slate-600 duration-75"
      >
        <EllipsisHorizontalIcon class="w-8 p-1" />
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
        class="absolute left-[-200px] z-[10000] mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
      >
        <div class="py-1">
          <MenuItem v-slot="{ active }">
            <RouterLink
              :to="{ name: 'profile', params: { id: member?.information?.id } }"
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><UserIcon class="w-5 h-5" />Trang cá nhân</span
              >
            </RouterLink>
          </MenuItem>
        </div>
        <MenuItem v-slot="{ active }" v-if="member?.information?.id !== group?.admin?.id">
            <div
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><UserIcon class="w-5 h-5" />Cấm khỏi nhóm</span
              >
            </div>
          </MenuItem>
        <MenuItem v-slot="{ active }" v-if="member?.information?.id !== group?.admin?.id">
            <div
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><UserIcon class="w-5 h-5" />Mời làm quản trị viên</span
              >
            </div>
          </MenuItem>
        <div class="py-1">
          <MenuItem
            v-slot="{ active }"
            @click="
              member?.information?.id !== group?.admin?.id
                ? $emit('removeMember', member)
                : $emit('leaveGroup')
            "
          >
            <div
              href="#"
              :class="[
                active ? 'bg-gray-100 text-rose-700' : 'text-rose-700',

                'block px-4 py-2 text-sm cursor-pointer',
              ]"
            >
              <span class="flex items-center gap-3"
                ><UserMinusIcon class="w-5 h-5" />{{ member?.information?.id !== group?.admin?.id ? 'Xóa thành viên' : 'Rời nhóm' }}</span
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
  UserMinusIcon,
  EllipsisHorizontalIcon,
  UserIcon,
} from "@heroicons/vue/24/solid";
import { RouterLink } from "vue-router";
import { useUserStore } from "../../stores/user";
import { usePageStore } from "../../stores/page";
export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    RouterLink,
    UserMinusIcon,
    EllipsisHorizontalIcon,
    UserIcon,
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
    member: Object,
    group: Object,
  },
};
</script>

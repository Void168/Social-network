<template>
    <Menu
      as="div"
      class="relative xm:hidden inline-block text-left font-medium justify-center dark:hover:bg-slate-600 duration-75 xm:text-sm text-xs"
    >
      <div>
        <MenuButton class="flex gap-2 items-center">
          <span>Xem thêm</span>
          <ChevronDownIcon class="w-5" />
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
          class="absolute left-[-140px] top-4 z-50 mt-2 w-56 origin-top-right bg-white dark:bg-slate-600 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
        >
          <div class="py-1">
            <MenuItem v-slot="{ active }">
              <RouterLink
                :to="{ name: 'pageusers', params: { id: page.id } }"
                :class="[
                  active
                    ? ' text-gray-900 dark:text-neutral-200'
                    : 'text-gray-700 dark:text-neutral-200',
                  'block px-4 py-2 text-sm cursor-pointer',
                ]"
              >
                <span class="flex items-center gap-3">Người theo dõi</span>
              </RouterLink>
            </MenuItem>
            <MenuItem v-slot="{ active }">
              <RouterLink
                :to="{ name: 'pagephotos', params: { id: page.id } }"
                :class="[
                  active
                    ? ' text-gray-900 dark:text-neutral-200'
                    : 'text-gray-700 dark:text-neutral-200',
                  'block px-4 py-2 text-sm cursor-pointer',
                ]"
              >
                <span class="flex items-center gap-3">Ảnh</span>
              </RouterLink>
            </MenuItem>
          </div>
          <div class="py-1">
            <MenuItem v-slot="{ active }">
              <RouterLink
                :to="{ name: 'pagephotos', params: { id: page.id } }"
                :class="[
                  active
                    ? ' text-gray-700 dark:text-neutral-200'
                    : 'text-gray-700 dark:text-neutral-200',
  
                  'block px-4 py-2 text-sm cursor-pointer',
                ]"
              >
                <span class="flex items-center gap-3">Video</span>
              </RouterLink>
            </MenuItem>
          </div>
        </MenuItems>
      </transition>
    </Menu>
  </template>
  
  <script>
  import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
  import { ChevronDownIcon } from "@heroicons/vue/24/solid";
  import { RouterLink } from "vue-router";
  
  export default {
    components: {
      Menu,
      MenuButton,
      MenuItem,
      MenuItems,
      ChevronDownIcon,
      RouterLink,
    },
  
    props: {
      page: Object,
    },
  };
  </script>
  
  <style scoped>
  .router-link-active {
    --tw-text-opacity: 1;
    color: rgb(16 185 129 / var(--tw-text-opacity));
    position: relative;
  }
  
  .router-link-active::before {
    --tw-text-opacity: 1;
    content: "";
    position: absolute;
    bottom: 0;
    height: 4px;
    width: 80%;
    z-index: 10;
    background-color: rgb(16 185 129 / var(--tw-text-opacity));
  }
  </style>
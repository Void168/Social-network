<template>
  <div class="relative">
    <div class="mb-2 flex items-center justify-between">
      <div class="flex items-center space-x-6 p-4">
        <img
          :src="
            !poll?.is_anonymous
              ? poll?.created_by?.information?.get_avatar
              : 'https://cdn-icons-png.flaticon.com/512/350/350351.png'
          "
          class="w-12 h-12 rounded-full"
        />
        <div class="flex gap-1 items-center flex-wrap">
          <strong class="group" v-if="!poll.is_anonymous">
            <RouterLink
              :to="{
                name: poll?.created_by?.is_page ? 'page' : 'profile',
                params: { id: poll?.created_by?.information?.id },
              }"
              >{{ poll.created_by?.information?.name }}</RouterLink
            >
          </strong>

          <strong class="group" v-else> Người tham gia ẩn danh </strong>
          <div class="md:hidden items-center gap-2 flex">
            <UserGroupIcon class="w-6" v-if="group?.is_private_group" />
            <GlobeAsiaAustraliaIcon class="w-6" v-else />
            <div class="relative group md:hidden">
              <p
                class="text-gray-600 dark:text-neutral-200 sm:text-base xs:text-sm group-hover:underline"
              >
                {{ poll?.created_at_formatted }} trước
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="p-4 md:flex items-center gap-2 hidden">
        <UserGroupIcon class="w-6" v-if="group?.is_private_group" />
        <GlobeAsiaAustraliaIcon class="w-6" v-else />
        <div class="relative group">
          <RouterLink :to="{ name: 'grouppost', params: { postid: poll.id } }">
            <p
              class="text-gray-600 dark:text-neutral-200 md:block hidden group-hover:underline"
            >
              {{ poll?.created_at_formatted }} trước
            </p>
          </RouterLink>
        </div>
      </div>
    </div>

    <p class="pb-4 text-lg">{{ poll.body }}</p>
    <div class="space-y-2">
      <div v-for="option in sortOptions" :key="option.id">
        <PollOption
          :key="componentKey"
          :option="option"
          @voteOption="voteOption"
          :totalVote="totalVote"
          :voteCount="option.vote_by.length"
        />
      </div>
    </div>
    <div class="p-4 my-6 flex justify-between">
      <div
        class="absolute bottom-0 right-4 shadow-lg rounded-lg ease-in duration-300"
      >
        <Menu as="div" class="relative inline-block text-left">
          <div>
            <MenuButton
              class="inline-flex w-full justify-center rounded-md bg-white md:px-3 md:py-2 px-2 py-1 text-gray-900 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 hover:text-gray-900"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"
                />
              </svg>
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
              <div
                class="py-1"
                v-if="
                  userStore.user.id === poll?.created_by?.id ||
                  pageStore.pageId === poll?.created_by?.id ||
                  userStore.user.id === poll?.created_by?.information?.id ||
                  group?.admin?.id === userStore.user.id
                "
              >
                <MenuItem v-slot="{ active }" @click="openModal">
                  <div
                    :class="[
                      active ? 'bg-gray-100 text-rose-700' : 'text-rose-700',
                      'block px-4 py-2 text-sm cursor-pointer',
                    ]"
                  >
                    <span class="flex items-center gap-3"
                      ><TrashIcon class="w-5 h-5" />Xóa bài viết</span
                    >
                  </div>
                </MenuItem>
              </div>
              <div class="py-1" v-else>
                <MenuItem v-slot="{ active }" @click="reportPost">
                  <div
                    href="#"
                    :class="[
                      active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                      'block px-4 py-2 text-sm cursor-pointer',
                    ]"
                  >
                    <span class="flex items-center gap-3"
                      ><ShieldCheckIcon class="w-5 h-5" />Báo cáo bài viết</span
                    >
                  </div>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
        <DeletePostModal
          :show="isOpen"
          @closeModal="closeModal"
          @deletePost="deletePost"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { RouterLink } from "vue-router";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ShieldCheckIcon, TrashIcon } from "@heroicons/vue/24/solid";
import {
  UserGroupIcon,
  GlobeAsiaAustraliaIcon,
} from "@heroicons/vue/24/outline";
import { HeartIcon as HeartLike } from "@heroicons/vue/24/solid";
import { useUserStore } from "../../../../stores/user";
import { useToastStore } from "../../../../stores/toast";
import { usePageStore } from "../../../../stores/page";
import DeletePostModal from "../../../modals/post/DeletePostModal.vue";
import PollOption from "./PollOption.vue";

export default (await import("vue")).defineComponent({
  props: {
    poll: Object,
    group: Object,
    currentMember: Object,
  },

  data() {
    return {
      isOpen: false,
      isLike: false,
      checkLike: false,
      totalVote: null,
      componentKey: 0,
    };
  },

  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore();

    return {
      userStore,
      toastStore,
      pageStore,
    };
  },

  computed: {
    sortOptions() {
      return this.poll.options.sort((a, b) => a.body - b.body);
    },
  },

  mounted() {
    this.getTotalVote();
  },

  // updated() {
  //   this.getTotalVote();
  // },

  methods: {
    deletePost() {
      this.$emit("deletePost", this.poll.id);
      axios
        .delete(`/api/posts/group/${this.poll.id}/delete/`)
        .then((res) => {
          console.log(res.data)
          setTimeout(() => {
            this.closeModal();
          }, 1000);
          this.toastStore.showToast(
            5000,
            "Cuộc thảo luận đã được xóa",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            5000,
            "Xóa cuộc thảo luận thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
    reportPost() {
      axios
        .post(`/api/posts/group/${this.poll.id}/report/`)
        .then((res) => {
          // console.log(res.data);
          this.toastStore.showToast(
            5000,
            "Đã báo cáo bài viết",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            5000,
            "Báo cáo bài viết thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
    getTotalVote() {
      this.totalVote = this.poll.options
        .map((option) => option.vote_by.length)
        .reduce((a, c) => a + c, 0);
        // console.log(this.totalVote)
    },
    forceRerender() {
      this.componentKey += 1;
    },
    voteOption(option) {
      this.forceRerender()
      axios
        .post(
          `/api/posts/group/${this.$route.params.id}/poll/option/${option.id}/vote/`
        )
        .then((res) => {
          if (res.data.message === "Remove vote") {
            this.totalVote -= 1;
            option.vote_by.length -= 1
          } else {
            this.totalVote += 1;
            option.vote_by.length += 1
          }
          // console.log(this.totalVote)
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  components: {
    RouterLink,
    DeletePostModal,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ShieldCheckIcon,
    TrashIcon,
    HeartLike,
    UserGroupIcon,
    GlobeAsiaAustraliaIcon,
    PollOption,
  },
});
</script>

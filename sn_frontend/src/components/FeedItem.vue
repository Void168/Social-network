<template>
  <div class="relative">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center space-x-6">
        <img :src="post.created_by.get_avatar" class="w-10 h-10 rounded-full" />

        <p>
          <strong>
            <RouterLink
              :to="{ name: 'profile', params: { id: post.created_by.id } }"
              >{{ post.created_by.name }}</RouterLink
            >
          </strong>
        </p>
      </div>

      <p class="text-gray-600">{{ post.created_at_formatted }} trước</p>
    </div>

    <p>{{ post.body }}</p>

    <div v-if="post.attachments?.length" class="mt-4">
      <img
        v-for="image in post.attachments"
        v-bind:key="image.id"
        :src="image.get_image"
        class="w-full mb-4 rounded-xl"
      />
    </div>

    <div class="my-6 flex justify-between">
      <div class="flex space-x-6">
        <div class="flex items-center space-x-2" @click="likePost(post.id)">
          <HeartLike class="w-6 h-6 text-rose-500" v-if="isLike" />
          <HeartIcon class="w-6 h-6" v-else />
          <span class="text-gray-500 text-xs"
            >{{ post.likes_count }} lượt thích</span
          >
        </div>

        <div class="flex items-center space-x-2">
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
              d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"
            />
          </svg>

          <RouterLink
            :to="{ name: 'postview', params: { id: post.id } }"
            class="text-gray-500 text-xs"
            >{{ post?.comments_count }} bình luận</RouterLink
          >
        </div>
      </div>
      <div
        class="absolute bg-emerald-400 right-0 bottom-0 shadow-lg rounded-lg ease-in duration-300"
      >
        <Menu as="div" class="relative inline-block text-left">
          <div>
            <MenuButton
              class="inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 hover:text-gray-900"
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
              <div class="py-1" v-if="userStore.user.id === post.created_by.id">
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
import { HeartIcon } from "@heroicons/vue/24/outline";
import { HeartIcon as HeartLike } from "@heroicons/vue/24/solid";
import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";
import DeletePostModal from "../components/modals/DeletePostModal.vue";

export default (await import("vue")).defineComponent({
  props: {
    post: Object,
  },

  data() {
    return {
      isOpen: false,
      isLike: false,
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

  mounted() {
    this.like();
  },

  methods: {
    like() {
      const is_like = this.post.likes
        .map((like) => like.created_by)
        .map((created_by) => created_by.id);
      if (is_like.includes(this.userStore.user.id)) {
        this.isLike = true;
      }
    },
    likePost(id) {
      axios
        .post(`/api/posts/${id}/like/`)
        .then((res) => {
          if (res.data.message == "like created") {
            this.post.likes_count += 1;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deletePost() {
      this.$emit("deletePost", this.post.id);

      axios
        .delete(`/api/posts/${this.post.id}/delete/`)
        .then((res) => {
          setTimeout(() => {
            this.closeModal();
          }, 1000);
          this.toastStore.showToast(
            5000,
            "Bài viết đã được xóa",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            5000,
            "Xóa bài viết thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
    reportPost() {
      axios
        .post(`/api/posts/${this.post.id}/report/`)
        .then((res) => {
          console.log(res.data);
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
  },
  components: {
    RouterLink,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ShieldCheckIcon,
    TrashIcon,
    HeartIcon,
    HeartLike,
    DeletePostModal,
  },
});
</script>

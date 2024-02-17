<template>
  <div class="relative">
    <div class="mb-2 flex items-center justify-between">
      <div class="flex items-center space-x-6 p-4">
        <img :src="post.created_by.get_avatar" class="w-12 h-12 rounded-full" />

        <div class="flex gap-1 items-center flex-wrap">
          <strong class="group">
            <RouterLink
              :to="{
                name: post.created_by.is_page ? 'page' : 'profile',
                params: { id: post.created_by.id },
              }"
              >{{ post.created_by.name }}</RouterLink
            >
            <TooltipProfileVue
              :user="post.created_by"
              class="hidden md:group-hover:block lg:left-[-150px] md:left-0"
            />
          </strong>
          <div v-if="post.post_to" class="flex gap-1">
            <p>cùng với</p>
            <strong class="group">
              <RouterLink
                :to="{ name: 'profile', params: { id: post.post_to.id } }"
                >{{ post.post_to.name }}</RouterLink
              >
              <TooltipProfileVue
                :user="post.post_to"
                class="hidden md:group-hover:block lg:left-[-150px] md:left-0"
              />
            </strong>
          </div>

          <span
            v-if="post.is_avatar_post === true"
            class="sm:text-base xs:text-sm"
            >đã thay đổi ảnh đại diện</span
          >
          <div class="md:hidden items-center gap-2 flex">
            <div class="relative group" v-if="!isAdjust">
              <PrivacyTooltip :post="post" />
              <GlobeAsiaAustraliaIcon
                class="w-5 h-5"
                v-if="
                  (post.is_private === false && post.only_me === false) ||
                  post.created_by.is_page
                "
              />
              <UserGroupIcon
                class="w-5 h-5"
                v-else-if="post.is_private === true && post.only_me === false"
              />
              <LockClosedIcon
                class="w-5 h-5"
                v-else-if="post.is_private === true && post.only_me === true"
              />
            </div>
            <PrivacySelector
              v-else
              @getOption="getOption"
              :privacies="privacies"
              v-model="privacy"
              class="w-full"
              :style="''"
            />
            <div class="relative group md:hidden">
              <p
                class="text-gray-600 dark:text-neutral-200 sm:text-base xs:text-sm group-hover:underline"
              >
                {{ post.created_at_formatted }} trước
              </p>
              <CreatedAtTooltip :post="post" />
            </div>
          </div>
        </div>
      </div>
      <div class="p-4 md:flex items-center gap-2 hidden">
        <div class="relative group" v-if="!isAdjust">
          <PrivacyTooltip :post="post" />
          <GlobeAsiaAustraliaIcon
            class="w-5 h-5"
            v-if="
              (post.is_private === false && post.only_me === false) ||
              post.created_by.is_page
            "
          />
          <UserGroupIcon
            class="w-5 h-5"
            v-else-if="post.is_private === true && post.only_me === false"
          />
          <LockClosedIcon
            class="w-5 h-5"
            v-else-if="post.is_private === true && post.only_me === true"
          />
        </div>
        <PrivacySelector
          v-else
          @getOption="getOption"
          :privacies="privacies"
          v-model="privacy"
          class="w-full"
          :style="''"
        />
        <div class="relative group w-full">
          <RouterLink :to="{ name: 'postview', params: { id: post.id } }">
            <p
              class="text-gray-600 dark:text-neutral-200 md:block hidden group-hover:underline"
            >
              {{ post.created_at_formatted }} trước
            </p>
          </RouterLink>
          <CreatedAtTooltip :post="post" />
        </div>
      </div>
    </div>
    <textarea
      v-if="isAdjust"
      type="text"
      class="form-control resize-none w-full px-4 text-lg"
      rows="5"
      v-model="post.body"
    ></textarea>
    <p class="px-4 text-lg" v-else>{{ post.body }}</p>

    <div
      v-if="post.attachments?.length && post.is_avatar_post"
      class="mt-4 flex justify-center relative sm:h-[400px] xm:h-[350px] xs:h-[300px]"
    >
      <div class="w-full">
        <img
          :src="post.created_by.get_cover_image"
          alt="cover_image"
          class="max-h-[300px] w-full rounded-none"
        />
      </div>

      <img
        v-for="image in post.attachments"
        v-bind:key="image.id"
        :src="image.get_image"
        class="absolute top-5 mb-4 rounded-full md:w-96 md:h-96 xm:w-80 xm:h-80 xs:w-64 xs:h-64 shadow-md ring-8 ring-white dark:ring-slate-700"
        alt="avatar"
      />
    </div>

    <div v-else class="mt-4 px-4">
      <img
        v-for="image in post.attachments"
        v-bind:key="image.id"
        :src="image.get_image"
        class="w-full mb-4 rounded-xl"
      />
    </div>

    <div class="p-4 my-6 flex justify-between" v-if="!isAdjust">
      <div class="flex space-x-6">
        <div class="flex items-center space-x-2">
          <HeartLike
            class="w-6 h-6 text-rose-500 cursor-pointer"
            v-if="!pageStore.pageId && checkUserLike"
          />
          <HeartLike
            class="w-6 h-6 text-rose-500 cursor-pointer"
            v-else-if="pageStore.pageId && checkPageLike"
          />
          <HeartLike
            class="w-6 h-6 text-rose-500 cursor-pointer"
            v-else-if="isLike"
          />
          <HeartLike
            v-else
            @click="likePost(post.id)"
            class="w-6 h-6 cursor-pointer text-gray-400 hover:text-rose-500 transition-colors duration-75"
          />
          <span class="text-gray-500 text-xs dark:text-neutral-200"
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
            :to="{
              name: post.created_by.is_page ? 'pagepostview' : 'postview',
              params: { id: post.id },
            }"
            class="text-gray-500 text-xs dark:text-neutral-200"
            >{{ post?.comments_count }} bình luận</RouterLink
          >
        </div>
      </div>
      <div class="absolute right-4 shadow-lg rounded-lg ease-in duration-300">
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
                  userStore.user.id === post.created_by.id ||
                  pageStore.pageId === post.created_by.id
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
                <MenuItem v-slot="{ active }" @click="openPostAdjustment">
                  <div
                    :class="[
                      active ? 'bg-gray-100 text-gray-700' : 'text-gray-700',
                      'block px-4 py-2 text-sm cursor-pointer',
                    ]"
                  >
                    <span class="flex items-center gap-3"
                      ><AdjustmentsHorizontalIcon class="w-5 h-5" />Chỉnh sửa
                      bài viết</span
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
    <div class="mt-4 flex justify-end gap-3 p-4" v-else>
      <button
        type="button"
        class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
        @click="closePostAdjustment"
      >
        Hủy
      </button>
      <button
        type="button"
        class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
        @click="submitForm"
      >
        Đồng ý
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { RouterLink } from "vue-router";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  ShieldCheckIcon,
  TrashIcon,
  AdjustmentsHorizontalIcon,
} from "@heroicons/vue/24/solid";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";
import { HeartIcon as HeartLike } from "@heroicons/vue/24/solid";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { usePageStore } from "../../../stores/page";
import DeletePostModal from "../../modals/post/DeletePostModal.vue";
import CreatedAtTooltip from "./Tooltip/CreatedAtTooltip.vue";
import PrivacyTooltip from "./Tooltip/PrivacyTooltip.vue";
import TooltipProfileVue from "../profile/TooltipProfile.vue";
import PrivacySelector from "../../dropdown/PrivacySelector.vue";

export default (await import("vue")).defineComponent({
  props: {
    post: Object,
  },

  data() {
    return {
      isOpen: false,
      isLike: false,
      isAdjust: false,
      privacies: [
        { name: "Công khai" },
        { name: "Bạn bè" },
        { name: "Chỉ mình tôi" },
      ],
      privacy: {
        name: "",
      },
      is_private: this.post.is_private,
      only_me: this.post.only_me,
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
    checkUserLike() {
      return this.post?.likes
        ?.map((like) => like?.created_by?.id)
        .includes(this.userStore.user.id);
    },
    checkPageLike() {
      return this.post?.page_likes
        ?.map((like) => like?.created_by?.id)
        .includes(this.pageStore.pageId);
    },
  },

  beforeMount() {
    this.like();
    this.getPostsPrivacy();
  },

  methods: {
    getPostsPrivacy() {
      if (!this.is_private && !this.only_me) {
        this.privacy.name === "Công khai";
      }
      if (this.is_private && !this.only_me) {
        this.privacy.name === "Bạn bè";
      } else {
        this.privacy.name === "Chỉ mình tôi";
      }
    },
    like() {
      const is_like = this.post.likes
        .map((like) => like.created_by)
        .map((created_by) => created_by.id);
      if (is_like.includes(this.userStore.user.id)) {
        this.isLike = true;
      }
    },
    likePost(id) {
      if (!this.post.created_by.is_page) {
        axios
          .post(`/api/posts/${id}/like/`)
          .then((res) => {
            if (res.data.message !== "post already liked") {
              this.post.likes_count += 1;
              this.isLike = true;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
      if (this.post.created_by.is_page && this.pageStore.pageId) {
        axios
          .post(`/api/posts/page/${this.pageStore.pageId}/${id}/like-by-page/`)
          .then((res) => {
            if (res.data.message !== "post already liked") {
              this.post.likes_count += 1;
              this.isLike = true;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .post(`/api/posts/${id}/like-by-user/`)
          .then((res) => {
            if (res.data.message !== "post already liked") {
              this.post.likes_count += 1;
              this.isLike = true;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    deletePost() {
      this.$emit("deletePost", this.post.id);

      if (!this.post.created_by.is_page) {
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
      } else {
        axios
          .delete(
            `/api/posts/page/${this.pageStore.pageId}/${this.post.id}/delete/`
          )
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
      }
    },
    reportPost() {
      axios
        .post(`/api/posts/${this.post.id}/report/`)
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
    openPostAdjustment() {
      this.isAdjust = true;
    },
    closePostAdjustment() {
      this.isAdjust = false;
    },
    getOption() {
      if (this.privacy.name === "Công khai") {
        this.is_private = false;
        this.only_me = false;
      }
      if (this.privacy.name === "Bạn bè") {
        this.is_private = true;
        this.only_me = false;
      }
      if (this.privacy.name === "Chỉ mình tôi") {
        this.is_private = true;
        this.only_me = true;
      }
    },
    submitForm() {
      if (!this.privacy.name) {
        axios
          .post(`/api/posts/${this.post.id}/update/`, {
            body: this.post.body,
          })
          .then((res) => {
            if (res.data) {
              this.body = res.data.body;
              this.closePostAdjustment();
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .post(`/api/posts/${this.post.id}/update/`, {
            body: this.post.body,
            is_private: this.is_private,
            only_me: this.only_me,
          })
          .then((res) => {
            if (res.data) {
              this.body = res.data.body;
              this.is_private = res.data.is_private;
              this.only_me = res.data.only_me;
              this.closePostAdjustment();
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
  components: {
    RouterLink,
    DeletePostModal,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    PrivacySelector,
    ShieldCheckIcon,
    AdjustmentsHorizontalIcon,
    TrashIcon,
    HeartLike,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
    CreatedAtTooltip,
    PrivacyTooltip,
    TooltipProfileVue,
  },
});
</script>

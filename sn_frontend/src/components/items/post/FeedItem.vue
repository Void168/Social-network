<template>
  <div class="relative">
    <div class="mb-2 flex items-center justify-between">
      <div class="flex items-center space-x-6 p-4">
        <img
          loading="lazy"
          :src="post?.created_by?.get_avatar"
          class="w-12 h-12 rounded-full"
        />

        <div class="flex gap-1 items-center flex-wrap">
          <strong class="group">
            <RouterLink
              :to="{
                name: post?.created_by?.is_page ? 'page' : 'profile',
                params: { id: post?.created_by?.id },
              }"
              >{{ post?.created_by?.name }}</RouterLink
            >
            <TooltipProfileVue
              :user="post?.created_by"
              class="hidden md:group-hover:block lg:left-[-150px] md:left-0"
            />
          </strong>
          <div v-if="post?.post_to" class="flex gap-1">
            <p>cùng với</p>
            <strong class="group">
              <RouterLink
                :to="{ name: 'profile', params: { id: post?.post_to?.id } }"
                >{{ post?.post_to?.name }}</RouterLink
              >
              <TooltipProfileVue
                :user="post?.post_to"
                class="hidden md:group-hover:block lg:left-[-150px] md:left-0"
              />
            </strong>
          </div>

          <span v-if="post?.is_avatar_post" class="sm:text-base xs:text-sm vs:text-xs">{{
            post?.created_by?.is_page
              ? "đã thay đổi ảnh đại diện của họ"
              : "đã thay đổi ảnh đại diện"
          }}</span>
          <div class="md:hidden items-center gap-2 flex">
            <div class="relative group" v-if="!isAdjust">
              <PrivacyTooltip :post="post" />
              <GlobeAsiaAustraliaIcon
                class="w-5 h-5"
                v-if="
                  (post?.is_private === false && post?.only_me === false) ||
                  post?.created_by?.is_page
                "
              />
              <UserGroupIcon
                class="w-5 h-5"
                v-else-if="post?.is_private && post?.only_me"
              />
              <LockClosedIcon
                class="w-5 h-5"
                v-else-if="post?.is_private === true && post?.only_me === true"
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
                class="text-gray-600 dark:text-neutral-200 sm:text-base xs:text-sm vs:text-xs group-hover:underline"
              >
                {{ post?.created_at_formatted }} trước
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
              (post?.is_private === false && post?.only_me === false) ||
              post?.created_by?.is_page
            "
          />
          <UserGroupIcon
            class="w-5 h-5"
            v-else-if="post?.is_private === true && post?.only_me === false"
          />
          <LockClosedIcon
            class="w-5 h-5"
            v-else-if="post?.is_private === true && post?.only_me === true"
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
              {{ post?.created_at_formatted }} trước
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
      rows="3"
      v-model="post.body"
    ></textarea>
    <p class="px-4 sm:text-lg xs:text-base vs:text-sm" v-else>{{ post?.body }}</p>

    <ImagePostModal
      :show="isImagePostOpen"
      @closeModal="closeImagePostModal"
      :imageId="post?.id"
      :post="post"
    />
    <div
      v-if="post?.attachments?.length && post?.is_avatar_post"
      @click="openImagePostModal"
      class="mt-4 flex justify-center relative sm:h-[400px] xm:h-[350px] xs:h-[250px] cursor-pointer"
    >
      <div class="w-full">
        <img
          loading="lazy"
          :src="post?.created_by?.get_cover_image"
          alt="cover_image"
          class="max-h-[300px] w-full rounded-none"
        />
      </div>

      <img
        loading="lazy"
        v-for="image in post?.attachments"
        v-bind:key="image?.id"
        :src="image?.get_image"
        class="absolute top-5 mb-4 rounded-full md:w-96 md:h-96 xm:w-80 xm:h-80 xs:w-64 xs:h-64 vs:w-40 vs:h-40 shadow-md ring-8 ring-white dark:ring-slate-700"
        alt="avatar"
      />
    </div>

    <div v-else class="mt-4 px-4 cursor-pointer" @click="openImagePostModal">
      <img
        loading="lazy"
        v-for="image in post?.attachments"
        v-bind:key="image?.id"
        :src="image?.get_image"
        class="w-full mb-4 rounded-xl"
      />
    </div>

    <div
    v-if="post.post"
      class="mx-4 border dark:border-slate-500 rounded-lg p-4 dark:text-neutral-200 space-y-2 mb-4"
    >
      <div class="flex gap-2 items-center">
        <img :src="post.post.created_by.get_avatar" class="w-8 h-8 rounded-full" />
        <div>
          <h5 class="font-semibold text-sm">
            {{ post.post.created_by.name }}
          </h5>
          <div
            class="dark:text-neutral-300 text-xs text-neutral-400 flex items-center gap-1"
          >
            <p>{{ post.post.created_at_formatted }} &middot;</p>
            <GlobeAsiaAustraliaIcon
              v-if="!post.post.only_me && !post.post.is_private"
              class="w-4 h-4"
            />
            <UserGroupIcon
              v-else-if="!post.post.only_me && post.post.is_private"
              class="w-4 h-4"
            />
            <LockClosedIcon
              v-else-if="post.post.only_me && post.post.is_private"
              class="w-4 h-4"
            />
          </div>
        </div>
      </div>
      <h5 class="xs:text-base vs:text-sm">
        {{ post.post.body }}
      </h5>
      <div v-if="post.attachments.length">
        <img :src="post.attachments[0].get_image" />
      </div>
    </div>

    <div class="p-4 xm:my-6 mt-16 xm:mt-0 flex justify-between" v-if="!isAdjust">
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
            @click="likePost(post?.id)"
            class="w-6 h-6 cursor-pointer text-gray-400 hover:text-rose-500 transition-colors duration-75"
          />
          <span class="text-gray-500 text-xs dark:text-neutral-200"
            >{{ post?.likes_count }}</span
          >
          <span class="text-gray-500 text-xs dark:text-neutral-200 xm:inline vs:hidden">lượt thích</span>
        </div>

        <div class="flex items-center space-x-2">
          <ChatBubbleOvalLeftIcon class="w-6 h-6" />

          <RouterLink
            :to="{
              name: post?.created_by?.is_page ? 'pagepostview' : 'postview',
              params: { id: post?.id },
            }"
            class="text-gray-500 text-xs dark:text-neutral-200"
            >{{ post?.comments_count }} <span class="text-gray-500 text-xs dark:text-neutral-200 xm:inline vs:hidden">bình luận</span></RouterLink
          >
        </div>
        <div
          class="flex items-center space-x-2 cursor-pointer"
          @click="openShareModal"
        >
          <ShareIcon class="w-6 h-6" />
          <span class="text-gray-500 text-xs dark:text-neutral-200 xm:inline vs:hidden">Chia sẻ</span>
          <!-- <h5 class="text-gray-500 text-xs dark:text-neutral-200">Chia sẻ</h5> -->
          <SharePostModal
            :show="isShareOpen"
            @closeShareModal="closeShareModal"
            :post="post"
          />
        </div>
      </div>
      <div class="absolute right-4 sm:bottom-4 vs:top-4 vs:bottom-auto sm:top-auto shadow-lg rounded-lg ease-in duration-300">
        <Menu as="div" class="relative inline-block text-left">
          <div>
            <MenuButton
              class="inline-flex w-full justify-center rounded-md bg-white md:px-3 md:py-2 px-0 py-0 text-gray-900 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 hover:text-gray-900"
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
                  userStore?.user.id === post?.created_by?.id ||
                  pageStore?.pageId === post?.created_by?.id
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
                <MenuItem v-slot="{ active }" @click="openShareModal">
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
    <div class="xm:mt-4 mt-12 flex justify-end gap-3 p-4" v-else>
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
  ChatBubbleOvalLeftIcon,
  ShareIcon,
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
import ImagePostModal from "../../modals/post/ImagePostModal.vue";
import SharePostModal from "../../modals/post/SharePostModal.vue";

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
      isImagePostOpen: false,
      isShareOpen: false,
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
      const is_like = this.post?.likes
        ?.map((like) => like?.created_by)
        .map((created_by) => created_by?.id);
      if (is_like?.includes(this.userStore.user.id)) {
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
    openShareModal() {
      this.isShareOpen = true;
    },
    closeShareModal() {
      this.isShareOpen = false;
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
    openImagePostModal() {
      this.isImagePostOpen = true;
    },
    closeImagePostModal() {
      this.isImagePostOpen = false;
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
    ImagePostModal,
    ShareIcon,
    ChatBubbleOvalLeftIcon,
    SharePostModal,
  },
});
</script>

<template>
  <div class="max-w-7xl grid grid-cols-3 xl:mx-auto md:mx-8 mx-2 gap-4">
    <CoverImage
      class="col-span-3 md:max-h-[400px] sm:max-h-[300px] xs:max-h-[200px] lg:max-h-max"
      :page="page"
    />
    <div class="col-span-3 grid grid-cols-3 gap-4 relative">
      <div
        class="col-span-3 flex lg:justify-between justify-center items-center px-4 py-2 gap-4 lg:text-lg md:text-base xm:text-sm xs:text-xs font-semibold dark:text-neutral-200"
      >
        <div class="flex gap-6">
          <RouterLink :to="{ name: 'page', params: { id: page.id } }"
            >Bài viết</RouterLink
          >
          <RouterLink :to="{ name: 'page', params: { id: page.id } }"
            >Giới thiệu</RouterLink
          >
          <RouterLink :to="{ name: 'pageusers', params: { id: page.id } }"
            >Người theo dõi</RouterLink
          >
          <RouterLink :to="{ name: 'photos', params: { id: page.id } }"
            >Ảnh</RouterLink
          >
          <span>Video</span>
          <span>Xem thêm</span>
        </div>
        <div class="flex items-start gap-2">
          <button
            @click="openContactModal"
            class="dark:text-neutral-200 bg-slate-200 dark:bg-slate-800 md:px-4 md:py-2 p-1 shadow-md rounded-md hover:bg-slate-300 dark:hover:bg-slate-900 transition"
          >
            <span class="md:block hidden">Thông tin liên lạc</span>
            <PencilSquareIcon class="w-6 md:hidden" />
          </button>
          <div class="flex flex-col gap-3 items-center">
            <button
              v-if="!checkInLikes && !isLike && !pageStore.pageId"
              class="btn flex gap-1 items-center"
              @click="likePage"
            >
              <HandThumbUpIcon class="w-6" />
              <span>Thích</span>
            </button>
            <button
              v-else-if="!checkInPageLikes && !isLike && pageStore.pageId && page.id !== pageStore.pageId"
              class="btn flex gap-1 items-center"
              @click="likePage"
            >
              <HandThumbUpIcon class="w-6" />
              <span>Thích</span>
            </button>
            <PageOptionsDropdown
              v-else-if="isLike && !pageStore.pageId || checkInLikes && !pageStore.pageId"
              :followers="page.followers"
              :likes="page.likes"
              @followPage="followPage"
              @unfollowPage="unfollowPage"
              @dislikePage="dislikePage"
            />
            <PageOptionsDropdown
              v-else-if="isLike && page.is_page && page.id !== pageStore.pageId || checkInPageLikes && page.is_page && page.id !== pageStore.pageId"
              :followers="pageFollowers"
              :likes="pageLikes"
              @followPage="followPage"
              @unfollowPage="unfollowPage"
              @dislikePage="dislikePage"
            />
            <button
              v-if="page.id !== pageStore.pageId && !pageStore.pageId"
              @click="sendDirectMessage"
              class="bg-violet-400 hover:bg-violet-600 btn w-full"
            >
              Nhắn tin
            </button>
          </div>

          <ContactModal
            :show="contactIsOpen"
            @closeContactModal="closeContactModal"
          />
        </div>
      </div>
      <hr class="col-span-3" />
      <div class="relative main-left top-0 lg:col-span-1 col-span-4">
        <div class="h-[88px] frame"></div>
        <div
          class="px-4 pb-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col rounded-lg shadow-md overflow-hidden lg:w-full w-[90%] mx-auto"
        >
          <div class="flex justify-center items-center flex-col">
            <div
              class="icon relative w-[200px] h-[100px] bg-gray-100 dark:bg-slate-700 rounded-bl-[100px] rounded-br-[100px] before:content-[''] after:content-[''] before:absolute after:absolute before:top-0 after:top-0 before:left-[-50px] before:w-[55px] before:h-[35px] before:bg-transparent before:rounded-tr-[50px] before:shadow-[20px_-20px_0_20px_rgba(243,244,246,1)] after:right-[-50px] after:w-[55px] after:h-[35px] after:bg-transparent after:rounded-tl-[50px] after:shadow-[-20px_-20px_0_20px_rgba(243,244,246,1)] before:dark:shadow-[20px_-20px_0_20px_rgba(51,65,85,1)] after:dark:shadow-[-20px_-20px_0_20px_rgba(51,65,85,1)]"
            >
              <span
                v-if="pageStore.pageId === page.id"
                @click="openAvatarModal"
                class="mb-6 rounded-full w-8 h-8 shadow-xl absolute flex justify-center items-center top-16 right-6 z-10 bg-neutral-200 dark:bg-slate-700 hover:ring-2 hover:ring-slate-300 dark:hover:ring-slate-500 transition cursor-pointer"
              >
                <CameraIcon
                  class="dark:text-neutral-200 w-5 h-5 dark:hover:text-neutral-300 hover:text-slate-700 transition"
                />
              </span>
            </div>
            <img
              :src="page.get_avatar"
              alt=""
              class="rounded-full w-44 h-44 shadow-xl absolute top-2"
            />
            <AvatarModal
              v-if="pageStore.pageId === page.id"
              :show="avatarIsOpen"
              @closeAvatarModal="closeAvatarModal"
            />

            <p>
              <strong class="text-2xl">{{ page.name }}</strong>
            </p>
            <p class="mt-6 font-semibold text-lg">{{ page.biography }}</p>
          </div>
          <div class="mt-6 flex space-x-8">
            <ul class="flex flex-col !justify-start space-y-4 text-sm">
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <div class="flex gap-1 items-center">
                  <ExclamationCircleIcon class="h-6 w-6" />
                  <span>Trang</span>
                  <span>&middot;</span>
                  <span>{{ page.page_type }}</span>
                </div>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2 font-semibold"
              >
                <UserGroupIcon class="h-6 w-6" />
                <span>{{ page.followers_count }} người theo dõi</span>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2 font-semibold"
              >
                <HandThumbUpIcon class="h-6 w-6" />
                <span>{{ page.likes_count }} lượt thích</span>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <EnvelopeIcon class="h-6 w-6" />
                <span>{{ page.email }}</span>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <ClipboardDocumentListIcon class="h-6 w-6" />
                {{ page.posts_count }} bài đăng
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
                v-if="page.location"
              >
                <MapPinIcon class="w-6 h-6 dark:text-neutral-200" />
                <p>{{ page.location }}</p>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-300 flex items-center gap-2"
              >
                <ClockIcon class="w-6 h-6 dark:text-neutral-200" />
                <p>
                  Đã tạo vào Tháng {{ page?.created_at?.slice(5, 7) }} năm
                  {{ page?.created_at?.slice(0, 4) }}
                </p>
              </li>
            </ul>
          </div>
          <RouterLink
            to="/page/edit"
            class="flex justify-center items-center w-full"
            v-if="checkCurrentUserInPage && pageStore.pageId"
          >
            <button class="mt-4 btn lg:min-w-min xs:min-w-full">
              Chỉnh sửa chi tiết
            </button>
          </RouterLink>
        </div>
        <div class="bg-white dark:bg-slate-600 dark:text-neutral-200 my-4 p-4">
          <div class="flex justify-between items-center mb-4">
            <p class="font-bold text-2xl">Ảnh</p>
            <RouterLink
              :to="{ name: 'photos', params: { id: userStore.user.id } }"
            >
              <p class="text-lg hover:underline cursor-pointer">
                Xem tất cả ảnh
              </p>
            </RouterLink>
          </div>
          <div class="grid grid-cols-3 gap-1">
            <div v-for="image in images" v-bind:key="image.id">
              <ImageShowcase v-bind:post="image" />
            </div>
          </div>
        </div>
      </div>

      <div
        class="main-center lg:col-span-2 col-span-4 space-y-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 p-4"
        id="profile-frame"
      >
        <div
          v-if="checkCurrentUserInPage && pageStore.pageId"
          class="p-4 bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
        >
          <PostForm :user="user" :posts="posts" :page="page" />
        </div>
        <p class="font-semibold text-2xl">Bài viết của {{ page.name }}</p>
        <div v-if="posts?.length">
          <div
            class="bg-white border border-gray-200 rounded-lg mt-4 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200"
            v-for="post in posts"
            v-bind:key="post.id"
          >
            <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
          </div>
          <SkeletonLoadingPostVue
            v-show="!loadMore"
            v-if="posts.length !== postsList.length"
          />
        </div>
        <p v-else class="text-center text-lg">
          {{ user.name }} Chưa có bài viết nào
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PostForm from "../../components/forms/PostForm.vue";
import FeedItem from "../../components/items/post/FeedItem.vue";
import CoverImage from "../../components/CoverImage.vue";
import ImageShowcase from "../../components/items/profile/ImageShowcase.vue";
import PageOptionsDropdown from "../../components/dropdown/PageOptionsDropdown.vue";
import SkeletonLoadingPostVue from "../../components/loadings/SkeletonLoadingPost.vue";

import ContactModal from "../../components/modals/profile/ContactModal.vue";
import AvatarModal from "../../components/modals/profile/AvatarModal.vue";
import UnfollowedModal from "../../components/modals/profile/UnfollowedModal.vue";

import {
  ClockIcon,
  ClipboardDocumentListIcon,
  UserGroupIcon,
  MapPinIcon,
  CameraIcon,
  PencilSquareIcon,
  HandThumbUpIcon,
  ExclamationCircleIcon,
  EnvelopeIcon,
} from "@heroicons/vue/24/solid";

import { RouterLink } from "vue-router";

import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { usePageStore } from "../../stores/page";

export default {
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
  name: "FeedView",
  components: {
    FeedItem,
    RouterLink,
    PostForm,
    CoverImage,
    SkeletonLoadingPostVue,
    ImageShowcase,
    UnfollowedModal,
    PageOptionsDropdown,
    EnvelopeIcon,
    ClockIcon,
    ClipboardDocumentListIcon,
    MapPinIcon,
    UserGroupIcon,
    CameraIcon,
    PencilSquareIcon,
    HandThumbUpIcon,
    ExclamationCircleIcon,
    ContactModal,
    AvatarModal,
  },

  data() {
    return {
      posts: [],
      postsList: [],
      user: {
        id: null,
      },
      page: {},
      pageLikes: [],
      pageFollowers: [],
      PostToShow: 5,
      loadMore: false,
      images: [],
      contactIsOpen: false,
      avatarIsOpen: false,
      isLike: false,
    };
  },

  computed: {
    checkCurrentUserInPage() {
      return this.pageStore.pagesList
        .map((page) => page.id)
        .includes(this.$route.params.id);
    },
    checkInLikes() {
      return this.page?.likes
        ?.map((user) => user.id)
        .includes(this.userStore.user.id);
    },
    checkInPageLikes() {
        return this.pageLikes
          ?.map((page) => page.id)
          .includes(this.pageStore.pageId);
    }
  },

  beforeMount() {
    this.getPageInfo();
  },

  mounted() {
    this.getFeed();
    this.getImages();
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getFeed();
        this.getPageInfo();
        this.getImages();
      },
      deep: true,
      immediate: true,
    },
  },

  // beforeUpdate(){
  //   this.getPageInfo()
  // },

  methods: {
    async getPageInfo() {
      await axios
        .get(`/api/page/get-page/${this.$route.params.id}`)
        .then((res) => {
          this.page = res.data.data;
          this.pageLikes = res.data.other_page_likes
          this.pageFollowers = res.data.other_page_followers
        })
        .catch((error) => console.log(error));
    },
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },
    async getImages() {
      await axios
        .get(`/api/posts/page/${this.$route.params.id}/attachments/`)
        .then((res) => {
          this.images = res.data;
          // console.log(res.data)
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    sendDirectMessage() {
      axios
        .get(`/api/chat/${this.userStore.user.id}/get-or-create/page/${this.$route.params.id}/`)
        .then((res) => {
          this.$router.push("/chat");
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    async getFeed() {
      await axios
        .get(`/api/posts/page/profile/${this.$route.params.id}/`)
        .then((res) => {
          this.postsList = res.data;
          this.posts = res.data.slice(0, this.PostToShow);

          // console.log(res.data);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    infinateScroll() {
      const frame = document.getElementById("profile-frame");
      let height = frame.scrollHeight;
      let scrollY = window.scrollY;
      if (height < scrollY + 800) {
        setTimeout(() => {
          this.loadMore = true;
        }, 1000);
        if (this.loadMore === true) {
          const newPosts = this.postsList.slice(
            this.posts.length,
            this.posts.length + this.PostToShow
          );
          this.posts.push(...newPosts);
        }
      } else {
        this.loadMore = false;
      }
    },

    openContactModal() {
      this.contactIsOpen = true;
    },
    closeContactModal() {
      this.contactIsOpen = false;
    },

    openAvatarModal() {
      this.avatarIsOpen = true;
    },
    closeAvatarModal() {
      this.avatarIsOpen = false;
    },

    likePage() {
      if (!this.pageStore.pageId) {
        axios
          .post(`/api/page/${this.$route.params.id}/like/`)
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã thích ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
              this.isLike = true;
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .post(
            `/api/page/${this.pageStore.pageId}/like/${this.$route.params.id}/`
          )
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã thích ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
              this.isLike = true;
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    followPage() {
      if(!this.pageStore.pageId){
        axios.post(`/api/page/${this.$route.params.id}/follow/`).then((res) => {
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã theo dõi ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      } else {
        axios.post(`/api/page/${this.pageStore.pageId}/follow/page/${this.$route.params.id}/`).then((res) => {
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã theo dõi ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      }
    },

    dislikePage() {
      if(!this.pageStore.pageId){
        axios.post(`/api/page/${this.$route.params.id}/dislike/`).then((res) => {
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã bỏ thích ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      } else {
        axios.post(`/api/page/${this.pageStore.pageId}/dislike/page/${this.$route.params.id}/`).then((res) => {
          console.log(res.data)
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã bỏ thích ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      }
    },

    unfollowPage() {
      if(!this.pageStore.pageId){
        axios.post(`/api/page/${this.$route.params.id}/unfollow/`).then((res) => {
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã bỏ theo dõi ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      } else {
        axios.post(`/api/page/${this.pageStore.pageId}/unfollow/page/${this.$route.params.id}/`).then((res) => {
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã bỏ theo dõi ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      }
    },
  },
};
</script>

<style scoped>
.frame {
  border: none !important;
  box-shadow: none !important;
  border-radius: 0% !important;
}

.router-link-active {
  --tw-text-opacity: 1;
  color: rgb(16 185 129 / var(--tw-text-opacity));
  border-width: 2px;
  border-left: 2px;
  border-top: 2px;
  border-right: 2px;
  border-color: rgb(16 185 129 / var(--tw-text-opacity));
}
</style>

<template>
  <div class="col-span-3 grid grid-cols-3 gap-4 relative">
    <div class="col-span-1 lg:block hidden"></div>
    <div class="col-span-3 grid grid-cols-3 gap-4 relative">
      <div class="main-left top-0 lg:col-span-1 col-span-4">
        <div class="h-20 frame !shadow-none"></div>
        <div
          class="px-4 pb-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col justify-center items-center rounded-lg shadow-md overflow-hidden lg:w-full w-[90%] mx-auto"
        >
          <div
            class="icon relative w-[200px] h-[100px] bg-gray-200 dark:bg-slate-700 rounded-bl-[100px] rounded-br-[100px] before:content-[''] after:content-[''] before:absolute after:absolute before:top-0 after:top-0 before:left-[-50px] before:w-[55px] before:h-[35px] before:bg-transparent before:rounded-tr-[50px] before:shadow-[20px_-20px_0_20px_rgba(229,231,235,1)] after:right-[-50px] after:w-[55px] after:h-[35px] after:bg-transparent after:rounded-tl-[50px] after:shadow-[-20px_-20px_0_20px_rgba(229,231,235,1)] before:dark:shadow-[20px_-20px_0_20px_rgba(51,65,85,1)] after:dark:shadow-[-20px_-20px_0_20px_rgba(51,65,85,1)]"
          >
            <span
              @click="openAvatarModal"
              class="mb-6 rounded-full w-8 h-8 shadow-xl absolute flex justify-center items-center top-16 right-6 z-10 bg-neutral-200 dark:bg-slate-700 hover:ring-2 hover:ring-slate-300 dark:hover:ring-slate-500 transition cursor-pointer"
            >
              <CameraIcon
                class="dark:text-neutral-200 w-5 h-5 dark:hover:text-neutral-300 hover:text-slate-700 transition"
              />
            </span>
          </div>
          <img
          loading="lazy"
            :src="user?.get_avatar"
            alt=""
            class="mb-6 rounded-full w-44 h-44 shadow-xl absolute top-0"
          />
          <AvatarModal
            :show="avatarIsOpen"
            @closeAvatarModal="closeAvatarModal"
          />

          <p>
            <strong class="text-2xl">{{ user?.name }}</strong>
          </p>
          <p v-if="user.nickname" class="text-xl">({{ user?.nickname }})</p>
          <p class="mt-6 font-semibold text-lg">{{ user.biography }}</p>
          <div class="mt-6 flex space-x-8">
            <ul class="flex flex-col space-y-4 text-lg">
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2"
              >
                <UserGroupIcon class="h-6 w-6" />
                {{ user.friends_count }} người bạn
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2"
              >
                <ClipboardDocumentListIcon class="h-6 w-6" />
                {{ user.posts_count }} bài đăng
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2"
                v-if="user.relationship_status"
              >
                <HeartIcon class="h-6 w-6" />
                <h2>{{ user.relationship_status }} với</h2>
                <strong
                  v-if="partnerId != '' && partnerId != 'null'"
                  @click="toPartner"
                  class="cursor-pointer"
                >
                  {{ partner?.user?.name }}
                </strong>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2"
                v-if="user.hometown"
              >
                <MapPinIcon class="w-6 h-6 dark:text-neutral-200" />
                <p>Đến từ {{ user.hometown }}</p>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2"
                v-if="user.hometown"
              >
                <HomeIcon class="w-6 h-6 dark:text-neutral-200" />
                <p>Sống tại {{ user.living_city }}</p>
              </li>
              <li
                class="text-gray-500 dark:text-neutral-200 flex items-center gap-2"
              >
                <ClockIcon class="w-6 h-6 dark:text-neutral-200" />
                <p>
                  Tham gia vào Tháng {{ user?.date_joined?.slice(5, 7) }} năm
                  {{ user?.date_joined?.slice(0, 4) }}
                </p>
              </li>
            </ul>
          </div>
          <RouterLink
            v-if="user.id === userStore.user.id"
            to="/profile/edit"
            class="md:max-w-max xs:w-full"
          >
            <button class="mt-4 btn w-full">Chỉnh sửa chi tiết</button>
          </RouterLink>
          <button
            v-if="userStore.user.id !== user.id"
            @click="sendDirectMessage"
            class="mt-6 bg-violet-400 hover:bg-violet-600 btn"
          >
            Nhắn tin
          </button>
        </div>
        <div
          class="lg:sticky !shadow-none"
          :style="{ top: `${toastStore.navbarHeight}px` }"
        >
          <div
            class="bg-white dark:bg-slate-600 dark:text-neutral-200 my-4 p-4 shadow-md rounded-lg"
          >
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
          <div
            class="shadow-md bg-white dark:bg-slate-600 dark:text-neutral-200 my-4 p-4 rounded-lg"
          >
            <div class="flex justify-between items-center mb-4">
              <div>
                <h1 class="font-bold text-2xl">Bạn bè</h1>
                <h3>{{ friends.length }} người bạn</h3>
              </div>
              <RouterLink
                :to="{ name: 'friends', params: { id: userStore.user.id } }"
              >
                <p class="text-lg hover:underline cursor-pointer">
                  Xem tất cả bạn bè
                </p>
              </RouterLink>
            </div>
            <div class="grid grid-cols-3 gap-1">
              <div v-for="friend in friendShowcase" :key="friend.id">
                <Friend :friend="friend" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="main-center lg:col-span-2 col-span-4 space-y-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 p-4"
        id="profile-frame"
      >
        <div
          v-if="userStore.user.id === user.id"
          class="p-4 bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
        >
          <PostForm v-bind:user="user" v-bind:posts="posts" @getNewPost="getNewPost"/>
        </div>
        <div
          v-else-if="friends.map((fr) => fr.id).includes(userStore.user.id)"
          class="p-4 bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
        >
          <div class="text-lg px-4">Viết gì đó cho {{ user.name }}</div>
          <PostToForm v-bind:user="user" v-bind:posts="posts" />
        </div>
        <div
          v-if="relationshipRequest.length && user.id === userStore.user.id"
          class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
        >
          <h2 class="mb-6 text-xl">
            Yêu cầu thiết lập mối quan hệ
            <strong>{{ relationshipRequest[0].relationship_type }}</strong>
          </h2>
          <div
            class="p-4 bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg mb-4"
          >
            <RouterLink
              :to="{
                name: 'profile',
                params: { id: relationshipRequest[0].created_by.id },
              }"
            >
              <img
              loading="lazy"
                :src="relationshipRequest[0].created_by.get_avatar"
                alt=""
                class="mb-6 rounded-full mx-auto w-20 h-20"
              />

              <p>
                <strong> {{ relationshipRequest[0].created_by.name }}</strong>
              </p>
              <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ relationshipRequest[0].created_by.friends_count }} người
                  bạn
                </p>
                <p class="text-xs text-gray-500 dark:text-neutral-200">
                  {{ relationshipRequest[0].created_by.posts_count }} bài đăng
                </p>
              </div>
            </RouterLink>
            <div class="mt-6 space-x-4">
              <button
                @click="
                  handleRequest(
                    'accepted',
                    relationshipRequest[0].created_by.id
                  )
                "
                class="btn"
              >
                Đồng ý
              </button>
              <button
                @click="
                  handleRequest(
                    'rejected',
                    relationshipRequest[0].created_by.id
                  )
                "
                class="bg-rose-400 hover:bg-rose-600 btn"
              >
                Từ chối
              </button>
            </div>
          </div>

          <hr />
        </div>
        <p class="font-semibold text-2xl">Bài viết của {{ user.name }}</p>
        <div v-if="posts?.length">
          <div
            class="bg-white border border-gray-200 rounded-lg mt-4 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200"
            v-for="post in posts"
            v-bind:key="post.id"
          >
          <!-- v-on:deletePost="deletePost" -->
            <FeedItem v-bind:post="post" v-on:deletePost="deletePost"/>
          </div>
          <SkeletonLoadingPost
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
import { RouterLink } from "vue-router";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { usePageStore } from "../../stores/page";
import { defineAsyncComponent } from "vue";

import {
  CameraIcon,
  UserGroupIcon,
  ClipboardDocumentListIcon,
  MapPinIcon,
  HeartIcon,
  HomeIcon,
  ClockIcon,
} from "@heroicons/vue/24/solid";
import AvatarModal from "../../components/modals/profile/AvatarModal.vue";
import PostForm from "../../components/forms/PostForm.vue";
import PostToForm from "../../components/forms/PostToForm.vue";
import FeedItem from "../../components/items/post/FeedItem.vue";

import SkeletonLoadingPost from "../../components/loadings/SkeletonLoadingPost.vue";
import SkeletonShowcaseLoading from "../../components/loadings/SkeletonShowcaseLoading.vue";

const ImageShowcase = defineAsyncComponent({
  loader: () => import("../../components/items/profile/ImageShowcase.vue"),
  loadingComponent: SkeletonShowcaseLoading,
  delay: 500,
  timeout: 3000,
});

const Friend = defineAsyncComponent({
  loader: () => import("../../components/items/profile/Friend.vue"),
  loadingComponent: SkeletonShowcaseLoading,
  delay: 500,
  timeout: 3000,
});

export default {
  name: "profiledetail",
  components: {
    RouterLink,
    CameraIcon,
    AvatarModal,
    UserGroupIcon,
    ClipboardDocumentListIcon,
    MapPinIcon,
    HeartIcon,
    HomeIcon,
    ClockIcon,
    ImageShowcase,
    PostForm,
    PostToForm,
    FeedItem,
    SkeletonLoadingPost,
    Friend
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore()
    const pageStore = usePageStore()

    return {
      userStore,
      toastStore,
      pageStore
    };
  },
  emits: ['getNewPost'],
  props: {
    user: Object,
    images: Array,
    friends: Array,
    friendShowcase: Array,
    relationshipRequest: Object,
    posts: Array,
    partnerId: String,
    partner: Object,
    postsList: Array,
    PostToShow: Number,
    getNewPost: Function,
    deletePost: Function
  },

  data() {
    return {
        avatarIsOpen: false,
        loadMore: false
    };
  },

  mounted(){
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  methods: {
    openAvatarModal() {
      this.avatarIsOpen = true;
    },
    closeAvatarModal() {
      this.avatarIsOpen = false;
    },
    // deletePost(id) {
    //   this.posts = this.posts.filter((post) => post.id !== id);
    // },
    sendDirectMessage() {
      if (!this.pageStore.pageId) {
        axios
          .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
          .then((res) => {
            this.$router.push("/chat");
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        axios
          .get(
            `/api/chat/${this.$route.params.id}/get-or-create/page/${this.pageStore.pageId}/`
          )
          .then((res) => {
            this.$router.push("/chat");
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    handleRequest(status, pk) {
      // console.log("handleRequest", status);

      axios
        .post(`/api/relationship/${pk}/${status}/`)
        .then((res) => {
          // console.log("data", res.data);

          if (status === "accepted") {
            this.toastStore.showToast(
              5000,
              "Đã đồng ý lời mời",
              "bg-emerald-500 text-white"
            );
            this.$router.go();
          }
          if (status === "rejected") {
            this.toastStore.showToast(
              5000,
              "Đã từ chối lời mời",
              "bg-amber-500 text-white"
            );
            setTimeout(() => {
              this.$router.go();
            }, 5500);
          } else {
            this.toastStore.showToast(
              5000,
              "Chấp nhận lời mời thất bại",
              "bg-red-500 text-white"
            );
          }
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
  },
};
</script>

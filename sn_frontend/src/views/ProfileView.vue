<template>
  <div class="max-w-7xl grid grid-cols-3 xl:mx-auto md:mx-8 mx-2 gap-4">
    <CoverImage class="col-span-3 md:max-h-[400px] sm:max-h-[300px] xs:max-h-[200px] lg:max-h-max" v-bind:user="user" />
    <div class="col-span-3 grid grid-cols-3 gap-4 relative">
      <div class="col-span-1 lg:block hidden"></div>

      <div
        class="lg:col-span-2 col-span-3 flex lg:justify-between justify-center items-center px-4 py-2 gap-4 lg:text-lg md:text-base xm:text-sm xs:text-xs font-semibold dark:text-neutral-200"
      >
        <div class="flex gap-4">
          <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
            >Bài viết</RouterLink
          >
          <RouterLink
            :to="{ name: 'profile', params: { id: userStore.user.id } }"
            >Giới thiệu</RouterLink
          >
          <RouterLink :to="{ name: 'photos', params: { id: user.id } }"
            >Ảnh</RouterLink
          >
          <div class="flex gap-1">
            <RouterLink :to="{ name: 'friends', params: { id: user.id } }">
              <span>Bạn bè</span>
            </RouterLink>
            <div class="flex gap-2" v-if="user.id === userStore.user.id && !pageStore.pageId">
              <span
                class="bg-rose-400 md:h-6 md:w-6 xs:h-4 xs:w-4 md:text-sm xs:text-xs text-center rounded-full font-semibold flex justify-center items-center"
                >{{ friendshipRequest.length }}
              </span>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div v-if="userStore.user.id !== user.id">
            <DeleteFriendModal
              :show="isDeleteFriendOpen"
              @closeDeleteFriendModal="closeDeleteFriendModal"
              @deleteFriend="deleteFriend"
            />
            <UnfollowedModal
              :followers="followers"
              :show="isUnfollowedOpen"
              @closeDeleteFriendModal="closeUnfollowedModal"
              @unfollowed="unfollowed"
            />
            <div v-if="filtered.includes(userStore.user.id)">
              <div v-for="(value, index) in filtered" :key="index">
                <FriendOptionsDropdown
                  :followers="followers"
                  v-if="value === userStore.user.id && !pageStore.pageId"
                  @openDeleteFriendModal="openDeleteFriendModal"
                  @openUnfollowedModal="openUnfollowedModal"
                  @followUser="followUser"
                />
              </div>
            </div>
            <button class="btn" v-else-if="checkRequest">
              Đã gửi lời mời kết bạn
            </button>
            <div v-else>
              <button class="btn" @click="sendFriendshipRequest">
                Thêm bạn bè
              </button>
            </div>
          </div>
          <button
            @click="openContactModal"
            class="dark:text-neutral-200 bg-slate-200 dark:bg-slate-800 md:px-4 md:py-2 p-1 shadow-md rounded-md hover:bg-slate-300 dark:hover:bg-slate-900 transition"
          >
            <span class="md:block hidden">Thông tin liên lạc</span>
            <PencilSquareIcon class="w-6 md:hidden"/>
          </button>
          <ContactModal
            :show="contactIsOpen"
            @closeContactModal="closeContactModal"
          />
        </div>
      </div>
      <hr class="col-span-3" />
      <div class="main-left top-0 lg:col-span-1 col-span-4">
        <div class="h-20 frame"></div>
        <div
          class="px-4 pb-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col justify-center items-center rounded-lg shadow-md overflow-hidden lg:w-full w-[90%] mx-auto"
        >
          <div
            class="icon relative w-[200px] h-[100px] bg-gray-100 dark:bg-slate-700 rounded-bl-[100px] rounded-br-[100px] before:content-[''] after:content-[''] before:absolute after:absolute before:top-0 after:top-0 before:left-[-50px] before:w-[55px] before:h-[35px] before:bg-transparent before:rounded-tr-[50px] before:shadow-[20px_-20px_0_20px_rgba(243,244,246,1)] after:right-[-50px] after:w-[55px] after:h-[35px] after:bg-transparent after:rounded-tl-[50px] after:shadow-[-20px_-20px_0_20px_rgba(243,244,246,1)] before:dark:shadow-[20px_-20px_0_20px_rgba(51,65,85,1)] after:dark:shadow-[-20px_-20px_0_20px_rgba(51,65,85,1)]"
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
            :src="user.get_avatar"
            alt=""
            class="mb-6 rounded-full w-44 h-44 shadow-xl absolute top-[90px]"
          />
          <AvatarModal
            :show="avatarIsOpen"
            @closeAvatarModal="closeAvatarModal"
          />

          <p>
            <strong class="text-2xl">{{ user.name }}</strong>
          </p>
          <p v-if="user.nickname" class="text-xl">({{ user.nickname }})</p>
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
          <RouterLink v-if="user.id === userStore.user.id" to="/profile/edit" class="md:max-w-max xs:w-full">
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
          v-if="userStore.user.id === user.id"
          class="p-4 bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
        >
          <PostForm v-bind:user="user" v-bind:posts="posts" />
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
            class="p-4 bg-gray-100 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 text-center rounded-lg mb-4"
          >
            <RouterLink
              :to="{
                name: 'profile',
                params: { id: relationshipRequest[0].created_by.id },
              }"
            >
              <img
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
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import PostForm from "../components/forms/PostForm.vue";
import FeedItem from "../components/items/post/FeedItem.vue";
import PostToForm from "../components/forms/PostToForm.vue";
import CoverImage from "../components/CoverImage.vue";
import ImageShowcase from "../components/items/profile/ImageShowcase.vue";
import SkeletonLoadingPostVue from "../components/loadings/SkeletonLoadingPost.vue";

import ContactModal from "../components/modals/profile/ContactModal.vue";
import AvatarModal from "../components/modals/profile/AvatarModal.vue";
import FriendOptionsDropdown from "../components/dropdown/FriendOptionsDropdown.vue";
import DeleteFriendModal from "../components/modals/profile/DeleteFriendModal.vue";
import UnfollowedModal from "../components/modals/profile/UnfollowedModal.vue";

import {
  ClockIcon,
  HeartIcon,
  ClipboardDocumentListIcon,
  UserGroupIcon,
  MapPinIcon,
  HomeIcon,
  CameraIcon,
  PencilSquareIcon
} from "@heroicons/vue/24/solid";

import { RouterLink } from "vue-router";

import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";
import { usePageStore } from "../stores/page" 

export default {
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const pageStore = usePageStore()

    return {
      userStore,
      toastStore,
      pageStore
    };
  },
  name: "FeedView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    RouterLink,
    PostForm,
    CoverImage,
    SkeletonLoadingPostVue,
    PostToForm,
    ImageShowcase,
    FriendOptionsDropdown,
    DeleteFriendModal,
    UnfollowedModal,
    ClockIcon,
    HeartIcon,
    ClipboardDocumentListIcon,
    MapPinIcon,
    UserGroupIcon,
    HomeIcon,
    CameraIcon,
    PencilSquareIcon,
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
      can_send_friendship_request: null,
      friendshipRequest: [],
      yourRequest: [],
      followers: [],
      status: "",
      friends: [],
      PostToShow: 5,
      loadMore: false,
      partnerId: "",
      partner: {
        id: null,
      },
      relationshipRequest: {},
      images: [],
      contactIsOpen: false,
      avatarIsOpen: false,
      isDeleteFriendOpen: false,
      isUnfollowedOpen: false,
    };
  },

  computed: {
    filtered() {
      return this.friends
        .map((friend) => friend.id)
        .filter((id) => id === this.userStore.user.id);
    },
    checkRequest() {
      return this.yourRequest[0]?.created_by?.id === this.userStore.user.id;
    },
  },

  beforeMount() {
    this.getUserInfo();
  },

  mounted() {
    this.getFriends();
    this.getFeed();
    this.getImages();
    window.addEventListener("scroll", this.infinateScroll);
    this.getRelationship();
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getFeed();
        this.getUserInfo();
        this.getImages();
      },
      deep: true,
      immediate: true,
    },
  },

  methods: {
    getUserInfo() {
      axios
        .get(`/api/user-info/${this.$route.params.id}`)
        .then((res) => {
          console.log(res.data)
          this.partnerId = res.data.user.partner;
          this.getPartnerInfo();
        })
        .catch((error) => console.log(error));
    },
    getPartnerInfo() {
      if (this.partnerId) {
        axios
          .get(`/api/user-info/${this.partnerId}`)
          .then((res) => {
            this.partner = res.data;
          })
          .catch((error) => console.log(error));
      } else {
        console.log("No partner");
      }
    },
    toPartner() {
      this.$router.push(`/profile/${this.partnerId}`);
    },
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },

    getImages() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/attachments/`)
        .then((res) => {
          this.images = res.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    sendDirectMessage() {
      axios
        .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
        .then((res) => {
          this.$router.push("/chat");
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    sendFriendshipRequest() {
      axios
        .post(`/api/friends/${this.$route.params.id}/request/`)
        .then((res) => {
          // console.log(res.data);
          this.status = res.data.message;
          if (this.status === "request already sent") {
            this.toastStore.showToast(
              5000,
              "Không thể gửi lần 2",
              "bg-rose-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              3000,
              "Đã gửi lời mời kết bạn",
              "bg-emerald-400 text-white"
            );
          }
          setTimeout(() => {
            this.$router.go();
          }, 3500);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getRelationship() {
      axios
        .get(`/api/relationship/${this.$route.params.id}/`)
        .then((res) => {
          this.relationshipRequest = res.data.request;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getFeed() {
      if(!this.pageStore.pageId){
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/`)
          .then((res) => {
            // console.log(res.data);
            this.postsList = res.data.posts;
            this.user = res.data.user;
            this.can_send_friendship_request =
              res.data.can_send_friendship_request;
            this.posts = res.data.posts.slice(0, this.PostToShow);
  
            // console.log(res.data);
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/${this.pageStore.pageId}/`)
          .then((res) => {
            // console.log(res.data);
            this.postsList = res.data.posts;
            this.user = res.data.user;
            this.can_send_friendship_request =
              res.data.can_send_friendship_request;
            this.posts = res.data.posts.slice(0, this.PostToShow);
  
            // console.log(res.data);
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
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

    getFriends() {
      axios
        .get(`/api/friends/${this.$route.params.id}/`)
        .then((res) => {
          this.friendshipRequest = res.data.requests;
          this.user = res.data.user;
          this.friends = res.data.friends;
          this.yourRequest = res.data.request_by;
          this.followers = res.data.followers;
        })
        .catch((error) => {
          console.log(error);
        });
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

    openDeleteFriendModal() {
      this.isDeleteFriendOpen = true;
    },

    closeDeleteFriendModal() {
      this.isDeleteFriendOpen = false;
    },

    deleteFriend() {
      this.isDeleteFriendOpen = false;

      axios
        .post(`/api/delete-friend/${this.$route.params.id}/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    openUnfollowedModal() {
      this.isUnfollowedOpen = true;
    },

    closeUnfollowedModal() {
      this.isUnfollowedOpen = false;
    },

    followUser() {
      axios
        .post(`/api/follow/${this.$route.params.id}/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    unfollowed() {
      axios
        .post(`/api/unfollowed/${this.$route.params.id}/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });

      this.isUnfollowedOpen = false;
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

    logout() {
      this.userStore.removeToken();

      this.$router.push("/login");
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

<template>
  <div class="max-w-7xl xl:mx-auto md:mx-8 mx-2 gap-4 pb-4">
    <ProfileHeader
      :user="user"
      :followers="followers"
      :friends="friends"
      :friendshipRequest="friendshipRequest"
      :yourRequest="yourRequest"
    />
    <router-view
      :user="user"
      :images="images"
      :friends="friends"
      :friendShowcase="friendShowcase"
      :relationshipRequest="relationshipRequest"
      :posts="posts"
      :partnerId="partnerId"
      :partner="partner"
      :postsList="postsList"
      :PostToShow="PostToShow"
    ></router-view>
    <div
      v-if="route.name === 'about' || route.name === 'friends'"
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Ảnh</p>
      <div class="grid lg:grid-cols-6 md:grid-cols-4 grid-cols-2 gap-3 my-4 max-h-96">
        <div v-for="image in images.slice(0, 12)" v-bind:key="image.id">
          <ImageShowcase v-bind:post="image" />
        </div>
      </div>
      <RouterLink
        :to="{ name: 'photos', params: { id: user.id } }"
        class="w-full flex justify-center items-center py-2 dark:bg-slate-700 bg-slate-200 hover:bg-slate-300 rounded-lg duration-75 dark:hover:bg-slate-800 cursor-pointer font-semibold text-lg"
      >
        Xem tất cả
      </RouterLink>
    </div>
    <div
      v-if="
        route.name === 'about' ||
        route.name === 'friends' ||
        route.name === 'photos'
      "
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Video</p>
      <div class="max-h-96 min-h-[192px] flex justify-center items-center">
        <h2 class="text-2xl font-semibold">
          {{ user.name }} chưa có video nào
        </h2>
      </div>
    </div>
    <div
      v-if="
        route.name === 'about' ||
        route.name === 'friends' ||
        route.name === 'photos'
      "
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Check in</p>
      <div class="max-h-96 min-h-[192px] flex justify-center items-center">
        <h2 class="text-2xl font-semibold">
          {{ user.name }} chưa tham quan nơi nào
        </h2>
      </div>
    </div>
    <div
      v-if="
        route.name === 'about' ||
        route.name === 'friends' ||
        route.name === 'photos'
      "
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Phim</p>
      <div class="max-h-96 min-h-[192px] flex justify-center items-center" v-if="!following.length">
        <h2 class="text-2xl font-semibold">
          {{ user.name }} chưa thích bộ phim nào
        </h2>
      </div>
      <div class="grid lg:grid-cols-6 md:grid-cols-4 grid-cols-2 gap-3 my-4 max-h-96" v-else>
        <div
          v-for="movie in moviePage"
          v-bind:key="movie.id"
        >
          <RouterLink :to="{name: 'page', params: {id: movie.id }}" class="relative group">
            <button
              class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
              v-on:click="openModal"
            ></button>
            <img
              :src="movie.get_avatar"
              class="cursor-pointer rounded-lg"
            />
          </RouterLink>
          <h3 class="font-medium mt-2">{{ movie.name }}</h3>
        </div>
      </div>
    </div>
    <div
      v-if="
        route.name === 'about' ||
        route.name === 'friends' ||
        route.name === 'photos'
      "
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Chương trình TV</p>
      <div class="max-h-96 min-h-[192px] flex justify-center items-center">
        <h2 class="text-2xl font-semibold">
          {{ user.name }} chưa thích chương trình TV nào
        </h2>
      </div>
    </div>
    <div
      v-if="
        route.name === 'about' ||
        route.name === 'friends' ||
        route.name === 'photos'
      "
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Thích</p>
      <div
        class="max-h-96 min-h-[192px] flex justify-center items-center"
        v-if="!following.length"
      >
        <h2 class="text-2xl font-semibold">
          Không có gì trong mục đã thích
        </h2>
      </div>
      <div class="grid lg:grid-cols-6 md:grid-cols-4 grid-cols-2 gap-3 my-4 max-h-96" v-else>
        <div
          v-for="followingPage in followingPages.slice(0, 6)"
          v-bind:key="followingPage.id"
        >
          <RouterLink :to="{name: 'page', params: {id: followingPage.id }}" class="relative group">
            <button
              class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
              v-on:click="openModal"
            ></button>
            <img
              :src="followingPage.get_avatar"
              :class="
                route.name !== 'profile'
                  ? 'xl:h-48 lg:h-24 cursor-pointer'
                  : ' md:w-full sm:h-48 xm:h-32 xs:h-24 cursor-pointer'
              "
              class="rounded-lg"
            />
          </RouterLink>
          <h3 class="font-medium mt-2">{{ followingPage.name }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import axios from "axios";
import ImageShowcase from "../../components/items/profile/ImageShowcase.vue";
import SkeletonLoadingPostVue from "../../components/loadings/SkeletonLoadingPost.vue";

import ProfileHeader from "../../components/items/profile/ProfileHeader.vue";

import {
  ClockIcon,
  HeartIcon,
  ClipboardDocumentListIcon,
  UserGroupIcon,
  MapPinIcon,
  HomeIcon,
  CameraIcon,
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
    const route = useRoute();

    return {
      userStore,
      toastStore,
      pageStore,
      route,
    };
  },
  name: "FeedView",
  components: {
    RouterLink,
    ProfileHeader,
    SkeletonLoadingPostVue,
    ImageShowcase,
    ClockIcon,
    HeartIcon,
    ClipboardDocumentListIcon,
    MapPinIcon,
    UserGroupIcon,
    HomeIcon,
    CameraIcon,
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
      following: [],
      followingPages: [],
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
      avatarIsOpen: false,
      friendShowcase: [],
    };
  },

  computed: {
    moviePage(){
      return this.followingPages.filter((fp) => fp.page_type === 'Phim ảnh')
    }
  },

  beforeMount() {
    this.getUserInfo();
  },

  mounted() {
    this.getFriends();
    this.getFeed();
    this.getImages();
    this.getRelationship();
    this.getFriendsShowCase();
    this.getFollowing()
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getFeed();
        this.getUserInfo();
        this.getImages();
        this.getFriendsShowCase();
      },
      deep: true,
      immediate: true,
    },
  },

  methods: {
    getFriendsShowCase() {
      axios
        .get(`/api/friends-showcase/${this.$route.params.id}/`)
        .then((res) => {
          this.friendShowcase = res.data.friends;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getUserInfo() {
      axios
        .get(`/api/user-info/${this.$route.params.id}`)
        .then((res) => {
          console.log(res.data);
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
      if (!this.pageStore.pageId) {
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
          .get(
            `/api/posts/profile/${this.$route.params.id}/${this.pageStore.pageId}/`
          )
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

    getFriends() {
      axios
        .get(`/api/friends/${this.$route.params.id}/`)
        .then((res) => {
          this.friendshipRequest = res.data.requests;
          this.user = res.data.user;
          this.friends = res.data.friends;
          this.yourRequest = res.data.request_by;
          this.followers = res.data.followers;
          this.following = res.data.following;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async getFollowing(){
      await axios.get("/api/page/following/").then((res) => {
        this.followingPages = res.data
      }).catch((error) => {
        console.log(error)
      })
    }
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

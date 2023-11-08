<template>
  <div class="max-w-7xl grid grid-cols-3 mx-auto gap-4">
    <CoverImage class="col-span-3" v-bind:user="user" />
    <div class="col-span-3 grid grid-cols-3">
      <div class="col-span-1"></div>
      <div class="col-span-2 px-4 py-2 flex gap-4 text-lg font-semibold">
        <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
          >Bài viết</RouterLink
        >
        <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }"
          >Giới thiệu</RouterLink
        >
        <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }"
          >Ảnh</RouterLink
        >
        <RouterLink :to="{ name: 'friends', params: { id: user.id } }"
          >Bạn bè</RouterLink
        >
      </div>
      <hr class="col-span-3" />
    </div>
    <div class="main-left col-span-1 relative">
      <div class="h-20 frame"></div>
      <div
        class="px-4 pb-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 flex flex-col justify-center items-center rounded-lg shadow-md overflow-hidden"
      >
        <div
          class="icon relative w-[200px] h-[100px] bg-gray-100 dark:bg-slate-700 rounded-bl-[100px] rounded-br-[100px] before:content-[''] after:content-[''] before:absolute after:absolute before:top-0 after:top-0 before:left-[-50px] before:w-[55px] before:h-[35px] before:bg-transparent before:rounded-tr-[50px] before:shadow-[20px_-20px_0_20px_rgba(243,244,246,1)] after:right-[-50px] after:w-[55px] after:h-[35px] after:bg-transparent after:rounded-tl-[50px] after:shadow-[-20px_-20px_0_20px_rgba(243,244,246,1)] before:dark:shadow-[20px_-20px_0_20px_rgba(51,65,85,1)] after:dark:shadow-[-20px_-20px_0_20px_rgba(51,65,85,1)]"
        ></div>
        <img
          :src="user.get_avatar"
          alt=""
          class="mb-6 rounded-full w-44 h-44 shadow-xl absolute top-0 z-50"
        />
        <p>
          <strong class="text-2xl">{{ user.name }}</strong>
        </p>
        <div class="mt-6 flex space-x-8 justify-around">
          <div>
            <p class="text-sm text-gray-500 dark:text-neutral-200">
              {{ user.friends_count }} người bạn
            </p>
            <router-link
              :to="{ name: 'friends', params: { id: user.id } }"
              v-if="userStore.user.id === user.id"
              ><p
                class="text-sm mt-4 relative gap-3 flex justify-center items-center"
              >
                <span
                  class="bg-rose-400 h-6 w-6 text-center rounded-full font-semibold flex justify-center items-center"
                  >{{ friendshipRequest.length }}</span
                >
                <span>lời mời kết bạn mới</span>
              </p></router-link
            >
            <div>
              {{ userInfo.relationship_status }} với
              <strong @click="toPartner" class="cursor-pointer">
                {{ partner?.user?.name }}
              </strong>
            </div>
          </div>

          <p class="text-sm text-gray-500 dark:text-neutral-200">
            {{ user.posts_count }} bài đăng
          </p>
        </div>
        <div class="flex flex-col mt-4">
          <div v-if="userStore.user.id !== user.id" class="mt-6">
            <div v-if="can_send_friendship_request === false">
              <div v-for="(value, index) in filtered" :key="index">
                <button class="btn" v-if="value === userStore.user.id">
                  Bạn bè
                </button>
                <button class="btn" v-else>Đã gửi lời mời kết bạn</button>
              </div>
            </div>
            <div v-else>
              <button class="btn" @click="sendFriendshipRequest">
                Thêm bạn bè
              </button>
            </div>
          </div>
        </div>

        <button
          v-if="userStore.user.id !== user.id"
          @click="sendDirectMessage"
          class="mt-6 bg-violet-400 hover:bg-violet-600 btn"
        >
          Nhắn tin
        </button>
      </div>
    </div>

    <div
      class="main-center col-span-2 space-y-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 p-4"
      id="feed-frame"
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
        <PostToForm v-bind:user="user" v-bind:posts="posts" />
      </div>

      <p class="font-semibold text-2xl">Bài viết của {{ user.name }}</p>
      <div v-if="posts?.length">
        <div
          class="p-4 bg-white border border-gray-200 rounded-lg mt-4 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200"
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
</template>

<script>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import PostForm from "../components/forms/PostForm.vue";
import FeedItem from "../components/FeedItem.vue";
import PostToForm from "../components/forms/PostToForm.vue";
import CoverImage from "../components/CoverImage.vue";
import SkeletonLoadingPostVue from "../components/loadings/SkeletonLoadingPost.vue";
import getUserInfo from "../api/getUserInfo";
import { onMounted, ref } from "vue";

import { RouterLink } from "vue-router";

import { useUserStore } from "../stores/user";
import { useToastStore } from "../stores/toast";

export default {
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const userInfo = ref({});

    onMounted(async () => {
      const res = await getUserInfo(userStore.user.id);
      userInfo.value = res;
    });

    return {
      userStore,
      toastStore,
      userInfo,
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
      status: "",
      friends: [],
      PostToShow: 5,
      loadMore: false,
      partnerId: "",
      partner: {
        id: null,
      },
    };
  },

  computed: {
    filtered() {
      return this.friends
        .map((friend) => friend.id)
        .filter((id) => id === this.userStore.user.id);
    },
  },

  beforeMount() {
    this.getUserInfo();
  },

  mounted() {
    this.getFriends();
    this.getFeed();
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getFeed();
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
          this.partnerId = res.data.user.partner;
          console.log(this.partnerId);
          this.getPartnerInfo();
        })
        .catch((error) => console.log(error));
    },
    getPartnerInfo() {
      axios
        .get(`/api/user-info/${this.partnerId}`)
        .then((res) => {
          this.partner = res.data;
        })
        .catch((error) => console.log(error));
    },
    toPartner(){
      this.$router.push(`/profile/${this.partnerId}`)
    },
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
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

    getFeed() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/`)
        .then((res) => {
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
    },

    infinateScroll() {
      const frame = document.getElementById("feed-frame");
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
          // console.log(res.data.friends);
        })
        .catch((error) => {
          console.log(error);
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

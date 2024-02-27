<template>
  <div class="max-w-7xl xl:mx-auto md:mx-8 mx-2 gap-4">
    <PageHeader
      :user="user"
      :page="page"
      :allFollowers="allFollowers"
      :pageLikes="pageLikes"
    />
    <router-view
      :user="user"
      :page="page"
      :images="images"
      :posts="posts"
      :postsList="postsList"
      :pageLikes="pageLikes"
      :allFollowers="allFollowers"
      :pageFollowing="pageFollowing"
      :PostToShow="PostToShow"
    ></router-view>
    <div
      v-if="route.name === 'pageabout' || route.name === 'pagephotos'"
      class="bg-neutral-200 dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Người theo dõi</p>
      <div
        class="grid lg:grid-cols-6 grid-cols-3 gap-3 my-4 max-h-96"
        v-if="allFollowers.length"
      >
        <div
          v-for="follower in allFollowers.slice(0, 12)"
          v-bind:key="follower.id"
        >
          <UserItem :user="follower" v-if="!follower.is_page" />
          <PageItem :page="follower" v-else />
        </div>
      </div>
      <div v-else class="flex items-center justify-center">
        Trang chưa có người theo dõi.
      </div>
    </div>
    <div
      v-if="route.name === 'pageabout' || route.name === 'pageusers'"
      class="bg-neutral-200 dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Ảnh</p>
      <div
        class="grid lg:grid-cols-6 md:grid-cols-4 grid-cols-2 gap-3 my-4 max-h-96"
      >
        <div v-for="image in images.slice(0, 12)" v-bind:key="image.id">
          <ImageShowcase v-bind:post="image" />
        </div>
      </div>
      <RouterLink
        :to="{ name: 'pagephotos', params: { id: page.id } }"
        class="w-full flex justify-center items-center py-2 dark:bg-slate-700 rounded-lg duration-75 dark:hover:bg-slate-800 cursor-pointer font-semibold text-lg"
      >
        Xem tất cả
      </RouterLink>
    </div>
    <div
      v-if="
        route.name === 'pageabout' ||
        route.name === 'pageusers' ||
        route.name === 'pagephotos'
      "
      class="bg-neutral-200 dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
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
        route.name === 'pageabout' ||
        route.name === 'pageusers' ||
        route.name === 'pagephotos'
      "
      class="bg-neutral-200 dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg mt-4"
    >
      <p class="text-xl font-bold">Thích</p>
      <div
        class="max-h-96 min-h-[192px] flex justify-center items-center"
        v-if="!pageFollowing?.length"
      >
        <h2 class="text-2xl font-semibold">Không có gì trong mục đã thích</h2>
      </div>
      <div
        class="grid md:grid-cols-6 xm:grid-cols-4 grid-cols-2 gap-3 my-4 max-h-96"
        v-else
      >
        <div
          v-for="pageFollowing in pageFollowing.slice(0, 6)"
          v-bind:key="pageFollowing.id"
        >
          <RouterLink
            :to="{ name: 'page', params: { id: pageFollowing.id } }"
            class="relative group"
          >
            <button
              class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
              v-on:click="openModal"
            ></button>
            <img
            loading="lazy"
              :src="pageFollowing.get_avatar"
              class="cursor-pointer rounded-lg"
            />
          </RouterLink>
          <h3 class="font-medium mt-2">{{ pageFollowing.name }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CoverImage from "../../components/CoverImage.vue";
import ImageShowcase from "../../components/items/profile/ImageShowcase.vue";
import PageHeader from "../../components/items/page/PageHeader.vue";

import ContactModal from "../../components/modals/profile/ContactModal.vue";
import AvatarModal from "../../components/modals/profile/AvatarModal.vue";

import { RouterLink } from "vue-router";

import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { usePageStore } from "../../stores/page";
import { useRoute } from "vue-router";

import UserItem from "../../components/items/profile/UserItem.vue";
import PageItem from "../../components/items/page/PageItem.vue";

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
    PageHeader,
    RouterLink,
    CoverImage,
    ImageShowcase,
    ContactModal,
    AvatarModal,
    UserItem,
    PageItem,
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
      allFollowers: [],
      pageFollowing: [],
      PostToShow: 5,
      loadMore: false,
      images: [],
      contactIsOpen: false,
      avatarIsOpen: false,
      isLike: false,
    };
  },

  beforeMount() {
    this.getPageInfo();
  },

  mounted() {
    this.getFeed();
    this.getImages();
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

  methods: {
    async getPageInfo() {
      await axios
        .get(`/api/page/get-page/${this.$route.params.id}`)
        .then((res) => {
          this.page = res.data.data;
          this.pageLikes = res.data.other_page_likes;
          this.allFollowers = res.data?.followers?.concat(
            res.data?.other_page_followers
          );
          this.pageFollowing = res.data.other_page_following;
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

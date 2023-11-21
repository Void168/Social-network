<template>
  <div class="grid grid-cols-6 gap-4" id="feed-frame">
    <div class="col-span-1"></div>
    <div class="mx-auto w-[70%] main-center col-span-4 space-y-4">
      <div class="p-4 bg-white border border-gray-200 dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 rounded-lg">
        <PostForm v-bind:user="null" v-bind:posts="posts" />
        <div>
          <div
            class="bg-white border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg mt-4 shadow-sm"
            v-for="post in posts"
            v-bind:key="post.id"
          >
            <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
          </div>
          
          <SkeletonLoadingPostVue v-show="!loadMore" v-if="posts.length !== postsList.length"/>
          <div v-else class="flex justify-center items-center h-48">
            <p class="text-xl font-semibold">Đã tải hết bài viết</p>
          </div>
        </div>
      </div>
    </div>
    <div class="main-right col-span-1 space-y-4 sticky top-[155px] h-[900px] z-9">
      <PeopleYouMayKnow />
      <Trends />
      <ChatContainer />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import ChatContainer from "../components/ChatContainer.vue";

import PostForm from "../components/forms/PostForm.vue";
import FeedItem from "../components/items/FeedItem.vue";
import SkeletonLoadingPostVue from '../components/loadings/SkeletonLoadingPost.vue';

export default {
  name: "FeedView",
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    PostForm,
    SkeletonLoadingPostVue,
    ChatContainer
  },

  data() {
    return {
      posts: [],
      postsList: [],
      body: "",
      PostToShow: 5,
      loadMore: false,
    };
  },

  mounted() {
    this.getFeed();
    window.addEventListener("scroll", this.infinateScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.infinateScroll);
  },

  methods: {
    getFeed() {
      axios
        .get("/api/posts/")
        .then((res) => {
          // console.log(res.data);
          this.postsList = res.data;
          this.posts = res.data.slice(0, this.PostToShow);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deletePost(id) {
      this.posts = this.posts.filter((post) => post.id !== id);
    },
    infinateScroll() {
      const frame = document.getElementById("feed-frame");
      let height = frame.scrollHeight;
      let scrollY = window.scrollY;
      if (height < scrollY + 1000) {
        setTimeout(() => {
          this.loadMore = true;
        }, 1000)
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
      console.log(this.loadMore)
    },
  },
};
</script>

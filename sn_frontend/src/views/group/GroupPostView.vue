<template>
  <SkeletonLoadingPost v-if="isLoading" />
  <div
    class="max-w-7xl w-full mx-auto flex justify-center items-center gap-4 sm:my-6 relative"
    v-else
  >
    <RouterLink
      :to="{ name: 'groupdiscuss', params: { id: group.id } }"
      class="absolute top-2 left-2 z-10"
    >
      <XMarkIcon
        class="w-10 h-10 cursor-pointer p-1 dark:bg-slate-800 rounded-full dark:hover:bg-slate-700 duration-75"
      />
    </RouterLink>
    <div class="space-y-4 xl:w-6/12 md:w-8/12 w-full sm:mx-2 md:mx-0">
      <div
        v-if="groupPost.id"
        class="p-4 bg-white border border-gray-200 sm:rounded-lg shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <GroupPost
          :post="groupPost"
          :group="group"
          :currentMember="currentMember"
        />
      </div>
      <div
        class="sm:p-4 bg-white border border-gray-200 sm:rounded-lg shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <div
              :class="
                words[0] === '' || !words.length
                  ? 'relative p-4 w-full bg-gray-100 dark:bg-slate-800 opacity-50 rounded-lg resize-none overflow-y-scroll scrollbar-none scrollbar scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800'
                  : 'relative p-4 w-full bg-gray-100 dark:bg-slate-800 rounded-lg resize-none overflow-y-scroll scrollbar-none scrollbar scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800'
              "
            >
              <div class="absolute z-[-1] dark:text-neutral-200">
                Viết bình luận...
              </div>
              <div
                contenteditable="true"
                spellcheck="false"
                ref="content"
                :onkeyup="getWords"
                class="outline-none"
              ></div>
            </div>
          </div>
          <div
            class="relative px-4 py-2 border-t border-gray-100 flex justify-end dark:border-slate-400"
          >
            <button
              :class="
                body.length
                  ? 'btn'
                  : ' bg-slate-300 font-semibold dark:bg-slate-500 dark:text-neutral-200 xm:px-4 xm:py-2 px-2 py-1 rounded-md shadow-md cursor-auto'
              "
              :disabled="body.length < 0"
            >
              Bình luận
            </button>
            <div
              class="w-full bg-slate-200 dark:bg-slate-800 dark:text-neutral-200 min-h-min overflow-y-scroll scrollbar-none scrollbar scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 absolute inset-0 z-10 open"
              v-if="autoComplete === true && filteredFriends.length > 0"
            >
              <ul
              >
                <li
                v-for="friend in filteredFriends"
                :key="friend.id"
                  @click="getTag(friend)"
                  class="hover:bg-slate-300 dark:hover:bg-slate-700 p-4 flex items-center gap-2 cursor-pointer sm:h-20 h-16 w-full "
                >
                  <img
                    loading="lazy"
                    :src="friend.get_avatar"
                    class="xm:w-10 xm:h-10 h-6 w-6 rounded-full"
                  />
                  <span>{{ friend.name }}</span>
                </li>
              </ul>
            </div>
          </div>
        </form>
      </div>

      <div
        class="xm:p-4 p-2 bg-white border border-gray-200 sm:rounded-lg sm:ml-10 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <div
          v-if="!groupPost.comments?.length"
          class="flex justify-center items-center"
        >
          Chưa có bình luận nào
        </div>
        <div
          v-else
          class="bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
          v-for="comment in allComments.slice(0, lastComment)"
          v-bind:key="comment?.id"
        >
          <MemberCommentItem :comment="comment" :post="groupPost" />
        </div>
        <div class="flex justify-end">
          <button
            class="hover:underline transition"
            @click="loadMore"
            v-if="lastComment < allComments.length"
          >
            Tải thêm bình luận
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import PeopleYouMayKnow from "../../components/PeopleYouMayKnow.vue";
import Trends from "../../components/Trends.vue";
import GroupPost from "../../components/items/post/GroupPost.vue";

import { XMarkIcon } from "@heroicons/vue/24/solid";
import SkeletonLoadingPost from "../../components/loadings/SkeletonLoadingPost.vue";
import MemberCommentItem from "../../components/items/group/post/MemberCommentItem.vue";
import { useUserStore } from "../../stores/user";
import { usePageStore } from "../../stores/page";

export default {
  name: "PostView",
  components: {
    PeopleYouMayKnow,
    Trends,
    GroupPost,
    MemberCommentItem,
    SkeletonLoadingPost,
    XMarkIcon,
  },

  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore();
    return {
      userStore,
      pageStore,
    };
  },

  props: {
    group: Object,
    currentMember: Object,
  },

  data() {
    return {
      groupPost: {
        id: null,
        comments: [],
      },
      lastComment: 5,
      body: "",
      words: [],
      autoComplete: false,
      friends: [],
      queries: [],
      tagInfo: {},
      tags: [],
      isLoading: false,
    };
  },

  watch: {
    handler: function () {
      this.getWords();
    },
  },

  computed: {
    filteredFriends() {
      return this.friends.filter((friend) =>
        friend.name
          .toLowerCase()
          .includes(this.queries[this.queries.length - 1]?.slice(1))
      );
    },
    allComments() {
      return this.groupPost?.comments;
    },
  },

  mounted() {
    this.getGroupPost();
    this.getFriends();
    document.addEventListener("click", this.clickOutside);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.clickOutside);
  },

  methods: {
    async getGroupPost() {
      this.isLoading = true;
      await axios
        .get(`/api/posts/group/${this.$route.params.postid}/detail/`)
        .then((res) => {
          // console.log("data", res.data);

          this.groupPost = res.data.post;
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getFriends() {
      await axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          this.friends = res.data.friends;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    loadMore() {
      this.lastComment = this.lastComment + 10;
      if (this.allComments.length < this.lastComment) {
        this.lastComment = this.allComments.length;
      }
    },
    getWords() {
      const commentContent = this.$refs.content;
      this.body = commentContent.innerHTML.replace(/&nbsp;/g, " ");
      this.words = this.body.split(" ").map((name) => name.toLowerCase());
      this.queries = this.words.filter((word) => word.indexOf("@") === 0);
      if (
        this.words[this.words.length - 1].indexOf("@") === 0 &&
        this.words[this.words.length - 1].length > 1
      ) {
        this.autoComplete = true;
      } else {
        this.autoComplete = false;
      }

      if (this.body.includes(this.tagInfo.name) === false) {
        this.tags.pop(this.tagInfo);
      }
    },
    getTag(friend) {
      const commentContent = this.$refs.content;
      this.queries[this.queries.length - 1] = friend.name;
      commentContent.innerHTML =
        commentContent.innerHTML.slice(
          0,
          commentContent.innerHTML.lastIndexOf("@") + 1
        ) + friend.name;
      this.tagInfo = friend;
      this.tags.push(this.tagInfo);

      this.body = commentContent.innerHTML.replace(/&nbsp;/g, " ");

      this.autoComplete = false;
    },
    clickOutside() {
      const modalContainer = document.querySelector(".open");

      if (modalContainer && !modalContainer.contains(event.target.parentNode)) {
        this.autoComplete = false;
      }
    },
    submitForm() {
      // console.log("submitForm", this.body);

      if (this.body.length > 0) {
        axios
          .post(
            `/api/posts/group/${this.$route.params.postid}/post/${this.$route.params.id}/comment/`,
            {
              body: this.body,
              tags: this.tags,
            }
          )
          .then((res) => {
            // console.log("data", res.data);

            this.words = [];
            this.body = "";
            this.tags = [];
            this.$refs.content.innerHTML = "";
            this.groupPost.comments.unshift(res.data);
            this.groupPost.comments_count += 1;
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else if (this.body.length > 0 && this.pageStore.pageId) {
        axios
          .post(
            `/api/posts/page/${this.pageStore.pageId}/${this.$route.params.id}/comment-by-page/`,
            {
              body: this.body,
              tags: this.tags,
            }
          )
          .then((res) => {
            // console.log("data", res.data);

            this.words = [];
            this.body = "";
            this.tags = [];
            this.$refs.content.innerHTML = "";
            this.groupPost.comments.unshift(res.data);
            this.groupPost.comments_count += 1;
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
  },
};
</script>

<template>
  <TransitionRoot @click="$emit('closeModal')" appear as="template">
    <Dialog as="div" class="relative z-10">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-75 z-50" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto z-50">
        <div class="flex min-h-[100%] justify-end text-center">
          <span class="fixed top-4 left-6 z-[60]"
            ><XMarkIcon class="text-neutral-200 h-6 w-6 cursor-pointer"
          /></span>
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-[90%] transform bg-slate-200 text-left align-middle shadow-xl transition-all"
            >
              <div class="grid grid-cols-4">
                <div class="col-span-3 bg-black relative group">
                  <div
                    class="w-full h-full flex justify-center items-center bg-black"
                  >
                    <img
                      :src="post?.attachments[0]?.get_image"
                      class="rounded-none"
                    />
                  </div>

                  <span
                    class="absolute h-[90%] hidden group translate-y-10 hover:translate-y-0 duration-150 ease-in-out transform w-full group-hover:flex items-center justify-between z-[60] inset-y-0 px-6"
                  >
                    <ArrowLeftCircleIcon
                      class="h-10 w-10 transition-all text-neutral-200 opacity-60 group-hover:block hover:opacity-80 cursor-pointer"
                    />
                    <ArrowRightCircleIcon
                      class="h-10 w-10 transition-all text-neutral-200 opacity-60 group-hover:block hover:opacity-80 cursor-pointer"
                    />
                  </span>
                </div>
                <div
                  class="relative col-span-1 overflow-y-scroll no-scrollbar scrollbar scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 h-screen border border-gray-200 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
                >
                  <div class="mb-6 flex items-center justify-between p-4">
                    <div class="flex items-center space-x-4">
                      <img
                        :src="post?.created_by.get_avatar"
                        class="w-12 h-12 rounded-full shadow-md"
                      />
                      <div class="flex gap-1 items-center">
                        <strong>
                          <RouterLink
                            :to="{
                              name: 'profile',
                              params: { id: post?.created_by?.id },
                            }"
                            >{{ post?.created_by.name }}</RouterLink
                          >
                        </strong>
                        <div v-if="post?.post_to" class="flex gap-1">
                          <p>cùng với</p>
                          <strong>
                            <RouterLink
                              :to="{
                                name: 'profile',
                                params: { id: post?.post_to?.id },
                              }"
                              >{{ post?.post_to?.name }}</RouterLink
                            >
                          </strong>
                        </div>
                      </div>

                      <GlobeAsiaAustraliaIcon
                        class="w-4 h-4"
                        v-if="
                          post?.is_private === false && post?.only_me === false
                        "
                      />
                      <UserGroupIcon
                        class="w-4 h-4"
                        v-else-if="
                          post?.is_private === true && post?.only_me === false
                        "
                      />
                      <LockClosedIcon
                        class="w-4 h-4"
                        v-else-if="
                          post?.is_private === true && post?.only_me === true
                        "
                      />
                    </div>
                    <p class="text-gray-600 dark:text-neutral-200">
                      {{ post?.created_at_formatted }} trước
                    </p>
                  </div>
                  <div class="flex space-x-6 my-4 p-4">
                    <div class="flex items-center space-x-2">
                      <HeartLike
                        class="w-6 h-6 text-rose-500 cursor-pointer"
                        v-if="isLike"
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

                      <div
                        class="text-gray-500 text-xs dark:text-neutral-200 cursor-pointer"
                      >
                        {{ post?.comments_count }} bình luận
                      </div>
                    </div>
                  </div>
                  <hr />
                  <div
                    class="p-4 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
                  >
                    <div
                      v-if="!post.comments?.length"
                      class="flex justify-center items-center"
                    >
                      Chưa có bình luận nào
                    </div>
                    <div v-else>
                      <div
                        class="bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
                        v-for="comment in post.comments.slice(0, lastComment)"
                        v-bind:key="comment.id"
                      >
                        <CommentItem v-bind:comment="comment" />
                      </div>
                    </div>
                    
                    <div class="flex justify-end">
                      <button
                      class="hover:underline transition"
                      @click="loadMore"
                      v-if="lastComment < post?.comments?.length"
                      >
                      Tải thêm bình luận
                    </button>
                  </div>
                  <div v-if="lastComment > 6" class="h-24"></div>
                  </div>
                  <div
                    class="bg-white border-t dark:bg-slate-600 dark:text-neutral-200 sticky z-60 bottom-0 px-4"
                  >
                    <form v-on:submit.prevent="submitForm" class="flex justify-center items-center">
                      <div class="py-4 flex items-center gap-2">
                        <img
                          :src="post?.created_by.get_avatar"
                          class="w-10 h-10 rounded-full shadow-md"
                        />
                        <textarea
                          v-model="body"
                          class="p-4 w-full bg-gray-100 rounded-lg resize-none"
                          cols="30"
                          rows="1"
                          placeholder="Viết bình luận..."
                        ></textarea>
                      </div>

                        <div
                          class="px-4 py-2 flex justify-end dark:border-slate-400"
                        >
                          <button><PaperAirplaneIcon class="w-6 h-6 text-slate-700 dark:text-slate-300 dark:hover:text-slate-400 transition"/></button>
                        </div>
                    </form>
                  </div>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import axios from "axios";

import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";
import { HeartIcon as HeartLike, XMarkIcon, PaperAirplaneIcon } from "@heroicons/vue/24/solid";
import {
  ArrowLeftCircleIcon,
  ArrowRightCircleIcon,
} from "@heroicons/vue/24/outline";

import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import CommentItem from "../CommentItem.vue";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  props: {
    isOpen: Boolean,
    imageId: String,
    post: Object,
  },

  data() {
    return {
      lastComment: 6,
      body: "",
      isLike: false,
    };
  },
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    HeartLike,
    XMarkIcon,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
    ArrowLeftCircleIcon,
    ArrowRightCircleIcon,
    PaperAirplaneIcon,
    CommentItem,
  },
  mounted() {
    this.like();
  },
  methods: {
    loadMore() {
      this.lastComment = this.lastComment + 10;
      if (this.post.comments.length < this.lastComment) {
        this.lastComment = this.post.comments.length;
      }
    },
    like() {
      const is_like = this.post.likes
        .map((like) => like.created_by)
        .map((created_by) => created_by.id);
      if (is_like.includes(this.userStore.user.id)) {
        this.isLike = true;
      }
      // console.log(this.post);
    },
    likePost(id) {
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
    },
    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post(`/api/posts/${this.post.id}/comment/`, {
          body: this.body,
        })
        .then((res) => {
          console.log("data", res.data);

          this.post.comments.unshift(res.data);
          this.post.comments_count += 1;
          this.body = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
});
</script>



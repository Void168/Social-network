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
        <div class="flex min-h-[90%] justify-center p-4 text-center">
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
              class="w-[70%] transform rounded-2xl bg-white text-left align-middle shadow-xl transition-all"
            >
              <div class="grid grid-cols-3">
                <div class="col-span-2">
                  <img
                    :src="post?.attachments[0]?.get_image"
                    class="h-full w-full rounded-none"
                  />
                </div>
                <div class="col-span-1 p-4 bg-white border border-gray-200 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200">
                  <div class="mb-6 flex items-center justify-between">
                    <div
                      class="flex items-center space-x-4 p-4"
                    >
                      <img
                        :src="post?.created_by.get_avatar"
                        class="w-10 h-10 rounded-full"
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

                  <div
                    class="p-4 bg-white border border-gray-200 rounded-lg shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
                  >
                    <form v-on:submit.prevent="submitForm">
                      <div class="p-4">
                        <textarea
                          v-model="body"
                          class="p-4 w-full bg-gray-100 rounded-lg"
                          cols="30"
                          rows="1"
                          placeholder="Viết bình luận..."
                        ></textarea>
                      </div>

                      <div
                        class="px-4 py-2 border-t border-gray-100 flex justify-end dark:border-slate-400"
                      >
                        <button class="btn">Bình luận</button>
                      </div>
                    </form>
                  </div>

                  <div
                    class="p-4 bg-white border border-gray-200 rounded-lg ml-10 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
                  >
                    <div
                      v-if="!post.comments?.length"
                      class="flex justify-center items-center"
                    >
                      Chưa có bình luận nào
                    </div>
                    <div
                      v-else
                      class="bg-white rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
                      v-for="comment in post.comments.slice(0, lastComment)"
                      v-bind:key="comment.id"
                    >
                      <CommentItem v-bind:comment="comment" />
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
import CommentItem from '../CommentItem.vue'

export default (await import("vue")).defineComponent({
  props: {
    isOpen: Boolean,
    imageId: String,
    post: Object,
  },

  data() {
    return {
      lastComment: 5,
      body: "",
      comments: [],
    };
  },
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
    CommentItem,
  },
  methods: {
    loadMore() {
      this.lastComment = this.lastComment + 10;
      if (this.post.comments.length < this.lastComment) {
        this.lastComment = this.post.comments.length;
      }
    },
    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post(`/api/posts/${this.$route.params.id}/comment/`, {
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
  }
});
</script>

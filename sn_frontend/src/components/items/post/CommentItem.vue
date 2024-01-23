<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-start gap-3 w-full relative">
        <div class="group">
          <RouterLink
            :to="{
              name: 'profile',
              params: { id: comment?.created_by?.id },
            }"
          >
            <img
              :src="comment?.created_by?.get_avatar"
              class="w-10 h-10 rounded-full"
            />
          </RouterLink>
          <TooltipProfile
            :user="comment?.created_by"
            class="hidden group-hover:block"
          />
        </div>
        <div
          class="flex justify-between border-none bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl w-full p-4"
        >
          <div>
            <div class="flex items-center gap-1 group">
              <strong class="group">
                <RouterLink
                  :to="{
                    name: 'profile',
                    params: { id: comment?.created_by?.id },
                  }"
                  >{{ comment?.created_by.name }}</RouterLink
                >
                <TooltipProfile
                  :user="comment?.created_by"
                  class="hidden md:group-hover:block"
                />
              </strong>
              <CommentDropDownVue
                v-if="comment?.created_by?.id === userStore.user.id && !pageStore.pageId"
                @deleteComment="deleteComment"
              />
              <CommentDropDownVue
                v-if="pageStore.pageId === post?.created_by?.id && pageStore.pageId"
                @deleteComment="deleteComment"
              />
            </div>
            <div class="flex gap-1 flex-wrap sm:text-base text-sm break-all">
              <span
                v-for="word in words"
                :key="word"
                :class="filteredTags.includes(word) ? 'text-emerald-400' : ''"
              >
                <RouterLink
                  v-if="filteredTags.includes(word)"
                  :to="{
                    name: 'profile',
                    params: {
                      id: tags.filter((tag) => word.includes(tag.name))[0].id,
                    },
                  }"
                >
                  {{ word }}
                </RouterLink>
                <span v-else>{{ word }}</span>
              </span>
            </div>
          </div>
          <p class="text-gray-600 dark:text-neutral-200 sm:text-base text-xs px-1">
            {{ comment?.created_at_formatted }} trước
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { RouterLink } from "vue-router";
import TooltipProfile from "../profile/TooltipProfile.vue";
import CommentDropDownVue from "../../dropdown/CommentDropDown.vue";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { usePageStore } from "../../../stores/page";
export default (await import("vue")).defineComponent({
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
  props: {
    comment: Object,
    post: Object
  },
  data() {
    return {
      tags: this.comment?.tags,
      filteredTags: [],
      onHover: false,
    };
  },
  computed: {
    words() {
      return this.comment?.body?.split(" ");
    },
  },

  mounted() {
    this.checkTag();
    console.log(this.comment)
  },

  methods: {
    checkTag() {
      if(this.tags){
        const tagNames = this.tags.map((tag) => tag.name);
        tagNames.forEach((name) => {
          const filter = this.words.filter((word) => word.includes(name));
          this.filteredTags.push(...filter);
        });
      }
    },
    deleteComment() {
      if(!this.post?.created_by?.is_page){
        axios
          .delete(`/api/posts/${this.$route.params.id}/comment/${this.comment.id}/delete/`)
          .then((res) => {
            if (res.data.message === "comment deleted") {
              this.toastStore.showToast(
                2000,
                "Đã xóa bình luận",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 2500);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .delete(`/api/posts/page/${this.$route.params.id}/comment/${this.comment.id}/delete/`)
          .then((res) => {
            if (res.data.message === "comment deleted") {
              this.toastStore.showToast(
                2000,
                "Đã xóa bình luận",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 2500);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
  components: { RouterLink, TooltipProfile, CommentDropDownVue },
});
</script>

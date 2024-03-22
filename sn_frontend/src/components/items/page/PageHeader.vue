<template>
  <div class="col-span-3">
    <CoverImage
      class="md:max-h-[400px] sm:max-h-[300px] vs:max-h-[200px] lg:max-h-max"
      :page="page"
    />
    <div class="col-span-3 grid grid-cols-3 lg:gap-4 relative py-4">
      <div
        class="lg:col-span-2 col-span-3 flex vs:flex-col xs:flex-row lg:justify-between justify-center items-center xs:px-4 py-2 gap-4 lg:text-lg md:text-base xm:text-sm vs:text-xs font-semibold dark:text-neutral-200"
      >
        <div class="flex gap-4 xs:w-auto vs:w-full vs:justify-center items-center xs:justify-start">
          <RouterLink :to="{ name: 'pagedetail', params: { id: page.id } }"
            >Bài viết</RouterLink
          >
          <RouterLink :to="{ name: 'pageabout', params: { id: page.id } }"
            >Giới thiệu</RouterLink
          >
          <RouterLink :to="{ name: 'pageusers', params: { id: page.id } }" class="hidden xm:block"
            >Người theo dõi</RouterLink
          >
          <RouterLink :to="{ name: 'pagephotos', params: { id: page.id } }" class="hidden xm:block"
            >Ảnh</RouterLink
          >
          <span class="hidden xm:block">Video</span>
          <PageRouterDropDown :page="page" /> 
        </div>
      </div>
      <div class="lg:col-span-1 col-span-3">
        <div class="flex items-center gap-3 lg:justify-end justify-center">
          <button
            @click="openContactModal"
            class="dark:text-neutral-200 bg-slate-200 dark:bg-slate-800 md:px-4 md:py-2 p-1 shadow-md rounded-md hover:bg-slate-300 dark:hover:bg-slate-900 transition"
          >
            <span class="md:block hidden">Thông tin liên lạc</span>
            <PencilSquareIcon class="w-6 md:hidden" />
          </button>
          <div class="flex flex-col gap-3 items-center">
            <button
              v-if="!checkInLikes && !isLike && !pageStore.pageId"
              class="btn flex gap-1 items-center"
              @click="likePage"
            >
              <HandThumbUpIcon class="w-6" />
              <span>Thích</span>
            </button>
            <button
              v-else-if="
                !checkInPageLikes &&
                !isLike &&
                pageStore.pageId &&
                page.id !== pageStore.pageId
              "
              class="btn flex gap-1 items-center"
              @click="likePage"
            >
              <HandThumbUpIcon class="w-6" />
              <span>Thích</span>
            </button>
            <PageOptionsDropdown
              v-else-if="
                (isLike && !pageStore.pageId) ||
                (checkInLikes && !pageStore.pageId)
              "
              :followers="page.followers"
              :likes="page.likes"
              @followPage="followPage"
              @unfollowPage="unfollowPage"
              @dislikePage="dislikePage"
            />
            <PageOptionsDropdown
              v-else-if="
                (isLike && page.is_page && page.id !== pageStore.pageId) ||
                (checkInPageLikes &&
                  page.is_page &&
                  page.id !== pageStore.pageId)
              "
              :followers="pageFollowers"
              :likes="pageLikes"
              @followPage="followPage"
              @unfollowPage="unfollowPage"
              @dislikePage="dislikePage"
            />
            <button
              v-if="page.id !== pageStore.pageId && !pageStore.pageId"
              @click="sendDirectMessage"
              class="bg-violet-400 hover:bg-violet-600 btn w-full"
            >
              Nhắn tin
            </button>
          </div>
          <ContactModal
            :show="contactIsOpen"
            @closeContactModal="closeContactModal"
          />
        </div>
      </div>
    </div>
    <hr class="col-span-3" />
  </div>
</template>

<script>
import CoverImage from "../../CoverImage.vue";
import DeleteFriendModal from "../../modals/profile/DeleteFriendModal.vue";
import UnfollowedModal from "../../modals/profile/UnfollowedModal.vue";
import FriendOptionsDropdown from "../../dropdown/FriendOptionsDropdown.vue";
import ContactModal from "../../modals/profile/ContactModal.vue";
import PageOptionsDropdown from "../../dropdown/PageOptionsDropdown.vue";
import PageRouterDropDown from "../../dropdown/PageRouterDropDown.vue";

import { PencilSquareIcon, HandThumbUpIcon } from "@heroicons/vue/24/solid";
import { useUserStore } from "../../../stores/user";
import { usePageStore } from "../../../stores/page";
import { useToastStore } from "../../../stores/toast";

export default (await import("vue")).defineComponent({
  components: {
    CoverImage,
    PencilSquareIcon,
    DeleteFriendModal,
    UnfollowedModal,
    FriendOptionsDropdown,
    ContactModal,
    HandThumbUpIcon,
    PageOptionsDropdown,
    PageRouterDropDown,
  },

  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore();
    const toastStore = useToastStore();

    return {
      userStore,
      pageStore,
      toastStore,
    };
  },

  props: {
    user: Object,
    page: Object,
    pageFollowers: Array,
    pageLikes: Array,
  },

  data() {
    return {
      isDeleteFriendOpen: false,
      isUnfollowedOpen: false,
      contactIsOpen: false,
      isLike: false,
    };
  },

  computed: {
    checkCurrentUserInPage() {
      return this.pageStore.pagesList
        .map((page) => page.id)
        .includes(this.$route.params.id);
    },
    checkInLikes() {
      return this.page?.likes
        ?.map((user) => user.id)
        .includes(this.userStore.user.id);
    },
    checkInPageLikes() {
      return this.pageLikes
        ?.map((page) => page.id)
        .includes(this.pageStore.pageId);
    },
  },

  methods: {
    openContactModal() {
      this.contactIsOpen = true;
    },
    closeContactModal() {
      this.contactIsOpen = false;
    },
    sendDirectMessage() {
      axios
        .get(
          `/api/chat/${this.userStore.user.id}/get-or-create/page/${this.$route.params.id}/`
        )
        .then((res) => {
          this.$router.push("/chat");
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    likePage() {
      if (!this.pageStore.pageId) {
        axios
          .post(`/api/page/${this.$route.params.id}/like/`)
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã thích ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
              this.isLike = true;
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .post(
            `/api/page/${this.pageStore.pageId}/like/${this.$route.params.id}/`
          )
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã thích ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
              this.isLike = true;
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    followPage() {
      if (!this.pageStore.pageId) {
        axios.post(`/api/page/${this.$route.params.id}/follow/`).then((res) => {
          if (res.data.success) {
            this.toastStore.showToast(
              5000,
              `Đã theo dõi ${this.page.name}`,
              "bg-emerald-400 text-white"
            );
          } else {
            this.toastStore.showToast(
              5000,
              "Thao tác thất bại",
              "bg-rose-400 text-white"
            );
          }
        });
      } else {
        axios
          .post(
            `/api/page/${this.pageStore.pageId}/follow/page/${this.$route.params.id}/`
          )
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã theo dõi ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          });
      }
    },

    dislikePage() {
      if (!this.pageStore.pageId) {
        axios
          .post(`/api/page/${this.$route.params.id}/dislike/`)
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã bỏ thích ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          });
      } else {
        axios
          .post(
            `/api/page/${this.pageStore.pageId}/dislike/page/${this.$route.params.id}/`
          )
          .then((res) => {
            console.log(res.data);
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã bỏ thích ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          });
      }
    },

    unfollowPage() {
      if (!this.pageStore.pageId) {
        axios
          .post(`/api/page/${this.$route.params.id}/unfollow/`)
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã bỏ theo dõi ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          });
      } else {
        axios
          .post(
            `/api/page/${this.pageStore.pageId}/unfollow/page/${this.$route.params.id}/`
          )
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                5000,
                `Đã bỏ theo dõi ${this.page.name}`,
                "bg-emerald-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                5000,
                "Thao tác thất bại",
                "bg-rose-400 text-white"
              );
            }
          });
      }
    },
  },
});
</script>

<style scoped>
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

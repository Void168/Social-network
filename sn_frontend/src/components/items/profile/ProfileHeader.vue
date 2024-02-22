<template>
  <div class="col-span-3">
    <CoverImage
      class="md:max-h-[400px] sm:max-h-[300px] xs:max-h-[200px] lg:max-h-max"
      :user="user"
    />
    <div class="col-span-3 grid grid-cols-3 gap-4 relative py-4">
      <div class="col-span-1 lg:block hidden"></div>
      <div
        class="lg:col-span-2 col-span-3 flex lg:justify-between justify-center items-center px-4 py-2 gap-4 lg:text-lg md:text-base xm:text-sm xs:text-xs font-semibold dark:text-neutral-200"
      >
        <div class="flex gap-4">
          <RouterLink :to="{ name: 'profiledetail', params: { id: user.id } }"
            >Bài viết</RouterLink
          >
          <RouterLink
            :to="{ name: 'about', params: { id: userStore.user.id } }"
            >Giới thiệu</RouterLink
          >
          <RouterLink :to="{ name: 'photos', params: { id: user.id } }"
            >Ảnh</RouterLink
          >
          <div class="flex gap-1">
            <RouterLink :to="{ name: 'friends', params: { id: user.id } }">
              <span>Bạn bè</span>
            </RouterLink>
            <div
              class="flex gap-2"
              v-if="user.id === userStore.user.id && !pageStore.pageId"
            >
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
            class="dark:text-neutral-200 bg-slate-300 dark:bg-slate-800 md:px-4 md:py-2 p-1 shadow-md rounded-md hover:bg-slate-300 dark:hover:bg-slate-900 transition"
          >
            <span class="md:block hidden">Thông tin liên lạc</span>
            <PencilSquareIcon class="w-6 md:hidden" />
          </button>
          <ContactModal
            :show="contactIsOpen"
            @closeContactModal="closeContactModal"
          />
        </div>
      </div>
    </div>
    <hr class="col-span-3 dark:border-slate-600 border-slate-300" />
  </div>
</template>

<script>
import CoverImage from "../../CoverImage.vue";
import DeleteFriendModal from "../../modals/profile/DeleteFriendModal.vue";
import UnfollowedModal from "../../modals/profile/UnfollowedModal.vue";
import FriendOptionsDropdown from "../../dropdown/FriendOptionsDropdown.vue";
import ContactModal from "../../modals/profile/ContactModal.vue";

import { PencilSquareIcon } from "@heroicons/vue/24/solid";
import { useUserStore } from "../../../stores/user";
import { usePageStore } from "../../../stores/page";
import { useToastStore } from "../../../stores/toast"

export default (await import("vue")).defineComponent({
  components: {
    CoverImage,
    PencilSquareIcon,
    DeleteFriendModal,
    UnfollowedModal,
    FriendOptionsDropdown,
    ContactModal,
  },

  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore();
    const toastStore = useToastStore()

    return {
      userStore,
      pageStore,
      toastStore
    };
  },

  props: {
    user: Object,
    followers: Array,
    friends: Array,
    friendshipRequest: Array,
    yourRequest: Array,
  },

  data() {
    return {
      isDeleteFriendOpen: false,
      isUnfollowedOpen: false,
      contactIsOpen: false,
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

  methods: {
    openDeleteFriendModal() {
      this.isDeleteFriendOpen = true;
    },

    closeDeleteFriendModal() {
      this.isDeleteFriendOpen = false;
    },

    openUnfollowedModal() {
      this.isUnfollowedOpen = true;
    },

    closeUnfollowedModal() {
      this.isUnfollowedOpen = false;
    },

    openContactModal() {
      this.contactIsOpen = true;
    },
    closeContactModal() {
      this.contactIsOpen = false;
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

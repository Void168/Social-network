<template>
  <div class="flex justify-center items-center w-full mx-auto dark:bg-slate-700 bg-white">
    <div class="flex flex-col 2xl:w-[80%] w-full">
      <div
        class="relative justify-end lg:h-[500px] sm:h-[300px] h-[200px] bg-cover bg-center bg-no-repeat rounded-b-lg bg-fit w-full"
        :style="bgImage"
      >
        <button
          @click="openCoverImageModal"
          class="bg-gray-200 text-white bg-opacity-20 px-4 py-2 rounded-lg absolute right-4 bottom-4 hover:bg-opacity-70 transition-colors shadow-lg"
        >
          Chọn ảnh
        </button>
        <GroupCoverImageModal
          :show="isCoverImageOpen"
          @closeCoverImageModal="closeCoverImageModal"
        />
      </div>
      <div
        class="flex sm:justify-between sm:flex-row flex-col sm:my-8 my-4 md:mx-1 lm:mx-4 mx-4"
      >
        <div class="flex flex-col gap-2">
          <h1 class="sm:text-2xl text-3xl font-bold">{{ group.name }}</h1>
          <div class="flex items-center gap-2">
            <GlobeAsiaAustraliaIcon
              v-if="!group.is_private_group"
              class="w-4"
            />
            <LockClosedIcon v-else class="w-4" />
            <h4 class="sm:text-sm">
              {{ group.is_private_group ? "Nhóm riêng tư" : "Nhóm công khai" }}
              &middot; {{ group.members_count }} thành viên
            </h4>
          </div>
          <div class="flex gap-1 items-center sm:mb-0 mb-4">
            <img
            loading="lazy"
              :src="group?.admin?.get_avatar"
              alt=""
              class="w-8 h-8 rounded-full"
            />
            <!-- v-if="isUserInGroup" -->
            <div v-for="moderator in group?.moderators" :key="moderator.id">
              <img
              loading="lazy"
                :src="moderator?.information?.get_avatar"
                alt="admin-avatar"
                class="w-8 h-8 rounded-full shadow-lg"
              />
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-end">
          <div
            class="flex lg:gap-4 gap-2 lg:text-lg md:text-xs"
            v-if="isUserInGroup"
          >
            <button
              class="flex items-center justify-center gap-1 sm:px-4 sm:py-2 font-semibold bg-emerald-500 hover:bg-emerald-400 rounded-lg duration-75 sm:max-w-max w-full sm:text-base md:text-sm text-xs"
            >
              <PlusIcon class="w-4" />
              Mời</button
            ><button
              class="flex items-center justify-center gap-1 sm:px-4 sm:py-2 font-semibold dark:bg-slate-800 bg-slate-300 dark:hover:bg-slate-900 rounded-lg duration-75 sm:max-w-max w-full sm:text-base md:text-sm text-xs"
            >
              <ShareIcon class="w-4" />
              Chia sẻ
            </button>
            <button
              @click="leaveGroup"
              class="flex items-center justify-center gap-1 sm:px-4 sm:py-2 font-semibold dark:bg-slate-800 bg-slate-300 dark:hover:bg-slate-900 rounded-lg duration-75 sm:max-w-max w-full sm:text-base md:text-sm text-xs"
            >
              <UserMinusIcon class="w-4" />
              Rời nhóm
            </button>
            <div class="flex items-center gap-2 sm:hidden">
              <MagnifyingGlassIcon
                @click="$emit('openModal')"
                class="w-10 p-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-800/70 duration-75 cursor-pointer"
              />

              <EllipsisHorizontalIcon
                class="w-10 p-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-800/70 duration-75 cursor-pointer"
              />
            </div>
          </div>
          <button
            @click="joinGroup"
            class="flex items-center gap-1 px-4 py-2 font-semibold bg-emerald-500 hover:bg-emerald-400 rounded-lg duration-75 sm:max-w-max w-full"
            v-else-if="!isJoinRequest"
          >
            <UserPlusIcon class="w-4" />
            Tham gia nhóm
          </button>
          <button
            @click="openCancelRequestModal"
            class="flex items-center gap-1 px-4 py-2 font-semibold bg-emerald-500 hover:bg-emerald-400 rounded-lg duration-75 sm:max-w-max w-full"
            v-else-if="isJoinRequest"
          >
            <UserPlusIcon class="w-4" />
            Đã gửi yêu cầu
          </button>
          <CancelRequestModal
            :show="isCancelOpen"
            @closeModal="closeCancelRequestModal"
            @cancelJoinRequest="cancelJoinRequest"
          />
          <ListQuestionModal
            :show="isQuestionOpen"
            @closeQuestionModal="closeQuestionModal"
            :group="group"
            :questions="questions"
          />
        </div>
      </div>
      <hr class="border dark:border-slate-600 mx-4" />
      <div class="flex sm:justify-between justify-end items-center xm:mx-4">
        <div
          class="flex items-center lg:text-base md:text-sm sm:text-base xm:text-sm text-xs"
        >
          <RouterLink
            :to="{ name: 'groupdiscuss', params: { id: group?.id } }"
            class="font-medium xm:p-4 p-2 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            Thảo luận
          </RouterLink>
          <RouterLink
            :to="{ name: 'groupabout', params: { id: group?.id } }"
            class="font-medium xm:p-4 p-2 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            Về nhóm
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupmembers', params: { id: group?.id } }"
            class="font-medium xm:p-4 p-2 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            Thành viên
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupmedia', params: { id: group?.id } }"
            class="font-medium xm:p-4 p-2 lm:flex sm:flex hidden justify-center dark:hover:bg-slate-600 duration-75 md:hidden"
          >
            File Phương Tiện
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupfile', params: { id: group?.id } }"
            class="font-medium xm:p-4 p-2 lm:flex sm:flex hidden justify-center dark:hover:bg-slate-600 duration-75 md:hidden"
          >
            File
          </RouterLink>
          <GroupRouterDropdown :group="group" />
        </div>
        <div class="sm:flex items-center gap-2 hidden">
          <MagnifyingGlassIcon
            @click="$emit('openModal')"
            class="lg:w-9 p-2 md:w-8 w-9 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-800/70 duration-75 cursor-pointer"
          />

          <EllipsisHorizontalIcon
            class="lg:w-9 p-2 md:w-8 w-9 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-800/70 duration-75 cursor-pointer"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { RouterLink } from "vue-router";
import ListQuestionModal from "../../modals/group/ListQuestionModal.vue";
import GroupCoverImageModal from "../../modals/group/GroupCoverImageModal.vue";
import GroupRouterDropdown from "../../dropdown/GroupRouterDropdown.vue";
import CancelRequestModal from "../../modals/group/CancelRequestModal.vue";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  PlusIcon,
  ShareIcon,
  UserPlusIcon,
  UserMinusIcon,
  EllipsisHorizontalIcon,
  MagnifyingGlassIcon,
} from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    PlusIcon,
    ShareIcon,
    UserPlusIcon,
    UserMinusIcon,
    EllipsisHorizontalIcon,
    MagnifyingGlassIcon,
    GroupCoverImageModal,
    ListQuestionModal,
    CancelRequestModal,
    GroupRouterDropdown,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  props: {
    group: Object,
    isUserInGroup: Boolean,
    isJoinRequest: Boolean,
  },

  data() {
    return {
      isOpen: false,
      isQuestionOpen: false,
      isCoverImageOpen: false,
      questions: [],
      isCancelOpen: false,
    };
  },

  computed: {
    bgImage() {
      return {
        backgroundImage: `url(${this.group?.get_cover_image})`,
      };
    },
  },

  mounted() {
    this.getGroupQuestions();
  },

  methods: {
    closeQuestionModal() {
      this.isQuestionOpen = false;
    },
    openCoverImageModal() {
      this.isCoverImageOpen = true;
    },
    closeCoverImageModal() {
      this.isCoverImageOpen = false;
    },
    openCancelRequestModal() {
      this.isCancelOpen = true;
    },
    closeCancelRequestModal() {
      this.isCancelOpen = false;
    },
    async getGroupQuestions() {
      await axios
        .get(`/api/group/${this.$route.params.id}/get-questions/`)
        .then((res) => {
          this.questions = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    joinGroup() {
      if (this.group.is_private_group && !this.isUserInGroup) {
        axios
          .post(`/api/group/${this.group?.id}/join/request/`)
          .then((res) => {
            if (this.questions?.length) {
              this.isQuestionOpen = true;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .post(`/api/group/public/${this.group?.id}/join/`)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    leaveGroup() {
      axios
        .post(`/api/group/${this.$route.params.id}/leave/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cancelJoinRequest() {
      axios
        .delete(`/api/group/${this.group.id}/join/cancel/`)
        .then((res) => {
          this.isCancelOpen = false
          if (res.data.message) {
            this.toastStore.showToast(
              3000,
              "Hủy yêu cầu thành công.",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0)
            }, 4000)
          }
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3000,
            "Hủy yêu cầu thất bại.",
            "bg-emerald-500 text-white"
          );
        });
    },
  },
});
</script>

<style scoped>
.router-link-active {
  --tw-text-opacity: 1;
  color: rgb(16 185 129 / var(--tw-text-opacity));
  position: relative;
}

.router-link-active::before {
  --tw-text-opacity: 1;
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  width: 100%;
  z-index: 10;
  background-color: rgb(16 185 129 / var(--tw-text-opacity));
}
</style>

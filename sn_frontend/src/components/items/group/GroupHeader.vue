<template>
  <div class="flex justify-center items-center w-full mx-auto bg-slate-700">
    <div class="flex flex-col w-[80%]">
      <div
        class="relative justify-end h-[500px] bg-cover bg-center bg-no-repeat rounded-b-lg bg-fit w-full"
        :style="bgImage"
      >
        <button
          @click="openCoverImageModal"
          class="bg-gray-200 text-white bg-opacity-20 px-4 py-2 rounded-lg absolute right-4 bottom-4 hover:bg-opacity-70 transition-colors shadow-lg"
        >
          Chọn ảnh
        </button>
        <GroupCoverImageModal :show="isCoverImageOpen" @closeCoverImageModal="closeCoverImageModal"/>
      </div>
      <div class="flex justify-between my-8 mx-4">
        <div class="flex flex-col gap-2">
          <h1 class="text-2xl font-bold">{{ group.name }}</h1>
          <div class="flex items-center gap-2">
            <GlobeAsiaAustraliaIcon
              v-if="!group.is_private_group"
              class="w-4"
            />
            <LockClosedIcon v-else class="w-4" />
            <h4 class="text-sm">
              {{ group.is_private_group ? "Nhóm riêng tư" : "Nhóm công khai" }}
              &middot; {{ group.members_count }} thành viên
            </h4>
          </div>
          <div class="flex gap-1 items-center">
            <img
              :src="group?.admin?.get_avatar"
              alt=""
              class="w-8 h-8 rounded-full"
            />
            <!-- v-if="isUserInGroup" -->
            <div v-for="moderator in group?.moderators" :key="moderator.id">
              <img
                :src="moderator?.information?.get_avatar"
                alt="admin-avatar"
                class="w-8 h-8 rounded-full shadow-lg"
              />
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-end">
          <div class="flex gap-4" v-if="isUserInGroup">
            <button
              class="flex items-center gap-1 px-4 py-2 font-semibold bg-emerald-500 hover:bg-emerald-400 rounded-lg duration-75"
            >
              <PlusIcon class="w-4" />
              Mời</button
            ><button
              class="flex items-center gap-1 px-4 py-2 font-semibold dark:bg-slate-800 bg-slate-300 dark:hover:bg-slate-900 rounded-lg duration-75"
            >
              <ShareIcon class="w-4" />
              Chia sẻ
            </button>
            <button
              @click="leaveGroup"
              class="flex items-center gap-1 px-4 py-2 font-semibold dark:bg-slate-800 bg-slate-300 dark:hover:bg-slate-900 rounded-lg duration-75"
            >
              <UserMinusIcon class="w-4" />
              Rời nhóm
            </button>
          </div>
          <button
            @click="joinGroup"
            class="flex items-center gap-1 px-4 py-2 font-semibold bg-emerald-500 hover:bg-emerald-400 rounded-lg duration-75"
            v-else
          >
            <UserPlusIcon class="w-4" />
            Tham gia nhóm
          </button>
          <ListQuestionModal
            :show="isQuestionOpen"
            @closeQuestionModal="closeQuestionModal"
            :group="group"
            :questions="questions"
          />
        </div>
      </div>
      <hr class="border dark:border-slate-600 mx-4" />
      <div class="flex justify-between items-center mx-4">
        <div class="flex items-center">
          <RouterLink
            :to="{ name: 'groupdiscuss', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            Thảo luận
          </RouterLink>
          <RouterLink
            :to="{ name: 'groupabout', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            Về nhóm
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupmembers', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            Thành viên
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupmedia', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            File Phương Tiện
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupfile', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            File
          </RouterLink>
        </div>
        <div class="flex items-center gap-2">
          <MagnifyingGlassIcon
            @click="$emit('openModal')"
            class="w-10 p-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-800/70 duration-75 cursor-pointer"
          />

          <EllipsisHorizontalIcon
            class="w-10 p-2 rounded-lg dark:bg-slate-800 dark:hover:bg-slate-800/70 duration-75 cursor-pointer"
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
  },

  data() {
    return {
      isOpen: false,
      isQuestionOpen: false,
      isCoverImageOpen: false,
      questions: [],
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
    openCoverImageModal(){
      this.isCoverImageOpen = true
    },
    closeCoverImageModal(){
      this.isCoverImageOpen = false
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
            console.log(res.data);
            if (this.questions?.length) {
              this.isQuestionOpen = true;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } 
      else{
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
  height: 4px;
  width: 100%;
  z-index: 10;
  background-color: rgb(16 185 129 / var(--tw-text-opacity));
}
</style>

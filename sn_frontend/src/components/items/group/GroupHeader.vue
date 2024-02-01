<template>
  <div class="flex justify-center items-center w-full mx-auto bg-slate-700">
    <div class="flex flex-col w-[80%]">
      <div
        class="relative justify-end h-[500px] bg-cover bg-no-repeat"
        :style="bgImage"
      >
        <button
          @click="openModal"
          class="bg-gray-200 text-white bg-opacity-20 px-4 py-2 rounded-lg absolute right-4 bottom-4 hover:bg-opacity-70 transition-colors shadow-lg"
        >
          Chọn ảnh
        </button>
      </div>
      <div class="flex justify-between my-8">
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
          <img
            :src="group?.admin?.get_avatar"
            alt=""
            class="w-8 h-8 rounded-full"
            v-if="isUserInGroup"
          />
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
          </div>
          <button
            @click="joinGroup"
            class="flex items-center gap-1 px-4 py-2 font-semibold bg-emerald-500 hover:bg-emerald-400 rounded-lg duration-75"
            v-else
          >
            <UserPlusIcon class="w-4" />
            Tham gia nhóm
          </button>
        </div>
      </div>
      <hr class="border dark:border-slate-600 mx-4" />
      <div class="flex justify-between items-center">
        <div class="flex items-center mx-4">
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
            :to="{ name: 'groupdetail', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            File Phương Tiện
          </RouterLink>
          <RouterLink
            v-if="isUserInGroup"
            :to="{ name: 'groupdetail', params: { id: group?.id } }"
            class="font-medium p-4 flex justify-center dark:hover:bg-slate-600 duration-75"
          >
            File
          </RouterLink>
        </div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { RouterLink } from "vue-router";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  PlusIcon,
  ShareIcon,
  UserPlusIcon,
} from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    PlusIcon,
    ShareIcon,
    UserPlusIcon,
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
    };
  },

  computed: {
    bgImage() {
      return {
        backgroundImage: `url(${this.group?.get_cover_image})`,
      };
    },
  },

  methods: {
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
    joinGroup() {
      if (this.group.is_private_group && !this.isUserInGroup) {
        axios
          .post(`/api/group/${this.group?.id}/join/request/`)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.log(error);
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

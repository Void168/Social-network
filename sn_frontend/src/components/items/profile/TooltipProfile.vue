<template>
  <div
    class="w-[400px] min-h-max bg-slate-800 absolute top-[-140px] left-[-150px] shadow-md rounded-xl p-4 space-y-4"
  >
    <div class="grid grid-cols-4 space-x-4">
      <div class="col-span-1">
        <router-link
          :to="{
            name: user.is_page ? 'page': 'profile',
            params: { id: user.id },
          }"
        >
          <img :src="user.get_avatar" class="w-20 h-20 rounded-full" />
        </router-link>
      </div>
      <div class="col-span-3 space-y-2">
        <router-link
          :to="{
            name: user.is_page ? 'page' : 'profile',
            params: { id: user.id },
          }"
        >
          <h2 class="text-lg font-bold text-center">{{ user.name }}</h2>
        </router-link>
        <span v-if="user.living_city" class="flex gap-2">
          <HomeIcon class="w-10 mb-auto" />
          <h3>
            Sống tại <strong>{{ user.living_city }}</strong>
          </h3>
        </span>
      </div>
    </div>
    <div class="flex justify-center gap-2">
      <button
        class="btn text-sm min-w-max flex gap-2 items-center justify-center"
        v-if="user.id !== userStore.user.id"
      >
        <ChatBubbleOvalLeftIcon class="w-6" />
        <h4>Nhắn tin</h4>
      </button>
      <button
        class="btn text-sm min-w-max gap-2 flex items-center justify-center"
        v-if="user.id === userStore.user.id && !checkIsFriend"
        @click="openModal"
      >
        <PlusIcon class="w-4" />
        <h4>Thêm vào tin</h4>
      </button>
      <CreateStoryModal
        :show="isOpen"
        :isTextStory="isTextStory"
        @closeModal="closeModal"
        @openTextStory="openTextStory"
        @closeTextStory="closeTextStory"
      />
      <button
        class="btn min-w-max gap-2 flex items-center justify-center"
        v-if="user.id !== userStore.user.id && !checkIsFriend"
      >
        <UserPlusIcon class="w-6" />
        <h4>Thêm bạn bè</h4>
      </button>
      <button
        class="btn text-sm min-w-max gap-2 flex items-center justify-center"
        v-if="user.id === userStore.user.id && !checkIsFriend"
      >
        <PencilIcon class="w-4" />
        <h4>Chỉnh sửa trang cá nhân</h4>
      </button>
      <button
        class="btn min-w-max gap-2 flex items-center justify-center"
        v-else
      >
        <UsersIcon class="w-6" />
        <h4>Bạn bè</h4>
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {
  HomeIcon,
  ChatBubbleOvalLeftIcon,
  UserPlusIcon,
  UsersIcon,
  PencilIcon,
  PlusIcon,
} from "@heroicons/vue/24/solid";
import { useUserStore } from "../../../stores/user";

import CreateStoryModal from "../../modals/story/CreateStoryModal.vue";
export default (await import("vue")).defineComponent({
  components: {
    HomeIcon,
    ChatBubbleOvalLeftIcon,
    UserPlusIcon,
    UsersIcon,
    PencilIcon,
    PlusIcon,
    CreateStoryModal,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    user: Object,
  },

  data() {
    return {
      currentUserFriends: [],
      isOpen: false,
      isTextStory: false,
    };
  },

  computed: {
    checkIsFriend() {
      return this.currentUserFriends.map((fr) => fr.id).includes(this.user.id);
    },
  },

  mounted() {
    this.getFriends();
  },

  methods: {
    async getFriends() {
      await axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          this.currentUserFriends = res.data.friends;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    sendFriendshipRequest() {
      axios
        .post(`/api/friends/${this.user.id}/request/`)
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
    openModal() {
      this.isOpen = true;
      this.isTextStory = false;
    },
    closeModal() {
      this.isOpen = false;
      this.isTextStory = false;
    },
    openTextStory() {
      this.isTextStory = true;
    },
    closeTextStory() {
      this.isTextStory = false;
    },
  },
});
</script>

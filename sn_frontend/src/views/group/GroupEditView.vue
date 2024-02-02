<template>
  <div class="flex flex-col items-center justify-center py-6 gap-4 w-[50%]">
    <div class="w-full dark:bg-slate-800 rounded-lg p-4">
      <h1 class="font-bold text-2xl">Thiết lập nhóm</h1>
      <div class="my-4">
        <div
          class="flex"
          :class="
            isNameOpen
              ? 'flex-col justify-start items-start gap-2'
              : 'items-center justify-between'
          "
        >
          <h3 class="text-lg font-semibold">Tên và mô tả</h3>
          <PencilIcon
            @click="toggleEditName"
            v-if="!isNameOpen"
            class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
          />
          <div v-else class="w-full space-y-2">
            <MUILikedInput :placeholder="'Tên'" v-model="group.name" />
            <textarea
              v-model="group.biography"
              class="p-4 w-full bg-gray-100 rounded-lg resize-none border"
              cols="30"
              rows="4"
              placeholder="Mô tả về nhóm"
            ></textarea>
            <div class="flex justify-end items-center gap-2">
              <button
                @click="toggleEditName"
                class="px-4 py-2 font-medium text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75 rounded-lg"
              >
                Hủy
              </button>
              <button
                @click="submitNameForm"
                :disabled="name === group.name && biography === ''"
                class="px-4 py-2 font-medium rounded-lg"
                :class="
                  name === group.name && biography === ''
                    ? 'text-neutral-400 bg-slate-600 cursor-not-allowed'
                    : 'text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75'
                "
              >
                Lưu
              </button>
            </div>
          </div>
        </div>
        <hr class="border border-slate-700 my-4" />
        <EditGroupRadioItem
          :name="'Ẩn nhóm'"
          :group="group"
          :isOpen="isShowOpen"
          :options="showSelections"
          :selectedOption="showOption"
          @getOption="getShowOption"
          @toggle="toggleEditShow"
          @submit="submitShowForm"
        />
        <hr class="border border-slate-700 my-4" />
        <div class="flex items-center justify-between">
          <div class="space-y-1">
            <h3 class="text-lg font-semibold">Vị trí</h3>
            <h5 class="text-sm">
              {{ group?.show_group ? "Ẩn" : "Hiên thị" }}
            </h5>
          </div>
          <PencilIcon
            class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
          />
        </div>
        <hr class="border border-slate-700 my-4" />
        <div
          class="flex"
          :class="
            isUrlOpen
              ? 'flex-col justify-start items-start gap-2'
              : 'items-center justify-between'
          "
        >
          <div class="space-y-1">
            <h3 class="text-lg font-semibold">Địa chỉ web</h3>
            <h5 class="text-sm" v-if="!isUrlOpen">
              {{ baseUrl + route.path.slice(0, route.path.length - 5) }}
            </h5>
          </div>
          <PencilIcon
            v-if="!isUrlOpen"
            @click="toggleWebShow"
            class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
          />
          <div v-else class="w-full space-y-4">
            <MUILikedInput :placeholder="'Tên'" v-model="url" />
            <div class="flex justify-end items-center gap-2">
              <button
                @click="toggleWebShow"
                class="px-4 py-2 font-medium text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75 rounded-lg"
              >
                Hủy
              </button>
              <button
                :disabled="name === group.name && biography === ''"
                class="px-4 py-2 font-medium rounded-lg"
                :class="
                  name === group.name && biography === ''
                    ? 'text-neutral-400 bg-slate-600 cursor-not-allowed'
                    : 'text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75'
                "
              >
                Lưu
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="w-full dark:bg-slate-800 rounded-lg p-4">
      <h1 class="font-bold text-2xl">Quản lý thành viên</h1>
      <div class="my-4">
        <EditGroupRadioItem
          :name="'Ai có thể tham gia nhóm'"
          :group="group"
          :isOpen="isRequestOpen"
          :options="requestSelections"
          :selectedOption="requestOption"
          @getOption="getRequestOption"
          @toggle="toggleRequestShow"
          @submit="submitRequestForm"
        />
        <hr class="border border-slate-700 my-4" />
        <div v-if="userStore.user.id === group?.admin?.id">
          <div class="flex items-center justify-between">
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Thêm quản trị viên</h3>
              <h5 class="text-sm">
                {{ group?.show_group ? "Ẩn" : "Hiên thị" }}
              </h5>
            </div>
            <PencilIcon
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
          </div>
          <hr class="border border-slate-700 my-4" />
        </div>
        <div>
          <div class="flex items-center justify-between">
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Danh sách cấm</h3>
            </div>
            <PencilIcon
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="w-full dark:bg-slate-800 rounded-lg p-4">
      <h1 class="font-bold text-2xl">Quản lý nội dung thảo luận</h1>
      <div class="my-4">
        <EditGroupRadioItem
          :name="'Đăng ẩn danh'"
          :group="group"
          :isOpen="isAnonymousOpen"
          :options="onOffSelections"
          :selectedOption="anonymousOption"
          @getOption="getAnonymousOption"
          @toggle="toggleAnonymousShow"
          @submit="submitAnonymousForm"
        />
        <hr class="border border-slate-700 my-4" />
        <EditGroupRadioItem
          :name="'Ai có thể đăng'"
          :group="group"
          :isOpen="isWhoCanPostOpen"
          :options="postSelections"
          :selectedOption="whoCanPostOption"
          @getOption="getWhoCanPostOption"
          @toggle="toggleWhoCanPostShow"
          @submit="submitPostForm"
        />
        <hr class="border border-slate-700 my-4" />
        <EditGroupRadioItem
          :name="'Cần phê duyệt bài viết'"
          :group="group"
          :isOpen="isPendingPostOpen"
          :options="onOffSelections"
          :selectedOption="pendingPostOption"
          @getOption="getPendingPostOption"
          @toggle="togglePendingPostShow"
          @submit="submitPendingForm"
        />
        <hr class="border border-slate-700 my-4" />
        <EditGroupRadioItem
          :name="'Ai có thể tham gia cuộc thảo luận'"
          :group="group"
          :isOpen="isPollOpen"
          :options="postSelections"
          :selectedOption="pollOption"
          @getOption="getPollOption"
          @toggle="togglePollShow"
          @submit="submitPollForm"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { PencilIcon } from "@heroicons/vue/20/solid";
import { useRoute } from "vue-router";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import MUILikedInput from "../../components/input/MUILikedInput.vue";
import CustomListRadio from "../../components/input/CustomListRadioButton.vue";
import EditGroupRadioItem from "../../components/items/group/EditGroupRadioItem.vue";

import selection from "../../data/selection";
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/solid";

export default {
  name: "groupedit",
  components: {
    PencilIcon,
    MUILikedInput,
    EyeIcon,
    EyeSlashIcon,
    CustomListRadio,
    EditGroupRadioItem,
  },
  setup() {
    const route = useRoute();
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      route,
      userStore,
      toastStore,
    };
  },
  props: {
    group: Object,
  },

  data() {
    return {
      baseUrl: import.meta.env.VITE_CLIENT_URL,
      isNameOpen: false,
      name: this.group.name,
      biography: this.group.biography,
      isShowOpen: false,
      showSelections: selection.showSelections,
      showOption: this.group.show_group,
      showOptionName: "",
      isUrlOpen: false,
      url: `http://localhost:5173/groups/${this.group.id}`,
      isRequestOpen: false,
      requestSelections: selection.requestSelections,
      requestOptionName: "",
      requestOption: this.group.anyone_can_join,
      isAddModeratorOpen: false,
      isBanListOpen: false,
      isAnonymousOpen: false,
      onOffSelections: selection.onOffSelections,
      anonymousOptionName: "",
      anonymousOption: this.group.anonymous_post,
      isWhoCanPostOpen: false,
      postSelections: selection.postSelections,
      whoCanPostOptionName: "",
      whoCanPostOption: this.group.anyone_can_post,
      isPendingPostOpen: false,
      pendingPostOption: this.group.pending_post,
      isPollOpen: false,
      pollOption:  this.group.anyone_can_poll,
    };
  },

  beforeUpdate() {

  },

  beforeMount() {
    console.log(this.group);
  },

  methods: {
    toggleEditName() {
      this.isNameOpen = !this.isNameOpen;
    },
    toggleEditShow() {
      this.isShowOpen = !this.isShowOpen;
      this.showOption = this.group.show_group;
    },
    toggleWebShow() {
      this.isUrlOpen = !this.isUrlOpen;
    },
    toggleRequestShow() {
      this.isRequestOpen = !this.isRequestOpen;
      this.requestOption = this.group.anyone_can_join;
    },
    toggleAnonymousShow() {
      this.isAnonymousOpen = !this.isAnonymousOpen;
      this.anonymousOption = this.group.anonymous_post;
    },
    toggleWhoCanPostShow() {
      this.isWhoCanPostOpen = !this.isWhoCanPostOpen;
      this.whoCanPostOption = this.group.anyone_can_post;
    },
    togglePendingPostShow() {
      this.isPendingPostOpen = !this.isPendingPostOpen;
      this.pendingPostOption = this.group.pending_post;
    },
    togglePollShow() {
      this.isPollOpen = !this.isPollOpen;
      this.pendingPostOption = this.group.anyone_can_poll;
    },
    getShowOption(data) {
      this.showOptionName = data.name;
      if (data.name === "Hiển thị") {
        this.showOption = true;
      } else {
        this.showOption = false;
      }
    },
    getRequestOption(data) {
    this.requestOptionName = data.name;
      if (data.name === "Trang cá nhân và trang") {
        this.requestOption = true;
      } else {
        this.requestOption = false;
      }
    },
    getAnonymousOption(data) {
      this.anonymousOptionName = data.name;
      if (data.name === "Bật") {
        this.anonymousOption = true;
      } else {
        this.anonymousOption = false;
      }
    },
    getWhoCanPostOption(data) {
      this.whoCanPostOptionName = data.name;
      if (data.name === "Bất cứ ai trong nhóm") {
        this.whoCanPostOption = true;
      } else {
        this.whoCanPostOption = false;
      }
    },
    getPendingPostOption(data) {
      if (data.name === "Bật") {
        this.pendingPostOption = true;
      } else {
        this.pendingPostOption = false;
      }
    },
    getPollOption(data) {
      if (data.name === "Bất cứ ai trong nhóm") {
        this.pollOption = true;
      } else {
        this.pollOption = false;
      }
    },
    submitNameForm() {
      let formData = new FormData();

      formData.append("name", this.group.name);
      formData.append("biography", this.group.biography);

      axios
        .post(`/api/group/${this.group.id}/info/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitShowForm() {
      axios
        .post(`/api/group/${this.group?.id}/show-group/`, {
          show_group: this.showOption,
        })
        .then((res) => {
          this.isShowOpen = false;
          this.toastStore.showToast(
            3500,
            "Đã lưu thông tin chỉnh sửa.",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chỉnh sửa thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
    submitRequestForm() {
      axios
        .post(`/api/group/${this.group?.id}/request-join-group/`, {
          anyone_can_join: this.requestOption,
        })
        .then((res) => {
          this.isRequestOpen = false;
          this.toastStore.showToast(
            3500,
            "Đã lưu thông tin chỉnh sửa.",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chỉnh sửa thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
    submitAnonymousForm() {
      axios
        .post(`/api/group/${this.group?.id}/set-anonymous-post/`, {
          anonymous_post: this.anonymousOption,
        })
        .then((res) => {
          this.isAnonymousOpen = false;
          this.toastStore.showToast(
            3500,
            "Đã lưu thông tin chỉnh sửa.",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chỉnh sửa thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
    submitPostForm() {
      axios
        .post(`/api/group/${this.group?.id}/set-anyone-post/`, {
          anyone_can_post: this.whoCanPostOption,
        })
        .then((res) => {
          // console.log(res.data)
          this.isWhoCanPostOpen = false;
          this.toastStore.showToast(
            3500,
            "Đã lưu thông tin chỉnh sửa.",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chỉnh sửa thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
    submitPendingForm() {
      axios
        .post(`/api/group/${this.group?.id}/set-pending-post/`, {
          pending_post: this.pendingPostOption,
        })
        .then((res) => {
          console.log(res.data)
          this.isPendingPostOpen = false;
          this.toastStore.showToast(
            3500,
            "Đã lưu thông tin chỉnh sửa.",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chỉnh sửa thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
    submitPollForm() {
      axios
        .post(`/api/group/${this.group?.id}/set-anyone-poll/`, {
          anyone_can_poll: this.pollOption,
        })
        .then((res) => {
          // console.log(res.data)
          this.isPollOpen = false;
          this.toastStore.showToast(
            3500,
            "Đã lưu thông tin chỉnh sửa.",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chỉnh sửa thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
  },
};
</script>

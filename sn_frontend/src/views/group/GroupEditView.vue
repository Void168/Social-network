<template>
  <div class="flex flex-col items-center justify-center py-6 gap-4 w-[50%]">
    <div class="w-full dark:bg-slate-800 rounded-lg p-4">
      <h1 class="font-bold text-2xl">Thiết lập nhóm</h1>
      <div class="my-4">
        <div>
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
                v-model="biography"
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
        </div>
        <div>
          <div
            class="flex"
            :class="
              isShowOpen
                ? 'flex-col justify-start items-start gap-2'
                : 'items-center justify-between'
            "
          >
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Ẩn nhóm</h3>
              <h5 class="text-sm" v-if="!isShowOpen">
                {{ group?.show_group ? "Ẩn" : "Hiên thị" }}
              </h5>
            </div>
            <PencilIcon
              v-if="!isShowOpen"
              @click="toggleEditShow"
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
            <div v-else class="w-full space-y-2">
              <div
                v-for="showSelection in showSelections"
                :key="showSelection.id"
                class="p-2 flex justify-between items-center dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
                @click="getShowOption(showSelection)"
              >
                <div class="flex gap-2 items-center">
                  <EyeIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-if="showSelection.id === 1"
                  />
                  <EyeSlashIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-else
                  />
                  <div class="flex flex-col gap-1">
                    <h4 class="font-medium">{{ showSelection.name }}</h4>
                    <h5 class="text-sm">{{ showSelection.content }}</h5>
                  </div>
                </div>
                <div class="relative w-10 h-10 rounded-full dark:bg-slate-600">
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="showOption && showSelection.id === 1"
                  ></span>
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="!showOption && showSelection.id === 2"
                  ></span>
                </div>
              </div>
              <div class="flex justify-end items-center gap-2">
                <button
                  @click="toggleEditShow"
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
          <hr class="border border-slate-700 my-4" />
        </div>
        <div>
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
        </div>
        <div>
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
    </div>
    <div class="w-full dark:bg-slate-800 rounded-lg p-4">
      <h1 class="font-bold text-2xl">Quản lý thành viên</h1>
      <div class="my-4">
        <div
            class="flex"
            :class="
              isRequestOpen
                ? 'flex-col justify-start items-start gap-2'
                : 'items-center justify-between'
            "
          >
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Ai có thể tham gia nhóm</h3>
              <h5 class="text-sm" v-if="!isRequestOpen">
                Chỉ trang cá nhân
              </h5>
            </div>
            <PencilIcon
              v-if="!isRequestOpen"
              @click="toggleRequestShow"
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
            <div v-else class="w-full space-y-2">
              <div
                v-for="requestSelection in requestSelections"
                :key="requestSelection.id"
                class="p-2 flex justify-between items-center dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
                @click="getRequestOption(requestSelection)"
              >
                <div class="flex gap-2 items-center">
                  <EyeIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-if="requestSelection.id === 1"
                  />
                  <EyeSlashIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-else
                  />
                  <div class="flex flex-col gap-1">
                    <h4 class="font-medium">{{ requestSelection.name }}</h4>
                    <h5 class="text-sm">{{ requestSelection.content }}</h5>
                  </div>
                </div>
                <div class="relative w-10 h-10 rounded-full dark:bg-slate-600">
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="requestOption && requestSelection.id === 1"
                  ></span>
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="!requestOption && requestSelection.id === 2"
                  ></span>
                </div>
              </div>
              <div class="flex justify-end items-center gap-2">
                <button
                  @click="toggleRequestShow"
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
        <div
            class="flex"
            :class="
              isAnonymousOpen
                ? 'flex-col justify-start items-start gap-2'
                : 'items-center justify-between'
            "
          >
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Đăng ẩn danh</h3>
              <h5 class="text-sm" v-if="!isAnonymousOpen">
                Tắt
              </h5>
            </div>
            <PencilIcon
              v-if="!isAnonymousOpen"
              @click="toggleAnonymousShow"
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
            <div v-else class="w-full space-y-2">
              <div
                v-for="anonymousSelection in onOffSelections"
                :key="anonymousSelection.id"
                class="p-2 flex justify-between items-center dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
                @click="getAnonymousOption(anonymousSelection)"
              >
                <div class="flex gap-2 items-center">
                  <EyeIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-if="anonymousSelection.id === 1"
                  />
                  <EyeSlashIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-else
                  />
                  <div class="flex flex-col gap-1">
                    <h4 class="font-medium">{{ anonymousSelection.name }}</h4>
                    <h5 class="text-sm">{{ anonymousSelection.content }}</h5>
                  </div>
                </div>
                <div class="relative w-10 h-10 rounded-full dark:bg-slate-600">
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="anonymousOption && anonymousSelection.id === 1"
                  ></span>
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="!anonymousOption && anonymousSelection.id === 2"
                  ></span>
                </div>
              </div>
              <div class="flex justify-end items-center gap-2">
                <button
                  @click="toggleAnonymousShow"
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
          <hr class="border border-slate-700 my-4" />
          <div
            class="flex"
            :class="
              isWhoCanPostOpen
                ? 'flex-col justify-start items-start gap-2'
                : 'items-center justify-between'
            "
          >
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Ai có thể đăng</h3>
              <h5 class="text-sm" v-if="!isWhoCanPostOpen">
                Bất cứ ai trong nhóm
              </h5>
            </div>
            <PencilIcon
              v-if="!isWhoCanPostOpen"
              @click="toggleWhoCanPostShow"
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
            <div v-else class="w-full space-y-2">
              <div
                v-for="whoCanSelection in postSelections"
                :key="whoCanSelection.id"
                class="p-2 flex justify-between items-center dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
                @click="getWhoCanPostOption(whoCanSelection)"
              >
                <div class="flex gap-2 items-center">
                  <EyeIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-if="whoCanSelection.id === 1"
                  />
                  <EyeSlashIcon
                    class="w-10 p-2 rounded-full bg-slate-600"
                    v-else
                  />
                  <div class="flex flex-col gap-1">
                    <h4 class="font-medium">{{ whoCanSelection.name }}</h4>
                    <h5 class="text-sm">{{ whoCanSelection.content }}</h5>
                  </div>
                </div>
                <div class="relative w-10 h-10 rounded-full dark:bg-slate-600">
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="whoCanPostOption && whoCanSelection.id === 1"
                  ></span>
                  <span
                    class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
                    v-if="!whoCanPostOption && whoCanSelection.id === 2"
                  ></span>
                </div>
              </div>
              <div class="flex justify-end items-center gap-2">
                <button
                  @click="toggleWhoCanPostShow"
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
          <hr class="border border-slate-700 my-4" />
        <div>
          <div class="flex items-center justify-between">
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">Cần phê duyệt bài viết</h3>
            </div>
            <PencilIcon
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
          </div>
        </div>
        <hr class="border border-slate-700 my-4" />
        <div>
          <div class="flex items-center justify-between">
            <div class="space-y-1">
              <h3 class="text-lg font-semibold">
                Ai có thể tham gia cuộc thảo luận
              </h3>
            </div>
            <PencilIcon
              class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { PencilIcon } from "@heroicons/vue/20/solid";
import { useRoute } from "vue-router";
import { useUserStore } from "../../stores/user";
import MUILikedInput from "../../components/input/MUILikedInput.vue";
import ListRadioButton from '../../components/input/ListRadioButton.vue';

import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/solid";

export default {
  name: "groupedit",
  components: {
    PencilIcon,
    MUILikedInput,
    EyeIcon,
    EyeSlashIcon,
    ListRadioButton,
  },
  setup() {
    const route = useRoute();
    const userStore = useUserStore();

    return {
      route,
      userStore,
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
      showSelections: [
        {
          id: 1,
          name: "Hiển thị",
          content: "Ai cũng có thể tìm thấy nhóm này.",
        },
        {
          id: 2,
          name: "Ẩn",
          content: "Chỉ thành viên mới tìm thấy nhóm này.",
        },
      ],
      showOption: this.group.show_group,
      isUrlOpen: false,
      url: `http://localhost:5173/groups/${this.group.id}`,
      isRequestOpen: false,
      requestSelections: [
      {
          id: 1,
          name: "Trang cá nhân và trang",
          content: "Cho phép cả Trang và trang cá nhân yêu cầu tham gia nhóm.",
        },
        {
          id: 2,
          name: "Chỉ trang cá nhân",
          content: "Chỉ cho phép trang cá nhân tham gia nhóm.",
        },
      ],
      requestOption: false,
      isAddModeratorOpen: false,
      isBanListOpen: false,
      isAnonymousOpen: false,
      onOffSelections: [
      {
          id: 1,
          name: "Bật",
          content: "Bật chức năng",
        },
        {
          id: 2,
          name: "Tắt",
          content: "Tắt chức năng",
        },
      ],
      anonymousOption: false,
      isWhoCanPostOpen: false,
      postSelections: [
          {
              id: 1,
              name: "Bất cứ ai trong nhóm",
              content: "",
            },
            {
                id: 2,
                name: "Chỉ chủ nhóm và quản trị viên",
                content: "",
            },
        ],
    whoCanPostOption: false,
      isPendingPostOpen: false,
      isPollOpen: false,
    };
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
    toggleRequestShow(){
        this.isRequestOpen = !this.isRequestOpen;
        this.requestOption = false
    },
    toggleAnonymousShow(){
        this.isAnonymousOpen = !this.isAnonymousOpen;
        this.anonymousOption = false
    },
    toggleWhoCanPostShow(){
        this.isWhoCanPostOpen = !this.isWhoCanPostOpen;
        this.whoCanPostOption = false
    },
    getShowOption(data) {
      if (data.name === "Hiển thị") {
        this.showOption = true;
      } else {
        this.showOption = false;
      }
    },
    getRequestOption(data) {
      if (data.name === "Trang cá nhân và trang") {
        this.requestOption = true;
      } else {
        this.requestOption = false;
      }
    },
    getAnonymousOption(data) {
      if (data.name === "Bật") {
        this.anonymousOption = true;
      } else {
        this.anonymousOption = false;
      }
    },
    getWhoCanPostOption(data) {
      if (data.name === "Bất cứ ai trong nhóm") {
        this.whoCanPostOption = true;
      } else {
        this.whoCanPostOption = false;
      }
    },
  },
};
</script>

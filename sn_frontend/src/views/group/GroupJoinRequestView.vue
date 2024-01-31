<template>
  <div
    class="dark:bg-slate-800 dark:text-neutral-200 grid lg:grid-cols-5 grid-cols-4 relative"
  >
    <div
      class="col-span-1 lg:block hidden dark:bg-slate-800 bg-slate-200 sticky overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border-r border-slate-600"
      :style="{
        height: `${toastStore.height}px`,
        top: `${toastStore.navbarHeight}px`,
      }"
    >
      <GroupDetailNavigation :group="group" :isUserInGroup="isUserInGroup" />
    </div>
    <div
      class="lg:col-span-4 md:col-span-3 col-span-4 dark:bg-slate-900 bg-slate-200 flex flex-col relative items-center"
    >
      <div
        class="w-full flex flex-col justify-center items-center sticky mx-auto dark:bg-slate-800"
        :style="{
          top: `${toastStore.navbarHeight}px`,
        }"
      >
        <div class="w-[60%] py-6">
          <div class="flex justify-between items-center">
            <h1 class="font-bold text-2xl">
              Yêu cầu làm thành viên &middot; {{ requests.length }}
            </h1>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer"
            >
              <AdjustmentsHorizontalIcon class="w-6" />
              <ChevronDownIcon class="w-4" />
            </div>
          </div>
          <div class="flex items-center gap-2 my-2">
            <div class="relative w-full">
              <MagnifyingGlassIcon
                class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
              />
              <input
                ref="input"
                type="text"
                placeholder="Tìm kiếm theo tên"
                class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
              />
            </div>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h3 class="font-semibold">Mới nhất trước</h3>
              <ChevronDownIcon class="w-4" />
            </div>
          </div>
          <div class="flex items-center flex-wrap gap-2">
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h4 class="font-semibold text-sm">Xóa bộ lọc</h4>
            </div>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h4 class="font-semibold text-sm">Ngày tham gia</h4>
              <ChevronDownIcon class="w-4" />
            </div>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h4 class="font-semibold text-sm">Thời gian yêu cầu</h4>
              <ChevronDownIcon class="w-4" />
            </div>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h4 class="font-semibold text-sm">Giới tính</h4>
              <ChevronDownIcon class="w-4" />
            </div>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h4 class="font-semibold text-sm">Ảnh đại diện</h4>
              <ChevronDownIcon class="w-4" />
            </div>
            <div
              class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
            >
              <h4 class="font-semibold text-sm">Bộ lọc khác</h4>
            </div>
          </div>
        </div>
      </div>
      <div class="w-[60%] my-12 space-y-4 dark:text-neutral-200">
        <div
          v-for="request in requests"
          :key="request.id"
          class="dark:bg-slate-700 rounded-lg p-4 flex gap-2"
        >
          <div class="flex flex-col justify-start">
            <img
              :src="request?.created_by?.get_avatar"
              alt="request-user-avatar"
              class="w-16 h-[60px] rounded-full"
            />
          </div>
          <div class="flex justify-between items-center w-full">
            <div class="flex flex-col space-y-2 w-full">
              <div>
                <h3 class="font-semibold text-lg">
                  {{ request?.created_by?.name }}
                </h3>
                <h4 class="dark:text-neutral-400">
                  Đã yêu cầu khoảng {{ request?.created_at_formatted }} trước
                </h4>
              </div>
              <div class="flex gap-3 items-center">
                <ClockIcon class="text-neutral-400 w-6 h-6" />
                <h4 class="dark:text-neutral-200">
                  Tham gia Social Network từ
                  {{ request?.created_by?.date_joined_formatted }} trước
                </h4>
              </div>
            </div>
            <div class="flex w-full gap-3">
              <button
              @click="
                handleRequest('accepted', request?.created_for?.id, request?.created_by?.id)
              "
                class="px-4 py-2 shadow-md bg-emerald-500 rounded-lg font-semibold w-full hover:bg-emerald-400 duration-75"
              >
                Phê duyệt
              </button>
              <button
              @click="
                handleRequest('rejected', request?.created_for?.id, request?.created_by?.id)
              "
                class="px-4 py-2 shadow-md bg-rose-500 rounded-lg font-semibold w-full hover:bg-rose-400 duration-75"
              >
                Từ chối
              </button>
              <EllipsisHorizontalIcon
                class="w-24 p-1 shadow-md dark:bg-slate-800 rounded-lg font-semibold dark:hover:bg-slate-600 duration-75 cursor-pointer"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";
import { RouterLink } from "vue-router";
import {
  ClockIcon,
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  EllipsisHorizontalIcon,
} from "@heroicons/vue/24/solid";
import GroupDetailNavigation from "../../components/items/group/GroupDetailNavigation.vue";

export default {
  name: "groupjoinrequest",
  components: {
    ClockIcon,
    AdjustmentsHorizontalIcon,
    ChevronDownIcon,
    MagnifyingGlassIcon,
    EllipsisHorizontalIcon,
    RouterLink,
    GroupDetailNavigation,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  data() {
    return {
      group: {},
      requests: [],
      isUserInGroup: false,
    };
  },

  mounted() {
    this.getGroupDetail();
  },

  methods: {
    async getGroupDetail() {
      await axios
        .get(`/api/group/${this.$route.params.id}/`)
        .then((res) => {
          this.group = res.data;
          this.getJoinRequests();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getJoinRequests() {
      axios
        .get(`/api/group/${this.group?.id}/get-join-request/`)
        .then((res) => {
          this.requests = res.data;
          //   console.log(res.data)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleRequest(status, pk, id) {
      axios
        .post(`/api/group/${pk}/user/${id}/request/${status}/`)
        .then((res) => {
            console.log(res.data)
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

<template>
  <div
    class="w-full flex flex-col justify-center items-center sticky"
    :style="{
      top: `${toastStore.navbarHeight}px`,
    }"
  >
    <div
      class="w-full flex flex-col justify-center items-center mx-auto dark:bg-slate-800 bg-white"
    >
      <div class="xl:w-[60%] w-full py-6 px-4">
        <div class="flex justify-between items-center">
          <h1 class="font-bold xm:text-2xl text-lg">
            Yêu cầu làm thành viên &middot; {{ requests.length }}
          </h1>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer"
          >
            <AdjustmentsHorizontalIcon class="w-6" />
            <ChevronDownIcon class="w-4" />
          </div>
        </div>
        <div class="flex xm:flex-row flex-col items-center gap-2 my-2">
          <div class="relative w-full">
            <MagnifyingGlassIcon
              class="absolute top-[18px] left-2 sm:w-6 sm:h-6 vs:w-3 vs:h-3 dark:text-neutral-400"
            />
            <input
              ref="input"
              type="text"
              placeholder="Tìm kiếm theo tên"
              class="w-full my-2 sm:py-2 sm:px-8 vs:py-1 vs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
            />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max xm:w-auto w-full xm:justify-start justify-center"
          >
            <h3 class="font-semibold xm:text-sm text-xs">Mới nhất trước</h3>
            <ChevronDownIcon class="w-4" />
          </div>
        </div>
        <div class="flex items-center flex-wrap gap-2">
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold xm:text-sm text-xs">Xóa bộ lọc</h4>
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold xm:text-sm text-xs">Ngày tham gia</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold xm:text-sm text-xs">Thời gian yêu cầu</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold xm:text-sm text-xs">Giới tính</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold xm:text-sm text-xs">Ảnh đại diện</h4>
            <ChevronDownIcon class="w-4" />
          </div>
          <div
            class="flex px-4 py-2 gap-2 items-center dark:bg-slate-700 bg-slate-300 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer min-w-max"
          >
            <h4 class="font-semibold xm:text-sm text-xs">Bộ lọc khác</h4>
          </div>
        </div>
      </div>
    </div>
    <div
      class="xl:w-[60%] w-full xm:my-12 my-4 space-y-4 dark:text-neutral-200 px-4"
    >
      <div
        v-for="request in requests"
        :key="request.id"
        class="dark:bg-slate-700 bg-white rounded-lg p-4 flex xm:flex-row flex-col gap-2"
      >
        <div class="flex gap-2 xm:items-start items-center justify-start">
          <img
            loading="lazy"
            :src="request?.created_by?.get_avatar"
            alt="request-user-avatar"
            class="xm:w-16 xm:h-[60px] vs:w-10 vs:h-[38px] rounded-full"
          />
          <div class="xm:hidden">
            <h3 class="font-semibold text-lg">
              {{ request?.created_by?.name }}
            </h3>
            <h4 class="dark:text-neutral-400 xm:text-base text-sm">
              Đã yêu cầu khoảng {{ request?.created_at_formatted }} trước
            </h4>
          </div>
        </div>
        <div
          class="flex justify-between 2xl:flex-row flex-col gap-2 items-start w-full"
        >
          <div class="flex flex-col space-y-2 w-full">
            <div class="xm:block hidden">
              <h3 class="font-semibold text-lg">
                {{ request?.created_by?.name }}
              </h3>
              <h4 class="dark:text-neutral-400 xm:text-base text-sm">
                Đã yêu cầu khoảng {{ request?.created_at_formatted }} trước
              </h4>
            </div>
            <div class="flex gap-3 items-center">
              <ClockIcon class="text-neutral-400 w-6 h-6" />
              <h4 class="dark:text-neutral-200 xm:text-base text-sm">
                Tham gia Social Network từ
                {{ request?.created_by?.date_joined_formatted }} trước
              </h4>
            </div>
            <div v-if="request.answers.length">
              <div v-for="answer in request.answers" :key="answer.id">
                <div class="px-4">
                  <h4 class="font-semibold xm:text-base text-sm">
                    {{ answer?.question?.body }}
                  </h4>
                  <h4 class="text-neutral-400 xm:text-base text-sm">
                    {{ answer?.body }}
                  </h4>
                </div>
              </div>
            </div>
          </div>
          <div class="flex xs:flex-row flex-col w-full items-end gap-3">
            <button
              @click="
                handleRequest(
                  'accepted',
                  request?.created_for?.id,
                  request?.created_by?.id
                )
              "
              class="px-4 py-2 shadow-md bg-emerald-500 rounded-lg font-semibold w-full xm:text-base text-sm hover:bg-emerald-400 duration-75"
            >
              Phê duyệt
            </button>
            <button
              @click="
                handleRequest(
                  'rejected',
                  request?.created_for?.id,
                  request?.created_by?.id
                )
              "
              class="px-4 py-2 shadow-md bg-rose-500 rounded-lg font-semibold w-full xm:text-base text-sm hover:bg-rose-400 duration-75"
            >
              Từ chối
            </button>
            <EllipsisHorizontalIcon
              class="xs:w-24 w-10 p-1 shadow-md dark:bg-slate-800 rounded-lg font-semibold dark:hover:bg-slate-600 duration-75 cursor-pointer"
            />
          </div>
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
import {
  ClockIcon,
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  EllipsisHorizontalIcon,
} from "@heroicons/vue/24/solid";
import GroupDetailNavigation from "../../../components/items/group/GroupDetailNavigation.vue";

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
    this.checkUserInGroup();
  },

  methods: {
    async checkUserInGroup() {
      await axios
        .get(`/api/group/check-user/${this.$route.params.id}`)
        .then((res) => {
          if (res.data.message === "User joined the group") {
            this.isUserInGroup = true;
          } else {
            this.isUserInGroup = false;
          }
          this.getGroupDetail();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getGroupDetail() {
      await axios
        .get(`/api/group/${this.$route.params.id}/`)
        .then((res) => {
          this.group = res.data;
          // console.log(res.data);
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
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleRequest(status, pk, id) {
      axios
        .post(`/api/group/${pk}/user/${id}/request/${status}/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

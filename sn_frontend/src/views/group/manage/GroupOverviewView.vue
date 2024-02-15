<template>
  <div
    class="w-[60%] flex flex-col justify-center items-center mx-auto my-4 space-y-4"
  >
    <div class="dark:bg-slate-800 w-full rounded-lg p-4 space-y-4">
      <div>
        <h3 class="text-xl font-semibold">Cần xem xét</h3>
        <h4 class="text-neutral-400">1 thông tin mới cần xem xét</h4>
      </div>
      <div class="grid lg:grid-cols-2 grid-cols-1 gap-4">
        <div
          class="p-2 flex justify-between items-start dark:hover:bg-slate-700 cursor-pointer rounded-lg duration-75"
          v-for="navigator in navigators"
          :key="navigator.name"
        >
          <div class="flex gap-2 items-start">
            <ExclamationTriangleIcon
              class="w-8 p-1 rounded-full bg-orange-500"
              v-if="navigators.indexOf(navigator) == 0"
            />
            <ClipboardDocumentCheckIcon
              class="w-8 p-1 rounded-full bg-cyan-500"
              v-if="navigators.indexOf(navigator) == 1"
            />
            <BellAlertIcon
              class="w-8 p-1 rounded-full bg-amber-500"
              v-if="navigators.indexOf(navigator) == 2"
            />
            <UserPlusIcon
              class="w-8 p-1 rounded-full bg-emerald-500"
              v-if="navigators.indexOf(navigator) == 3"
            />
            <div class="space-y-2">
              <h3 class="text-lg font-semibold">{{ navigator.name }}</h3>
              <h4 class="text-neutral-400">{{ navigator.content }}</h4>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <h3 class="text-xl font-semibold">0</h3>
            <ChevronRightIcon class="w-6" />
          </div>
        </div>
      </div>
    </div>
    <div class="dark:bg-slate-800 w-full rounded-lg p-4 space-y-4">
      <div>
        <h3 class="text-xl font-semibold">Tóm tắt thông tin chi tiết</h3>
        <h4 class="text-neutral-400">Trong 7 ngày qua</h4>
      </div>
      <div class="grid lg:grid-cols-2 grid-cols-1 gap-4">
        <div
          class="px-4 py-8 flex justify-between items-center bg-slate-700 rounded-lg duration-75"
          v-for="summary in summaries"
          :key="summary.name"
        >
          <div class="flex items-center gap-2">
            <DocumentTextIcon
              class="w-8"
              v-if="summaries.indexOf(summary) == 0"
            />
            <ChatBubbleLeftEllipsisIcon
              class="w-8"
              v-if="summaries.indexOf(summary) == 1"
            />
            <HandThumbUpIcon
              class="w-8"
              v-if="summaries.indexOf(summary) == 2"
            />
            <UserPlusIcon
              class="w-8"
              v-if="summaries.indexOf(summary) == 3"
            />
            <h4 class="font-semibold">{{ summary.name }}</h4>
          </div>
          <div class="flex items-center gap-2">
            <h3 class="text-lg font-semibold">1</h3>
            <ArrowRightIcon
              class="w-6"
              :class="[
                summary.rate > 0 ? 'rotate-[-45deg] text-emerald-500' : '',
                summary.rate < 0 ? 'rotate-45 text-rose-500' : '',
              ]"
            />
            <h5
              class="text-sm font-semibold"
              :class="[
                summary.rate > 0 ? ' text-emerald-500' : '',
                summary.rate < 0 ? ' text-rose-500' : '',
              ]"
            >
              {{ summary.rate }}%
            </h5>
          </div>
        </div>
      </div>
      <div class="flex justify-center items-center">
        <RouterLink
          :to="{ name: 'groupgrowth', params: { id: group.id } }"
          class="px-4 py-2 dark:bg-slate-600 rounded-lg max-w-max font-semibold cursor-pointer dark:hover:bg-slate-500 duration-75"
        >
          Xem thông tin chi tiết về lượt tương tác
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import {
  ChevronRightIcon,
  ExclamationTriangleIcon,
  BellAlertIcon,
  ClipboardDocumentCheckIcon,
  UserPlusIcon,
  ChatBubbleLeftEllipsisIcon,
  HandThumbUpIcon,
  DocumentTextIcon,
  ArrowRightIcon,
} from "@heroicons/vue/24/solid";
import { RouterLink } from "vue-router";
export default {
  name: "groupoverview",
  components: {
    ChevronRightIcon,
    ExclamationTriangleIcon,
    BellAlertIcon,
    ClipboardDocumentCheckIcon,
    UserPlusIcon,
    ChatBubbleLeftEllipsisIcon,
    HandThumbUpIcon,
    DocumentTextIcon,
    ArrowRightIcon,
    RouterLink,
  },
  setup() {
    const navigators = [
      {
        name: "Nội dung bị thành viên báo cáo",
        content: "0 mục nhập mới hôm nay",
        url: "",
      },
      {
        name: "Bài viết đang chờ",
        content: "0 mục nhập mới hôm nay",
        url: "",
      },
      {
        name: "Thông báo kiểm duyệt",
        content: "0 mục nhập mới hôm nay",
        url: "groupjoinrequest",
      },
      {
        name: "Yêu cầu làm thành viên",
        content: "0 mục nhập mới hôm nay",
        url: "groupjoinrequest",
      },
    ];

    const summaries = [
      {
        name: "Bài viết",
        rate: "1",
      },
      {
        name: "Bình luận",
        rate: "-1",
      },
      {
        name: "Cảm xúc",
        rate: "1",
      },
      {
        name: "Thành viên mới",
        rate: "1",
      },
    ];

    return {
      navigators,
      summaries,
    };
  },

  props: {
    group: Object,
  },
};
</script>

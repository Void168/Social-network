<template>
  <div
    class="lg:w-[60%] w-full xm:px-4 flex flex-col justify-center items-center mx-auto xm:my-4 space-y-4"
  >
    <div class="dark:bg-slate-800 bg-white w-full xm:rounded-lg p-4 space-y-4">
      <div>
        <h3 class="xm:text-xl text-lg font-semibold">Cần xem xét</h3>
        <h4 class="text-neutral-400 xm:text-base text-sm">1 thông tin mới cần xem xét</h4>
      </div>
      <div class="grid xl:grid-cols-2 grid-cols-1 gap-4">
        <div v-for="navigator in navigators" :key="navigator.name">
          <RouterLink
            :to="{ name: navigator.url, params: { id: group.id } }"
            class="p-2 flex justify-between gap-2 items-start dark:hover:bg-slate-700 hover:bg-slate-200 cursor-pointer rounded-lg duration-75"
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
                <h3 class="xm:text-lg font-semibold">{{ navigator.name }}</h3>
                <h4 class="text-neutral-400 xm:text-base text-sm">
                  {{ navigator.amount }} {{ navigator.content }}
                </h4>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <h3 class="xm:text-xl text-lg font-semibold">{{ navigator.amount }}</h3>
              <ChevronRightIcon class="xm:w-6 w-4" />
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
    <div class="dark:bg-slate-800 bg-white w-full xm:rounded-lg p-4 space-y-4">
      <div>
        <h3 class="xm:text-xl text-lg font-semibold">Tóm tắt thông tin chi tiết</h3>
        <h4 class="text-neutral-400 xm:text-base text-sm">Trong 7 ngày qua</h4>
      </div>
      <div class="grid xl:grid-cols-2 grid-cols-1 gap-4">
        <div
          class="px-4 py-8 flex justify-between items-center dark:bg-slate-700 bg-slate-200 rounded-lg duration-75"
          v-for="summary in summaries"
          :key="summary.name"
        >
          <div class="flex items-center gap-2">
            <DocumentTextIcon
              class="xm:w-8 w-6"
              v-if="summaries.indexOf(summary) == 0"
            />
            <ChatBubbleLeftEllipsisIcon
              class="xm:w-8 w-6"
              v-if="summaries.indexOf(summary) == 1"
            />
            <HandThumbUpIcon
              class="xm:w-8 w-6"
              v-if="summaries.indexOf(summary) == 2"
            />
            <UserPlusIcon class="xm:w-8 w-6" v-if="summaries.indexOf(summary) == 3" />
            <h4 class="font-semibold xm:text-base text-sm">{{ summary.name }}</h4>
          </div>
          <div class="flex items-center gap-2">
            <h3 class="xm:text-lg font-semibold">{{ summary.amount }}</h3>
            <ArrowRightIcon
              class="xm:w-6 w-4"
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
          class="px-4 text-center py-2 dark:bg-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg max-w-max font-semibold cursor-pointer dark:hover:bg-slate-500 duration-75"
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
import axios from "axios";
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

  props: {
    group: Object,
  },

  data() {
    return {
      navigators: [
        {
          name: "Nội dung bị thành viên báo cáo",
          content: "mục nhập mới hôm nay",
          amount: 0,
          url: "groupdiscuss",
        },
        {
          name: "Bài viết đang chờ",
          content: "mục nhập mới hôm nay",
          amount: 0,
          url: "grouppendingpost",
        },
        {
          name: "Thông báo kiểm duyệt",
          content: "mục nhập mới hôm nay",
          amount: 0,
          url: "groupdiscuss",
        },
        {
          name: "Yêu cầu làm thành viên",
          content: "mục nhập mới hôm nay",
          amount: 0,
          url: "groupjoinrequest",
        },
      ],
      summaries: [
        {
          name: "Bài viết",
          amount: 0,
          rate: 0,
        },
        {
          name: "Bình luận",
          amount: 0,
          rate: 0,
        },
        {
          name: "Cảm xúc",
          amount: 0,
          rate: 0,
        },
        {
          name: "Thành viên mới",
          amount: 0,
          rate: 0,
        },
      ],
    };
  },

  mounted() {
    this.getNewMembersDashboard();
  },

  methods: {
    async getNewMembersDashboard() {
      await axios
        .get(`/api/group/${this.$route.params.id}/overview/`)
        .then((res) => {
          console.log(res.data);
          this.summaries[0].amount = res.data.postSevenDays;
          this.summaries[0].rate =
            (res.data.postSevenDays - res.data.postTwentyEightDays) * 100;
          this.summaries[1].amount = res.data.commentSevenDays;
          this.summaries[1].rate =
            (res.data.commentSevenDays - res.data.commentTwentyEightDays) * 100;
          this.summaries[2].amount = res.data.likeSevenDays;
          this.summaries[2].rate =
            (res.data.likeSevenDays - res.data.likeTwentyEightDays) * 100;
          this.summaries[3].amount = res.data.memberSevenDays;
          this.summaries[3].rate =
            (res.data.memberSevenDays - res.data.memberTwentyEightDays) * 100;

          this.navigators[1].amount = res.data.pendingPosts;
          this.navigators[3].amount = res.data.joinRequests;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<template>
  <div class="flex flex-col">
    <div class="p-2">
      <div class="flex items-center gap-2">
        <img :src="group.get_cover_image" alt="" class="rounded-lg h-12 w-12" />
        <div class="flex flex-col space-y-2">
          <h4 class="font-semibold">{{ group.name }}</h4>
          <div class="flex items-center gap-2">
            <GlobeAsiaAustraliaIcon
              v-if="!group.is_private_group"
              class="w-4"
            />
            <LockClosedIcon v-else class="w-4" />
            <h5 class="text-sm">
              {{ group.is_private_group ? "Nhóm riêng tư" : "Nhóm công khai" }}
              &middot; {{ group.members_count }} thành viên
            </h5>
          </div>
        </div>
      </div>
    </div>
    <div class="p-2 space-y-1 w-full flex flex-col justify-center" v-if="isUserInGroup">
      <RouterLink
        :to="{ name: 'groupdetail', params: { id: group?.id } }"
        class="flex gap-2 items-center px-4 py-2 dark:hover:bg-slate-700 rounded-lg cursor-pointer duration-75 font-semibold w-full"
      >
        <HomeIcon class="w-6" />
        <h4>Trang chủ của cộng đồng</h4>
      </RouterLink>
      <RouterLink
        :to="{ name: 'groupdetail', params: { id: group?.id } }"
        class="px-4 py-2 dark:hover:bg-slate-700 rounded-lg cursor-pointer duration-75 font-semibold w-full"
      >
        Tổng quan
      </RouterLink>
    </div>
    <hr class="border dark:border-slate-700 mx-4" />
    <div class="p-2" v-if="isUserInGroup">
      <Disclosure
        v-slot="{ open }"
        v-for="groupNavigation in groupNavigations"
        :key="groupNavigation.id"
      >
        <DisclosureButton
          class="flex w-full justify-between rounded-lg dark:bg-slate-800 px-4 py-2 text-left font-medium dark:text-neutral-200/70 dark:hover:bg-slate-700 focus:outline-none focus-visible:ring"
        >
          <span>{{ groupNavigation.name }}</span>
          <ChevronUpIcon
            :class="open ? 'rotate-180 transform' : ''"
            class="h-5 w-5 dark:text-neutral-200"
          />
        </DisclosureButton>
        <DisclosurePanel
          class="px-4 py-2 text-sm dark:text-neutral-200 font-medium"
          v-for="category in groupNavigation.categories"
          :key="category.name"
        >
          <div class="flex flex-col space-y-2">
            <h3>{{ category.name }}</h3>
            <h4>{{ category.content }}</h4>
          </div>
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import { RouterLink } from "vue-router";

import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { ChevronUpIcon } from "@heroicons/vue/20/solid";

import {
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  HomeIcon,
} from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    HomeIcon,
    RouterLink,
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    ChevronUpIcon,
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
    isUserInGroup: Boolean
  },

  data() {
    return {
      groupNavigations: [
        {
          id: 1,
          name: "Công cụ quản trị",
          categories: [
            {
              name: "Hỗ trợ quản trị",
              content: "",
              url: "",
            },
            {
              name: "Yêu cầu làm thành viên",
              content: "",
              url: "",
            },
            {
              name: "Yêu huy hiệu",
              content: "",
              url: "",
            },
            {
              name: "Câu hỏi chọn thành viên",
              content: "",
              url: "",
            },
            {
              name: "Bài viết đang chờ",
              content: "",
              url: "",
            },
            {
              name: "Có thể là spam",
              content: "",
              url: "",
            },
            {
              name: "Bài viết đã lên lịch",
              content: "",
              url: "",
            },
            {
              name: "Nhật ký hoạt động",
              content: "",
              url: "",
            },
            {
              name: "Quy tắc nhóm",
              content: "",
              url: "",
            },
            {
              name: "Nội dung bị thành viên báo cáo",
              content: "",
              url: "",
            },
            {
              name: "Thông báo kiểm duyệt",
              content: "",
              url: "",
            },
            {
              name: "Trạng thái nhóm",
              content: "",
              url: "",
            },
            {
              name: "Vai trò trong cộng đồng",
              content: "",
              url: "",
            },
          ],
        },
        {
          id: 2,
          name: "Cài đặt",
          categories: [
            {
              name: "Cài đặt nhóm",
              content: "",
              url: "",
            },
            {
              name: "Thêm tính năng",
              content: "",
              url: "",
            },
          ],
        },
        {
          id: 3,
          name: "Thông tin chi tiết",
          categories: [
            {
              name: "Mức độ tăng trưởng",
              content: "",
              url: "",
            },
            {
              name: "Tương tác",
              content: "",
              url: "",
            },
            {
              name: "Quản trị viên & người kiểm duyệt",
              content: "",
              url: "",
            },
            {
              name: "Thành viên",
              content: "",
              url: "",
            },
          ],
        },
        {
          id: 4,
          name: "Hỗ trợ",
          categories: [
            {
              name: "Trung tâm trợ giúp",
              content: "",
              url: "",
            },
          ],
        },
      ],
    };
  },
});
</script>

<style scoped>
.router-link-active {
  --tw-text-opacity: 1;
  color: rgb(16 185 129 / var(--tw-text-opacity));
  background-color: rgb(16 185 129 / 0.3);
}
.router-link-active:hover {
  --tw-text-opacity: 1;
  color: rgb(16 185 129 / var(--tw-text-opacity));
  background-color: rgb(16 185 129 / 0.3);
}
</style>

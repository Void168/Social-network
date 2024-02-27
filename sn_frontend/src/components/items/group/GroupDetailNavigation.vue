<template>
  <div class="flex flex-col">
    <div class="p-2">
      <div class="flex items-center gap-2">
        <RouterLink :to="{ name: 'groupdetail', params: { id: group?.id } }" class="rounded-lg">
          <img
          loading="lazy"
            :src="group.get_cover_image"
            alt=""
            class="rounded-lg h-12 w-12"
          />
        </RouterLink>
        <div class="flex flex-col space-y-2">
          <h4 class="font-semibold">{{ group.name }}</h4>
          <div class="flex items-center gap-2">
            <GlobeAsiaAustraliaIcon
              v-if="!group.is_private_group"
              class="w-4"
            />
            <LockClosedIcon v-else class="w-4" />
            <RouterLink :to="{name: 'groupdetail', params: {id: group.id }}">
              <h5 class="text-sm">
                {{ group.is_private_group ? "Nhóm riêng tư" : "Nhóm công khai" }}
                &middot; {{ group.members_count }} thành viên
              </h5>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div
      class="p-2 space-y-1 w-full flex flex-col justify-center"
      v-if="isUserInGroup && group?.admin?.id === userStore.user.id"
    >
      <RouterLink
        :to="{ name: 'groupdiscuss', params: { id: group?.id } }"
        class="flex gap-2 items-center px-4 py-2 dark:hover:bg-slate-700 rounded-lg cursor-pointer duration-75 font-semibold w-full"
      >
        <HomeIcon class="w-6" />
        <h4>Trang chủ của cộng đồng</h4>
      </RouterLink>
      <RouterLink
      :to="{ name: 'groupoverview', params: { id: group?.id } }"
        class="flex gap-2 items-center px-4 py-2 dark:hover:bg-slate-700 rounded-lg cursor-pointer duration-75 font-semibold w-full"
      >
        <TableCellsIcon class="w-6" />
        <h4>Tổng quan</h4>
      </RouterLink>
    </div>
    <hr class="border dark:border-slate-700 mx-4" />
    <div class="p-2" v-if="isUserInGroup && group?.admin?.id === userStore.user.id">
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
          class="px-4 py-2 text-sm dark:text-neutral-200 font-medium dark:hover:bg-slate-700 duration-75 rounded-lg"
          v-for="category in groupNavigation.categories"
          :key="category.name"
        >
          <RouterLink
            :to="
              category.url
                ? { name: `${category.url}`, params: { id: group?.id } }
                : '/'
            "
          >
            <div class="flex flex-col">
              <h3>{{ category.name }}</h3>
              <h4>{{ category.content }}</h4>
            </div>
          </RouterLink>
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
  TableCellsIcon,
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
    TableCellsIcon,
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
      groupNavigations: [
        {
          id: 1,
          name: "Công cụ quản trị",
          categories: [
            {
              name: "Hỗ trợ quản trị",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Yêu cầu làm thành viên",
              content: "",
              url: "groupjoinrequest",
            },
            {
              name: "Yêu cầu huy hiệu",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Câu hỏi chọn thành viên",
              content: "",
              url: "groupquestion",
            },
            {
              name: "Bài viết đang chờ",
              content: "",
              url: "grouppendingpost",
            },
            {
              name: "Có thể là spam",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Bài viết đã lên lịch",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Nhật ký hoạt động",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Quy tắc nhóm",
              content: "",
              url: "grouprules",
            },
            {
              name: "Nội dung bị thành viên báo cáo",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Thông báo kiểm duyệt",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Trạng thái nhóm",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Vai trò trong cộng đồng",
              content: "",
              url: "groupdiscuss",
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
              url: "groupedit",
            },
            {
              name: "Thêm tính năng",
              content: "",
              url: "groupdiscuss",
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
              url: "groupgrowth",
            },
            {
              name: "Tương tác",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Quản trị viên & người kiểm duyệt",
              content: "",
              url: "groupdiscuss",
            },
            {
              name: "Thành viên",
              content: "",
              url: "groupdiscuss",
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
              url: "groupdiscuss",
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
  color: rgb(52 211 153 / var(--tw-text-opacity));
  background-color: rgb(16 185 129 / 0.3);
}
.router-link-active:hover {
  --tw-text-opacity: 1;
  color: rgb(16 185 129 / var(--tw-text-opacity));
  background-color: rgb(16 185 129 / 0.35);
}
</style>

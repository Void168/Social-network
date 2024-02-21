<template>
  <div class="py-4 max-w-7xl mx-auto gap-4">
    <div
      class="main-center space-y-4 grid grid-cols-4 dark:bg-slate-600 rounded-lg"
    >
      <div class="col-span-1 border-r dark:border-slate-500 py-4">
        <h2 class="text-2xl font-bold dark:text-neutral-200 px-5">
          Giới thiệu
        </h2>
        <ul class="px-1 my-4">
          <li
            v-for="navi in navigation"
            :key="navi.name"
            class="py-2 px-4 duration-75 dark:hover:bg-slate-700 rounded-lg cursor-pointer font-medium"
            :class="
              selectedNavigator?.name === navi?.name
                ? 'text-emerald-400 bg-emerald-700/50'
                : 'dark:text-neutral-300'
            "
            @click="getNavigator(navi)"
          >
            {{ navi.name }}
          </li>
        </ul>
      </div>
      <div class="px-4 col-span-3">
        <div
          class="flex flex-col gap-4"
          v-if="selectedNavigator?.name === 'Thông tin liên hệ và cơ bản'"
        >
          <div>
            <h3 class="text-lg font-semibold dark:text-neutral-300">
              Hạng mục
            </h3>
            <div class="dark:text-neutral-300">
              <div class="dark:text-neutral-300 space-y-1">
                <div class="flex gap-2 items-center">
                  <FolderIcon class="w-8" />
                  <h3 class="font-medium">
                    {{ page.page_type }}
                  </h3>
                </div>
              </div>
            </div>
          </div>
          <div class="dark:text-neutral-300">
            <h3 class="text-lg font-semibold">Thông tin liên hệ</h3>
            <div class="flex gap-2 items-center">
              <EnvelopeIcon class="w-8" />
              <div>
                <h3 class="font-medium">{{ page.email }}</h3>
                <h5 class="text-xs">Email</h5>
              </div>
            </div>
          </div>
          <div>
            <h3 class="text-lg font-semibold dark:text-neutral-300">
              Các trang web và liên kết xã hội
            </h3>
            <div class="dark:text-neutral-300">
              <div class="dark:text-neutral-300 space-y-1">
                <div class="flex gap-2 items-center">
                  <GlobeAltIcon class="w-8" />
                  <div>
                    <h3 class="font-medium"></h3>
                    <h5 class="text-xs">Websites</h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="selectedNavigator?.name?.includes('Chi tiết về')"
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Giới thiệu về bản thân</h3>
            <div class="flex gap-2 items-center" v-if="page.biography">
              <div class="flex gap-1 items-center">
                <h3 class="font-medium">
                  {{ page.biography }}
                </h3>
              </div>
            </div>
            <div v-else class="flex gap-2 items-center">
              <h3 class="font-medium">Chưa có lời giới thiệu</h3>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6 mb-4"
          v-if="selectedNavigator?.name === 'Tính minh bạch của trang'"
        >
          <div class="dark:text-neutral-300 space-y-2">
            <div>
                <h3 class="text-lg font-semibold">Tính minh bạch của Trang</h3>
                <h4 class="text-sm">Social Network hiển thị thông tin để bạn hiểu rõ mục đích của Trang này.</h4>
            </div>
            <div class="flex gap-2 items-center">
              <FlagIcon class="w-8" />
              <div>
                  <h3 class="font-medium">
                    {{ page.id }}
                  </h3>
                  <h5 class="text-xs">ID Trang</h5>
              </div>
            </div>
            <div class="flex gap-2 items-center">
              <ClockIcon class="w-8" />
              <div>
                  <h3 class="font-medium">
                    {{ page.created_at.slice(8, 10) }}/{{ page.created_at.slice(5, 7) }}/{{ page.created_at.slice(0, 4) }}
                  </h3>
                  <h5 class="text-xs">Ngày tạo</h5>
              </div>
            </div>
            <div class="flex gap-2 items-center">
              <UserGroupIcon class="w-8" />
              <div>
                  <h3 class="font-medium">
                    Thông tin về quản trị viên
                  </h3>
                  <h5 class="text-xs">Trang này có thể có nhiều quản trị viên. Họ có thể có quyền đăng nội dung, bình luận hoặc gửi tin nhắn dưới tên Trang.</h5>
              </div>
            </div>
            <div class="flex gap-2 items-center">
              <TvIcon class="w-8" />
              <div>
                  <h3 class="font-medium">
                    Trang này hiện không chạy quảng cáo.
                  </h3>
              </div>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="
            selectedNavigator?.name === 'Thông tin pháp lý và quyền riêng tư'
          "
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Thông tin pháp lý và quyền riêng tư</h3>
            <div class="flex gap-2 items-center">
              <ExclamationCircleIcon class="w-8" />
              <div>
                  <h3 class="font-medium">
                    From {{ page.created_at.slice(8, 10) }}/{{ page.created_at.slice(5, 7) }}/{{ page.created_at.slice(0, 4) }}
                  </h3>
                  <h5 class="text-xs">Tuyên bố quyền sở hữu và quyền tác giả</h5>
              </div>
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
import { RouterLink } from "vue-router";

import {
  BriefcaseIcon,
  AcademicCapIcon,
  MapPinIcon,
  HeartIcon,
  PhoneIcon,
  EnvelopeIcon,
  IdentificationIcon,
  ExclamationCircleIcon,
  GlobeAltIcon,
  UserGroupIcon,
  StarIcon,
  FolderIcon,
  FlagIcon,
  ClockIcon,
  TvIcon
} from "@heroicons/vue/24/solid";

export default {
  name: "about",
  components: {
    BriefcaseIcon,
    AcademicCapIcon,
    MapPinIcon,
    HeartIcon,
    PhoneIcon,
    EnvelopeIcon,
    IdentificationIcon,
    GlobeAltIcon,
    UserGroupIcon,
    ExclamationCircleIcon,
    StarIcon,
    FolderIcon,
    FlagIcon,
    ClockIcon,
    TvIcon,
    RouterLink,
  },
  setup() {
    const userStore = useUserStore();
    const navigation = [
      {
        name: "Thông tin liên hệ và cơ bản",
      },
      {
        name: "Thông tin pháp lý và quyền riêng tư",
      },
      {
        name: "Tính minh bạch của trang",
      },
      {
        name: `Chi tiết về ${userStore.user.name}`,
      },
    ];

    return {
      navigation,
      userStore,
    };
  },

  props: {
    user: Object,
    page: Object,
    partner: Object,
  },

  data() {
    return {
      websites: [],
      phoneNumbers: [],
      selectedNavigator: {},
    };
  },

  mounted() {
    this.getNavigator();
    this.setNavigator();
  },

  methods: {
    setNavigator() {
      this.selectedNavigator = {
        name: "Thông tin liên hệ và cơ bản",
      };
    },
    getNavigator(data) {
      this.selectedNavigator = data;
      if (this.selectedNavigator?.name === "Thông tin liên hệ và cơ bản") {
      }
    },
  },
};
</script>

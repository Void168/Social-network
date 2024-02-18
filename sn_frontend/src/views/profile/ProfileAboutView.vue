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
          class="flex flex-col gap-4 my-8"
          v-if="selectedNavigator?.name === 'Tổng quan'"
        >
          <div class="flex gap-2 items-center dark:text-neutral-300">
            <BriefcaseIcon class="w-8" />
            <h3 class="font-medium">Không có nơi làm việc để hiển thị</h3>
          </div>
          <div class="flex gap-2 items-center dark:text-neutral-300">
            <AcademicCapIcon class="w-8" />
            <h3 class="font-medium">Không có trường học nào để hiển thị</h3>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="user.living_city"
          >
            <MapPinIcon class="w-8" />
            <div class="">
              <h3 class="font-medium">Sống tại {{ user.living_city }}</h3>
            </div>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="user.hometown"
          >
            <MapPinIcon class="w-8" />
            <div class="">
              <h3 class="font-medium">Đến từ {{ user.hometown }}</h3>
            </div>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="!user.living_city && !user.hometown"
          >
            <MapPinIcon class="w-8" />
            <h3 class="font-medium">Không có địa điểm nào để hiển thị</h3>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="user.relationship_status"
          >
            <HeartIcon class="w-8" />
            <div class="flex gap-1 items-center">
              <h3 class="font-medium">
                {{ user.relationship_status }}
              </h3>
              <span>
                với
                <RouterLink
                  class="hover:underline font-medium"
                  :to="{ name: 'profile', params: { id: partner?.user?.id } }"
                  >{{ partner?.user?.name }}</RouterLink
                >
              </span>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="selectedNavigator?.name === 'Công việc và học vấn'"
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Công việc</h3>
            <div class="flex gap-2 items-center">
              <BriefcaseIcon class="w-8" />
              <h3 class="font-medium">Không có nơi làm việc để hiển thị</h3>
            </div>
          </div>
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Đại học</h3>
            <div class="flex gap-2 items-center">
              <AcademicCapIcon class="w-8" />
              <h3 class="font-medium">Không có trường học nào để hiển thị</h3>
            </div>
          </div>
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Trường trung học</h3>
            <div class="flex gap-2 items-center">
              <AcademicCapIcon class="w-8" />
              <h3 class="font-medium">Không có trường học nào để hiển thị</h3>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="selectedNavigator?.name === 'Nơi từng sống'"
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Công việc</h3>
            <div
              class="flex gap-2 items-center"
              v-if="!user.living_city && !user.hometown"
            >
              <MapPinIcon class="w-8" />
              <h3 class="font-medium">Không có địa điểm nào để hiển thị</h3>
            </div>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="user.living_city"
          >
            <MapPinIcon class="w-8" />
            <div class="">
              <h3 class="font-medium">{{ user.living_city }}</h3>
              <h5 class="text-xs">Tỉnh/Thành phố hiện tại</h5>
            </div>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="user.hometown"
          >
            <MapPinIcon class="w-8" />
            <div class="">
              <h3 class="font-medium">{{ user.hometown }}</h3>
              <h5 class="text-xs">Quê quán</h5>
            </div>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="!user.living_city && !user.hometown"
          >
            <MapPinIcon class="w-8" />
            <h3 class="font-medium">Không có địa điểm nào để hiển thị</h3>
          </div>
        </div>
        <div
          class="flex flex-col gap-4"
          v-if="selectedNavigator?.name === 'Thông tin liên hệ và cơ bản'"
        >
          <h3 class="text-lg font-semibold dark:text-neutral-300">
            Thông tin liên hệ
          </h3>
          <div class="dark:text-neutral-300" v-if="phoneNumbers.length">
            <div class="dark:text-neutral-300 space-y-1">
              <div class="flex gap-2 items-center">
                <PhoneIcon class="w-8" />
                <div>
                  <h3 class="font-medium">
                    {{ phoneNumbers[0]?.phone_number }}
                  </h3>
                  <h5 class="text-xs">Di động</h5>
                </div>
              </div>
            </div>
            <div class="dark:text-neutral-300 space-y-1">
              <h3 class="text-lg font-semibold"></h3>
              <div class="flex gap-2 items-center">
                <EnvelopeIcon class="w-8" />
                <div>
                  <h3 class="font-medium">{{ user.email }}</h3>
                  <h5 class="text-xs">Email</h5>
                </div>
              </div>
            </div>
          </div>
          <h3 class="text-lg font-semibold dark:text-neutral-300">
            Các trang web và liên kết xã hội
          </h3>
          <div class="dark:text-neutral-300" v-if="websites.length">
            <div class="dark:text-neutral-300 space-y-1">
              <div class="flex gap-2 items-center">
                <GlobeAltIcon class="w-8" />
                <div>
                  <h3 class="font-medium">
                    {{ websites[0].url }}
                  </h3>
                  <h5 class="text-xs">Websites</h5>
                </div>
              </div>
            </div>
          </div>         
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="!user.email && !phoneNumbers.length"
          >
            <IdentificationIcon class="w-8" />
            <h3 class="font-medium">
              Không có thông tin liên hệ nào để hiển thị
            </h3>
          </div>
          <div
            class="flex gap-2 items-center dark:text-neutral-300"
            v-if="!websites.length"
          >
            <GlobeAltIcon class="w-8" />
            <h3 class="font-medium">
              Không có thông tin liên hệ nào để hiển thị
            </h3>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="selectedNavigator?.name === 'Gia đình và các mối quan hệ'"
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Mối quan hệ</h3>
            <div class="flex gap-2 items-center" v-if="user.relationship_status">
              <HeartIcon class="w-8" />
              <div class="flex gap-1 items-center">
              <h3 class="font-medium">
                {{ user.relationship_status }}
              </h3>
              <span>
                với
                <RouterLink
                  class="hover:underline font-medium"
                  :to="{ name: 'profile', params: { id: partner?.user?.id } }"
                  >{{ partner?.user?.name }}</RouterLink
                >
              </span>
            </div>
            </div>
            <div v-else class="flex gap-2 items-center">
              <HeartIcon class="w-8" />
              <h3 class="font-medium">
                Không có mối quan hệ để hiển thị
              </h3>
            </div>
          </div>
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Thành viên trong gia đình</h3>
            <div class="flex gap-2 items-center">
              <UserGroupIcon class="w-8" />
              <h3 class="font-medium">Không có thành viên gia đình nào để hiển thị</h3>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="selectedNavigator?.name?.includes('Chi tiết về')"
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Giới thiệu về bản thân</h3>
            <div class="flex gap-2 items-center" v-if="user.biography">
              <div class="flex gap-1 items-center">
              <h3 class="font-medium">
                {{ user.biography }}
              </h3>
            </div>
            </div>
            <div v-else class="flex gap-2 items-center">
              <h3 class="font-medium">
                Chưa có lời giới thiệu
              </h3>
            </div>
          </div>
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Các tên khác</h3>
            <div class="flex gap-2 items-center" v-if="user.nickname">
              <h3 class="font-medium">{{ user.nickname }}</h3>
            </div>
            <div v-else class="flex gap-2 items-center">
              <h3 class="font-medium">
                Chưa có biệt danh
              </h3>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-6"
          v-if="selectedNavigator?.name === 'Sự kiện trong đời'"
        >
          <div class="dark:text-neutral-300 space-y-1">
            <h3 class="text-lg font-semibold">Sự kiện trong đời</h3>
            <div class="flex gap-2 items-center">
              <StarIcon class="w-8"/>
              <h3 class="font-medium">
                Không có sự kiện trong đời để hiển thị
              </h3>
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
  GlobeAltIcon,
  UserGroupIcon,
  StarIcon
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
    StarIcon,
    RouterLink,
  },
  setup() {
    const userStore = useUserStore();
    const navigation = [
      {
        name: "Tổng quan",
      },
      {
        name: "Công việc và học vấn",
      },
      {
        name: "Nơi từng sống",
      },
      {
        name: "Thông tin liên hệ và cơ bản",
      },
      {
        name: "Gia đình và các mối quan hệ",
      },
      {
        name: `Chi tiết về ${userStore.user.name}`,
      },
      {
        name: "Sự kiện trong đời",
      },
    ];

    return {
      navigation,
      userStore,
    };
  },

  props: {
    user: Object,
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
        name: "Tổng quan",
      };
    },
    getNavigator(data) {
      this.selectedNavigator = data;
      if(this.selectedNavigator?.name === 'Thông tin liên hệ và cơ bản'){
        this.getWebsitesList()
        this.getPhoneNumbersList()
      }
    },
    async getWebsitesList() {
      await axios
        .get(`/api/informations/${this.user.id}/websites/`)
        .then((res) => {
          this.websites = res.data.websites;
        })
        .catch((error) => console.log(error));
    },
    async getPhoneNumbersList() {
      await axios
        .get(`/api/informations/${this.user.id}/phone-numbers/`)
        .then((res) => {
          this.phoneNumbers = res.data.phone_numbers;
        })
        .catch((error) => console.log(error));
    },
  },
};
</script>

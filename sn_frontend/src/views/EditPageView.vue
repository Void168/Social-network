<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left md:block lg:col-span-1 col-span-2">
      <div
        class="flex flex-col space-y-6 p-12 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <div>
          <h1 class="mb-6 text-2xl">Chỉnh sửa thông tin</h1>
          <label class="text-lg font-semibold">Tiểu sử</label>
          <div
            v-if="!updateBio"
            class="flex flex-col justify-center items-center space-y-4"
          >
            <p v-if="page.biography" class="text-lg text-center font-semibold">
              {{ page.biography }}
            </p>
            <button
              @click="openBioForm"
              class="md:w-[50%] w-full px-4 py-2 bg-slate-200 dark:hover:bg-slate-800 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition"
            >
              Chỉnh sửa tiểu sử
            </button>
          </div>
          <form v-else>
            <div>
              <input
                v-model="page.biography"
                type="text"
                placeholder="Mô tả về bạn"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
              />
              <div class="flex gap-2 justify-end mt-4">
                <button
                  @click="openBioForm"
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
                >
                  Huỷ
                </button>
                <button
                  @click="submitBiographyForm"
                  v-bind:disabled="
                    page?.biography?.length === 0 &&
                    page.biography === 'undefined'
                  "
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
                >
                  Lưu
                </button>
              </div>
            </div>
          </form>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-4">Chọn danh mục cho trang</h3>
          <h4 class="font-semibold mb-4">Hiện tại: {{ page.page_type }}</h4>
          <ChooseTypePage
            :types="types"
            @getOption="getOption"
            ref="chooseType"
            v-model="type"
          />
        </div>
        <div class="flex flex-col space-y-4">
          <h3 class="text-lg font-semibold">Chọn địa điểm</h3>
          <div class="flex flex-col gap-3">
            <h3 class="font-semibold">Địa chỉ</h3>
            <input
              v-model="address"
              type="text"
              placeholder="Mô tả về bạn"
              class="w-full py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
            />
          </div>
          <div class="flex gap-3 min-w-full">
            <div class="w-full">
              <h4 class="font-semibold">Quốc gia</h4>
              <SelectCountryForm
                v-bind:countries="countries"
                @selectCountry="selectCountry(country?.isoCode)"
                v-model="country"
              />
            </div>
            <div class="w-full">
              <h4 class="font-semibold">Bang/Tỉnh</h4>
              <SelectStateForm
                v-bind:states="statesList"
                @selectState="selectState(state?.isoCode)"
                v-model="state"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="main-right flex justify-center col-span-2 lg:col-span-1">
      <div
        class="p-12 bg-white dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200 border boder-gray-200 rounded-lg w-full"
      >
        <template v-if="errors.length > 0">
          <div
            class="bg-rose-400 text-white text-center rounded-lg px-6 py-3 mb-4"
          >
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>
        </template>
        <div class="flex flex-col h-full justify-between">
          <div class="flex flex-col space-y-4">
            <div class="flex flex-col">
              <h3 class="font-semibold mb-4">Chủ trang</h3>
              <div
                class="flex items-center gap-3 py-2 px-4 bg-slate-700 rounded-lg"
              >
                <img
                  :src="page?.admin?.get_avatar"
                  class="w-12 h-12 rounded-full"
                />
                <h4 class="font-semibold">{{ page?.admin?.name }}</h4>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="font-semibold mb-4">Quản trị viên</h3>
              <div v-if="page?.moderators?.length">
                <div
                  class="flex items-center gap-3 py-2 px-4 bg-slate-700 rounded-lg"
                  v-for="moderator in page?.moderators"
                  :key="moderator.id"
                >
                  <img
                    :src="page?.admin?.get_avatar"
                    class="w-12 h-12 rounded-full"
                  />
                  <h4 class="font-semibold">{{ page?.admin?.name }}</h4>
                </div>
              </div>
              <div v-else class="flex items-center justify-center">
                <button
                    @click="openAddModeratorsModal"
                  class="flex gap-2 items-center justify-center md:w-[50%] w-full px-4 py-2 bg-slate-200 dark:hover:bg-slate-800 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition"
                >
                  <PlusCircleIcon class="w-8" />
                  <span class="font-semibold">Thêm quản trị viên</span>
                </button>
                <AddModeratorsModalVue
                    :options="options"
                    :show="isAddModeratorsOpen"
                    @closeModal="closeAddUsersModal"
                />
              </div>
            </div>
          </div>
          <form
            action=""
            class="space-y-6 flex flex-col"
            v-on:submit.prevent="submitForm"
          >
            <div>
              <label for="">Tên trang</label>
              <input
                v-model="page.name"
                type="text"
                placeholder="Họ và tên"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
              />
            </div>
            <div>
              <label for="">E-mail</label>
              <input
                type="email"
                v-model="page.email"
                placeholder="E-mail của bạn"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
              />
            </div>
            <div class="flex items-center justify-center">
              <button class="w-full btn">Lưu thay đổi</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="main-under flex justify-center col-span-2">
      <div
        class="w-full p-12 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <h1 class="text-2xl">Liên kết/Liên lạc</h1>
        <div class="grid xl:grid-cols-2 grid-cols-1 gap-4 my-4">
          <div class="col-span-1">
            <h2 class="text-lg font-semibold">Trang liên kết</h2>
            <div
              class="flex flex-col gap-2 my-4"
              v-for="website in websites"
              v-bind:key="website.id"
            >
              <WebsiteItem
                v-bind:website="website"
                v-on:deleteWebsite="deleteWebsite"
              />
            </div>
            <form action="" class="space-y-6 mt-4" v-if="addWebsite">
              <div>
                <label for="">Đường link</label>
                <input
                  v-model="websiteUrl"
                  type="text"
                  placeholder="Đường link của bạn"
                  class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
                />
              </div>
              <div class="flex items-center gap-2 justify-end">
                <button
                  @click="openAddWebsiteForm"
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 dark:hover:bg-slate-500 transition"
                >
                  Hủy
                </button>
                <button
                  @click="submitWebsiteForm"
                  type="button"
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 dark:hover:bg-slate-500 transition"
                >
                  Lưu
                </button>
              </div>
            </form>
            <div class="flex justify-center">
              <button
                v-if="!addWebsite"
                @click="openAddWebsiteForm"
                class="md:w-[50%] w-full px-4 py-2 bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-800 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition mt-4"
              >
                Thêm trang liên kết xã hội
              </button>
            </div>
          </div>
          <div class="col-span-1">
            <h2 class="text-lg font-semibold">Số điện thoại</h2>
            <div
              class="flex flex-col gap-2 my-4"
              v-for="number in phoneNumbers"
              v-bind:key="number.id"
            >
              <PhoneNumberItem
                v-bind:phoneNumber="number"
                v-on:deleteWebsite="deletePhoneNumber"
              />
            </div>
            <form action="" class="space-y-6 mt-4" v-if="addPhoneNumber">
              <div>
                <label for="">Các số điện thoại</label>
                <input
                  v-model="phoneNumber"
                  type="url"
                  placeholder="Số điện thoại của bạn"
                  class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
                />
              </div>
              <div class="flex items-center justify-end gap-2">
                <button
                  @click="openAddPhoneNumberForm"
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 dark:hover:bg-slate-500 transition"
                >
                  Hủy
                </button>
                <button
                  @click="submitPhoneNumberForm"
                  type="button"
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 dark:hover:bg-slate-500 transition"
                >
                  Lưu
                </button>
              </div>
            </form>
            <div class="flex justify-center mt-4">
              <button
                v-if="!addPhoneNumber"
                @click="openAddPhoneNumberForm"
                class="md:w-[50%] w-full px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 dark:hover:bg-slate-800 transition"
              >
                Thêm số điện thoại
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "../stores/user";
import { usePageStore } from "../stores/page";
import { onMounted, ref } from "vue";
import pageTypes from "../data/pageTypes";
import { Country, State } from "country-state-city";

import {
  PlusCircleIcon,
} from "@heroicons/vue/20/solid";
import ChooseTypePage from "../components/dropdown/ChooseTypePage.vue";
import SelectCountryForm from "../components/forms/SelectCountryForm.vue";
import SelectStateForm from "../components/forms/SelectStateForm.vue";
import WebsiteItem from "../components/items/profile/WebsiteItem.vue";
import PhoneNumberItem from "../components/items/profile/PhoneNumberItem.vue";
import { RouterLink } from "vue-router";
import AddModeratorsModalVue from '../components/modals/page/AddModeratorsModal.vue';
export default {
  components: {
    ChooseTypePage,
    SelectCountryForm,
    SelectStateForm,
    PlusCircleIcon,
    WebsiteItem,
    PhoneNumberItem,
    RouterLink,
    AddModeratorsModalVue,
  },
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();
    const pageStore = usePageStore();
    const countries = Country.getAllCountries();
    let selected = ref(null);
    let query = ref("");

    const selectedStatus = ref(status[0]);

    return {
      toastStore,
      userStore,
      selectedStatus,
      selected,
      query,
      countries,
      pageStore,
    };
  },
  data() {
    return {
      page: {},
      country: {},
      statesList: [],
      state: {},
      citiesList: [],
      address: "",
      city: {},
      type: {},
      types: pageTypes,
      isOpen: false,
      selection: "",
      errors: [],
      updateBio: false,
      addWebsite: false,
      addPhoneNumber: false,
      websites: [],
      phoneNumbers: [],
      websiteUrl: "",
      phoneNumber: "",
      options: [],
      isAddModeratorsOpen: false
    };
  },

  mounted() {
    this.getPageDetail();
  },

  methods: {
    async getPageDetail() {
      await axios
        .get(`/api/page/get-page/${this.pageStore.pageId}/detail/`)
        .then((res) => {
          this.page = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    closeAddUsersModal() {
      this.isAddModeratorsOpen = false;
    },
    openAddModeratorsModal() {
      this.isAddModeratorsOpen = true;
      axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          const usersId = this.page.moderators.map((user) => user.id);
          const filteredFiends = res.data.friends.filter(
            (friend) => !usersId.includes(friend.id)
          );
          filteredFiends.forEach((friend) => {
            const obj = {};
            obj["label"] = friend.name;
            obj["value"] = friend.id;
            this.options.push(obj);
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    openBioForm() {
      this.updateBio = !this.updateBio;
    },
    getOption(data) {
      this.type = data;
    },
    selectCountry(countryIsoCode) {
      if (countryIsoCode) {
        const states = State.getStatesOfCountry(countryIsoCode);
        this.statesList = states;
      } else {
        console.log("No country selected");
      }
      //console.log(this.country);
    },
    selectState(stateIsoCode) {
      if (stateIsoCode) {
        const cities = City.getCitiesOfState(
          this.country?.isoCode,
          stateIsoCode
        );
        this.citiesList = cities;
        console.log(cities);
      } else {
        console.log("No state selected");
      }
      //console.log(this.state);
    },
  },
};
</script>

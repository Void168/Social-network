<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4" ref="myScrollTarget">
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
                  @click="submitPageBiographyForm"
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
          <div
            v-if="type?.name && type?.name !== page.page_type"
            class="flex items-center justify-center mt-6"
            @click="submitPageTypeForm"
          >
            <button class="btn">Lưu thay đổi</button>
          </div>
        </div>

        <div class="flex flex-col space-y-4">
          <h3 class="text-lg font-semibold">Chọn địa điểm</h3>
          <h4 class="font-semibold mb-4" v-if="page.location">
            Hiện tại: {{ page.location }}
          </h4>
          <div
            v-if="!updatePageLocation"
            class="flex flex-col justify-center items-center space-y-4"
          >
            <button
              @click="openPageLocationForm"
              class="md:w-[50%] w-full px-4 py-2 bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-800 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition"
            >
              Chỉnh sửa địa điểm
            </button>
          </div>
          <div v-else class="flex flex-col gap-3">
            <div class="space-y-4">
              <h3 class="font-semibold">Địa chỉ</h3>
              <input
                v-model="address"
                type="text"
                placeholder="Địa chỉ cụ thể"
                class="w-full py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
              />
            </div>
            <div class="flex gap-3 min-w-full">
              <div class="w-full space-y-4">
                <h4 class="font-semibold">Quốc gia</h4>
                <SelectCountryForm
                  v-bind:countries="countries"
                  @selectCountry="selectCountry(country?.isoCode)"
                  v-model="country"
                />
              </div>
              <div class="w-full space-y-4">
                <h4 class="font-semibold">Bang/Tỉnh</h4>
                <SelectStateForm
                  v-bind:states="statesList"
                  @selectState="selectState(state?.isoCode)"
                  v-model="state"
                />
              </div>
            </div>
            <div class="flex gap-2 justify-end mt-4">
              <button
                @click="openPageLocationForm"
                class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
              >
                Huỷ
              </button>
              <button
                type="button"
                @click="submitPageLocationForm"
                class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
              >
                Lưu
              </button>
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
              <div v-if="page?.admin" class="">
                <RouterLink
                  :to="{ name: 'profile', params: { id: page?.admin?.id } }"
                  class="flex items-center gap-3 py-2 px-4 bg-slate-700 rounded-lg"
                >
                    <img
                      :src="page?.admin?.get_avatar"
                      class="w-12 h-12 rounded-full"
                    />
                    <h4 class="font-semibold">{{ page?.admin?.name }}</h4>
                </RouterLink>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="font-semibold mb-4">Quản trị viên</h3>
              <div v-if="page?.moderators?.length">
                  <div
                    class="py-2 px-4 bg-slate-700 rounded-lg w-full"
                    v-for="moderator in page?.moderators"
                    :key="moderator.id"
                  >
                    <RouterLink
                      :to="{ name: 'profile', params: { id: moderator?.id } }"
                      class="flex items-center gap-3"
                    >
                      <img
                        :src="moderator.get_avatar"
                        class="w-12 h-12 rounded-full"
                      />
                      <h4 class="font-semibold">{{ moderator.name }}</h4>
                    </RouterLink>
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
                  :page="page"
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
                :page="page"
                :website="website"
                :deleteWebsite="deleteWebsite"
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
                :phoneNumber="number"
                :deletePhoneNumber="deletePhoneNumber"
                :page="page"
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
    <!-- <Map :query="page.location"/> -->
    <div
      class="flex justify-end items-end col-span-2 mb-4 dark:text-neutral-200"
    >
      <div
        class="flex flex-col items-end space-y-4 rounded-lg"
        :class="isPasswordOpen ? 'dark:bg-slate-600 p-4' : ''"
      >
        <div v-if="isPasswordOpen">
          <label for="">Mật khẩu</label>
          <input
            autocomplete="off"
            type="password"
            v-model="adminPassword"
            placeholder="Mật khẩu của bạn"
            class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-800 shadow-md dark:border-slate-800 dark:text-neutral-200 rounded-lg"
          />
        </div>
        <div class="flex items-center justify-center gap-2">
          <button
            class="px-4 py-2 font-semibold dark:text-neutral-200 bg-rose-400 rounded-lg shadow-md"
            v-if="isPasswordOpen"
            @click="closePassword"
          >
            Hủy
          </button>
          <button
            class="px-4 py-2 font-semibold dark:text-neutral-200 bg-emerald-400 rounded-lg shadow-md"
            v-if="isPasswordOpen"
            @click="openDeletePageModal"
          >
            Đồng ý
          </button>
          <button
            class="px-4 py-2 font-semibold dark:text-neutral-200 bg-rose-400 rounded-lg shadow-md"
            v-if="!isPasswordOpen && userStore.user.id === page?.admin?.id"
            @click="openPassword"
          >
            Xóa trang
          </button>
        </div>
        <DeletePageModalVue
          :show="isDeletePageOpen"
          @closeDeletePageModal="closeDeletePageModal"
          @deletePage="deletePage"
        />
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

import { PlusCircleIcon } from "@heroicons/vue/20/solid";
import ChooseTypePage from "../components/dropdown/ChooseTypePage.vue";
import SelectCountryForm from "../components/forms/SelectCountryForm.vue";
import SelectStateForm from "../components/forms/SelectStateForm.vue";
import WebsiteItem from "../components/items/profile/WebsiteItem.vue";
import PhoneNumberItem from "../components/items/profile/PhoneNumberItem.vue";
import { RouterLink } from "vue-router";
import AddModeratorsModalVue from "../components/modals/page/AddModeratorsModal.vue";
import DeletePageModalVue from "../components/modals/page/DeletePageModal.vue";
// import Map from '../components/map/Map.vue'
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
    DeletePageModalVue,
    //Map,
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
      updatePageLocation: false,
      addWebsite: false,
      addPhoneNumber: false,
      websites: [],
      phoneNumbers: [],
      websiteUrl: "",
      phoneNumber: "",
      options: [],
      isAddModeratorsOpen: false,
      page_website_is_private: false,
      page_website_only_me: false,
      page_phoneNumber_is_private: false,
      page_phoneNumber_only_me: false,
      adminPassword: "",
      isPasswordOpen: false,
      isDeletePageOpen: false,
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
          this.getPageWebsitesList();
          this.getPagePhoneNumbersList();
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
    openAddPhoneNumberForm() {
      this.addPhoneNumber = !this.addPhoneNumber;
    },
    openAddWebsiteForm() {
      this.addWebsite = !this.addWebsite;
    },
    openPageLocationForm() {
      this.updatePageLocation = !this.updatePageLocation;
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
    },
    submitPageBiographyForm() {
      this.errors = [];

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("biography", this.page.biography);

        axios
          .post(`/api/page/set-biography/${this.page.id}/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message !== "Failed") {
              this.updateBio = false;
              this.toastStore.showToast(
                3500,
                "Đã lưu thông tin chỉnh sửa.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 4000);
            } else {
              this.toastStore.showToast(
                3500,
                `${res.data.message}`,
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    submitPageTypeForm() {
      this.errors = [];

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("page_type", this.type?.name);

        axios
          .post(`/api/page/set-type/${this.page.id}/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message !== "Failed") {
              this.toastStore.showToast(
                3500,
                "Đã lưu thông tin chỉnh sửa.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 4000);
            } else {
              this.toastStore.showToast(
                3500,
                `${res.data.message}`,
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    submitPageLocationForm() {
      let formData = new FormData();
      if (this.address) {
        formData.append(
          "location",
          `${this.address}, ${this.state.name}, ${this.country.name}`
        );
      } else if (this.state.name && !this.address) {
        formData.append("location", `${this.state.name}, ${this.country.name}`);
      } else if (!this.state.name) {
        formData.append("location", `${this.country.name}`);
      }

      axios
        .post(`/api/page/set-location/${this.page.id}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.data.message !== "Failed") {
            this.toastStore.showToast(
              3500,
              "Đã lưu thông tin",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 4000);
          } else {
            this.toastStore.showToast(
              3500,
              `${res.data.message}`,
              "bg-rose-400 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 4000);
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    submitForm() {
      this.errors = [];

      if (this.page.email === "") {
        this.errors.push("E-mail trống");
      }

      if (this.page.name === "") {
        this.errors.push("Tên đăng nhập trống");
      }

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("name", this.page.name);
        formData.append("email", this.page.email);

        axios
          .post(`/api/page/edit-profile-page/${this.page.id}/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message === "information updated") {
              this.toastStore.showToast(
                3500,
                "Đã lưu thông tin chỉnh sửa.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 4000);
            } else {
              this.toastStore.showToast(
                3500,
                `${res.data.message}`,
                "bg-rose-400 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 4000);
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    async getPageWebsitesList() {
      await axios
        .get(`/api/informations/page/${this.page?.id}/websites/`)
        .then((res) => {
          this.websites = res.data.websites;
          //console.log(this.websites)
        })
        .catch((error) => console.log(error));
    },
    async getPagePhoneNumbersList() {
      await axios
        .get(`/api/informations/page/${this.page?.id}/phone-numbers/`)
        .then((res) => {
          this.phoneNumbers = res.data.phone_numbers;
        })
        .catch((error) => console.log(error));
    },
    submitPhoneNumberForm() {
      let formData = new FormData();
      formData.append("phone_number", this.phoneNumber);
      formData.append("is_private", this.page_phoneNumber_is_private);
      formData.append("only_me", this.page_phoneNumber_only_me);
      axios
        .post(
          `/api/informations/page/${this.page.id}/create/phone-number/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((res) => {
          //console.log("data", res.data);

          this.phoneNumbers.unshift(res.data);
          this.phoneNumber = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    submitWebsiteForm() {
      let formData = new FormData();
      formData.append("url", this.websiteUrl);
      formData.append("is_private", this.page_website_is_private);
      formData.append("only_me", this.page_website_only_me);

      axios
        .post(
          `/api/informations/page/${this.page.id}/create/website/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((res) => {
          //console.log("data", res.data);

          this.websites.unshift(res.data);
          this.websiteUrl = "";
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    deletePhoneNumber(id) {
      this.phoneNumbers = this.phoneNumbers.filter(
        (phoneNumber) => phoneNumber.id !== id
      );
    },
    deleteWebsite(id) {
      this.websites = this.websites.filter((website) => website.id !== id);
    },
    deletePage() {
      let formData = new FormData();
      formData.append("username", this.userStore.user.email);
      formData.append("password", this.adminPassword);

      axios
        .post(`/api/page/delete/${this.page.id}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          this.isDeletePageOpen = false;
          if (res.data.message === "success") {
            this.pageStore.outPage();
            this.toastStore.showToast(
              3500,
              "Thành công",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              window.location = "/";
            }, 4000);
          } else {
            this.toastStore.showToast(
              3500,
              "Mật khẩu không đúng",
              "bg-rose-500 text-white"
            );
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    closePassword() {
      this.isPasswordOpen = false;
      this.adminPassword = "";
    },
    openPassword() {
      this.isPasswordOpen = true;
      const targetRef = this.$refs.myScrollTarget;

      this.$nextTick(() => {
        targetRef.scrollTo({
          top: targetRef.scrollHeight,
          left: 0,
          behavior: "smooth",
        });
      });
    },
    closeDeletePageModal() {
      this.isDeletePageOpen = false;
    },
    openDeletePageModal() {
      this.isDeletePageOpen = true;
    },
  },
};
</script>

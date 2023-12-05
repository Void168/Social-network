<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left md:block lg:col-span-1 col-span-2">
      <div
        class="p-12 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <h1 class="mb-6 text-2xl">Chỉnh sửa thông tin</h1>
        <div class="mb-6">
          <label class="text-lg font-semibold">Tiểu sử</label>
          <div
            v-if="!updateBio"
            class="flex flex-col justify-center items-center space-y-4"
          >
            <p
              v-if="userInfo.biography"
              class="text-lg text-center font-semibold"
            >
              {{ userInfo.biography }}
            </p>
            <button
              @click="openBioForm"
              class="w-[50%] px-4 py-2 bg-slate-200 dark:hover:bg-slate-800 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition"
            >
              Chỉnh sửa tiểu sử
            </button>
          </div>
          <form v-else>
            <div>
              <input
                v-model="userInfo.biography"
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
                    biographyForm.content?.length === 0 &&
                    biographyForm.content === 'undefined'
                  "
                  class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
                >
                  Lưu
                </button>
              </div>
            </div>
          </form>
        </div>
        <div class="mb-6">
          <label class="text-lg font-semibold">Quê quán</label>
          <div
            v-if="!updateHometown"
            class="flex flex-col justify-center items-center space-y-4"
          >
            <p
              v-if="userInfo.hometown"
              class="text-lg text-center font-semibold"
            >
              {{ userInfo.hometown }}
            </p>
            <button
              @click="openHometownForm"
              class="w-[50%] px-4 py-2 bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-800 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition"
            >
              Chỉnh sửa quê quán
            </button>
          </div>
          <form v-else>
            <div class="flex gap-2">
              <div>
                <p>Quốc gia</p>
                <SelectCountryForm
                  v-bind:countries="countries"
                  @selectCountry="selectCountry(country?.isoCode)"
                  v-model="country"
                />
              </div>
              <div>
                <p>Tỉnh thành/Bang</p>
                <SelectStateForm
                  v-bind:states="statesList"
                  @selectState="selectState(state?.isoCode)"
                  v-model="state"
                />
              </div>
              <div>
                <p>Thành phố/Huyện</p>
                <SelectCityForm
                  v-bind:cities="citiesList"
                  @selectCity="selectCity"
                  v-model="city"
                />
              </div>
            </div>
            <div class="flex gap-2 justify-end mt-4">
              <button
                @click="openHometownForm"
                class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
              >
                Huỷ
              </button>
              <button
                type="button"
                @click="submitHometownForm"
                class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
              >
                Lưu
              </button>
            </div>
          </form>
        </div>
        <div class="mb-6">
          <label class="text-lg font-semibold">Nơi sinh sống</label>
          <div
            v-if="!updateLivingCity"
            class="flex flex-col justify-center items-center space-y-4"
          >
            <p
              v-if="userInfo.living_city"
              class="text-lg text-center font-semibold"
            >
              {{ userInfo.living_city }}
            </p>
            <button
              @click="openLivingCityForm"
              class="w-[50%] px-4 py-2 bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-800 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition"
            >
              Chỉnh sửa nơi sinh sống
            </button>
          </div>
          <form v-else action="" class="flex flex-col">
            <div class="flex gap-2">
              <div>
                <p>Quốc gia</p>
                <SelectCountryForm
                  v-bind:countries="countries"
                  @selectCountry="selectLivedCountry(country?.isoCode)"
                  v-model="country"
                />
              </div>
              <div>
                <p>Tỉnh thành/Bang</p>
                <SelectStateForm
                  v-bind:states="statesList"
                  @selectState="selectLivedState(state?.isoCode)"
                  v-model="state"
                />
              </div>
              <div>
                <p>Thành phố/Huyện</p>
                <SelectCityForm
                  v-bind:cities="citiesList"
                  @selectCity="selectLivedCity"
                  v-model="city"
                />
              </div>
            </div>
            <div class="flex gap-2 justify-end mt-4">
              <button
                @click="openLivingCityForm"
                class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
              >
                Hủy
              </button>
              <button
                type="button"
                @click="submitLivingCityForm"
                class="px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-300 transition"
              >
                Lưu
              </button>
            </div>
          </form>
        </div>
        <div class="flex justify-between mb-4">
          <h2 class="font-semibold text-lg">Mối quan hệ hiện tại:</h2>
          <div
            v-if="
              userInfo.relationship_status !== 'Độc thân' ||
              userInfo.relationship_status ||
              partnerId != ''
            "
            class="flex gap-2"
          >
            <div class="flex gap-1">
              <h2>
                {{ userInfo.relationship_status }}
              </h2>
              <h2 v-if="partnerId != '' && partnerId != 'null'">
                với
                <strong @click="toPartner" class="cursor-pointer">
                  {{ partner?.user?.name }}
                </strong>
              </h2>
            </div>

            <div
              v-if="userInfo.relationship_status !== ''"
              class="hover:underline cursor-pointer"
              @click="openModal"
            >
              Xóa
            </div>
            <DeleteRelationshipModal
              :show="isOpen"
              @closeModal="closeModal"
              @deleteRelationship="deleteRelationship"
            />
          </div>
        </div>
        <form
          action=""
          class="space-y-6"
          v-on:submit.prevent="sendRelationshipRequest"
        >
          <Listbox v-model="selectedStatus" class="w-full">
            <div class="relative mt-1 flex justify-end w-2/12">
              <ListboxButton
                class="relative flex justify-center w-full cursor-default rounded-lg font-semibold bg-gray-200 dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm"
              >
                <span
                  class="block truncate"
                  v-if="userInfo.relationship_status"
                  >{{ userInfo.relationship_status }}</span
                >
                <span class="block truncate" v-else>{{
                  selectedStatus.name
                }}</span>
                <span
                  class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
                >
                  <ChevronUpDownIcon
                    class="h-5 w-5 text-gray-400"
                    aria-hidden="true"
                  />
                </span>
              </ListboxButton>

              <transition
                leave-active-class="transition duration-100 ease-in"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
              >
                <ListboxOptions
                  class="absolute top-10 w-full z-50 mt-1 max-h-60 overflow-auto rounded-md bg-white dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
                >
                  <ListboxOption
                    v-slot="{ active, selected }"
                    v-for="selectOption in status"
                    :key="selectOption.name"
                    :value="selectOption"
                    as="template"
                    @click="getOption"
                  >
                    <li
                      :class="[
                        active
                          ? 'bg-emerald-100 text-emerald-900'
                          : 'text-gray-900 dark:text-neutral-200',
                        'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]"
                    >
                      <span
                        :value="selection"
                        :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                        ]"
                        >{{ selectOption.name }}</span
                      >
                      <span
                        v-if="selected"
                        class="absolute inset-y-0 left-0 flex items-center pl-3 text-emerald-600"
                      >
                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                      </span>
                    </li>
                  </ListboxOption>
                </ListboxOptions>
              </transition>
            </div>
          </Listbox>
          <div
            v-if="
              selectedStatus.name === 'Hẹn hò' ||
              selectedStatus.name === 'Đã đính hôn' ||
              selectedStatus.name === 'Đã kết hôn' ||
              selectedStatus.name === 'Tìm hiểu'
            "
          >
            <h2>Bạn đời</h2>
            <!-- v-model="relationshipForm.partner" -->
            <Combobox v-model="partner">
              <div class="relative mt-1">
                <div
                  class="relative w-full cursor-default overflow-hidden rounded-lg bg-white text-left shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm"
                >
                  <ComboboxInput
                    class="w-full border-none py-2 pl-3 pr-10 text-sm leading-5 text-gray-900 focus:ring-0"
                    @change="query = $event.target.value"
                    :displayValue="(friend) => friend.name"
                  />
                  <ComboboxButton
                    class="absolute inset-y-0 right-0 flex items-center pr-2"
                  >
                    <ChevronUpDownIcon
                      class="h-5 w-5 text-gray-400"
                      aria-hidden="true"
                    />
                  </ComboboxButton>
                </div>
                <TransitionRoot
                  leave="transition ease-in duration-100"
                  leaveFrom="opacity-100"
                  leaveTo="opacity-0"
                  @after-leave="query = ''"
                >
                  <ComboboxOptions
                    class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
                  >
                    <div
                      v-if="filteredFriends.length === 0 && query !== ''"
                      class="relative cursor-default select-none py-2 px-4 text-gray-700"
                    >
                      Không tìm thấy
                    </div>

                    <ComboboxOption
                      v-for="friend in filteredFriends"
                      as="template"
                      :key="friend.id"
                      :value="friend"
                      v-slot="{ selected, active }"
                    >
                      <li
                        @click="getFriendInfo(friend)"
                        class="relative cursor-default select-none py-2 pl-10 pr-4"
                        :class="{
                          'bg-teal-600 text-white': active,
                          'text-gray-900': !active,
                        }"
                      >
                        <span
                          class="block truncate"
                          :class="{
                            'font-medium': selected,
                            'font-normal': !selected,
                          }"
                        >
                          {{ friend.name }}
                        </span>
                        <span
                          v-if="selected"
                          class="absolute inset-y-0 left-0 flex items-center pl-3"
                          :class="{
                            'text-white': active,
                            'text-teal-600': !active,
                          }"
                        >
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ComboboxOption>
                  </ComboboxOptions>
                </TransitionRoot>
              </div>
            </Combobox>
          </div>
          <div
            v-if="selectedStatus.name !== 'Trạng thái'"
            class="flex items-center justify-center mt-6"
          >
            <button class="btn">Lưu thay đổi</button>
          </div>
        </form>
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
        <form
          action=""
          class="space-y-6 flex flex-col"
          v-on:submit.prevent="submitForm"
        >
          <div>
            <label for="">Tên người dùng</label>
            <input
              v-model="form.name"
              type="text"
              placeholder="Họ và tên"
              class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
            />
          </div>
          <div>
            <label for="">Biệt danh</label>
            <input
              v-model="userInfo.nickname"
              type="text"
              placeholder="Biệt danh của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
            />
          </div>
          <div>
            <label for="">E-mail</label>
            <input
              type="email"
              v-model="form.email"
              placeholder="E-mail của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
            />
          </div>
          <div class="flex justify-between items-center">
            <div class="w-[20%]">
              <p>Giới tính: {{ userInfo.gender }}</p>
              <GenderSelector
                :genders="genders"
                v-model="gender.name"
                :gender="gender"
                @selectGender="selectGender"
                :user="userInfo"
              />
            </div>
            <RouterLink
              to="/profile/edit/password"
              class="hover:underline flex justify-end"
              >Đổi mật khẩu</RouterLink
            >
          </div>
          <div class="flex items-center justify-center">
            <button class="w-full btn">Lưu thay đổi</button>
          </div>
        </form>
      </div>
    </div>
    <div class="main-under flex justify-center col-span-2">
      <div
        class="w-full p-12 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <h1 class="text-2xl">Liên kết/Liên lạc</h1>
        <div class="grid grid-cols-2 gap-4 my-4">
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
                class="w-[50%] px-4 py-2 bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-800 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 transition mt-4"
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
                class="w-[50%] px-4 py-2 bg-slate-200 dark:bg-slate-700 rounded-xl shadow-md font-semibold hover:bg-slate-500 hover:text-neutral-200 dark:hover:bg-slate-800 transition"
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
import { onMounted, ref } from "vue";
import { Country, State, City } from "country-state-city";
import relationshipStatus from "../data/relationshipStatus";

import {
  Listbox,
  ListboxLabel,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from "@headlessui/vue";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid";
import getUserInfo from "../api/getUserInfo";
import DeleteRelationshipModal from "../components/modals/DeleteRelationship.vue";
import SelectCountryForm from "../components/forms/SelectCountryForm.vue";
import SelectCityForm from "../components/forms/SelectCityForm.vue";
import SelectStateForm from "../components/forms/SelectStateForm.vue";
import GenderSelector from "../components/dropdown/GenderSelector.vue";
import WebsiteItem from "../components/items/WebsiteItem.vue";
import PhoneNumberItem from "../components/items/PhoneNumberItem.vue";
import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  components: {
    Listbox,
    ListboxLabel,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
    Combobox,
    ComboboxInput,
    ComboboxButton,
    ComboboxOptions,
    ComboboxOption,
    TransitionRoot,
    CheckIcon,
    ChevronUpDownIcon,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
    DeleteRelationshipModal,
    SelectCountryForm,
    SelectCityForm,
    SelectStateForm,
    GenderSelector,
    WebsiteItem,
    PhoneNumberItem,
    RouterLink,
  },
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();
    const userInfo = ref({});
    const countries = Country.getAllCountries();
    let selected = ref(null);
    let query = ref("");

    onMounted(async () => {
      const res = await getUserInfo(userStore.user.id);
      userInfo.value = res;
    });

    const status = relationshipStatus;
    const selectedStatus = ref(status[0]);

    return {
      toastStore,
      userStore,
      selectedStatus,
      userInfo,
      selected,
      query,
      countries,
    };
  },

  computed: {
    filteredFriends() {
      return this.query === ""
        ? this.friends
        : this.friends.filter((friend) => {
            friend.name
              .toLowerCase()
              .replace(/\s+/g, "")
              .includes(this.query.toLowerCase().replace(/\s+/g, ""));
          });
    },
    getFriendId() {
      return this.query === ""
        ? this.friends
        : this.friends.filter((friend) => {
            friend.id;
          });
    },
  },

  data() {
    return {
      form: {
        email: this.userStore.user.email,
        name: this.userStore.user.name,
      },
      biographyForm: {
        content: this.userInfo.biography,
      },
      status: relationshipStatus,
      genders: [{ name: "Nam" }, { name: "Nữ" }, { name: "Khác" }],
      relationshipForm: {
        status: this.userInfo.relationship_status,
        partner: {
          id: null,
        },
      },
      country: {},
      statesList: [],
      state: {},
      citiesList: [],
      city: {},
      isOpen: false,
      selection: "",
      errors: [],
      friends: [],
      partnerId: "",
      partner: {
        id: null,
      },
      updateBio: false,
      updateHometown: false,
      updateLivingCity: false,
      addWebsite: false,
      addPhoneNumber: false,
      gender: {},
      websites: [],
      phoneNumbers: [],
      websiteUrl: "",
      phoneNumber: "",
      website_is_private: false,
      website_only_me: false,
      phoneNumber_is_private: false,
      phoneNumber_only_me: false,
    };
  },

  beforeMount() {
    this.getUserInfo();
  },

  mounted() {
    this.getFriends();
    this.getWebsitesList();
    this.getPhoneNumbersList();
    console.log(this.websiteUrl);
  },

  methods: {
    selectGender() {
      // console.log(this.gender);
      this.userInfo.gender = this.gender.name.name;
    },
    getUserInfo() {
      axios
        .get(`/api/user-info/${this.userStore.user.id}`)
        .then((res) => {
          this.partnerId = res.data.user.partner;
          this.getPartnerInfo();
        })
        .catch((error) => console.log(error));
    },
    getPartnerInfo() {
      if (this.partnerId !== "" && this.partnerId !== "null") {
        axios
          .get(`/api/user-info/${this.partnerId}`)
          .then((res) => {
            this.partner = res.data;
          })
          .catch((error) => console.log(error));
      } else {
        console.log("partnerId null");
      }
    },
    getOption() {
      this.selection = this.selectedStatus;
    },
    getFriends() {
      axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          this.friends = res.data.friends;
          this.user = res.data.user;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getFriendInfo(value) {
      this.partner = value;
    },
    getWebsitesList() {
      axios
        .get(`/api/informations/${this.userStore.user.id}/websites/`)
        .then((res) => {
          this.websites = res.data.websites;
          //console.log(this.websites)
        })
        .catch((error) => console.log(error));
    },
    getPhoneNumbersList() {
      axios
        .get(`/api/informations/${this.userStore.user.id}/phone-numbers/`)
        .then((res) => {
          this.phoneNumbers = res.data.phone_numbers;
        })
        .catch((error) => console.log(error));
    },
    toPartner() {
      this.$router.push(`/profile/${this.partnerId}`);
    },
    openBioForm() {
      this.updateBio = !this.updateBio;
    },
    openHometownForm() {
      this.updateHometown = !this.updateHometown;
    },
    openLivingCityForm() {
      this.updateLivingCity = !this.updateLivingCity;
    },
    openAddWebsiteForm() {
      this.addWebsite = !this.addWebsite;
    },
    openAddPhoneNumberForm() {
      this.addPhoneNumber = !this.addPhoneNumber;
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
    selectCity() {
      //console.log("Select city");
      //console.log(this.city);
    },
    submitHometownForm() {
      let formData = new FormData();
      if (this.city.name) {
        formData.append(
          "hometown",
          `${this.city.name}, ${this.state.name}, ${this.country.name}`
        );
      }
      if (!this.city.name) {
        formData.append("hometown", `${this.state.name}, ${this.country.name}`);
      }
      if (!this.city.name && !this.state.name) {
        formData.append("hometown", `${this.country.name}`);
      }

      axios
        .post("/api/set-hometown/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.data.message !== "Failed") {
            this.toastStore.showToast(
              5000,
              "Đã lưu thông tin quê quán",
              "bg-emerald-500 text-white"
            );
            this.updateHometown = false;
          } else {
            this.toastStore.showToast(
              5000,
              `${res.data.message}`,
              "bg-rose-400 text-white"
            );
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    submitLivingCityForm() {
      let formData = new FormData();
      if (this.city.name) {
        formData.append(
          "living_city",
          `${this.city.name}, ${this.state.name}, ${this.country.name}`
        );
      }
      if (!this.city.name) {
        formData.append(
          "living_city",
          `${this.state.name}, ${this.country.name}`
        );
      }
      if (!this.city.name && !this.state.name) {
        formData.append("living_city", `${this.country.name}`);
      }

      axios
        .post("/api/set-livingcity/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.data.message !== "Failed") {
            this.toastStore.showToast(
              5000,
              "Đã lưu thông tin nơi sống",
              "bg-emerald-500 text-white"
            );
            this.updateLivingCity = false;
          } else {
            this.toastStore.showToast(
              5000,
              `${res.data.message}`,
              "bg-rose-400 text-white"
            );
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    selectLivedCountry(countryIsoCode) {
      if (countryIsoCode) {
        const states = State.getStatesOfCountry(countryIsoCode);
        this.statesList = states;
      } else {
        console.log("No country selected");
      }
    },
    selectLivedState(stateIsoCode) {
      if (stateIsoCode) {
        const cities = City.getCitiesOfState(
          this.country?.isoCode,
          stateIsoCode
        );
        this.citiesList = cities;
      } else {
        console.log("No state selected");
      }
    },
    selectLivedCity() {
      //console.log(this.city);
    },
    submitBiographyForm() {
      this.errors = [];

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("biography", this.userInfo.biography);

        axios
          .post("/api/set-biography/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message !== "Failed") {
              this.toastStore.showToast(
                5000,
                "Đã lưu thông tin chỉnh sửa.",
                "bg-emerald-500 text-white"
              );
              this.updateBio = false;
              // this.biographyForm.content = userInfo.biography
            } else {
              this.toastStore.showToast(
                5000,
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
    sendRelationshipRequest() {
      let formRelationshipData = new FormData();
      if (
        this.selection.name === "Độc thân" ||
        this.selection.name === "Có mối quan hệ phức tạp" ||
        this.selection.name === "Đã ly thân" ||
        this.selection.name === "Đã ly hôn"
      ) {
        formRelationshipData.append("relationship_status", this.selection.name);

        formRelationshipData.append("partner", "");

        axios
          .post("/api/set-relationship/", formRelationshipData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            console.log(res.data);

            if (res.data.message === "Failed") {
              this.toastStore.showToast(
                5000,
                "Thiết lập tình trạng quan hệ thất bại",
                "bg-rose-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                3000,
                "Thiết lập tình trạng quan hệ thành công",
                "bg-emerald-400 text-white"
              );
              // setTimeout(() => {
              //   this.$router.go(0);
              // }, 3500);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        formRelationshipData.append("relationship_status", this.selection.name);

        formRelationshipData.append("partner", this.partner.id);
        axios
          .post(
            `/api/relationship/${this.partner.id}/request/`,
            formRelationshipData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )
          .then((res) => {
            console.log(res.data);
            this.status = res.data.message;
            if (this.status === "request already sent") {
              this.toastStore.showToast(
                5000,
                "Không thể gửi lần 2",
                "bg-rose-400 text-white"
              );
            } else if (this.status === "don't be a third person") {
              this.toastStore.showToast(
                5000,
                "Đừng trở thành người thứ 3",
                "bg-rose-400 text-white"
              );
            } else {
              this.toastStore.showToast(
                3000,
                "Đã gửi lời mời",
                "bg-emerald-400 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 3500);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    deleteRelationship() {
      axios
        .delete("/api/delete-relationship/")
        .then((res) => {
          setTimeout(() => {
            this.closeModal();
          }, 500);
          this.toastStore.showToast(
            5000,
            "Đã xóa mối quan hệ",
            "bg-emerald-500 text-white"
          );
          setTimeout(() => {
            this.$router.go(0);
          }, 6000);
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            5000,
            "Xóa mối quan hệ thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
    submitForm() {
      this.errors = [];

      if (this.form.email === "") {
        this.errors.push("E-mail trống");
      }

      if (this.form.name === "") {
        this.errors.push("Tên đăng nhập trống");
      }

      if (
        this.form.name.includes("^[\w.@+-]+\Z") ||
        /\s/.test(this.form.name)
      ) {
        this.errors.push("Tên chi cho phép chứa các ký tự . hoặc _");
      }

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("name", this.form.name);
        formData.append("nickname", this.userInfo.nickname);
        formData.append("email", this.form.email);
        formData.append("gender", this.userInfo.gender);

        axios
          .post("/api/edit-profile/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message === "information updated") {
              this.toastStore.showToast(
                5000,
                "Đã lưu thông tin chỉnh sửa.",
                "bg-emerald-500 text-white"
              );

              this.userStore.setUserInfo({
                id: this.userStore.user.id,
                name: this.form.name,
                email: this.form.email,
                avatar: this.userInfo.get_avatar,
              });

              this.$router.go(0);
            } else {
              this.toastStore.showToast(
                5000,
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
    submitPhoneNumberForm() {
      let formData = new FormData();
      formData.append("phone_number", this.phoneNumber);
      formData.append("is_private", this.phoneNumber_is_private);
      formData.append("only_me", this.phoneNumber_only_me);

      axios
        .post("/api/informations/create/phone-number/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          //console.log("data", res.data);

          this.phoneNumbers.unshift(res.data);
          this.phoneNumber = "";
          this.phoneNumber_is_private = false;
          this.phoneNumber_only_me = false;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    submitWebsiteForm() {
      let formData = new FormData();
      formData.append("url", this.websiteUrl);
      formData.append("is_private", this.website_is_private);
      formData.append("only_me", this.website_only_me);

      axios
        .post("/api/informations/create/website/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          //console.log("data", res.data);

          this.websites.unshift(res.data);
          this.websiteUrl = "";
          this.website_is_private = false;
          this.website_only_me = false;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    deleteWebsite(id) {
      this.websites = this.websites.filter((website) => website.id !== id);
    },
    deletePhoneNumber(id) {
      this.phoneNumbers = this.phoneNumbers.filter(
        (phoneNumber) => phoneNumber.id !== id
      );
    },
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
});
</script>

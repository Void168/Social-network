<template>
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 xs:grid-cols-1 gap-4">
    <div class="main-left md:block xs:hidden">
      <div
        class="p-12 bg-white border border-gray-200 rounded-lg dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
      >
        <h1 class="mb-6 text-2xl">Chỉnh sửa thông tin</h1>
        <div class="flex justify-between">
          <h2>Mối quan hệ:</h2>
          <h2
            v-if="
              userInfo.relationship_status !== 'Độc thân' ||
              userInfo.relationship_status
            "
          >
            Hiện tại
            <strong
              >{{ userInfo.relationship_status }} với
              <RouterLink
                :to="{ name: 'profile', params: { id: partnerId } }"
                >{{ partner?.user?.name }}</RouterLink
              ></strong
            >
          </h2>
        </div>
        <form
          action=""
          class="space-y-6"
          v-on:submit.prevent="submitRelationship"
        >
          <Listbox v-model="selectedStatus" class="w-full">
            <div class="relative mt-1 flex justify-end w-2/12">
              <ListboxButton
                class="relative flex justify-center w-full cursor-default rounded-lg font-semibold bg-gray-200 dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm"
              >
                <span class="block truncate">{{ selectedStatus.name }}</span>
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
                      Nothing found.
                    </div>

                    <ComboboxOption
                      v-for="friend in filteredFriends"
                      as="template"
                      :key="friend.id"
                      :value="friend"
                      v-slot="{ selected, active }"
                    >
                      <li
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

        <RouterLink
          to="/profile/edit/password"
          class="hover:underline flex justify-end"
          >Đổi mật khẩu</RouterLink
        >
      </div>
    </div>

    <div class="main-right flex justify-center">
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
        <form action="" class="space-y-6" v-on:submit.prevent="submitForm">
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
            <label for="">E-mail</label>
            <input
              type="email"
              v-model="form.email"
              placeholder="E-mail của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
            />
          </div>
          <div class="flex flex-col">
            <label class="text-center">Ảnh đại diện</label>
            <input type="file" ref="file" />
          </div>
          <div class="flex items-center justify-center">
            <button class="w-full btn">Lưu thay đổi</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "../stores/user";
import { onMounted, ref } from "vue";
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
  },
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();
    const userInfo = ref({});
    let selected = ref(null);
    let query = ref("");

    onMounted(async () => {
      const res = await getUserInfo(userStore.user.id);
      userInfo.value = res;
    });

    const status = [
      { name: "Trạng thái" },
      { name: "Độc thân" },
      { name: "Hẹn hò" },
      { name: "Đã đính hôn" },
      { name: "Đã kết hôn" },
      { name: "Tìm hiểu" },
      { name: "Có mối quan hệ phức tạp" },
      { name: "Đã ly thân" },
      { name: "Đã ly hôn" },
      { name: "Góa" },
    ];
    const selectedStatus = ref(status[0]);

    return {
      toastStore,
      userStore,
      selectedStatus,
      userInfo,
      selected,
      query,
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
  },

  data() {
    return {
      form: {
        email: this.userStore.user.email,
        name: this.userStore.user.name,
        avatar: null,
      },
      status: [
        { name: "Trạng thái" },
        { name: "Độc thân" },
        { name: "Hẹn hò" },
        { name: "Đã đính hôn" },
        { name: "Đã kết hôn" },
        { name: "Tìm hiểu" },
        { name: "Có mối quan hệ phức tạp" },
        { name: "Đã ly thân" },
        { name: "Đã ly hôn" },
        { name: "Góa" },
      ],
      relationshipForm: {
        status: this.userInfo.relationship_status,
        partner: {
          id: null,
        },
      },
      selection: "",
      errors: [],
      friends: [],
      partnerId: "",
      partner: {
        id: null,
      },
    };
  },

  beforeMount() {
    this.getFriends();
    this.getUserInfo();
  },

  methods: {
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
      axios
        .get(`/api/user-info/${this.partnerId}`)
        .then((res) => {
          this.partner = res.data;
          console.log(res.data);
        })
        .catch((error) => console.log(error));
    },
    getOption() {
      this.selection = this.selectedStatus;
    },
    getFriends() {
      axios
        .get(`/api/friends/${this.userStore.user.id}/`)
        .then((res) => {
          console.log(res.data);

          this.friendshipRequests = res.data.requests;
          this.friends = res.data.friends;
          this.user = res.data.user;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitRelationship() {
      let formRelationshipData = new FormData();
      if (this.selection.name === "Trạng thái") {
        this.userInfo.relationship_status = "";
      } else {
        formRelationshipData.append("relationship_status", this.selection.name);
      }
      formRelationshipData.append("partner", this.partner.id);

      axios
        .post("/api/set-relationship/", formRelationshipData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (!res.data.error) {
            this.toastStore.showToast(
              2500,
              "Đã lưu thông tin mối quan hệ.",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 3000);
          } else {
            this.toastStore.showToast(
              5000,
              `${res.data.error}`,
              "bg-rose-400 text-white"
            );
          }
        })
        .catch((error) => {
          console.log("error", error);
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

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("avatar", this.$refs.file.files[0]);
        formData.append("name", this.form.name);
        formData.append("email", this.form.email);

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
                avatar: res.data.user.get_avatar,
              });

              this.$router.go(-1);
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
  },
});
</script>

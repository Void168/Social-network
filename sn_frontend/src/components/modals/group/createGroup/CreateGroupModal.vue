<template>
  <TransitionRoot appear as="template">
    <Dialog as="div" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto z-50">
        <div class="flex items-center justify-center text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full h-screen transform grid grid-cols-5 overflow-hidden bg-white dark:bg-slate-900 text-left align-middle shadow-xl transition-all"
            >
              <div
                class="lg:col-span-1 hidden bg-slate-800 dark:text-neutral-200 border-r-[1px] border-slate-700 lg:flex flex-col justify-between"
              >
                <div>
                  <button
                    @click="removeAll"
                    class="m-4 p-2 bg-slate-900 rounded-full hover:bg-slate-700"
                  >
                    <XMarkIcon
                      @click="$emit('closeCreateGroupModal')"
                      class="text-neutral-200 h-8 w-8 cursor-pointer transition"
                    />
                  </button>
                  <div class="flex justify-between items-center px-4">
                    <h2 class="text-2xl font-bold min-w-max">Tạo nhóm</h2>
                  </div>

                  <div
                    class="flex gap-3 my-4 py-4 items-center border-b border-slate-700 px-4"
                  >
                    <img
                      :src="userStore.user.avatar"
                      alt="group-owner"
                      class="w-10 h-10 rounded-full shadow-lg"
                    />
                    <div>
                      <h4 class="font-semibold">
                        {{ userStore.user.name }}
                      </h4>
                      <h5 class="text-sm">Chủ nhóm</h5>
                    </div>
                  </div>
                  <div class="px-4 space-y-4">
                    <MUILikedInput :placeholder="'Tên nhóm'" v-model="name" :type="'text'"/>
                    <div class="flex flex-col gap-2">
                      <div class="flex items-center gap-2">
                        <h4>Chọn quyền riêng tư</h4>
                        <GlobeAsiaAustraliaIcon
                          class="w-6"
                          v-if="privacy.name === 'Công khai'"
                        />
                        <LockClosedIcon
                          class="w-6"
                          v-if="privacy.name === 'Riêng tư'"
                        />
                      </div>
                      <PrivacySelector
                        @getOption="getPrivacyOption"
                        :privacies="privacies"
                        v-model="privacy"
                        class="w-full border rounded-md dark:border-slate-600 py-2"
                        :style="'w-full mt-10'"
                      />
                      <h5 v-if="privacy.name === 'Công khai'" class="text-xs">
                        Thành viên và khách truy cập có thể đăng bài trong nhóm.
                        Quản trị viên có thể xét duyệt người lần đầu tham gia.
                      </h5>
                      <h5 v-if="privacy.name === 'Riêng tư'" class="text-xs">
                        Để bảo vệ quyền riêng tư của thành viên, nhóm riêng tư
                        không thể chuyển thành công khai.
                        <span class="text-emerald-400 underline cursor-pointer"
                          >Tìm hiểu thêm</span
                        >
                      </h5>
                    </div>
                    <PrivacySelector
                      v-if="privacy.name === 'Riêng tư'"
                      @getOption="getShowOption"
                      :privacies="showOptions"
                      v-model="showOption"
                      class="w-full border rounded-md dark:border-slate-600 py-2"
                      :style="'w-full mt-10'"
                    />
                    <Multiselect
                      v-model="value"
                      mode="tags"
                      :close-on-select="false"
                      :searchable="true"
                      :create-option="false"
                      :options="friendOptions"
                      :limit="3"
                      :infinite="true"
                      :on-create="getValue(value)"
                      placeholder="Mời bạn bè (không bắt buộc)"
                      @click="getFriends"
                      class="dark:text-gray-800 dark:bg-slate-800 border dark:border-slate-700"
                      :classes="{
                        tagsSearch:
                          'absolute inset-0 border-0 dark:bg-slate-800 dark:text-neutral-200 outline-none focus:ring-0 appearance-none p-0 text-base font-sans box-border w-full',
                        container:
                          'relative mx-auto w-full flex items-center justify-end box-border cursor-pointer border dark:border-slate-700 rounded bg-white text-base leading-snug outline-none',
                        option:
                          'flex items-center justify-start box-border dark:border-slate-700 text-left cursor-pointer text-base leading-snug py-2 px-3 dark:bg-slate-800 dark:text-neutral-200',
                        dropdown:
                          'max-h-60 absolute -left-px -right-px bottom-0 transform translate-y-full border dark:border-slate-700 -mt-px overflow-y-scroll z-50 bg-white flex flex-col rounded-b scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800',
                        dropdownTop:
                          '-translate-y-full top-px bottom-auto rounded-b-none rounded-t',
                        dropdownHidden: 'hidden',
                        optionPointed:
                          'text-gray-800 bg-gray-100 dark:text-emerald-500 dark:bg-slate-100 font-semibold',
                      }"
                    >
                    </Multiselect>
                  </div>
                </div>
                <div class="p-4">
                  <button
                    :disabled="isDisabled"
                    @click="submitForm"
                    class="w-full py-2 px-4 shadow-md rounded-lg font-semibold"
                    :class="
                      isDisabled
                        ? 'dark:bg-slate-500'
                        : 'dark:bg-emerald-500 dark:hover:bg-emerald-400 duration-75'
                    "
                  >
                    Tạo
                  </button>
                </div>
              </div>
              <div
                class="lg:col-span-4 col-span-5 flex lg:flex-row flex-col items-center gap-6 w-full"
              >
                <DisplayGroup
                  :isDeviceActive="isDeviceActive"
                  :name="name"
                  :privacy="privacy"
                  :showOption="showOption"
                  @computerActive="computerActive"
                  @deviceActive="deviceActive"
                />
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../../../stores/user";
import { useToastStore } from "../../../../stores/toast";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import {
  XMarkIcon,
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/solid";
import MUILikedInput from "../../../input/MUILikedInput.vue";
import PrivacySelector from "../../../dropdown/PrivacySelector.vue";
import Multiselect from "@vueform/multiselect";
import DisplayGroup from "./DisplayGroup.vue";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    Multiselect,
    DisplayGroup,
    XMarkIcon,
    MUILikedInput,
    PrivacySelector,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
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
    isOpen: Boolean,
  },

  data() {
    return {
      body: "",
      caption: "",
      name: "",
      isPrivateGroup: false,
      isShowGroup: true,
      isDeviceActive: false,
      privacy: { name: "Công khai" },
      showOption: { name: "Hiển thị" },
      privacies: [{ name: "Công khai" }, { name: "Riêng tư" }],
      showOptions: [{ name: "Hiển thị" }, { name: "Ẩn" }],
      value: [],
      friendOptions: [],
    };
  },

  computed: {
    isDisabled() {
      return this.name === "" || !this.privacy.name;
    },
  },

  methods: {
    removeAll() {
      this.name = "";
      this.isDeviceActive = false;
      this.isPrivateGroup = false;
      this.isShowGroup = true;
      this.privacy = { name: "Công khai" };
      this.showOption = { name: "Hiển thị" };
    },
    computerActive() {
      this.isDeviceActive = false;
    },
    deviceActive() {
      this.isDeviceActive = true;
    },
    getPrivacyOption() {
      if (this.privacy.name === "Công khai") {
        this.isPrivateGroup = false;
      } else {
        this.isPrivateGroup = true;
      }
    },
    getShowOption() {
      if (this.showOption.name === "Hiển thị") {
        this.isShowGroup = true;
      } else {
        this.isShowGroup = false;
      }
    },
    getValue(value) {
      this.value = value;
    },
    async getFriends() {
      if (!this.friendOptions.length) {
        await axios
          .get(`/api/friends/${this.userStore.user.id}/`)
          .then((res) => {
            const fiends = res.data.friends;
            fiends.forEach((friend) => {
              const obj = {};
              obj["label"] = friend.name;
              obj["value"] = friend.id;
              this.friendOptions.push(obj);
            });
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    submitForm() {
      let formData = new FormData();

      formData.append("name", this.name);
      formData.append("is_private_group", this.isPrivateGroup);
      formData.append("show_group", this.isShowGroup);

      axios
        .post("/api/group/create/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log(res.data);
          if (!res.data.error) {
            this.toastStore.showToast(
              3500,
              "Tạo nhóm thành công.",
              "bg-emerald-500 text-white"
            );
          }
        }).catch((error) => {
          this.toastStore.showToast(
            3500,
            "Tạo nhóm thất bại.",
            "bg-rose-500 text-white"
          );
          console.log(error)
        });
    },
  },
});
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

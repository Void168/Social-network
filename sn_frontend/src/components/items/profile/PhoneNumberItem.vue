<template>
  <div class="bg-slate-200 dark:bg-slate-700 p-4 rounded-lg shadow-md">
    <div class="flex md:flex-row flex-col gap-4 justify-between items-center">
      <input
        v-model="number"
        v-if="edit"
        class="w-[60%] mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 rounded-lg"
      />
      <p v-else>{{ phoneNumber.phone_number }}</p>
      <div class="flex gap-2 sm:flex-row vs:flex-col w-full sm:w-auto">
        <button
          @click="editWebsite"
          class="px-4 py-2 bg-slate-300 dark:bg-slate-600 sm:text-base vs:text-sm rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-400 transition"
        >
          Chỉnh sửa
        </button>
        <button
          @click="openModal"
          class="px-4 py-2 bg-slate-300 dark:bg-slate-600 sm:text-base vs:text-sm rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-400 transition"
        >
          Xóa
        </button>
      </div>
    </div>
    <div class="flex items-center xm:flex-row flex-col gap-4 justify-between mt-4">
      <div class="flex gap-4 items-center xl:w-[60%] sm:w-[40%] min-w-max">
        <div class="flex gap-3 items-center w-full">
          <p class="sm:block hidden">Quyền riêng tư</p>
          <span
            ><GlobeAsiaAustraliaIcon
              class="w-4 h-4"
              v-if="
                phoneNumber.is_private === false &&
                phoneNumber.only_me === false
              " />
            <UserGroupIcon
              class="w-4 h-4"
              v-else-if="
                phoneNumber.is_private === true && phoneNumber.only_me === false
              " />
            <LockClosedIcon
              class="w-4 h-4"
              v-else-if="
                phoneNumber.is_private === true && phoneNumber.only_me === true
              "
          /></span>
        </div>
        <PrivacySelector
          @getOption="getOption"
          :privacies="privacies"
          v-model="privacy"
          :phoneNumber="phoneNumber"
          class="w-full"
          :style="''"
        />
      </div>
      <button
        :disabled="
          number === phoneNumber.phone_number &&
          phoneNumber.is_private === is_private &&
          phoneNumber.only_me === only_me
        "
        @click="submitForm"
        class="px-4 py-2 bg-slate-300 sm:text-base vs:text-sm dark:bg-slate-600 rounded-xl shadow-md font-semibold dark:hover:bg-slate-500 hover:bg-slate-400 transition sm:w-auto w-full"
      >
        Lưu
      </button>
    </div>
    <DeletePhoneNumberModal
      :show="isOpen"
      @closeModal="closeModal"
      @deletePhoneNumber="deletePhoneNumber"
    />
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import DeletePhoneNumberModal from "../../modals/profile/DeletePhoneNumberModal.vue";
import PrivacySelector from "../../dropdown/PrivacySelector.vue";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  props: {
    phoneNumber: Object,
    page: Object,
  },

  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },

  data() {
    return {
      isOpen: false,
      isLike: false,
      privacies: [
        { name: "Công khai" },
        { name: "Bạn bè" },
        { name: "Chỉ mình tôi" },
      ],
      privacy: {},
      is_private: this.phoneNumber.is_private || false,
      only_me: this.phoneNumber.only_me || false,
      number: this.phoneNumber.phone_number,
      edit: false,
    };
  },

  methods: {
    deletePhoneNumber() {
      this.$emit("deletePhoneNumber", this.phoneNumber.id);

      if(!this.page){
        axios
          .delete(`/api/informations/${this.phoneNumber.id}/delete/phone-number/`)
          .then((res) => {
            setTimeout(() => {
              this.closeModal();
            }, 1000);
            this.toastStore.showToast(
              5000,
              "Số điện thoại đã được xóa",
              "bg-emerald-500 text-white"
            );
          })
          .catch((error) => {
            console.log(error);
            this.toastStore.showToast(
              5000,
              "Xóa số điện thoại thất bại",
              "bg-rose-500 text-white"
            );
          });
      } else {
        axios
          .delete(`/api/informations/page/${this.page.id}/delete/phone-number/${this.phoneNumber.id}/`)
          .then((res) => {
            setTimeout(() => {
              this.closeModal();
            }, 1000);
            this.toastStore.showToast(
              5000,
              "Số điện thoại đã được xóa",
              "bg-emerald-500 text-white"
            );
          })
          .catch((error) => {
            console.log(error);
            this.toastStore.showToast(
              5000,
              "Xóa số điện thoại thất bại",
              "bg-rose-500 text-white"
            );
          });
      }
    },
    getOption() {
      if (this.privacy.name === "Công khai") {
        this.is_private = false;
        this.only_me = false;
      }
      if (this.privacy.name === "Bạn bè") {
        this.is_private = true;
        this.only_me = false;
      }
      if (this.privacy.name === "Chỉ mình tôi") {
        this.is_private = true;
        this.only_me = true;
      }
      // console.log(this.privacy.name);
    },
    editWebsite() {
      this.edit = !this.edit;
    },
    submitForm() {
      // console.log("submitForm");

      let formData = new FormData();
      formData.append("phone_number", this.number);
      formData.append("is_private", this.is_private);
      formData.append("only_me", this.only_me);
      axios
        .post(
          `/api/informations/${this.phoneNumber.id}/edit-phone-number/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((res) => {
          // console.log(res.data);
          this.$router.go(0)
        })
        .catch((error) => console.log(error));
    },
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },

  components: {
    DeletePhoneNumberModal,
    PrivacySelector,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
  },
});
</script>

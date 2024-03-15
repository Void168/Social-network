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
        <div class="fixed inset-0 bg-black bg-opacity-50" />
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
                v-if="isExpand"
                class="w-full h-full absolute bg-slate-700/50 z-10 duration-100"
                @click="expandNavigation"
              ></div>
              <div
                @click="expandNavigation"
                class="fixed flex lg:hidden left-0 z-20 inset-y-2/4 w-5 h-20 bg-slate-800 rounded-r-2xl"
                :class="isExpand ? 'translate-x-[320px]' : 'translate-x-0'"
              >
                <ChevronRightIcon
                  class="dark:text-slate-200"
                  v-if="!isExpand"
                />
                <ChevronLeftIcon class="dark:text-slate-200" v-else />
              </div>
              <div
                @click="expandNavigation"
                class="lg:col-span-1 h-screen dark:bg-slate-800 dark:border-slate-700 bg-white dark:text-neutral-200 border-r-[1px] border-slate-200 lg:static fixed z-50 overflow-y-scroll"
                :class="
                  isExpand
                    ? 'block w-[320px]'
                    : 'hidden lg:flex flex-col justify-between'
                "
              >
                <div class="flex flex-col space-y-2">
                  <XMarkIcon
                    @click="
                      $emit('closeCreatePageModal');
                      removeAll();
                    "
                    class="h-8 w-8 p-1 mt-2 ml-2 mb-4 bg-slate-200 dark:bg-slate-600 rounded-full hover:bg-slate-300 dark:hover:bg-slate-500 transition duration-100 cursor-pointer"
                  />
                  <div class="flex gap-1 px-4" v-if="step === 1">
                    <span>Trang</span>
                    <span>&middot;</span>
                    <span>Tạo trang</span>
                  </div>
                  <div class="px-4">Bước {{ step }}/3</div>
                  <div class="w-full px-4">
                    <div
                      class="dark:bg-white bg-slate-200 rounded-lg h-2 relative"
                    >
                      <span
                        :style="{ width: `${(step * 100) / 3}%` }"
                        class="bg-emerald-400 absolute z-20 h-2 rounded-lg"
                      />
                    </div>
                  </div>
                  <h1 class="2xl:text-2xl text-xl font-bold px-4" v-if="step === 1">
                    Tạo trang
                  </h1>
                  <h1 class="text-2xl font-bold px-4" v-if="step === 2">
                    Hoàn tất quá trình thiết lập Trang
                  </h1>
                  <h1 class="text-2xl font-bold px-4" v-if="step === 3">
                    Tùy chỉnh Trang
                  </h1>
                  <div class="px-4 flex flex-col space-y-4" v-if="step === 1">
                    <h3 class="px-4 2xl:text-lg">
                      Trang sẽ hiển thị thông tin về bạn để mọi người tìm hiểu
                      thêm. Hãy chắc chắn là Trang của bạn có mọi thông tin cần
                      thiết nhé.
                    </h3>
                    <MUILikedInput
                      :placeholder="'Tên trang (bắt buộc)'"
                      v-model="name"
                      :type="'text'"
                    />
                    <h4 class="text-xs">
                      Dùng tên doanh nghiệp/thương hiệu/tổ chức của bạn hoặc tên
                      góp phần giải thích về Trang của bạn.
                      <span
                        class="text-emerald-500 hover:underline transition duration-75 cursor-pointer"
                        >Tìm hiểu thêm</span
                      >
                    </h4>
                    <h3>Hạng mục (bắt buộc)</h3>
                    <ChooseTypePage
                      :types="types"
                      @getOption="getOption"
                      ref="chooseType"
                      v-model="type"
                    />
                    <h4 class="text-xs">
                      Hãy nhập hạng mục mô tả chính xác nhất về bạn nhé.
                    </h4>
                    <div class="relative">
                      <textarea
                        v-model="biography"
                        class="p-4 w-full bg-gray-100 dark:bg-slate-800 rounded-lg resize-none border dark:border-slate-600"
                        cols="30"
                        rows="4"
                        :placeholder="
                          isBioFocus ? '' : 'Tiểu sử (Không bắt buộc)'
                        "
                        @focus="bioFocus"
                        @focusout="bioFocusOut"
                      ></textarea>
                      <span
                        class="absolute left-4 text-xs top-1 text-emerald-400"
                        v-if="isBioFocus"
                        >Tiểu sử (Không bắt buộc)</span
                      >
                    </div>
                    <h4 class="text-xs">
                      Hãy chia sẻ đôi nét về những gì bạn làm nhé.
                    </h4>
                  </div>
                  <div v-if="step === 2" class="flex flex-col">
                    <h3 class="px-4 text-lg">
                      Thành công rồi! Bạn đã tạo được <strong>{{ name }}</strong
                      >. Hãy bổ sung chi tiết ngay để mọi người dễ kết nối với
                      bạn nhé.
                    </h3>
                    <div
                      class="overflow-y-scroll scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-700"
                    >
                      <div class="my-2 h-[550px] space-y-4 px-4">
                        <h2 class="mb-2 text-lg">Thông tin liên hệ</h2>
                        <MUILikedInput
                          :placeholder="'Email'"
                          v-model="email"
                          :type="'email'"
                        />
                        <MUILikedInput
                          :placeholder="'Số điện thoại'"
                          v-model="phone"
                          :type="'text'"
                        />
                        <h2 class="mb-2 text-xl">Vị trí</h2>
                        <MUILikedInput
                          :placeholder="'Địa chỉ'"
                          v-model="address"
                          :type="'text'"
                        />
                        <MUILikedInput
                          :placeholder="'Thành phố/Thị xã'"
                          v-model="location"
                          :type="'text'"
                        />
                        <MUILikedInput :placeholder="'Mã zip'" :type="'text'" />
                        <div>
                          <h2 class="font-semibold text-lg">Giờ mở cửa</h2>
                          <h3 class="text-sm">
                            Thông báo về giờ mở cửa tại vị trí của bạn.
                          </h3>
                        </div>
                        <ListRadioButton :plans="plans" />
                      </div>
                    </div>
                  </div>
                  <div v-if="step === 3" class="flex flex-col px-4">
                    <h3 class="px-4 text-lg">
                      Ảnh đại diện của bạn là một trong những thứ đầu tiên mọi
                      người nhìn thấy. Hãy thử dùng logo hoặc hình ảnh khiến họ
                      dễ liên tưởng đến bạn.
                    </h3>
                    <div class="flex flex-col space-y-4 mt-4">
                      <div class="relative">
                        <TrashIcon
                          v-if="avatarUrl"
                          class="absolute z-10 top-2 right-2 w-8 p-1 rounded-full bg-slate-600 hover:bg-slate-500 transition duration-75 cursor-pointer"
                          @click="removeAvatar"
                        />
                        <label for="page-avatar">
                          <div
                            class="w-full h-36 dark:bg-slate-800 flex flex-col justify-center items-center rounded-lg border dark:border-slate-600 cursor-pointer"
                          >
                            <img
                            loading="lazy"
                              v-if="avatarUrl"
                              :src="avatarUrl"
                              class="w-full p-1 absolute rounded-lg h-full"
                            />
                            <input
                              type="file"
                              ref="pageAvatar"
                              id="page-avatar"
                              name="page-avatar"
                              hidden
                              @change="onAvatarChange"
                            />
                            <PhotoIcon
                              class="w-10 p-2 rounded-full bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 transition duration-75"
                            />
                            <h3>Thêm ảnh đại diện</h3>
                          </div>
                        </label>
                      </div>
                      <div class="relative">
                        <TrashIcon
                          v-if="coverImageUrl"
                          class="absolute top-2 right-2 z-10 w-8 p-1 rounded-full bg-slate-600 hover:bg-slate-500 transition duration-75 cursor-pointer"
                          @click="removeCoverImage"
                        />
                        <label for="cover-image">
                          <div
                            class="w-full h-36 dark:bg-slate-800 flex flex-col justify-center items-center rounded-lg border dark:border-slate-600 cursor-pointer"
                          >
                            <img
                            loading="lazy"
                              v-if="coverImageUrl"
                              :src="coverImageUrl"
                              class="w-full p-1 absolute rounded-lg h-full"
                            />
                            <input
                              type="file"
                              ref="coverImage"
                              id="cover-image"
                              name="cover-image"
                              hidden
                              @change="onCoverImageChange"
                            />
                            <PhotoIcon
                              class="w-10 p-2 rounded-full bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 transition duration-75"
                            />
                            <h3>Thêm ảnh bìa</h3>
                          </div>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col w-full gap-2 px-4">
                  <div class="flex gap-2">
                    <button
                      @click="prevStep"
                      :class="
                        isDisabled
                          ? 'dark:bg-slate-600 py-2 rounded-lg font-semibold dark:text-slate-400'
                          : 'btn'
                      "
                      class="w-full"
                      v-if="step > 1"
                    >
                      Quay lại bước {{ step - 1 }}
                    </button>
                    <button
                      @click="nextStep"
                      v-if="step < 3"
                      :class="
                        isDisabled
                          ? 'dark:bg-slate-600 py-2 rounded-lg font-semibold text-slate-400 bg-slate-200'
                          : 'btn'
                      "
                      :disabled="isDisabled"
                      class="w-full"
                    >
                      Bước tiếp theo
                    </button>
                    <button
                      @click="createPage"
                      v-else
                      :class="
                        isDisabled
                          ? 'dark:bg-slate-600 py-2 rounded-lg font-semibold dark:text-slate-400'
                          : 'btn'
                      "
                      :disabled="isDisabled"
                      class="w-full"
                    >
                      Tạo trang
                    </button>
                  </div>
                  <h4 class="text-xs text-center">
                    Bằng việc tạo Trang, bạn đồng ý với
                    <span
                      class="text-emerald-400 cursor-pointer hover:underline transition duration-75"
                      >Chính sách về Trang, Nhóm và Sự kiện</span
                    >
                  </h4>
                </div>
              </div>
              <div
                class="lg:col-span-4 col-span-5 justify-center flex flex-col items-center py-2"
              >
                <DisplayPage
                  :isDeviceActive="isDeviceActive"
                  :coverImageUrl="coverImageUrl"
                  :avatarUrl="avatarUrl"
                  :name="name"
                  :biography="biography"
                  :type="type?.name"
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
import pageTypes from "../../../../data/pageTypes";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import {
  XMarkIcon,
  PhotoIcon,
  TrashIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
} from "@heroicons/vue/24/solid";
import ChooseTypePage from "../../../dropdown/ChooseTypePage.vue";
import MUILikedInput from "../../../input/MUILikedInput.vue";
import ListRadioButton from "../../../input/ListRadioButton.vue";
import DisplayPage from "./DisplayPage.vue";
import { useToastStore } from "../../../../stores/toast";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    DisplayPage,
    ChooseTypePage,
    MUILikedInput,
    ListRadioButton,
    XMarkIcon,
    PhotoIcon,
    TrashIcon,
    ChevronRightIcon,
    ChevronLeftIcon,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    isCreatePageOpen: Boolean,
  },

  data() {
    return {
      isExpand: false,
      isLoading: false,
      isBioFocus: false,
      isDeviceActive: false,
      name: "",
      email: "",
      type: {},
      biography: "",
      phone: "",
      address: "",
      location: "",
      avatarUrl: null,
      coverImageUrl: null,
      business_hours_status: "",
      start_time: "",
      close_time: "",
      types: pageTypes,
      step: 1,
      plans: [
        {
          name: "Không có giờ làm việc",
          description: "Không hiển thị giờ làm việc.",
        },
        {
          name: "Luôn mở cửa",
          description: "Bạn đang mở cửa 24 giờ mỗi ngày.",
        },
        {
          name: "Mở cửa vào khung giờ nhất định",
          description: "Nhập khung giờ cụ thể.",
        },
      ],
    };
  },

  computed: {
    isDisabled() {
      return this.name === "" || !this.type;
    },
  },

  mounted() {},

  methods: {
    expandNavigation() {
      this.isExpand = !this.isExpand;
    },
    bioFocus() {
      this.isBioFocus = true;
    },
    bioFocusOut() {
      this.isBioFocus = false;
    },
    computerActive() {
      this.isDeviceActive = false;
    },
    deviceActive() {
      this.isDeviceActive = true;
    },
    onAvatarChange(e) {
      const file = e.target.files[0];
      this.avatarUrl = URL.createObjectURL(file);
    },
    onCoverImageChange(e) {
      const file = e.target.files[0];
      this.coverImageUrl = URL.createObjectURL(file);
    },
    removeAvatar() {
      this.avatarUrl = null;
    },
    removeCoverImage() {
      this.coverImageUrl = null;
    },
    removeAll() {
      this.isDeviceActive = false;
      this.name = "";
      this.email = "";
      this.type = {};
      this.biography = "";
      this.phone = "";
      this.address = "";
      this.location = "";
      this.step = 1;
      this.avatarUrl = null;
      this.coverImageUrl = null;
    },
    nextStep() {
      this.isLoading = true;
      setTimeout(() => {
        this.step += 1;
        this.isLoading = false;
      }, 1500);
    },
    prevStep() {
      this.step -= 1;
    },
    getOption(data) {
      this.type = data;
    },
    createPage() {
      if (this.name && this.type) {
        let formData = new FormData();

        formData.append("name", this.name);
        formData.append("page_type", this.type?.name);
        formData.append("email", this.email);
        formData.append("phone_number", this.phone);
        formData.append("location", this.location);
        formData.append("biography", this.biography);
        formData.append("business_hours_status", this.biography);
        formData.append("start_time", this.start_time);
        formData.append("close_time", this.close_time);
        formData.append("avatar", this.$refs.pageAvatar.files[0]);
        formData.append("cover_image", this.$refs.coverImage.files[0]);

        axios
          .post("/api/page/create/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.success) {
              this.toastStore.showToast(
                3000,
                "Tạo trang thành công.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 3500);
            } else {
              this.toastStore.showToast(
                3500,
                "Tạo trang thất bại.",
                "bg-rose-500 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
            this.toastStore.showToast(
              5000,
              "Tạo trang thất bại.",
              "bg-rose-500 text-white"
            );
          });
      } else {
        console.log("Failed");
      }
    },
  },
});
</script>

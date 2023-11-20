<template>
  <TransitionRoot @click="$emit('closeAvatarModal')" appear as="template">
    <Dialog as="div" class="relative z-10">
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

      <div class="fixed inset-0 top-36 overflow-y-auto">
        <div class="flex min-h-[90%] justify-center p-4">
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
              class="w-[50%] relative overflow-y-auto transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 dark:text-neutral-200 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 dark:text-neutral-200 text-center"
              >
                Chọn ảnh đại diện
              </DialogTitle>
              <div class="flex justify-end items-center gap-5">
                <span
                  ><GlobeAsiaAustraliaIcon
                    class="w-6 h-6"
                    v-if="privacy.name === 'Công khai'" />
                  <UserGroupIcon
                    class="w-6 h-6"
                    v-else-if="privacy.name === 'Bạn bè'" />
                  <LockClosedIcon
                    class="w-6 h-6"
                    v-else-if="privacy.name === 'Chỉ mình tôi'"
                /></span>
                <PrivacySelector
                  @getOption="getOption"
                  :privacies="privacies"
                  v-model="privacy"
                  class="text-left"
                />
              </div>
              <div
                class="relative flex flex-col justify-center items-center my-4"
              >
                <div
                  class="h-96 w-96 border-4 border-dashed px-2 py-1 rounded-full"
                >
                  <div v-if="url" class="relative mt-1">
                    <img
                      :src="url"
                      class="w-[360px] h-[360px] rounded-full p-1"
                    />
                    <span
                      class="absolute top-3 right-3 cursor-pointer"
                      @click="removeAvatar"
                      ><svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        class="w-8 h-8"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                    </span>
                  </div>
                </div>
                <form
                  v-on:submit.prevent="submitForm"
                  method="post"
                  class="right-0 bottom-2"
                >
                  <div class="p-4 flex justify-end">
                    <label for="avatar-image">
                      <div
                        class="py-3 px-6 text-white bg-gray-400 font-semibold rounded-lg transition-colors hover:bg-gray-600 dark:hover:bg-gray-500 cursor-pointer"
                      >
                        <span>Chọn ảnh</span>
                      </div>
                      <input
                        type="file"
                        ref="avatar"
                        id="avatar-image"
                        name="avatar-image"
                        hidden
                        @change="onAvatarChange"
                      />
                    </label>
                  </div>
                </form>
              </div>

              <div class="my-4 flex justify-center gap-3">
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-6 py-3 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeAvatarModal')"
                >
                  Hủy
                </button>
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-6 py-3 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="submitForm"
                  v-on:click="$emit('closeAvatarModal')"
                >
                  Đồng ý
                </button>
              </div>
              <div
                class="flex gap-2 items-center mb-4 cursor-pointer"
                @click="checkRadioButton"
              >
                <span
                  class="relative h-5 w-5 border-neutral-200 border-2 rounded-full"
                >
                  <span
                    v-if="share"
                    class="h-[10px] w-[10px] bg-neutral-200 rounded-full absolute top-[3.2px] left-[3.9px]"
                  ></span>
                </span>
                <span class="text-lg">Chia sẻ lên trang cá nhân</span>
              </div>
              <hr />
              <div class="my-4">
                <p class="text-2xl">Ảnh đã tải lên</p>
                <div class="grid grid-cols-6 gap-3 mt-4">
                  <div
                    v-for="image in images"
                    :key="image.id"
                    class="col-span-1"
                  >
                    <img
                      :src="image.attachments[0].get_image"
                      class="h-36 cursor-pointer hover:ring-2 hover:ring-slate-500 dark:hover:ring-neutral-200 transition"
                      @click="
                        chooseExistedImage(image.attachments[0].get_image)
                      "
                    />
                  </div>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";

import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/20/solid";

import PrivacySelector from "../dropdown/PrivacySelector.vue";

export default (await import("vue")).defineComponent({
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();

    return {
      toastStore,
      userStore,
    };
  },
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    PrivacySelector,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
  },
  props: {
    isOpen: Boolean,
  },

  data() {
    return {
      url: null,
      images: [],
      privacies: [
        { name: "Công khai" },
        { name: "Bạn bè" },
        { name: "Chỉ mình tôi" },
      ],
      privacy: {},
      share: false,
    };
  },

  mounted() {
    this.getImages();
  },

  methods: {
    onAvatarChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
      console.log(this.url);
    },
    removeAvatar() {
      this.url = null;
    },

    checkRadioButton() {
      this.share = !this.share;
    },

    getImages() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/attachments`)
        .then((res) => {
          this.images = res.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    chooseExistedImage(url) {
      this.url = url;
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
      //   console.log(this.privacy.name);
    },

    submitForm() {
      this.errors = [];

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("avatar", this.$refs.avatar.files[0]);

        axios
          .post("/api/edit-avatar/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message === "avatar updated") {
                console.log(res.data)
              this.toastStore.showToast(
                5000,
                "Thay đổi ảnh đại diện thành công.",
                "bg-emerald-500 text-white"
              );
              localStorage.setItem("user.avatar", this.url);
              setTimeout(() => {
                this.$router.go(0);
              }, 1500);
            } else {
              this.toastStore.showToast(
                5000,
                "Thay đổi ảnh đại diện thất bại.",
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

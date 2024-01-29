<template>
  <TransitionRoot @click="$emit('closeAvatarModal')" appear as="template">
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

      <div class="fixed inset-0 top-36 overflow-y-auto ">
        <div class="flex max-h-[90%] justify-center p-4">
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
              class="lg:w-[50%] relative overflow-y-auto transform overflow-hidden scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 rounded-2xl bg-white dark:bg-slate-700 dark:text-neutral-200 p-6 text-left align-middle shadow-xl transition-all"
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
                  :style="''"
                />
              </div>
              <div
                class="relative flex flex-col justify-center items-center my-4"
              >
                <div
                  class="xm:h-96 xm:w-96 xs:h-72 xs:w-72 border-4 border-dashed px-2 py-1 rounded-full"
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
                  class="right-0 bottom-2 w-full flex flex-col items-center"
                >
                  <div class="p-4 flex justify-center">
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
                  <textarea
                    v-model="body"
                    class="p-4 lg:w-[50%] bg-gray-100 rounded-lg resize-none"
                    cols="30"
                    rows="3"
                    placeholder="Mô tả về ảnh đại diện..."
                  ></textarea>
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
import { usePageStore } from "../../../stores/page";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/20/solid";

import PrivacySelector from "../../dropdown/PrivacySelector.vue";

export default (await import("vue")).defineComponent({
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();
    const pageStore = usePageStore()
    
    return {
      toastStore,
      userStore,
      pageStore,
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
      share: true,
      is_private: false,
      only_me: false,
      body: "",
    };
  },

  mounted() {
    this.getImages();
  },

  methods: {
    onAvatarChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
      // console.log(this.url);
    },
    removeAvatar() {
      this.url = null;
    },

    checkRadioButton() {
      this.share = !this.share;
    },

    getImages() {
      if(this.pageStore.pageActive.is_page === false){
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/attachments`)
          .then((res) => {
            this.images = res.data;
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        console.log('hello')
      }
    },

    chooseExistedImage(url) {
      this.chooseImage = true;
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
        if(this.pageStore.pageActive.is_page === false){
          axios
            .post("/api/edit-avatar/", formData, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            })
            .then((res) => {
              
              if (res.data.message === "avatar updated") {
                this.toastStore.showToast(
                  5000,
                  "Thay đổi ảnh đại diện thành công.",
                  "bg-emerald-500 text-white"
                );
                localStorage.setItem("user.avatar", this.url);
              } else {
                this.toastStore.showToast(
                  5000,
                  "Thay đổi ảnh đại diện thất bại.",
                  "bg-rose-400 text-white"
                );
              }
  
              if (this.share === true) {
                let form = new FormData();
  
                form.append("image", this.$refs.avatar.files[0]);
                form.append("body", this.body);
                form.append("is_private", this.is_private);
                form.append("only_me", this.only_me);
                form.append("is_avatar_post", this.share)
  
                axios
                  .post("/api/posts/create/", form, {
                    headers: {
                      "Content-Type": "multipart/form-data",
                    },
                  })
                  .then((res) => {
                    // console.log("data", res.data);
  
                    this.body = "";
                    this.$refs.file.value = null;
                    this.is_private = false;
                    this.only_me = false;
                    this.share = false;
                    this.url = null;
  
                    if (this.user) {
                      this.user.posts_count += 1;
                    }
                  })
                  .catch((error) => {
                    console.log("error", error);
                  });
              }
  
              setTimeout(() => {
                  this.$router.go(0);
                }, 1500);
  
            })
            .catch((error) => {
              console.log("error", error);
            });
        } else {
          console.log('hello')
        }
      }
    },
  },
});
</script>

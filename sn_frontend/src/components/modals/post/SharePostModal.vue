<template>
  <TransitionRoot @click="$emit('closeShareModal')" appear as="template">
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

      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
        >
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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 text-left align-middle shadow-xl transition-all relative"
            >
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 dark:text-slate-200 text-center py-4"
              >
                Viết bài
              </DialogTitle>
              <XMarkIcon
                @click="$emit('closeShareModal')"
                class="w-10 h-10 p-1 cursor-pointer dark:hover:bg-slate-800/70 duration-75 text-gray-900 dark:text-slate-200 bg-slate-800 rounded-full right-4 absolute top-2"
              />

              <hr class="border dark:border-slate-600" />
              <div class="p-6 text-gray-900 dark:text-slate-200 space-y-4">
                <textarea
                  v-model="body"
                  class="p-4 w-full bg-gray-100 rounded-lg resize-none"
                  cols="30"
                  rows="2"
                  placeholder="Bạn đang nghĩ gì?"
                ></textarea>
                <div
                  id="preview-share"
                  v-if="urlPost"
                  class="flex relative justify-center items-center w-32 p-2 border-[1px] border-slate-400 rounded-lg my-2"
                >
                  <XMarkIcon
                    class="absolute top-0 right-0 cursor-pointer w-6 h-6"
                    @click="removeImage"
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
                  </XMarkIcon>
                  <img
                    loading="lazy"
                    :src="urlPost"
                    class="w-full rounded-lg"
                  />
                </div>
                <div class="flex justify-between items-center">
                  <label for="doc-share">
                    <div
                      class="py-3 px-6 text-black bg-gray-400 dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 dark:hover:bg-white dark:hover:text-slate-800 font-semibold rounded-lg transition-colors hover:bg-gray-600 hover:text-white cursor-pointer"
                    >
                      <span class="xm:text-base text-xs">Chọn ảnh</span>
                    </div>
                    <input
                      type="file"
                      ref="file"
                      id="doc-share"
                      name="doc-share"
                      hidden
                      @change="onFileChange"
                    />
                  </label>
                  <PrivacySelector
                    @getOption="getOption"
                    :privacies="privacies"
                    v-model="privacy"
                    class="max-w-max"
                    :style="''"
                  />
                </div>
                <div
                  class="border dark:border-slate-600 rounded-lg p-4 dark:text-neutral-200 space-y-2"
                >
                  <div class="flex gap-2 items-center">
                    <img
                      :src="post.created_by.get_avatar"
                      class="w-8 h-8 rounded-full"
                    />
                    <div>
                      <h5 class="font-semibold text-sm">
                        {{ post.created_by.name }}
                      </h5>
                      <div
                        class="dark:text-neutral-300 text-xs text-neutral-400 flex items-center gap-1"
                      >
                        <p>{{ post.created_at_formatted }} &middot;</p>
                        <GlobeAsiaAustraliaIcon
                          v-if="!post.only_me && !post.is_private"
                          class="w-4 h-4"
                        />
                        <UserGroupIcon
                          v-else-if="!post.only_me && post.is_private"
                          class="w-4 h-4"
                        />
                        <LockClosedIcon
                          v-else-if="post.only_me && post.is_private"
                          class="w-4 h-4"
                        />
                      </div>
                    </div>
                  </div>
                  <h5>
                    {{ post.body }}
                  </h5>
                  <div v-if="post.attachments.length">
                    <img :src="post.attachments[0].get_image" />
                  </div>
                </div>
                <div class="mt-4" @click="$emit('closeShareModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 w-full"
                    @click="sharePost"
                  >
                    Chia sẻ
                  </button>
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
import axios from "axios";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon } from "@heroicons/vue/24/solid";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import PrivacySelector from "../../dropdown/PrivacySelector.vue";


export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    PrivacySelector,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore()

    return {
      userStore,
      toastStore
    };
  },
  props: {
    isShareOpen: Boolean,
    post: Object,
  },
  data() {
    return {
      body: "",
      is_private: false,
      only_me: false,
      privacies: [
        { name: "Công khai" },
        { name: "Bạn bè" },
        { name: "Chỉ mình tôi" },
      ],
      privacy: {
        name: "",
      },
      selection: "",
      urlPost: null,
    };
  },
  methods: {
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
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.urlPost = URL.createObjectURL(file);
    },

    removeImage() {
      this.urlPost = null;
    },
    sharePost() {
      let formData = new FormData();

      formData.append("body", this.body);
      formData.append("is_private", this.is_private);
      formData.append("only_me", this.only_me);

      axios
        .post(`/api/posts/create/${this.post.id}/share/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log(res.data);
          this.toastStore.showToast(
            3500,
            "Đã chia sẻ bài viết",
            "bg-emerald-500 text-white"
          );
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Chia sẻ bài viết thất bại",
            "bg-emerald-500 text-white"
          );
        });
    },
  },
});
</script>

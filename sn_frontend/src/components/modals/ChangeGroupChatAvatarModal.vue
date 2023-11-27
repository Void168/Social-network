<template>
  <TransitionRoot @click="$emit('closeModal')" appear as="template">
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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 text-center"
              >
                Thay đổi ảnh đoạn chat nhóm
              </DialogTitle>
              <div class="mt-2 flex flex-col items-center">
                <div
                  class="h-32 w-32 border-4 border-dashed rounded-full"
                >
                  <div v-if="url" class="relative">
                    <img
                      :src="url"
                      class="w-[120px] h-[120px] rounded-full p-1 ml-[1.5px]"
                    />
                    <span
                      class="absolute top-0 right-0 cursor-pointer"
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
                  method="post"
                  class="right-0 bottom-2 w-full flex flex-col items-center"
                >
                  <div class="p-4 flex justify-center">
                    <label for="avatar-group">
                      <div
                        class="py-3 px-6 text-white bg-gray-400 font-semibold rounded-lg transition-colors hover:bg-gray-600 dark:hover:bg-gray-500 cursor-pointer"
                      >
                        <span>Chọn ảnh</span>
                      </div>
                      <input
                        type="file"
                        ref="avatarGroup"
                        id="avatar-group"
                        name="avatar-group"
                        hidden
                        @change="onAvatarGroupChange"
                      />
                    </label>
                  </div>
                </form>
              </div>

              <div class="mt-4 flex justify-end gap-3">
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeModal')"
                >
                  Hủy
                </button>
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="submitAvatarForm"
                >
                  Đồng ý
                </button>
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

import { useToastStore } from "@/stores/toast";

import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    isChangeAvatarOpen: Boolean,
    activeConversation: Object,
  },

  data() {
    return {
      url: null,
    };
  },

  methods: {
    onAvatarGroupChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },
    removeAvatar() {
      this.url = null;
    },

    submitAvatarForm() {
      this.errors = [];

      if (this.errors.length === 0) {
        let form = new FormData();
        form.append("avatar", this.$refs.avatarGroup.files[0]);

        axios
          .post(`/api/chat/group/${this.activeConversation.id}/change-group-avatar/`, form, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message === "avatar updated") {
              this.toastStore.showToast(
                3000,
                "Thay đổi ảnh nhóm thành công.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 3500)
            } else {
              this.toastStore.showToast(
                3000,
                "Thay đổi ảnh nhóm thất bại.",
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
  }
});
</script>

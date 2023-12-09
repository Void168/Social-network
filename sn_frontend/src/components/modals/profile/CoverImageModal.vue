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
                Chọn ảnh bìa
              </DialogTitle>
              <div class="flex flex-col justify-center items-center my-4">
                <div class="h-64 w-96 border-4 border-dashed p-2">
                  <div v-if="url" class="relative mt-1">
                    <img :src="url" class="w-full h-56 rounded-lg" />
                    <span
                      class="absolute top-3 right-3 cursor-pointer"
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
                    </span>
                  </div>
                </div>
                <form
                  v-on:submit.prevent="submitForm"
                  method="post"
                  class="right-0 bottom-2"
                >
                  <div class="p-4 flex justify-end">
                    <label for="cover-image">
                      <div
                        class="py-3 px-6 text-white bg-gray-400 font-semibold rounded-lg transition-colors hover:bg-gray-600 cursor-pointer"
                      >
                        <span>Chọn ảnh</span>
                      </div>
                      <input
                        type="file"
                        ref="image"
                        id="cover-image"
                        name="cover-image"
                        hidden
                        @change="onImageChange"
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
                  @click="submitForm"
                  v-on:click="$emit('closeModal')"
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

export default (await import("vue")).defineComponent({
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore()

    return {
      toastStore,
      userStore
    };
  },
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
  },
  props: {
    isOpen: Boolean,
  },

  data() {
    return {
      url: null,
    };
  },

  methods: {
    onImageChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },
    removeImage() {
      this.url = null;
    },
    submitForm() {
      this.errors = [];

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("cover_image", this.$refs.image.files[0]);

        axios
          .post("/api/edit-cover-image/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message === "cover image updated") {
              this.toastStore.showToast(
                5000,
                "Thay đổi ảnh bìa thành công.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 1500)
            } else {
              this.toastStore.showToast(
                5000,
                "Thay đổi ảnh bìa thất bại.",
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

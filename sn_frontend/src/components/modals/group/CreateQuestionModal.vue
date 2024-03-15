<template>
  <TransitionRoot @click="$emit('closeModal')" appear as="template">
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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-xl font-bold leading-6 text-gray-900 dark:text-slate-200 flex justify-between items-center"
              >
                Chỉnh sửa câu hỏi
                <XMarkIcon
                  @click="$emit('closeModal')"
                  class="w-8 h-8 dark:bg-slate-800 dark:hover:bg-slate-800/70 p-1 rounded-full cursor-pointer"
                />
              </DialogTitle>
              <hr class="border border-slate-600 my-2" />
              <div class="mt-2">
                <MUILikedInput
                  :placeholder="'Bạn hỏi gì đi'"
                  v-model="question"
                />
              </div>

              <div class="mt-4 flex justify-end gap-3">
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeModal')"
                >
                  Hủy
                </button>
                <div @click="$emit('closeModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="createQuestion"
                  >
                    Đồng ý
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
import MUILikedInput from "../../input/MUILikedInput.vue";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    MUILikedInput,
  },
  props: {
    isOpen: Boolean,
  },

  data() {
    return {
      question: "",
    };
  },

  methods: {
    createQuestion() {
      let formData = new FormData();

      formData.append("body", this.question);
      axios
        .post(
          `/api/group/${this.$route.params.id}/create-question/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

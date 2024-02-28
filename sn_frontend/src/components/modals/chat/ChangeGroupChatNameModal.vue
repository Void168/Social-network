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
                Thay đổi tên đoạn chat nhóm
              </DialogTitle>
              <div class="mt-4">
                <form>
                  <div class="flex gap-2 items-center">
                    <PencilSquareIcon class="w-6 h-6"/>
                    <input
                      v-model="form.name"
                      type="text"
                      placeholder="Tên nhóm"
                      class="w-full py-2 px-6 border border-gray-200 rounded-lg"
                    />
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
                <div @click="$emit('closeModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="submitForm"
                    :disabled="form.name === activeConversation.group_name"
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
import { useToastStore } from "../../../stores/toast";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

import { PencilSquareIcon } from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    PencilSquareIcon
  },
  setup() {
    const toastStore = useToastStore()

    return {
      toastStore
    }
  },
  props: {
    activeConversation: Object,
    isChangeNameOpen: Boolean,
  },
  data() {
    return {
      form: {
        name: this.activeConversation.group_name
      }
    }
  },

  methods: {
    submitForm() {
      let formData = new FormData();
      formData.append("group_name", this.form.name);

      axios
        .post(`/api/chat/group/${this.activeConversation.id}/change-group-name/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.data.message !== "Failed") {
              this.toastStore.showToast(
                3000,
                "Thay đổi tên nhóm chat thành công.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 3500)
            } else {
              this.toastStore.showToast(
                3000,
                "Thay đổi tên nhóm chat thất bại.",
                "bg-rose-400 text-white"
              );
            }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  }
});
</script>

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
              class="w-full flex flex-col justify-between relative max-w-md h-80 transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <div>
                <DialogTitle
                  as="h3"
                  class="text-2xl font-medium leading-6 text-gray-900 text-center"
                >
                  Tạo một đoạn chat nhóm
                </DialogTitle>
                <div class="my-2 flex justify-center font-semibold">
                  <p class="text-lg text-gray-500">
                    Người tạo nhóm {{ userStore.user.name }}
                  </p>
                </div>
                <div class="output hidden" @change="getValue">{{ value }}</div>
                <div>
                  <Multiselect
                    v-model="value"
                    mode="tags"
                    :close-on-select="false"
                    :searchable="true"
                    :create-option="true"
                    :options="options"
                    :limit="3"
                    :infinite="true"
                    :on-create="getValue(value)"
                  >
                  </Multiselect>
                </div>
              </div>

              <div class="mt-4 flex justify-end gap-3">
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeModal')"
                >
                  Hủy
                </button>
                <div  @click="$emit('closeModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="createGroupChat"
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
import { useUserStore } from "../../../stores/user";
import Multiselect from "@vueform/multiselect";

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
    Multiselect,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    isCreateGroupOpen: Boolean,
    options: Array
  },
  data() {
    return {
      value: [],
    };
  },

  methods: {
    getValue(value) {
      this.value = value;
      // console.log(this.value)
    },
    createGroupChat() {
      if (this.value.length > 1) {
        axios
          .post("/api/chat/create-group-chat/", {
            users: this.value
          })
          .then((res) => {
            // console.log(res.data)
            this.value = [];
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        console.log('Nhóm phải từ 3 người')
      }
    },
  },
});
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

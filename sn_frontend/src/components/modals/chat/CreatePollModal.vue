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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-slate-600 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 dark:text-neutral-200 text-center"
              >
                Tạo cuộc thăm dò ý kiến
              </DialogTitle>
              <div class="mt-2">
                <div class="my-6">
                  <label for="" class="text-lg dark:text-neutral-200"
                    >Tên cuộc thăm dò</label
                  >
                  <input
                    v-model="pollName"
                    type="text"
                    placeholder="Đặt tên cho cuộc thăm dò"
                    class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
                  />
                  <VueDatePicker
                    v-model="date"
                    :teleport="true"
                    placeholder="Nhập ngày ..."
                    :format="format"
                    text-input
                    class="my-6"
                  />
                  <div
                    class="flex flex-col items-center justify-center my-4 dark:text-neutral-200"
                  >
                    <PlusCircleIcon
                      @click="createOption"
                      class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                    />
                    <span>Thêm lựa chọn</span>
                  </div>
                  <div class="dark:text-neutral-200 max-h-96 overflow-y-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800" v-if="options.length">
                    <span class="text-lg">Danh sách lựa chọn</span>
                    <div v-for="option in options" :key="option" class="my-4">
                      <div
                        class="flex items-center justify-between px-4 py-2 bg-neutral-200 dark:bg-slate-700 rounded-lg"
                      >
                        <p>{{ option.name }}</p>
                        <TrashIcon
                          @click="deleteOption(option)"
                          class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                        />
                      </div>
                    </div>
                  </div>
                  <div v-if="isAddOptionOpen">
                    <label for="" class="text-lg dark:text-neutral-200"
                      >Tên lựa chọn</label
                    >
                    <div class="flex items-center justify-between gap-3">
                      <input
                        v-model="optionName"
                        type="text"
                        placeholder="Tên lựa chọn"
                        class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-lg"
                      />
                      <div class="flex gap-1">
                        <XCircleIcon
                          @click="cancelOption"
                          class="w-8 h-8 p-1 shadow-md text-rose-400 bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                        /><CheckCircleIcon
                          @click="addOption"
                          class="w-8 h-8 p-1 shadow-md text-emerald-400 bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                        />
                      </div>
                    </div>
                  </div>
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
                <div @click="$emit('closeModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="submitForm"
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
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

import {
  PlusCircleIcon,
  CheckCircleIcon,
  XCircleIcon,
  TrashIcon,
} from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    VueDatePicker,
    PlusCircleIcon,
    CheckCircleIcon,
    XCircleIcon,
    TrashIcon,
  },
  props: {
    isCreatePollOpen: Boolean,
    activeConversation: Object,
  },
  data() {
    return {
      optionName: "",
      pollName: "",
      options: [],
      isAddOptionOpen: false,
      date: null,
    };
  },

  methods: {
    createOption() {
      this.isAddOptionOpen = true;
    },
    cancelOption() {
      this.isAddOptionOpen = false;
    },
    addOption() {
      if (this.optionName) {
        const obj = {};
        obj["name"] = this.optionName;
        this.options.push(obj);
        this.isAddOptionOpen = false;
        this.optionName = "";
      } else {
        console.log("Hãy điền lựa chọn");
      }
    },
    deleteOption(deletedOption) {
      this.options.shift(deletedOption);
    },
    format(date) {
      const day = date?.getDate();
      const month = date?.getMonth() + 1;
      const year = date?.getFullYear();

      if (day && month && year) {
        return `${day}/${month}/${year}`;
      } else {
        return "";
      }
    },
    submitForm() {
      this.$emit("closeModal");
      
      if (this.options.length > 1) {
        axios
          .post(`/api/chat/group/${this.activeConversation.id}/create-poll/`, {
            poll_name: this.pollName,
            options: this.options,
            time_end: this.date,
          })
          .then((res) => {
            console.log(res.data)
            this.pollName = "";
            this.options = [];
            this.date = null;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        console.log("Phải có từ 2 lựa chọn");
      }
    },
  },
});
</script>

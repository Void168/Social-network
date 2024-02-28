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
              class="w-full flex flex-col justify-between max-w-md transform overflow-hidden h-80 rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <div>
                <DialogTitle
                  as="h3"
                  class="text-2xl font-medium leading-6 text-gray-900 text-center"
                >
                  Thêm quản trị viên
                </DialogTitle>
                <div class="mt-2">
                  <div>
                    <p class="text-lg font-semibold mb-2">Thành viên</p>
                    <Multiselect
                      v-model="value"
                      mode="tags"
                      :close-on-select="false"
                      :searchable="true"
                      :options="options"
                      :filter-results="true"
                      :limit="3"
                      :infinite="true"
                      :on-create="getValue(value)"
                    >
                      <template v-slot:option="{ option }">
                        <div class="flex items-center gap-2">
                            <img loading="lazy" class="w-10 h-10 rounded-full" :src="option.icon" />
                            <h4 class="font-medium">{{ option.label }}</h4>
                        </div>
                      </template>
                    </Multiselect>
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
                    @click="addModerators"
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

import Multiselect from "@vueform/multiselect";
import { useToastStore } from "@/stores/toast";

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
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    isAddModeratorsOpen: Boolean,
    options: Array,
  },
  data() {
    return {
      value: [],
      profileId: "",
    };
  },
  computed: {},
  methods: {
    getValue(value) {
      this.value = value;
    },
    addModerators() {
      if (this.value.length) {
        axios
          .post(`/api/group/${this.$route.params.id}/add-moderators/`, {
            moderators: this.value,
          })
          .then((res) => {
            this.value = [];
            if (res.data.message === "moderators update") {
              this.toastStore.showToast(
                3000,
                "Thêm quản trị viên thành công.",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 3500);
            } else {
              this.toastStore.showToast(
                3000,
                "Thêm quản trị viên thất bại.",
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        console.log("Phải lớn hơn 1 người");
      }
    },
  },
});
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

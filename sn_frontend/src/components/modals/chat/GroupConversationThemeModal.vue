<template>
  <TransitionRoot
    @click="$emit('closeGroupConversationThemeModal')"
    appear
    as="template"
  >
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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-slate-800 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 dark:text-neutral-200 text-center"
              >
                Chọn chủ đề
              </DialogTitle>
              <div class="text-xl dark:text-neutral-200 my-2">
                <p>Chủ đề hiện tại:</p>
                <div class="flex flex-col items-center">
                  <div class="rounded-full xm:h-24 xm:w-24 xs:h-16 xs:w-16 h-10 w-10 shadow-md my-2" :class="selectedTheme?.background"></div>
                  
                  <p class="xm:text-base text-sm">{{ chosenTheme }}</p>
                </div>
              </div>
              <div class="grid grid-cols-4 gap-4">
                <div class="mt-2" v-for="theme in themes" :key="theme.name">
                  <ConversationTheme
                    :color="theme"
                    @chooseTheme="chooseTheme(theme)"
                  />
                </div>
              </div>

              <div class="mt-4 flex justify-end gap-3">
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white xm:px-4 xm:py-2 px-2 py-1 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeGroupConversationThemeModal')"
                >
                  Hủy
                </button>
                <div @click="$emit('closeGroupConversationThemeModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white xm:px-4 xm:py-2 px-2 py-1 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="confirmGroupConversationTheme"
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

import ConversationTheme from "../../items/chat/ConversationTheme.vue";
import themes from '../../../data/themes'

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    ConversationTheme,
  },
  props: {
    isGroupConversationThemeModalOpen: Boolean,
    currentTheme: Object,
  },
  data() {
    return {
      themes: themes,
      chosenTheme: "",
    };
  },
  computed: {
    selectedTheme() {
      return this.themes.filter((theme) => theme.name === this.chosenTheme)[0];
    },
  },

  mounted() {
    this.getTheme();
  },

  methods: {
    getTheme() {
      axios
        .get(`/api/chat/group/${this.currentTheme?.id}/get/`)
        .then((res) => {
          this.chosenTheme = res.data.theme;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    chooseTheme(theme) {
      this.chosenTheme = theme.name;
    },
    confirmGroupConversationTheme() {
      let formData = new FormData();

      formData.append("theme", this.chosenTheme);

      axios
        .post(`/api/chat/group/${this.currentTheme?.id}/choose_group_theme/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          // console.log(res.data)
        })
        .catch((error) => console.log(error));
    },
  },
});
</script>

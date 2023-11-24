<template>
  <TransitionRoot
    @click="$emit('closeConversationThemeModal')"
    appear
    as="template"
  >
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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 p-6 text-left align-middle shadow-xl transition-all"
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
                  <div class="rounded-full h-24 w-24 shadow-md my-2" :class="selectedTheme?.background"></div>
                  
                  <p>{{ chosenTheme }}</p>
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
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeConversationThemeModal')"
                >
                  Hủy
                </button>
                <div @click="$emit('closeConversationThemeModal')">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="confirmConversationTheme"
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

import ConversationTheme from "../items/ConversationTheme.vue";

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
    isOpen: Boolean,
    currentTheme: Object,
  },
  data() {
    return {
      themes: [
        {
          name: "Ngân hà",
          background:
            "bg-gradient-to-r from-blue-800 via-indigo-800 to-violet-800",
        },
        {
          name: "Hoàng hôn",
          background:
            "bg-gradient-to-r from-blue-500 via-pink-500 to-orange-500",
        },
        {
          name: "Bãi biển",
          background: "bg-gradient-to-r from-blue-500 via-sky-500 to-amber-500",
        },
        {
          name: "Giáng sinh",
          background:
            "bg-gradient-to-r from-neutral-100 via-emerald-500 to-rose-500",
        },
        {
          name: "Mùa xuân",
          background:
            "bg-gradient-to-r from-neutral-200 via-rose-400 to-amber-300",
        },
        {
          name: "Mùa hè",
          background:
            "bg-gradient-to-r from-amber-300 via-cyan-300 to-emerald-400",
        },
        {
          name: "Mùa thu",
          background:
            "bg-gradient-to-r from-rose-600 via-amber-700 to-orange-700",
        },
        {
          name: "Mùa đông",
          background: "bg-gradient-to-r from-cyan-200 via-neutral-200 to-white",
        },
        {
          name: "Tình nhân",
          background: "bg-gradient-to-r from-white via-rose-400 to-red-500",
        },
        {
          name: "Cà phê",
          background:
            "bg-gradient-to-r from-yellow-700 via-amber-700 to-orange-900",
        },
        {
          name: "Bóng đá",
          background:
            "bg-gradient-to-r from-neutral-300 via-emerald-500 to-slate-600",
        },
        {
          name: "Cổ điển",
          background: "bg-emerald-500",
        },
      ],
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
        .get(`/api/chat/${this.currentTheme?.id}/get/`)
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
    confirmConversationTheme() {
      let formData = new FormData();

      formData.append("theme", this.chosenTheme);

      axios
        .post(`/api/chat/${this.currentTheme?.id}/choose_theme/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          // this.selectedTheme.background = res.data.theme;
          console.log(res.data)
        })
        .catch((error) => console.log(error));
    },
  },
});
</script>

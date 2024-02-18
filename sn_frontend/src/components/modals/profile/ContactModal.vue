<template>
  <TransitionRoot @click="$emit('closeContactModal')" appear as="template">
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
              class="w-full relative max-w-md transform overflow-hidden rounded-2xl bg-slate-200 dark:bg-slate-600 dark:text-neutral-200 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-3xl font-medium leading-6 text-center"
              >
                Thông tin liên lạc
              </DialogTitle>
              <div class="my-4">
                <p class="text-xl dark:text-gray-200 mb-2">Liên kết</p>
                <hr />
                <ul v-for="website in websites" v-bind:key="website.id">
                  <li class="text-center my-2 break-all">{{ website.url }}</li>
                </ul>
              </div>
              <div class="my-4">
                <p class="text-xl dark:text-gray-200 mb-2">Liên lạc</p>
                <hr />
                <ul v-for="phoneNumber in phoneNumbers" v-bind:key="phoneNumber.id">
                  <li class="text-center my-2">{{ phoneNumber.phone_number }}</li>
                </ul>
              </div>
              <button
                @click="$emit('closeContactModal')"
                class="absolute top-2 right-2"
              >
                <XMarkIcon class="h-6 w-6"/>
              </button>
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
import { usePageStore } from "../../../stores/page";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
  },

  setup() {
    const pageStore = usePageStore()

    return {
      pageStore
    }
  },

  props: {
    contactIsOpen: Boolean,
  },

  data() {
    return {
      websites: [],
      phoneNumbers: [],
      user: {},
    };
  },

  mounted() {
    this.getUserInfo();
  },

  methods: {
    getUserInfo() {
      if(!this.pageStore.pageActive.is_page){
        axios
          .get(`/api/user-info/${this.$route.params.id}`)
          .then((res) => {
            this.user = res.data.user;
            this.getWebsitesList();
            this.getPhoneNumbersList();
          })
          .catch((error) => console.log(error));
      } else {
        console.log('hello')
      }
    },
    async getWebsitesList() {
      if(!this.pageStore.pageActive.is_page){
        await axios
          .get(`/api/informations/${this.user.id}/websites/`)
          .then((res) => {
            this.websites = res.data.websites;
          })
          .catch((error) => console.log(error));
      } else {
        console.log('hello')
      }
    },
    async getPhoneNumbersList() {
      if(!this.pageStore.pageActive.is_page){
        await axios
          .get(`/api/informations/${this.user.id}/phone-numbers/`)
          .then((res) => {
            this.phoneNumbers = res.data.phone_numbers;
          })
          .catch((error) => console.log(error));
      } else {
        console.log('hello')
      }
    },
  },
});
</script>

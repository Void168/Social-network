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

      <div class="fixed inset-0 overflow-y-auto z-50">
        <div class="flex items-center justify-center text-center">
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
              class="w-full h-screen transform grid grid-cols-5 overflow-hidden bg-white dark:bg-slate-900 text-left align-middle shadow-xl transition-all"
            >
              <div
                class="col-span-1 bg-slate-800 dark:text-neutral-200 border-r-[1px] border-slate-700"
              >
                <button class="m-4 p-2 bg-neutral-900 rounded-full hover:bg-neutral-700">
                  <XMarkIcon
                    @click="$emit('closeModal')"
                    class="text-neutral-200 h-8 w-8 cursor-pointer transition"
                  />
                </button>

                <div class="flex justify-between items-center px-4">
                  <h2 class="text-2xl font-bold">Tin của bạn</h2>
                  <Cog8ToothIcon
                    class="text-neutral-200 h-10 w-10 cursor-pointer p-1 bg-slate-600 rounded-full hover:bg-neutral-600 transition duration-100"
                  />
                </div>
                <div
                  class="flex gap-3 my-4 py-4 items-center border-b border-neutral-700 px-4"
                >
                  <img
                    :src="userStore.user.avatar"
                    alt="story-owner"
                    class="w-16 h-16 rounded-full shadow-lg"
                  />
                  <h3 class="text-xl font-semibold">
                    {{ userStore.user.name }}
                  </h3>
                </div>
              </div>
              <div class="col-span-4 flex justify-center items-center gap-6">
                <div
                  class="group relative flex flex-col space-y-2 justify-center items-center w-60 h-[360px] bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg cursor-pointer"
                >
                  <PhotoIcon
                    class="text-neutral-200 h-14 w-14 cursor-pointer p-3 bg-slate-600 shadow-transparent rounded-full hover:bg-neutral-600 transition duration-100"
                  />
                  <div
                    class="w-full h-full bg-white bg-opacity-25 absolute hidden group-hover:block rounded-lg"
                  ></div>
                  <h4 class="font-bold text-neutral-200">Tạo tin ảnh</h4>
                </div>
                <div
                  class="group relative flex flex-col space-y-2 justify-center items-center w-60 h-[360px] bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-lg cursor-pointer"
                >
                  <div
                    class="w-full h-full bg-white bg-opacity-25 absolute hidden group-hover:block rounded-lg"
                  ></div>
                  <span
                    class="flex justify-center items-center font-semibold text-xl shadow-transparent text-neutral-200 h-14 w-14 cursor-pointer p-1 bg-slate-600 rounded-full hover:bg-neutral-600 transition duration-100"
                  >
                    Aa</span
                  >
                  <h4 class="font-bold text-neutral-200">
                    Tạo tin dạng văn bản
                  </h4>
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
import { useUserStore } from "../../stores/user";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon, Cog8ToothIcon, PhotoIcon } from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    Cog8ToothIcon,
    PhotoIcon,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    isOpen: Boolean,
  },
});
</script>

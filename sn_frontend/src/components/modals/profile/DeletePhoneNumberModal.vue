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
                class="w-full max-w-md transform overflow-hidden rounded-2xl dark:bg-slate-700 bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <DialogTitle
                  as="h3"
                  class="text-2xl font-medium leading-6 text-gray-900 text-center dark:text-neutral-200"
                >
                  Xóa liên lạc?
                </DialogTitle>
                <div class="mt-2">
                  <p class="text-sm text-gray-500 dark:text-neutral-200">
                    Bạn muốn số điện thoại này?
                  </p>
                </div>
  
                <div class="mt-4 flex justify-end gap-3">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium  hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="$emit('closeModal')"
                  >
                    Hủy
                  </button>
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-emerald-400 text-white px-4 py-2 text-sm font-medium  hover:bg-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="$emit('deletePhoneNumber')"
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
  
  export default (await import("vue")).defineComponent({
    components: {
      TransitionRoot,
      TransitionChild,
      Dialog,
      DialogPanel,
      DialogTitle,
    },
    props: {
      isOpen: Boolean
    }
  });
  </script>
  
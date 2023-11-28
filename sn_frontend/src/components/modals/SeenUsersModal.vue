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
              class="relative w-full max-w-md transform overflow-hidden rounded-2xl py-6 bg-white dark:bg-neutral-700 dark:text-neutral-200 text-left align-middle shadow-xl transition-all"
            >
              <XMarkIcon
                @click="$emit('closeModal')"
                class="w-10 h-10 absolute top-2 right-2 cursor-pointer p-1 hover:bg-slate-600 rounded-full transition duration-100"
              />
              <DialogTitle
                as="h3"
                class="text-2xl pb-4 font-bold leading-6 text-gray-900 dark:text-neutral-200 text-center border-b"
              >
                Người đã xem tin nhắn
              </DialogTitle>
              <div class="my-4 px-4" v-for="user in lastMessage" :key="user.id">
                <div class="flex gap-2 items-center">
                  <img
                    :src="user.created_by.get_avatar"
                    alt=""
                    class="w-12 h-12 rounded-full"
                  />
                  <div class="flex flex-col">
                    <p>{{ user.created_by.name }}</p>
                    <p class="text-sm">
                      Đã xem lúc {{ user.created_at.slice(11, 19) }} ngày
                      {{
                        user.created_at
                          .slice(0, 10)
                          .split("-")
                          .reverse()
                          .join("-")
                      }}
                    </p>
                  </div>
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
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon } from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
  },
  props: {
    isOpen: Boolean,
    lastMessage: Object,
  },
});
</script>

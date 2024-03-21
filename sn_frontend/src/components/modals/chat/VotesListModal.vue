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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 p-6 text-left align-middle shadow-xl transition-all"
            >
              <XMarkIcon
                @click="$emit('closeModal')"
                class="w-10 h-10 absolute top-2 right-2 cursor-pointer p-1 hover:bg-slate-600 dark:text-neutral-200 rounded-full transition duration-100"
              />
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 text-center dark:text-neutral-200"
              >
                Danh sách bỏ phiếu
              </DialogTitle>
              <div
                class="my-4"
                v-for="user in option.users_vote"
                :key="user.id"
              >
                <div class="flex gap-4 items-center">
                  <img
                  loading="lazy"
                    :src="user.get_avatar"
                    alt="avatar-vote"
                    class="w-12 h-12 rounded-full"
                  />
                  <p class="dark:text-neutral-200 font-semibold text-lg">
                    {{ user.name }}
                  </p>
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
    option: Object,
  },
});
</script>

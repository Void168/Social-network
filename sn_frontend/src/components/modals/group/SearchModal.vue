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

      <div class="fixed inset-0 overflow-y-auto dark:text-slate-200">
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
              <div class="flex justify-between items-center">
                <DialogTitle
                  as="h3"
                  class="text-2xl font-medium leading-6 text-gray-900 dark:text-slate-200"
                >
                  Tìm kiếm
                </DialogTitle>
                <XMarkIcon
                  @click="$emit('closeModal')"
                  class="w-10 p-1 dark:text-neutral-200 rounded-full dark:bg-slate-700 dark:hover:bg-slate-700/70 duration-75 cursor-pointer"
                />
              </div>
              <div class="mt-2">
                <div class="relative">
                  <MagnifyingGlassIcon
                    class="absolute top-[18px] left-2 sm:w-6 sm:h-6 xs:w-3 xs:h-3 dark:text-neutral-400"
                  />
                  <input
                    @keyup="getQuery"
                    ref="input"
                    type="text"
                    placeholder="Tìm kiếm trong nhóm này"
                    class="w-full my-2 sm:py-2 sm:px-8 xs:py-1 xs:px-6 border border-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
                  />
                </div>
              </div>
              <div class="my-4 flex justify-between gap-2 items-center">
                <h3 class="text-lg font-semibold">Tìm kiếm gần đây</h3>
                <h4
                  class="text-emerald-400 px-4 py-2 hover:bg-slate-400 dark:hover:bg-slate-600 rounded-lg duration-75 cursor-pointer"
                >
                  Chỉnh sửa
                </h4>
              </div>
              <div
                class="px-4 flex flex-col dark:text-neutral-200 py-2 rounded-lg dark:hover:bg-slate-700 duration-75 cursor-pointer"
                v-for="n in 6"
                :key="n"
              >
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-3">
                    <ClockIcon class="w-8 p-1 dark:bg-slate-900 rounded-full" />
                    <h3>g</h3>
                  </div>
                  <XMarkIcon
                    class="w-8 p-1 dark:hover:bg-slate-600 rounded-full"
                  />
                </div>
              </div>
              <div
                class="mt-4 flex flex-col justify-center items-center dark:text-neutral-200"
              >
                <h4 class="font-semibold">Bạn đang tìm gì à?</h4>
                <h5 class="text-center text-sm">
                  Tìm kiếm bài viết, bình luận hoặc thành viên trong
                  {{ groupName }}.
                </h5>
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
import { XMarkIcon, MagnifyingGlassIcon } from "@heroicons/vue/20/solid";
import { ClockIcon } from "@heroicons/vue/24/outline";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    MagnifyingGlassIcon,
    ClockIcon,
  },
  props: {
    isOpen: Boolean,
    groupName: String,
  },

  methods: {
    getQuery() {},
  },
});
</script>

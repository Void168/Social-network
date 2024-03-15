<template>
  <TransitionRoot @click="$emit('closeListVoteModal')" appear as="template">
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
              class="w-full max-w-md h-96 transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-xl font-bold leading-6 text-gray-900 dark:text-slate-200 flex justify-between items-center"
              >
                <h2 class="w-full text-center">{{ option.body }}</h2>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md text-white text-sm font-medium"
                  @click="$emit('closeListVoteModal')"
                >
                  <XMarkIcon
                    class="w-8 h-8 dark:bg-slate-800 dark:hover:bg-slate-800/70 p-1 rounded-full cursor-pointer"
                  />
                </button>
              </DialogTitle>
              <hr class="border border-slate-600 my-2" />
              <div class="mt-4 gap-3 dark:text-slate-200">
                <h2 class="text-xl font-bold">
                  {{
                    totalVote > 0
                      ? Math.round((voteCount / totalVote) * 100, 0)
                      : 0
                  }}% &middot; {{ voteCount }} lượt bình chọn
                </h2>
                <div class="my-4" v-for="user in option.vote_by" :key="user.id">
                  <div class="flex items-center gap-2">
                    <img loading="lazy" :src="user?.information?.get_avatar" class="w-10 h-10 rounded-full" alt="vote-avatar"/>
                    <h4 class="font-semibold">{{ user?.information?.name }}</h4>
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
import axios from "axios";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon } from "@heroicons/vue/24/solid";

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
    isListVoteOpen: Boolean,
    option: Object,
    totalVote: Number,
    voteCount: Number,
  },
});
</script>

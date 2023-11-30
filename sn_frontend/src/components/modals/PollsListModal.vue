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
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-neutral-700 dark:text-neutral-200 p-6 text-left align-middle shadow-xl transition-all"
            >
              <button>
                <XMarkIcon
                  @click="$emit('closeModal')"
                  class="w-10 h-10 absolute top-2 right-2 cursor-pointer p-1 hover:bg-slate-600 rounded-full transition duration-100"
                />
              </button>
              <DialogTitle
                as="h3"
                class="text-2xl font-medium leading-6 text-gray-900 dark:text-neutral-200 text-center"
              >
                Danh sách cuộc thảo luận
              </DialogTitle>
              <div v-if="pollslist.length">
                <div
                  class="mt-2 flex gap-3 justify-around items-center"
                  v-for="poll in pollslist"
                  :key="poll.id"
                >
                  <div
                    class="p-4 bg-neutral-200 dark:bg-slate-600 rounded-xl shadow-md my-2 w-[70%]"
                  >
                    <p class="font-semibold text-center">
                      {{ poll.poll_name }}
                    </p>
                    <p class="font-semibold text-center text-sm">
                      Hạn chót {{ poll.time_end.slice(11, 19) }} ngày
                      {{
                        poll.time_end
                          .slice(0, 10)
                          .split("-")
                          .reverse()
                          .join("-")
                      }}
                    </p>
                    <div v-for="option in poll.poll_options" :key="option.id">
                      <div class="flex justify-between items-center gap-4">
                        <PollVote
                          :option="option"
                          :activeConversation="activeConversation"
                        />
                      </div>
                    </div>
                  </div>
                  <TrashIcon
                    @click="openDeletePollModal"
                    class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                  />
                  <DeletePollModal
                    :show="isOpen"
                    @closeModal="closeModal"
                    @deletePoll="deletePoll(poll.id)"
                  />
                </div>
              </div>
              <p v-else class="text-center text-lg mt-4">Nhóm bạn chưa có cuộc thảo luận nào</p>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import axios from "axios";
import { useToastStore } from "../../stores/toast";

import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon, TrashIcon } from "@heroicons/vue/24/outline";
import themes from "../../data/themes";

import PollVote from "../forms/PollVote.vue";
import DeletePollModal from "../modals/DeletePollModal.vue";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    PollVote,
    DeletePollModal,
    XMarkIcon,
    TrashIcon,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    isPollsListOpen: Boolean,
    pollslist: Object,
    activeConversation: Object,
  },

  data() {
    return {
      themes: themes,
      isOpen: false,
    };
  },

  computed: {
    selectedTheme() {
      return this.themes.filter(
        (theme) => theme.name === this.activeConversation.theme
      )[0];
    },
  },

  methods: {
    openDeletePollModal() {
      this.isOpen = !this.isOpen;
    },
    closeModal() {
      this.isOpen = false;
    },
    deletePoll(id) {
      axios
        .delete(`/api/chat/group/${id}/delete-poll/`)
        .then((res) => {
          setTimeout(() => {
            this.closeModal();
          }, 500);
          this.toastStore.showToast(
            5000,
            "Đã xóa đoạn cuộc thảo luận",
            "bg-emerald-500 text-white"
          );
          setTimeout(() => {
            this.$router.go(0);
          }, 6000);
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            5000,
            "Xóa cuộc thảo luận thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
  },
});
</script>

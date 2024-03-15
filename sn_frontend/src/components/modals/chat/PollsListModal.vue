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
                class="text-2xl font-medium leading-6 text-gray-900 dark:text-neutral-200 text-center mb-4"
              >
                Danh sách cuộc thảo luận
              </DialogTitle>
              <div
                v-if="pollslist.length"
                class="max-h-72 overflow-y-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
              >
                <div
                  class="mt-2 mb-8 flex gap-3 items-center"
                  v-for="poll in pollslist"
                  :key="poll.id"
                >
                  <div
                    v-if="new Date(poll.time_end).getTime() > date"
                    class="w-full flex flex-col justify-around items-center"
                  >
                    <div
                      class="p-4 bg-neutral-200 dark:bg-slate-600 rounded-xl shadow-md mb-2 w-[70%]"
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
                      v-if="
                        userStore.user.id === poll.created_by.id ||
                        userStore.user.id === activeConversation.admin.id
                      "
                      @click="deletePoll(poll.id)"
                      class="w-8 h-8 p-1 shadow-md bg-neutral-100 dark:bg-slate-700 hover:bg-neutral-200 dark:hover:bg-slate-500 transition rounded-full cursor-pointer"
                    />
                  </div>
                  <div
                    v-else
                    class="p-4 bg-neutral-200 dark:bg-slate-600 rounded-xl shadow-md my-2 w-[70%]"
                  >
                    <p class="font-semibold text-center">
                      {{ poll.poll_name }}
                    </p>
                    <p class="font-semibold text-center text-sm">
                      Đã kết thúc vào {{ poll.time_end.slice(11, 19) }} ngày
                      {{
                        poll.time_end
                          .slice(0, 10)
                          .split("-")
                          .reverse()
                          .join("-")
                      }}
                    </p>
                    <p class="my-2">Kết quả</p>
                    <p class="text-center font-bold text-lg">
                      {{
                        poll.poll_options
                          .map((poll_option) => poll_option)
                          .filter((option) =>
                            Math.max(option.users_vote.length)
                          )[0].poll_option_name
                      }}
                    </p>
                  </div>
                </div>
              </div>
              <p v-else class="text-center text-lg mt-4">
                Nhóm bạn chưa có cuộc thảo luận nào
              </p>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import axios from "axios";
import { useToastStore } from "../../../stores/toast";
import { useUserStore } from "../../../stores/user";

import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon, TrashIcon } from "@heroicons/vue/24/outline";
import themes from "../../../data/themes";

import PollVote from "../../forms/PollVote.vue";
import DeletePollModal from "./DeletePollModal.vue";

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
    const userStore = useUserStore();

    return {
      toastStore,
      userStore,
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
    date() {
      return new Date().getTime();
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

<template>
  <TransitionRoot @click="$emit('closeQuestionModal')" appear as="template">
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
              class="w-[600px] transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-xl font-bold leading-6 text-gray-900 dark:text-slate-200 flex justify-between items-center"
              >
                Trả lời câu hỏi
                <XMarkIcon
                  @click="$emit('closeQuestionModal')"
                  class="w-8 h-8 dark:bg-slate-800 dark:hover:bg-slate-800/70 p-1 rounded-full cursor-pointer"
                />
              </DialogTitle>
              <hr class="border border-slate-600 my-2" />
              <div class="flex items-center gap-2 dark:text-neutral-200">
                <RouterLink
                  :to="{ name: 'groupdetail', params: { id: group?.id } }"
                  class="rounded-lg"
                >
                  <img
                  loading="lazy"
                    :src="group.get_cover_image"
                    alt=""
                    class="rounded-lg xm:h-16 xm:w-16 h-10 w-10"
                  />
                </RouterLink>
                <div class="flex flex-col xm:space-y-2">
                  <h4 class="font-semibold">{{ group.name }}</h4>
                  <div class="flex items-center gap-2">
                    <GlobeAsiaAustraliaIcon
                      v-if="!group.is_private_group"
                      class="w-4"
                    />
                    <LockClosedIcon v-else class="w-4" />
                    <h5 class="text-sm">
                      {{
                        group.is_private_group
                          ? "Nhóm riêng tư"
                          : "Nhóm công khai"
                      }}
                      &middot; {{ group.members_count }} thành viên
                    </h5>
                  </div>
                </div>
              </div>
              <div
                class="my-2 dark:bg-slate-800 dark:text-neutral-200 rounded-lg p-4"
              >
                <h3 class="xm:text-lg font-semibold">
                  Yêu cầu tham gia của bạn đang chờ phê duyệt
                </h3>
                <h4 class="xm:text-base text-sm">
                  Hãy trả lời những câu hỏi sau của quản trị viên nhóm để họ có
                  thể xem xét yêu cầu tham gia của bạn. Câu trả lời của bạn sẽ
                  chỉ hiển thị với quản trị viên và người kiểm duyệt.
                </h4>
              </div>
              <div
                v-for="question in questions"
                :key="question.id"
              >
                <GroupAnswer :question="question" @getAnswer="getAnswer" :index="questions.indexOf(question) + 1"/>
              </div>
              <div class="mt-4 flex xm:flex-row flex-col gap-2 justify-between items-center">
                <h5 class="dark:text-neutral-200 text-xs">
                  Không nhập mật khẩu hoặc thông tin nhạy cảm khác tại đây, ngay
                  cả khi quản trị viên nhóm {{ group.name }} yêu cầu.
                </h5>
                <div class="flex items-center gap-2 w-full">
                  <button
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 w-full"
                    @click="$emit('closeQuestionModal')"
                  >
                    Hủy
                  </button>
                  <button
                    @click="submitForm"
                    :disabled="!answer1 && !answer2 && !answer3"
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent  text-white px-4 py-2 text-sm font-medium  focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 w-full"
                    :class="!answer1 && !answer2 && !answer3 ? 'bg-slate-400 hover:bg-slate-400' : 'bg-emerald-400 hover:bg-emerald-600'"
                  >
                    Gửi
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
import {
  XMarkIcon,
  GlobeAsiaAustraliaIcon,
  LockClosedIcon,
  EllipsisHorizontalIcon,
} from "@heroicons/vue/24/solid";
import { RouterLink } from "vue-router";
import GroupAnswer from "../../items/group/GroupAnswer.vue";

export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    GlobeAsiaAustraliaIcon,
    LockClosedIcon,
    EllipsisHorizontalIcon,
    GroupAnswer,
  },
  props: {
    isQuestionOpen: Boolean,
    group: Object,
    questions: Array,
  },

  data(){
    return {
      answer1: "",
      answer2: "",
      answer3: "",
    }
  },

  methods: {
    getAnswer(answer, index){
      if(index === 1){
        this.answer1 = answer
      }
      if(index === 2){
        this.answer2 = answer
      }
      if(index === 3){
        this.answer3 = answer
      }
    },
    submitForm(){
      axios.post(`/api/group/${this.$route.params.id}/answer/`, {
        answer1: this.answer1,
        answer2: this.answer2,
        answer3: this.answer3,
      }).then((res) => {
        this.$router.go(0)
        console.log(res.data)
      }).catch((error) => {
        console.log(error)
      })
    }
  },
});
</script>

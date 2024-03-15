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
              class="w-full max-w-lg transform overflow-hidden rounded-2xl bg-white dark:bg-slate-700 p-6 text-center align-middle shadow-xl transition-all relative"
            >
              <DialogTitle
                as="h3"
                class="text-xl font-bold leading-6 text-gray-900 dark:text-slate-200"
              >
                Tạo quy tắc
                <XMarkIcon
                  @click="$emit('closeModal')"
                  class="absolute w-8 h-8 top-4 right-4 dark:bg-slate-800 dark:hover:bg-slate-800/70 p-1 rounded-full cursor-pointer"
                />
              </DialogTitle>
              <hr class="border border-slate-600 my-4" />
              <h3
                class="text-lg font-bold text-left leading-6 text-gray-900 dark:text-slate-200"
              >
                Quy tắc mẫu
              </h3>
              <div class="flex flex-wrap gap-2 my-2">
                <div
                  v-for="rule in ruleTemplates"
                  :key="rule.id"
                  class="py-2 px-4 rounded-full w-52 cursor-pointer"
                  :class="
                    index === rule.id
                      ? 'bg-emerald-800/50 dark:text-emerald-400'
                      : 'dark:bg-slate-800 dark:text-neutral-200 dark:hover:bg-slate-600 duration-75'
                  "
                  @click="chooseRuleTemplate(rule)"
                >
                  <h4 class="truncate font-semibold">
                    {{ rule.name }}
                  </h4>
                </div>
              </div>
              <h3
                class="text-lg font-bold text-left leading-6 text-gray-900 dark:text-slate-200 mt-4"
              >
                Viết quy tắc riêng
              </h3>
              <div class="mt-2">
                <MUILikedInput :placeholder="'Tiêu đề'" v-model="name" />
              </div>
              <div class="mt-2">
                <textarea
                  type="text"
                  class="form-control resize-none w-full rounded-lg p-4"
                  rows="4"
                  placeholder="Mô tả"
                  v-model="body"
                ></textarea>
              </div>

              <div class="mt-4 flex justify-end gap-3">
                <button
                  type="button"
                  class="btn inline-flex justify-center rounded-md border border-transparent bg-rose-400 text-white px-4 py-2 text-sm font-medium hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('closeModal')"
                >
                  Hủy
                </button>
                <div @click="$emit('closeModal')">
                  <button
                    :disabled="!name"
                    type="button"
                    class="btn inline-flex justify-center rounded-md border border-transparent px-4 py-2 text-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="createRule"
                    :class="
                      !name
                        ? 'dark:bg-slate-600 dark:text-neutral-400 dark:hover:bg-slate-600'
                        : 'bg-emerald-400 text-white hover:bg-emerald-600'
                    "
                  >
                    Tạo
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
import { XMarkIcon } from "@heroicons/vue/24/solid";
import MUILikedInput from "../../input/MUILikedInput.vue";
import { useToastStore } from "../../../stores/toast";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    MUILikedInput,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    isOpen: Boolean,
  },

  data() {
    return {
      body: "",
      name: "",
      index: 0,
      ruleTemplates: [
        {
          id: 1,
          name: "Hãy tử tế và lịch sự",
          body: "Tất cả chúng ta cùng có mặt ở đây để tạo nên một môi trường thân thiện. Hãy tôn trọng tất cả mọi người. Tranh luận lành mạnh là điều hết sức tự nhiên nhưng cũng cần tử tế.",
        },
        {
          id: 2,
          name: "Không dùng ngôn từ gây thù ghét hoặc bắt nạt",
          body: "Hãy đảm bảo mọi người cảm thấy an toàn. Mọi hình thức bắt nạt đều không được cho phép và những bình luận hạ nhục về chủng tộc, tôn giáo, văn hóa, thiên hướng tính dục, giới tính hoặc bản sắc sẽ không được chấp nhận.",
        },
        {
          id: 3,
          name: "Không quảng cáo hoặc spam",
          body: "Trong nhóm, hãy cho đi nhiều hơn nhận lại. Bạn không được tự quảng bá, spam và đăng liên kết không phù hợp.",
        },
        {
          id: 4,
          name: "Tôn trọng quyền riêng tư của mọi người",
          body: "Tham gia nhóm này đòi hỏi phải có sự tin tưởng từ hai phía. Các cuộc thảo luận thực, mang tính biểu đạt giúp nhóm trở nên tuyệt vời nhưng cũng có thể nhạy cảm và riêng tư. Không tiết lộ nội dung được chia sẻ trong nhóm ra bên ngoài.",
        },
      ],
    };
  },

  methods: {
    chooseRuleTemplate(rule) {
      if (this.index === rule.id) {
        this.index = 0;
      } else {
        this.index = rule.id;
        this.name = this.ruleTemplates[this.index - 1].name;
        this.body = this.ruleTemplates[this.index - 1].body;
      }
    },
    createRule() {
      let formData = new FormData();

      formData.append("name", this.name);
      formData.append("body", this.body);
      axios
        .post(`/api/group/${this.$route.params.id}/add-rule/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (res.data.message) {
            this.toastStore.showToast(
              3500,
              "Đã tạo quy tắc",
              "bg-emerald-500 text-white"
            );
          }
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Đã tạo quy tắc thất bại",
            "bg-emerald-500 text-white"
          );
        });
    },
  },
});
</script>

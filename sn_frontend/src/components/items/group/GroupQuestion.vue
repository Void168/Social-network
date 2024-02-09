<template>
  <div class="p-4 dark:bg-slate-800 rounded-lg">
    <h4 class="text-sm">Câu hỏi {{ index }}</h4>
    <h3 class="font-semibold" v-if="!isUpdate">{{ question.body }}</h3>
    <div
      class="my-4 dark:bg-slate-700 rounded-lg relative h-20"
      v-if="!isUpdate"
    >
      <span class="absolute top-2 left-2 dark:text-neutral-400"
        >Viết câu trả lời...</span
      >
    </div>
    <MUILikedInput
      v-else
      :placeholder="'Chỉnh sửa câu hỏi'"
      :type="'text'"
      v-model="body"
      class="my-4"
    />
    <div class="py-4 flex justify-center items-center gap-2" v-if="!isUpdate">
      <button
        @click="openUpdateQuestion"
        class="py-2 px-4 font-semibold text-emerald-300 rounded-lg bg-emerald-500/70 hover:bg-emerald-500/50 duration-75 w-full"
      >
        Chỉnh sửa
      </button>
      <button
        @click="deleteQuestion(question)"
        class="py-2 px-4 font-semibold dark:text-neutral-200 rounded-lg dark:bg-slate-600 dark:hover:bg-slate-700 duration-75 w-full"
      >
        Xóa
      </button>
    </div>
    <div class="py-4 flex justify-center items-center gap-2" v-else>
      <button
        @click="closeUpdateQuestion"
        class="py-2 px-4 font-semibold dark:text-neutral-200 rounded-lg dark:bg-slate-600 dark:hover:bg-slate-700 duration-75 w-full"
      >
        Hủy
      </button>
      <button
        class="py-2 px-4 font-semibold text-emerald-300 rounded-lg bg-emerald-500/70 hover:bg-emerald-500/50 duration-75 w-full"
        @click="updateQuestion(body)"
      >
        Lưu
      </button>
    </div>
  </div>
</template>

<script>
import MUILikedInput from "../../input/MUILikedInput.vue";
import axios from "axios";
import { useToastStore } from "../../../stores/toast";

export default (await import("vue")).defineComponent({
  components: {
    MUILikedInput,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    question: Object,
    index: Number,
  },

  data() {
    return {
      isUpdate: false,
      isDelete: false,
      body: this.question.body || "",
    };
  },

  methods: {
    openUpdateQuestion() {
      this.isUpdate = true;
      this.body = this.question.body;
    },
    closeUpdateQuestion() {
      this.isUpdate = false;
      this.body = this.question.body;
    },
    updateQuestion(body) {
      let formData = new FormData();

      formData.append("body", body);

      if (body !== "") {
        axios
          .post(`/api/group/${this.question.id}/update-question/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message) {
              this.toastStore.showToast(
                3500,
                "Đã chỉnh sửa câu hỏi.",
                "bg-emerald-500 text-white"
              );
              this.isUpdate = false
            }
          })
          .catch((error) => {
            console.log(error);
            this.toastStore.showToast(
              3500,
              "Chỉnh sửa câu hỏi thất bại.",
              "bg-rose-500 text-white"
            );
          });
      }
    },
    deleteQuestion(question) {
      axios
        .post(`/api/group/${question.id}/delete-question/`)
        .then((res) => {
          if (res.data.message) {
            this.toastStore.showToast(
              3500,
              "Đã xóa câu hỏi.",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 4000);
          }
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Xóa câu hỏi thất bại.",
            "bg-rose-500 text-white"
          );
        });
    },
  },
});
</script>

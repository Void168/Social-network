<template>
  <div class="w-full flex justify-center my-12">
    <div class="w-[30%] flex justify-center flex-col items-center space-y-4">
      <img
        src="https://www.call2customer.com/wp-content/uploads/2020/01/brochure.png"
        alt=""
        class="w-32 h-32"
      />
      <div class="text-neutral-400">
        <h2 class="text-2xl text-center font-semibold">
          Câu hỏi chọn thành viên
        </h2>
        <h3 class="text-center">
          Đặt tối đa 3 câu hỏi chọn thành viên cho người muốn tham gia nhóm. Chỉ
          quản trị viên và người kiểm duyệt mới xem được câu trả lời.
        </h3>
      </div>
      <div v-for="question in questions" :key="question.id" class="w-full">
        <GroupQuestion :question="question" :index="questions.indexOf(question) + 1"/>
      </div>
      <div
        @click="openModal"
        class="font-semibold px-4 py-2 bg-emerald-500 rounded-lg hover:bg-emerald-400 cursor-pointer"
      >
        Thêm câu hỏi
      </div>
      <CreateQuestionModal :show="isOpen" @closeModal="closeModal" />
    </div>
  </div>
</template>

<script>
import CreateQuestionModal from "../../../components/modals/group/CreateQuestionModal.vue";
import GroupQuestion from "../../../components/items/group/GroupQuestion.vue";
import axios from "axios";

export default {
  name: "groupquestion",
  components: {
    CreateQuestionModal,
    GroupQuestion
  },
  data() {
    return {
      isOpen: false,
      questions: [],
    };
  },

  mounted() {
    this.getGroupQuestions();
  },

  methods: {
    openModal() {
      this.isOpen = true;
    },
    closeModal() {
      this.isOpen = false;
    },
    async getGroupQuestions() {
      await axios
        .get(`/api/group/${this.$route.params.id}/get-questions/`)
        .then((res) => {
          this.questions = res.data
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

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
      <div
        @click="openModal"
        class="font-semibold px-4 py-2 bg-emerald-500 rounded-lg hover:bg-emerald-400 cursor-pointer"
      >
        Thêm câu hỏi
      </div>
      <CreateQuestion
        :show="isOpen"
        @closeModal="closeModal"
        @deletePost="deletePost"
      />
    </div>
  </div>
</template>

<script>
import CreateQuestion from "../../components/modals/group/CreateQuestion.vue";

export default {
  name: "groupquestion",
  components: {
    CreateQuestion,
  },
  data() {
    return{
        isOpen: false,
    }
  },

  methods: {
    openModal() {
        this.isOpen = true
    },
    closeModal() {
        this.isOpen = false
    },
    deletePost() {},
  },
};
</script>

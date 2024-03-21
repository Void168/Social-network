<template>
  <div
    class="max-w-7xl xm:mx-auto mx-4 flex justify-center gap-2 items-center dark:text-neutral-200"
    :style="{ height: `${toastStore.height}px` }"
  >
    <div
      class="flex flex-col justify-center gap-4 items-center xm:w-[440px] w-full text-center"
    >
      <img
        src="https://www.facebook.com/images/comet/empty_states_icons/permissions/permissions_dark_mode.svg"
        class="xm:w-32 xm:h-32 h-20 w-20 shadow-none"
      />
      <h3 class="font-bold xm:text-xl">Bạn hiện không xem được nội dung này</h3>
      <h4 class="dark:text-neutral-400 xm:text-base text-sm">
        Lỗi này thường do chủ sở hữu chỉ chia sẻ nội dung với một nhóm nhỏ, thay
        đổi người được xem hoặc đã xóa nội dung.
      </h4>
      <RouterLink
        :to="{ name: 'feed' }"
        class="px-6 py-2 font-semibold xm:text-base text-sm bg-emerald-500 hover:bg-emerald-400 duration-75 rounded-lg"
      >
        Đi tới bảng tin
      </RouterLink>
      <div class="font-semibold dark:text-emerald-400 text-emerald-500 flex flex-col justify-center items-center">
          <h4 @click="goBack" class="cursor-pointer hover:underline max-w-max">Quay lại</h4>
          <h4>Truy cập trung tâm trợ giúp</h4>
      </div>
    </div>
  </div>
</template>

<script>
import { useToastStore } from "../stores/toast";
import { RouterLink } from "vue-router";
export default {
  components: {
    RouterLink,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },

  methods: {
    goBack(){
        this.$router.go(-1)
    }
  }
};
</script>

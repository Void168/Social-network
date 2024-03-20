<template>
  <div
    class="relative justify-end 2xl:h-[500px] xl:h-[400px] lg:h-[300px] h-[500px] bg-center bg-cover bg-no-repeat"
    :style="bgImage"
  >
    <button @click="openModal" class="bg-gray-200 text-white bg-opacity-20 px-4 py-2 rounded-lg absolute right-4 bottom-4 hover:bg-opacity-70 transition-colors shadow-lg">Chọn ảnh</button>
    <CoverImageModal
      :show="isOpen"
      @closeModal="closeModal"
    />
  </div>
</template>
<script>
import { useUserStore } from "../stores/user";
import { usePageStore } from "../stores/page";
import CoverImageModal from "./modals/profile/CoverImageModal.vue";

export default {
  setup() {
    const userStore = useUserStore();
    const pageStore = usePageStore()
    return {
      userStore,
      pageStore
    };
  },
  props: {
    user: Object,
    posts: Array,
    page: Object,
  },
  data() {
    return {
      isOpen: false,
    };
  },

  computed: {
    bgImage(){
      return {
        backgroundImage: `url(${this.page?.get_cover_image || this.user?.get_cover_image})`
      }
    }
  },
  methods: {
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
  components: { CoverImageModal },
};
</script>

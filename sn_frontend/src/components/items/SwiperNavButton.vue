<template>
  <div class="flex items-center w-full justify-between absolute z-[60] inset-y-0 px-4">
    <button @click="swiper.slidePrev()">
      <ChevronLeftIcon
        class="w-12 bg-slate-700 p-2 rounded-full hover:bg-slate-600 transition duration-100"
      />
    </button>
    <button @click="swiper.slideNext()">
      <ChevronRightIcon
        class="w-12 bg-slate-700 p-2 rounded-full hover:bg-slate-600 transition duration-100"
      />
    </button>
  </div>
</template>

<script>
import { useSwiper } from "swiper/vue";
import { ChevronRightIcon, ChevronLeftIcon } from "@heroicons/vue/24/solid";

export default {
  components: { ChevronRightIcon, ChevronLeftIcon },
  setup() {
    const swiper = useSwiper();

    return {
      swiper,
    };
  },
};
</script>

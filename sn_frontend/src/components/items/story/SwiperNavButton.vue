<template>
  <div class="px-4">
    <button @click="swiper.slidePrev()" class="absolute inset-y-0 z-10 left-4">
      <ChevronLeftIcon
        class="w-12 bg-slate-700 p-2 rounded-full hover:bg-slate-600 transition duration-100"
      />
    </button>
    <button @click="swiper.slideNext()" class="absolute inset-y-0 z-10 right-4">
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

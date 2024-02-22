<template>
  <div class="px-4">
    <button
      @click="swiper.slidePrev(0, false)"
      class="absolute inset-y-0 z-10 left-4"
      v-if="
        (activeSlide > 0 &&
          currentStoryStore.listId.indexOf(currentStoryStore.currentUserId) ===
            0) ||
        currentStoryStore.listId.indexOf(currentStoryStore.activeStory) > 0
      "
    >
      <div @click="$emit('prev')">
        <ChevronLeftIcon
          class="w-12 dark:bg-slate-700/50 dark:hover:bg-slate-600 bg-slate-300 hover:bg-slate-400 p-2 rounded-full  transition duration-100"
        />
      </div>
    </button>
    <button
      @click="swiper.slideNext(0, false)"
      class="absolute inset-y-0 z-10 right-4"
      v-if="
        (activeSlide > 0 &&
          currentStoryStore.listId.indexOf(currentStoryStore.currentUserId) ===
            currentStoryStore.listId.length - 1) ||
        currentStoryStore.listId.indexOf(currentStoryStore.currentUserId) <
          currentStoryStore.listId.length
      "
    >
      <div @click="$emit('next')">
        <ChevronRightIcon
          class="w-12 dark:bg-slate-700/50 dark:hover:bg-slate-600 bg-slate-300 hover:bg-slate-400 dark:text-neutral-200 text-black p-2 rounded-full  transition duration-100"
        />
      </div>
    </button>
  </div>
</template>

<script>
import { useSwiper } from "swiper/vue";
import { ChevronRightIcon, ChevronLeftIcon } from "@heroicons/vue/24/solid";
import { useCurrentStoryStore } from "../../../stores/currentStory";

export default {
  components: { ChevronRightIcon, ChevronLeftIcon },
  setup() {
    const swiper = useSwiper();
    const currentStoryStore = useCurrentStoryStore();

    return {
      swiper,
      currentStoryStore,
    };
  },

  props: {
    activeSlide: Number,
  },
};
</script>

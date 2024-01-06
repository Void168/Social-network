<template>
  <div
    class="flex items-center justify-between absolute bottom-0 w-full p-4 z-20"
  >
    {{ stories[currentStoryStore.activeSlide].caption }}
  </div>
</template>

<script>
import { useCurrentStoryStore } from "../../../stores/currentStory";

export default (await import("vue")).defineComponent({

  setup() {
    const currentStoryStore = useCurrentStoryStore();
    return {
      currentStoryStore,
    };
  },

  props: {
    stories: Array,
  },
});
</script>

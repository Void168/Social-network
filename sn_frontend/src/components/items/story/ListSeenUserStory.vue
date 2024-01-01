<template>
  <div
    class="flex items-start absolute bottom-0 max-h-min p-4 z-50 w-full h-[90%] flex-col bg-slate-700 rounded-lg"
  >
    <XMarkIcon class="absolute top-3 right-2 h-10 w-10 cursor-pointer p-2 hover:bg-neutral-600 rounded-full" @click="$emit('closeListSeen')"/>
    <p
      class="pb-4 border-b border-slate-600 font-bold text-lg w-full text-center"
    >
      Chi tiết về tin
    </p>
    <div
      v-for="user in stories[currentStoryStore.activeSlide]?.seen_by"
      :key="user.id"
    >
      <p class="">{{ user.name }}</p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";
import { XMarkIcon } from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    XMarkIcon,
  },
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();
    return {
      userStore,
      currentStoryStore,
    };
  },

  props: {
    stories: Array,
  },

  data() {
    return {
      isOpen: false,
    };
  },
});
</script>

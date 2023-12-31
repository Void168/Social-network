<template>
  <div
    @click="$emit('otherStory')"
    class="flex gap-3 items-center py-4 px-8 hover:bg-slate-700 rounded-lg cursor-pointer"
    :class="
      currentStoryStore.activeStory === story[0]?.created_by?.id
        ? 'bg-slate-700'
        : ''
    "
  >
    <img
      :src="story[0].created_by.get_avatar"
      alt="story-owner"
      class="w-16 h-16 rounded-full ring-4 ring-emerald-400"
    />
    <div class="flex flex-col space-y-2">
      <h3 class="text-lg font-semibold">{{ story[0]?.created_by.name }}</h3>
      <p class="flex gap-2">
        <span class="text-emerald-400">{{ story.length }} thẻ mới</span>
        <span>{{ story[0].created_at_formatted }} trước</span>
      </p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();

    return {
      userStore,
      currentStoryStore,
    };
  },

  props: {
    story: Object,
    isOtherStory: Boolean,
  },
});
</script>

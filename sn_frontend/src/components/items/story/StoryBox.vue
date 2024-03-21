<template>
  <div
    @click="$emit('otherStory')"
    class="flex gap-3 items-center xm:py-4 xm:px-8 py-2 px-4 dark:hover:bg-slate-700 hover:bg-slate-200 rounded-lg cursor-pointer"
    :class="
      currentStoryStore.activeStory === story[0]?.created_by?.id
        ? 'dark:bg-slate-700 bg-slate-200'
        : ''
    "
  >
    <img
    loading="lazy"
      :src="story[0].created_by.get_avatar"
      alt="story-owner"
      class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 vs:w-10 vs:h-10 rounded-full ring-4"
      :class="haveSeen ? 'ring-slate-500' : 'ring-emerald-400'"
    />
    <div class="flex flex-col 2xl:space-y-2 w-full">
      <h3 class="xl:text-lg font-semibold">{{ story[0]?.created_by.name }}</h3>
      <p class="flex 2xl:gap-2 2xl:flex-row xl:text-base vs:text-sm flex-wrap flex-col w-full">
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

  computed: {
    haveSeen(){
      return this.story[0]?.seen_by?.map((user) => user.id === this.userStore.user.id)
    }
  }
});
</script>

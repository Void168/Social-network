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
      class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 xs:w-10 xs:h-10 rounded-full ring-4"
      :class="haveSeen ? 'ring-slate-500' : 'ring-emerald-400'"
    />
    <div class="flex flex-col 2xl:space-y-2 w-full">
      <h3 class="xl:text-lg font-semibold">{{ story[0]?.created_by.name }}</h3>
      <p class="flex 2xl:gap-2 2xl:flex-row xl:text-base xs:text-sm flex-wrap flex-col w-full">
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

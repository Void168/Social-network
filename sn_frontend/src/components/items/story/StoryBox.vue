<template>
  <div
    class="flex gap-3 items-center py-4 px-8 hover:bg-slate-700 rounded-lg cursor-pointer"
  >
    <img
      :src="story[0].created_by.get_avatar"
      alt="story-owner"
      class="w-16 h-16 rounded-full ring-4 ring-emerald-400"
    />
    <div class="flex flex-col space-y-2">
      <h3 class="text-lg font-semibold">{{ userStore.user.name }}</h3>
      <p class="flex gap-2">
        <span class="text-emerald-400">{{ story.length }} thẻ mới</span>
        <span>{{story[0].created_at_formatted}} trước</span>
      </p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  props: {
    story: Object,
  },
});
</script>

<template id="card-template">
  <div class="rounded-md p-4 w-full">
    <div class="animate-pulse flex flex-col">
      <div class="flex gap-5">
        <div
          class="rounded-full bg-slate-200 dark:bg-slate-700 h-10 w-10"
        ></div>
        <div class="flex-1 space-y-6 py-1 w-full">
          <div class="h-full bg-slate-200 dark:bg-slate-700 rounded"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  HeartIcon as HeartLike,
  ChatBubbleOvalLeftIcon,
} from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    HeartLike,
    ChatBubbleOvalLeftIcon,
  },
});
</script>

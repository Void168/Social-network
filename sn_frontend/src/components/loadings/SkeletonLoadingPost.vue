<template id="card-template">
  <div class="shadow rounded-md p-4 w-full">
    <div class="animate-pulse flex flex-col">
      <div class="flex gap-5">
        <div
          class="rounded-full bg-slate-200 dark:bg-slate-700 h-10 w-10"
        ></div>
        <div class="flex-1 space-y-6 py-1 w-full">
          <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded"></div>
          <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded"></div>
          <div class="space-y-3">
            <div class="grid grid-cols-3 gap-4">
              <div
                class="h-2 bg-slate-200 dark:bg-slate-700 rounded col-span-2"
              ></div>
              <div
                class="h-2 bg-slate-200 dark:bg-slate-700 rounded col-span-1"
              ></div>
            </div>
            <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded"></div>
          </div>
        </div>
      </div>

      <div class="flex gap-2 mt-4">
        <HeartLike class="w-6 h-6 text-slate-200 dark:text-slate-700" />
        <ChatBubbleOvalLeftIcon class="w-6 h-6 text-slate-200 dark:text-slate-700" />
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

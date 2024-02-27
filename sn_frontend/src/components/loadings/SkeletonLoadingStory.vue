<template id="card-template">
    <div class="shadow rounded-md p-4 w-full h-[213px] animate-pulse bg-slate-200 dark:bg-slate-700">
      <div class="flex flex-col">
        <div class="flex gap-5">
          <div
            class="rounded-full bg-slate-200 dark:bg-slate-900 h-10 w-10"
          ></div>
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
  
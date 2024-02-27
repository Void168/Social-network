<template id="card-template">
    <div class="shadow rounded-md p-4 w-[40%] h-full bg-slate-200 animate-pulse dark:bg-slate-600 mt-8">
      <div class="animate-pulse flex flex-col">
        <div class="flex gap-5">
          <div
            class="rounded-full bg-slate-200 dark:bg-slate-700 h-10 w-10"
          ></div>
          <div class="flex-1 space-y-6 py-1 w-full">
            <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded"></div>
            <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default (await import("vue")).defineComponent({
  });
  </script>
  
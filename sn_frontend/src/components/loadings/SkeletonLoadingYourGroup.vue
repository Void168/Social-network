<template id="card-template">
  <div class="shadow rounded-md p-4 bg-slate-200 dark:bg-slate-800 w-full">
    <div class="animate-pulse flex flex-col space-y-2">
      <div class="flex gap-5">
        <div class="bg-slate-200 dark:bg-slate-700 rounded-lg h-20 w-20"></div>
        <div class="flex-1 px-4 space-y-6 py-1 w-full">
          <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded w-20"></div>
          <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded w-40"></div>
        </div>
      </div>
      <div
        class="space-y-3 bg-slate-200 dark:bg-slate-700 rounded w-full h-6"
      ></div>
    </div>
  </div>
</template>

<script>
export default (await import("vue")).defineComponent({});
</script>

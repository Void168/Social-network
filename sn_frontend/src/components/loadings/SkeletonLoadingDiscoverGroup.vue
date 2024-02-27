<template id="card-template">
  <div class="shadow rounded-md w-80 bg-slate-200 dark:bg-slate-800 pb-4">
    <div class="animate-pulse flex flex-col">
      <div class="flex flex-col gap-5">
        <div
          class="w-full bg-slate-200 dark:bg-slate-700 h-10 rounded-t-lg  md:h-48 sm:h-64 xs:h-56"
        ></div>
        <div class="flex-1 px-4 space-y-6 py-1 w-full">
          <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded w-20"></div>
          <div class="h-2 bg-slate-200 dark:bg-slate-700 rounded w-40"></div>
            <div
              class="space-y-3 bg-slate-200 dark:bg-slate-700 rounded w-full h-6"
            ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default (await import("vue")).defineComponent({});
</script>

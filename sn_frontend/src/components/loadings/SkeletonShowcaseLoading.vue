<template id="card-template">
    <div class="animate-pulse shadow p-4 rounded-lg bg-slate-200 dark:bg-slate-700" :class="route.name === 'profiledetail' || route.name === 'pagedetail'  ? 'xl:h-32 lg:h-24 md:w-full sm:h-48 xm:h-32 xs:h-24 cursor-pointer' : 'md:h-48 sm:h-64 xm:h-56 xs:h-32 w-full cursor-pointer'">
    </div>
  </template>
  
  <script>
  import { useRoute } from "vue-router";

  export default (await import("vue")).defineComponent({
    setup() {
    const route = useRoute();

    return {
      route,
    };
  },
  });
  </script>
  
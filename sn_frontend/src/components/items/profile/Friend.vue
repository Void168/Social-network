<template>
  <RouterLink :to="{name: 'profile', params: {id: friend.id}}">
    <div class="text-slate-900 dark:text-neutral-200 bg-white dark:bg-slate-600">
      <div class="relative group">
        <button
          class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
        ></button>
        <img loading="lazy" :src="friend?.get_avatar" class="xl:h-32 lg:h-24 w-full sm:h-48 xm:h-32 xs:h-24 cursor-pointer rounded-lg" />
      </div>
      <h4 class="text-sm font-semibold my-2 text-center">{{ friend.name }}</h4>
    </div>
  </RouterLink>
  </template>
  
  <script>
  import { RouterLink } from "vue-router";
  import { useUserStore } from "../../../stores/user";
  import { useRoute } from "vue-router";
  
  export default (await import("vue")).defineComponent({
    setup() {
      const userStore = useUserStore();
      const route = useRoute();
      const path = route.fullPath
  
      return {
        userStore,
        route,
        path
      };
    },
    props: {
      friend: Object,
    },

    components: { RouterLink },
  });
  </script>
  
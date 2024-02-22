<template>
    <RouterLink
      :to="{ name: 'page', params: { id: page.id } }"
      class="flex flex-col items-center"
    >
      <img :src="page.get_avatar" alt="" class="sm:w-32 sm:h-32 h-16 w-16 mb-6 rounded-full" />
      <p>
        <strong> {{ page.name }}</strong>
      </p>
      <div class="mt-6 flex space-x-8 justify-around" v-if="route.name === 'pageusers'">
        <p class="text-xs text-gray-500 dark:text-neutral-200">
          {{ page.followers_count }} người bạn
        </p>
        <p class="text-xs text-gray-500 dark:text-neutral-200">
          {{ page.posts_count }} bài đăng
        </p>
      </div>
    </RouterLink>
  </template>
  
  <script>
  import { RouterLink, useRoute } from "vue-router";
  export default (await import("vue")).defineComponent({
    setup(){
    const route = useRoute()

     return {
      route
     }
  },
  
    components: {
      RouterLink,
    },
  
    props: {
      page: Object
    }
  });
  </script>
  
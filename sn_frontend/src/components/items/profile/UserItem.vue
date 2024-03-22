<template>
  <RouterLink
    :to="{ name: 'profile', params: { id: user.id } }"
    class="flex flex-col items-center"
  >
    <img loading="lazy" :src="user.get_avatar" alt="" class="sm:w-32 sm:h-32 h-16 w-16 mb-6 rounded-full" />
    <p>
      <strong> {{ user.name }}</strong>
    </p>
    <div class="mt-6 flex xm:flex-row flex-col xm:space-x-8 xm:justify-around" v-if="route.name === 'pageusers'">
      <p class="text-xs text-gray-500 dark:text-neutral-200">
        {{ user.friends_count }} người bạn
      </p>
      <p class="text-xs text-gray-500 dark:text-neutral-200">
        {{ user.posts_count }} bài đăng
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
    user: Object
  }
});
</script>

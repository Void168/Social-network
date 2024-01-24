<template>
  <RouterLink
    :to="{ name: 'profile', params: { id: user.id } }"
    class="flex flex-col items-center"
  >
    <img :src="user.get_avatar" alt="" class="w-32 h-32 mb-6 rounded-full" />
    <p>
      <strong> {{ user.name }}</strong>
    </p>
    <div class="mt-6 flex space-x-8 justify-around">
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
import { RouterLink } from "vue-router";
export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
  },

  props: {
    user: Object
  }
});
</script>

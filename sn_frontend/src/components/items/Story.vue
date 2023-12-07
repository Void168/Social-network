<template>
  <div class="relative min-h-max w-40 cursor-pointer rounded-lg">
    <img :src="userStore.user.avatar" alt="" class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 ring-blue-500">
    <img
      src="https://assets.catawiki.nl/assets/2017/10/29/1/8/4/184748d5-042b-4c98-ad28-1305006e9499.jpg"
      alt="story-image"
    />
  </div>
</template>

<script>
import { useUserStore } from '../../stores/user';

export default (await import("vue")).defineComponent({
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    }
})
</script>

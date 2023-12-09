<template>
  <div class="relative cursor-pointer rounded-lg group">
    <RouterLink to="/stories">
      <img
        :src="userStore.user.avatar"
        alt=""
        class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 ring-emerald-400 z-20"
      />
      <div
        class="relative h-[213px] flex items-center justify-center overflow-hidden shadow-sm rounded-lg cursor-pointer"
      >
        <div
          alt="story-image"
          class="h-full w-full group-hover:scale-105 group-hover:rounded-lg absolute z-10 bg-cover transition bg-[url('https://assets.catawiki.nl/assets/2017/10/29/1/8/4/184748d5-042b-4c98-ad28-1305006e9499.jpg')]"
        />
      </div>
    </RouterLink>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
});
</script>

<template>
  <div class="text-slate-900 dark:text-neutral-200 bg-white dark:bg-slate-600">
    <div class="relative group">
      <button
        class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
        v-on:click="openModal"
      ></button>
      <img :src="post.attachments[0].get_image" :class="path.includes('photos') ? 'h-48 cursor-pointer' : 'h-32 cursor-pointer'" />
    </div>
    <ImagePostModal
      :show="isOpen"
      @closeModal="closeModal"
      :imageId="post.id"
      v-bind:post="post"
    />
  </div>
</template>

<script>
import { RouterLink } from "vue-router";
import { useUserStore } from "../../../stores/user";
import ImagePostModal from "../../modals/chat/ImagePostModal.vue";
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
    post: Object,
  },
  data() {
    return {
      isOpen: false,
      image: {},
    };
  },

  methods: {
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
  components: { RouterLink, ImagePostModal },
});
</script>

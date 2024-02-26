<template>
  <div class="text-slate-900 dark:text-neutral-200">
    <div class="relative group">
      <button
        class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
        v-on:click="openModal"
      ></button>
      <img :src="post.attachments[0].get_image" :class="route.name === 'profiledetail' || route.name === 'pagedetail'  ? 'xl:h-32 lg:h-24 md:w-full sm:h-48 xm:h-32 xs:h-24 cursor-pointer' : 'md:h-48 sm:h-64 xm:h-56 xs:h-32 w-full cursor-pointer'" class="rounded-lg"
      />
    </div>
    <ImagePostModal
      :show="isOpen"
      @closeModal="closeModal"
      :imageId="post.id"
      :post="post"
    />
  </div>
</template>

<script>
import { RouterLink } from "vue-router";
import { useUserStore } from "../../../stores/user";
import ImagePostModal from "../../modals/post/ImagePostModal.vue";
import { useRoute } from "vue-router";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();
    const route = useRoute();

    return {
      userStore,
      route,
    };
  },
  props: {
    post: Object,
  },
  data() {
    return {
      isOpen: false,
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

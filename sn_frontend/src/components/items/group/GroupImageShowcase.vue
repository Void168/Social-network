<template>
  <div
    class="text-slate-900 dark:text-neutral-200 bg-white dark:bg-slate-600"
    :class="[
      index == 0 ? 'rounded-tl-md' : '',
      index == 1 ? 'rounded-tr-md' : '',
      index == 2 ? 'rounded-bl-md' : '',
      index == 3 ? 'rounded-br-md' : '',
    ]"
  >
    <div class="relative group">
      <button
        class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer transition"
        :class="[
          index == 0 ? 'rounded-tl-md' : '',
          index == 1 ? 'rounded-tr-md' : '',
          index == 2 ? 'rounded-bl-md' : '',
          index == 3 ? 'rounded-br-md' : '',
        ]"
        v-on:click="openModal"
      ></button>
      <img
        :src="groupPost.attachments[0].get_image"
        class="xl:h-32 lg:h-24 sm:h-48 xm:h-32 xs:h-24 cursor-pointer"
        :class="[
          index == 0 ? 'rounded-tl-md' : '',
          index == 1 ? 'rounded-tr-md' : '',
          index == 2 ? 'rounded-bl-md' : '',
          index == 3 ? 'rounded-br-md' : '',
        ]"
      />
    </div>
    <!-- <ImagePostModal
        :show="isOpen"
        @closeModal="closeModal"
        :imageId="post.id"
        :post="post"
      /> -->
  </div>
</template>

<script>
import { RouterLink } from "vue-router";
import { useUserStore } from "../../../stores/user";
import ImagePostModal from "../../modals/post/ImagePostModal.vue";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    groupPost: Object,
    index: Number,
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

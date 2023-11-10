<template>
  <div
    class=" text-slate-900 dark:text-neutral-200 bg-white dark:bg-slate-600"
  >
  <div class="relative group" >
    <!-- @click="getPost(post.id)" -->
  <button
        class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
        v-on:click="openModal"
      ></button>
      <img :src="post.attachments[0].get_image" class="h-32 cursor-pointer" />
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
import axios from "axios";
import { RouterLink } from "vue-router";
import { useUserStore } from "../stores/user";
import ImagePostModal from "./modals/ImagePostModal.vue";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    post: Object,
  },
  data() {
    return {
      isOpen: false,
      image: {}
    };
  },
  components: { RouterLink, ImagePostModal },
  // mounted() {
  //   this.getImages();
  // },

  methods: {
    // getImages() {
    //   axios
    //     .get(`/api/posts/profile/${this.$route.params.id}/attachments`)
    //     .then((res) => {
    //       this.images = res.data;
    //     })
    //     .catch((error) => {
    //       console.log("error", error);
    //     });
    // },
    // async getPost(id) {
    //   await axios
    //     .get(`/api/posts/${id}/`)
    //     .then((res) => {
    //       this.post = res.data.post;
    //     })
    //     .catch((error) => {
    //       console.log(error);
    //     });
    // },
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
});
</script>

<template>
  <div
    class="mt-4 p-4 text-slate-900 dark:text-neutral-200 bg-white dark:bg-slate-600"
  >
    <div class="flex justify-between items-center mb-4">
      <p class="font-bold text-2xl">Ảnh</p>
      <RouterLink :to="{ name: 'photos', params: { id: userStore.user.id } }">
        <p class="text-lg hover:underline cursor-pointer">Xem tất cả ảnh</p>
      </RouterLink>
    </div>

    <div class="grid grid-cols-3 gap-1">
      <div v-for="image in images" v-bind:key="image.id">
        <ImagePostModal
          :show="isOpen"
          @closeModal="closeModal"
          imageId="post.id"
          v-bind:post="post"
        />
        <div
          v-for="attachment in image.attachments"
          v-bind:key="attachment.id"
          class="col-span-1 relative group"
          @click="getImageId(image.id)"
        >
          <div
            class="absolute z-10 group-hover:bg-white/20 w-full h-full cursor-pointer rounded-md transition"
            @click="openModal"
          ></div>
          <img :src="attachment.get_image" class="h-28 cursor-pointer" />
        </div>
      </div>
    </div>
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
  data() {
    return {
      images: [],
      isOpen: false,
      post: {
        id: null,
      },
    };
  },
  components: { RouterLink, ImagePostModal },
  mounted() {
    this.getImages();
  },

  methods: {
    getImages() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/attachments`)
        .then((res) => {
          this.images = res.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    getImageId(id) {
      this.post.id = id;
      this.getPost();
    },
    getPost() {
      axios
        .get(`/api/posts/${this.post.id}/`)
        .then((res) => {
          this.post = res.data.post;
          console.log(this.post);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    closeModal() {
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
  },
});
</script>

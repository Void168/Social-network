<template>
  <div class="max-w-7xl mx-auto gap-4">
    <div
      class="bg-neutral-200 dark:bg-slate-600 p-4 rounded-md dark:text-neutral-200 w-full"
    >
      <p class="text-xl font-bold">Ảnh</p>
      <div class="grid grid-cols-6 gap-3 my-4">
        <div v-for="image in images" v-bind:key="image.id">
          <ImageShowcase v-bind:post="image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ImageShowcase from "../../components/items/profile/ImageShowcase.vue";

export default {
  components: {
    ImageShowcase,
  },
  data() {
    return {
        images: []
    }
  },

  mounted() {
    this.getImages()
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
  }
};
</script>

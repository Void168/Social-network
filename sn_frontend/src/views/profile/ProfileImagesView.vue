<template>
  <div class="max-w-7xl mx-auto gap-4">
    <div
      class="bg-white dark:bg-slate-600 p-4 dark:text-neutral-200 w-full rounded-lg my-4"
    >
      <p class="text-xl font-bold">Ảnh</p>
      <div class="grid lg:grid-cols-6 md:grid-cols-4 grid-cols-2 gap-3 my-4">
        <div v-for="image in images" v-bind:key="image.id">
          <Suspense>
            <ImageShowcase v-bind:post="image" />
            <template #fallback>
              <SkeletonLoadingContainer
                class="flex justify-center items-center w-full"
              />
            </template>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SkeletonLoadingContainer from "../../components/loadings/SkeletonLoadingContainer.vue";
import SkeletonShowcaseLoading from "../../components/loadings/SkeletonShowcaseLoading.vue";
import { defineAsyncComponent } from "vue";

const ImageShowcase = defineAsyncComponent({
  loader: () => import("../../components/items/profile/ImageShowcase.vue"),
  loadingComponent: SkeletonShowcaseLoading,
  delay: 500,
  timeout: 3000,
});

export default {
  name: "photos",
  components: {
    ImageShowcase,
    SkeletonLoadingContainer,
  },
  data() {
    return {
      images: [],
    };
  },

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
  },
};
</script>

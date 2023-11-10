<template>
  <div
    class="mt-4 p-4 text-slate-900 dark:text-neutral-200 bg-white dark:bg-slate-600"
  >
    <div class="flex justify-between items-center mb-4">
      <p class="font-bold text-2xl">Ảnh</p>
      <RouterLink :to="{name: 'photos', params: userStore.user.id}">
        <p class="text-lg hover:underline cursor-pointer">Xem tất cả ảnh</p>
      </RouterLink>
    </div>

    <div class="grid grid-cols-3 gap-1">
      <div v-for="image in images" v-bind:key="image.id">
        <div
          v-for="attachment in image.attachments"
          v-bind:key="attachment.id"
          class="col-span-1"
        >
          <img :src="attachment.get_image" class="h-28" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { RouterLink } from "vue-router";
import { useUserStore } from "../stores/user";

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
    };
  },
  components: { RouterLink },
  mounted() {
    this.getImages();
  },

  methods: {
    getImages() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/attachments`)
        .then((res) => {
          this.images = res.data;
          console.log(this.images);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
});
</script>

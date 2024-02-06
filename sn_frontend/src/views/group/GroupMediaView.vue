<template>
  <div class="w-[80%] mx-auto gap-4 my-6">
    <div
      class="bg-neutral-200 dark:bg-slate-700 p-4 rounded-md dark:text-neutral-200 w-full"
    >
      <p class="text-xl font-bold">Ảnh</p>
      <div class="grid grid-cols-6 gap-3 my-4">
        <div v-for="image in groupImages" :key="image.id">
          <GroupImageShowcase :groupPost="image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import GroupImageShowcase from "../../components/items/group/GroupImageShowcase.vue";

export default {
  components: {
    GroupImageShowcase,
  },
  data() {
    return {
        groupImages: [],
    };
  },

  mounted() {
    this.getGroupImage();
  },

  methods: {
    async getGroupImage() {
      await axios
        .get(`/api/posts/group/${this.$route.params.id}/attachments/`)
        .then((res) => {
          this.groupImages = res.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

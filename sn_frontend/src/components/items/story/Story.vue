<template>
  <div
    class="relative cursor-pointer rounded-lg group"
    @click="getUserStories(story.created_by.id)"
  >
    <img
      :src="story.created_by.get_avatar"
      alt=""
      class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 ring-emerald-400 z-20"
    />
    <div
      class="relative h-[213px] flex items-center justify-center overflow-hidden shadow-sm rounded-lg cursor-pointer"
    >
      <div
        alt="story-image"
        class="flex justify-center items-center h-full w-full group-hover:scale-105 group-hover:rounded-lg absolute z-10 bg-cover transition"
        :class="[selectedFont?.font, selectedTheme?.background]"
      >
        <span class="text-xs" :class="[selectedTheme?.textColor]">{{
          story?.body
        }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";

import axios from "axios";

import themes from "../../../data/themes";
import fonts from "../../../data/fonts";

export default (await import("vue")).defineComponent({
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();

    return {
      userStore,
      currentStoryStore,
    };
  },

  props: {
    story: Object,
  },

  data() {
    return {
      themes: themes,
      fonts: fonts,
    };
  },

  computed: {
    selectedTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.story?.theme
      )[0];
    },
    selectedFont() {
      return this.fonts?.filter((font) => font.name === this.story?.font)[0];
    },
  },

  methods: {
    getUserStories(userId) {
      axios
        .get(`/api/story/get-text-stories/${userId}`)
        .then((res) => {
          this.currentStoryStore.getCurrentUserStory(res.data.stories);
          // console.log(res.data)

          setTimeout(() => {
            this.$router.push("/stories");
          }, 200);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
});
</script>

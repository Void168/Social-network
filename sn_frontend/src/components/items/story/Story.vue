<template>
  <div class="relative cursor-pointer rounded-lg group">
    <RouterLink to="/stories">
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
          :class="[selectedFont.font, selectedTheme.background]"
        >
          <span class="text-xs" :class="[selectedTheme.textColor]">{{ story?.body }}</span>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { RouterLink } from "vue-router";
import themes from "../../../data/themes";
import fonts from "../../../data/fonts";
import { computed } from "vue";

export default (await import("vue")).defineComponent({
  components: {
    RouterLink,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
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
});
</script>

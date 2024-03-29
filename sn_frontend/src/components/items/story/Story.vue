<template>
  <div
    class="relative cursor-pointer rounded-lg group"
    @click="getUserStories(story.created_by.id)"
  >
    <div v-if="story?.body">
      <img
      loading="lazy"
        :src="story?.created_by?.get_avatar"
        alt=""
        class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 z-20"
        :class="haveSeen.length ? 'ring-slate-500' : 'ring-emerald-300'"
      />
      <div
        class="relative xs:h-[213px] h-[190px] flex items-center justify-center overflow-hidden shadow-sm rounded-lg cursor-pointer"
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
    <div v-if="story?.attachments">
      <img
      loading="lazy"
        :src="story?.created_by?.get_avatar"
        alt=""
        class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 z-20"
        :class="haveSeen.length ? 'ring-slate-500' : 'ring-emerald-300'"
      />
      <div
        class="relative xs:h-[213px] h-[190px] flex items-center justify-center overflow-hidden shadow-sm rounded-lg cursor-pointer"
      >
        <div
          alt="story-image"
          class="flex justify-center items-center h-full w-full group-hover:scale-105 group-hover:rounded-lg absolute z-10 bg-cover transition"
          :style="{ backgroundColor: story.theme }"
          :class="story?.attachments[0]?.get_video ? 'bg-black' : ''"
        >
          <img
          loading="lazy"
            v-if="story?.attachments[0]?.get_image"
            :src="story?.attachments[0]?.get_image"
            class="rounded-none"
            :class="[story?.attachments[0]?.rotate]"
            ref="image"
            :style="{ scale: story?.attachments[0]?.zoom_image }"
          />
          <video
            v-else
            muted
            class="rounded-none w-full shadow-none"
            ref="myVideo"
          >
            <source :src="story?.attachments[0]?.get_video" type="video/mp4" />
          </video>
        </div>
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
      dimensions: {
        width: 0,
        height: 0,
      },
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
    haveSeen() {
      return this.story?.seen_by?.filter(
        (user) => user.id === this.userStore.user.id
      );
    },
  },

  mounted() {
    this.getImagePixel();
  },

  methods: {
    getImagePixel() {
      let height = this.$refs.image?.clientHeight;
      this.dimensions.height = height;
    },
    getUserStories(userId) {
      this.currentStoryStore.resetCurrentStory();

      axios
        .get(`/api/story/get-text-stories/${userId}`)
        .then((res) => {
          this.currentStoryStore.getCurrentUserStory(res.data.stories);
          // console.log(res.data)
        })
        .catch((error) => {
          console.log("error", error);
        });

      axios
        .get(`/api/story/get-media-stories/${userId}`)
        .then((res) => {
          this.currentStoryStore.getCurrentUserStory(res.data.stories);
        })
        .catch((error) => {
          console.log("error", error);
        });

      setTimeout(() => {
        this.$router.push("/stories");
      }, 200);
    },
  },
});
</script>

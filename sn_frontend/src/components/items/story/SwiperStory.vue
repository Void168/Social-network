<template>
  <Swiper
    @swiper="onSwiper"
    class="detail-story h-full w-full"
    :class="selectedTheme?.background"
    :centeredSlides="true"
    :centerInsufficientSlides="true"
    :centeredSlidesBounds="true"
    :keyboard="true"
    :watchSlidesProgress="true"
    :space-between="0"
    :setWrapperSize="true"
    :simulate-touch="false"
    :speed="0"
    :autoplay="{
      stopOnLastSlide: true,
      disableOnInteraction: false,
    }"
    :pagination="{
      clickable: false,
      type: 'progressbar',
    }"
    :modules="modules"
    containerModifierClass="swiper-wrapper"
    progressbarFillClass="swiper-pagination-progressbar-fill"
    modifierClass="swiper-pagination"
    slideClass="swiper-slide"
  >
    <SwiperSlide
      :data-swiper-autoplay="duration?.toString()"
      v-for="story in stories"
      :key="story.id"
      class="overflow-hidden"
      ><div
        v-if="story.attachments"
        class="w-full h-full flex justify-center items-center"
        :style="{ backgroundColor: story?.theme }"
      >
        <img
          :src="story?.attachments[0]?.get_image"
          :style="{ scale: story?.attachments[0]?.zoom_image }"
          class="rounded-none w-full"
          :class="[story?.attachments[0]?.rotate]"
          alt="img-story"
        />
      </div>
      <div v-else class="w-full flex justify-center items-center">
        <span
          class="text-2xl"
          :class="[selectedFont?.font, selectedTheme?.textColor]"
        >
          {{ story.body }}
        </span>
      </div>
    </SwiperSlide>
    <SwiperStoryContainerButton
      @prev="$emit('prev')"
      @next="
        $emit('next');
        next();
      "
      :activeSlide="activeSlide"
    />
  </Swiper>
</template>

<script>
import axios from "axios";

import { Swiper, SwiperSlide } from "swiper/vue";
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";
import { Autoplay, Mousewheel, Keyboard, Pagination } from "swiper/modules";

import SwiperStoryContainerButton from "./SwiperStoryContainerButton.vue";
import "swiper/css/pagination";
import "swiper/css";

import themes from "../../../data/themes";
import fonts from "../../../data/fonts";

export default (await import("vue")).defineComponent({
  components: {
    Swiper,
    SwiperSlide,
    SwiperStoryContainerButton,
  },
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();
    return {
      userStore,
      currentStoryStore,
      modules: [Autoplay, Mousewheel, Keyboard, Pagination],
    };
  },
  props: {
    stories: Array,
    isPause: Boolean,
  },

  data() {
    return {
      percentage: 0,
      activeSlide: 0,
      themes: themes,
      fonts: fonts,
    };
  },

  computed: {
    selectedTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.stories[this.activeSlide]?.theme
      )[0];
    },
    selectedFont() {
      return this.fonts?.filter(
        (font) => font.name === this.stories[this.activeSlide]?.font
      )[0];
    },
    duration() {
      return this.stories[this.activeSlide]?.duaration * 1000;
    },
  },

  beforeMount() {
    this.onSwiper();
  },

  mounted() {
    this.doProgress();
  },

  updated() {
    this.updatedActiveSlide();
  },

  methods: {
    onSwiper(sw) {
      this.swiper = sw;
    },

    updatedActiveSlide() {
      this.activeSlide = this.swiper.realIndex;
    },

    doProgress() {
      const INTERVAL_TIME = (this.duration * 2) / 100;

      const progressbar = document.querySelectorAll(
        ".swiper-pagination-progressbar-fill"
      );

      const pagination = document.querySelectorAll(".swiper-pagination");
      for (let i = 1; i <= this.stories.length; i++) {
        const progressItem = document.createElement("span");
        pagination[0]?.appendChild(progressItem);
        progressItem.className = "progress-item";
      }

      const interval = setInterval(() => {
        if (this.percentage < 1 && this.currentStoryStore.activeStory) {
          this.activeSlide = this.swiper.realIndex;
          this.currentStoryStore.getActiveSlide(this.swiper.realIndex);
          this.percentage +=
            (this.duration * 2) / 1000 / 1000 / this.stories.length;
          progressbar[0]?.style?.setProperty(
            "transform",
            `scaleX(${this.percentage})`,
            "important"
          );

          // console.log(length)
        } else {
          this.percentage = 0;
          clearInterval(interval);
            // setTimeout(() => {
            //   this.$emit('next');
            // }, 100);
        }
      }, INTERVAL_TIME);
    },
    next() {
      if (this.stories.length > 0) {
        this.percentage =
          (this.currentStoryStore.activeSlide + 1) / this.stories.length;
      }
    },
  },
});
</script>

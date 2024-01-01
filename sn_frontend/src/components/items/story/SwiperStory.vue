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
      @prev="
        $emit('prev');
        prev();
      "
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
import { useRoute } from "vue-router";
import { reactive } from "vue";
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
    const story = reactive({
      nextIndex: 0,
      prevIndex: 0,
    });

    const route = useRoute();

    return {
      route,
      story,
      userStore,
      currentStoryStore,
      modules: [Autoplay, Mousewheel, Keyboard, Pagination],
    };
  },
  props: {
    stories: Array,
    isPause: Boolean,
    nextFunction: Function,
  },

  data() {
    return {
      percentage: 0,
      activeSlide: 0,
      themes: themes,
      fonts: fonts,
      isNext: false,
      isPrev: false,
      interval: null,
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
    currentStoryId() {
      return this.stories[this.currentStoryStore.activeSlide]?.id;
    },
  },

  created() {
    this.onSwiper();
  },

  mounted() {
    this.doProgress();
  },

  unmounted() {
    clearInterval(this.interval);
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

    getCurrentStoryId() {
      this.currentStoryStore.getActiveStoryId(this.currentStoryId);
    },

    async doProgress() {
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

      this.interval = setInterval(() => {
        if (this.percentage <= 1) {
          this.activeSlide = this.swiper.realIndex;
          this.currentStoryStore.getActiveSlide(this.swiper.realIndex);

          this.percentage +=
            (this.duration * 2) / 1000 / 1000 / this.stories.length;
          progressbar[0]?.style?.setProperty(
            "transform",
            `scaleX(${this.percentage})`,
            "important"
          );
        } else {
          this.percentage = 0;
          clearInterval(this.interval);
          if (this.isNext === false) {
            setTimeout(() => {
              this.nextFunction();
            }, 500);
          }
        }
      }, INTERVAL_TIME);
      if (this.isNext || this.isPrev) {
        clearInterval(this.interval);
      }
        if(this.stories[this.currentStoryStore.activeSlide].body){
          await axios
            .post(`/api/story/seen-text-story/${this.currentStoryId}/`)
            .then((res) => {
              if(res.data){
                console.log(res.data)
              }
            })
            .catch((error) => {
              console.log(error);
            });
        } else if(this.stories[this.currentStoryStore.activeSlide].attachments){
          await axios
            .post(`/api/story/seen-media-story/${this.currentStoryId}/`)
            .then((res) => {
              if(res.data){
                console.log(res.data)
              }
            })
            .catch((error) => {
              console.log(error);
            });
        }

    },
    next() {
      this.story.nextIndex = this.currentStoryStore.activeSlide + 1;

      if (this.stories.length > 0) {
        this.percentage =
          (this.currentStoryStore.activeSlide + 1) / this.stories.length;
      }
      if (
        (!this.stories.length &&
          this.story.nextIndex >
            this.currentStoryStore?.currentStory?.length - 1) ||
        (this.stories.length && this.story.nextIndex > this.stories?.length - 1)
      ) {
        this.isNext = true;
      } else {
        this.isNext = false;
      }
    },
    prev() {
      this.story.prevIndex = this.currentStoryStore.activeSlide;

      if (this.stories.length > 0) {
        this.percentage =
          (this.currentStoryStore.activeSlide - 1) / this.stories.length;
      }

      if (this.story.prevIndex < 0) {
        this.isPrev = true;
      } else {
        this.isPrev = false;
      }
    },
  },
});
</script>

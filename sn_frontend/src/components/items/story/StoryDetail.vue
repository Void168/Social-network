<template>
  <div class="flex items-center justify-center h-full">
    <div
      class="relative border-2 w-[35%] h-full rounded-lg flex items-center justify-center"
    >
      <div
        class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="userStore.user.avatar"
            alt=""
            class="rounded-full w-12 h-12"
          />
          <div class="flex gap-1 items-center">
            <span class="font-semibold text-lg">{{ userStore.user.name }}</span>
            <span>3 giờ</span>
            <GlobeAsiaAustraliaIcon class="w-5 h-5" />
          </div>
        </div>
        <div class="flex gap-2 items-center">
          <PauseIcon
            class="w-6 h-6 cursor-pointer"
            @click="pause"
            v-if="!isPause"
          />
          <PlayIcon class="w-6 h-6 cursor-pointer" @click="pause" v-else />
          <SpeakerWaveIcon
            class="w-6 h-6 cursor-pointer"
            @click="mute"
            v-if="!isMute"
          />
          <SpeakerXMarkIcon
            class="w-6 h-6 cursor-pointer"
            @click="mute"
            v-else
          />
          <EllipsisHorizontalIcon class="w-8 h-8 cursor-pointer" />
        </div>
      </div>
      <Swiper
        @swiper="onSwiper"
        class="detail-story h-full"
        :centeredSlides="true"
        :centerInsufficientSlides="true"
        :centeredSlidesBounds="true"
        :keyboard="true"
        :watchSlidesProgress="true"
        :space-between="0"
        :setWrapperSize="true"
        :autoplay="{
          stopOnLastSlide: true,
          disableOnInteraction: false,
        }"
        :pagination="{
          clickable: false,
        }"
        :modules="modules"
        containerModifierClass="swiper-wrapper"
        bulletActiveClass="swiper-pagination-bullet-active"
        bulletClass="swiper-pagination-bullet"
        modifierClass="swiper-pagination"
        slideClass="swiper-slide"
      >
        <SwiperSlide data-swiper-autoplay="3000"
          ><img
            :src="userStore.user.avatar"
            class="rounded-none"
            alt="img-story"
        /></SwiperSlide>
        <SwiperSlide data-swiper-autoplay="3000"
          ><img
            src="https://assets.catawiki.nl/assets/2017/10/29/1/8/4/184748d5-042b-4c98-ad28-1305006e9499.jpg"
            class="rounded-none"
            alt="img-story"
        /></SwiperSlide>
        <SwiperSlide data-swiper-autoplay="3000"
          ><img
            :src="userStore.user.avatar"
            class="rounded-none"
            alt="img-story"
        /></SwiperSlide>
        <SwiperStoryContainerButton
          @prev="prev"
          @next="next"
          :activeSlide="activeSlide"
        />
      </Swiper>
    </div>
  </div>
</template>

<script>
import { Swiper, SwiperSlide } from "swiper/vue";
import { useUserStore } from "../../../stores/user";
import { Autoplay, Mousewheel, Keyboard, Pagination } from "swiper/modules";
import {
  GlobeAsiaAustraliaIcon,
  PlayIcon,
  PauseIcon,
  EllipsisHorizontalIcon,
  SpeakerXMarkIcon,
  SpeakerWaveIcon,
} from "@heroicons/vue/24/solid";
import SwiperStoryContainerButton from "./SwiperStoryContainerButton.vue";

import "swiper/css/pagination";
import "swiper/css";

export default (await import("vue")).defineComponent({
  components: {
    Swiper,
    SwiperSlide,
    SwiperStoryContainerButton,
    GlobeAsiaAustraliaIcon,
    PlayIcon,
    PauseIcon,
    EllipsisHorizontalIcon,
    SpeakerXMarkIcon,
    SpeakerWaveIcon,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
      modules: [Autoplay, Mousewheel, Keyboard, Pagination],
    };
  },

  data() {
    return {
      isPause: false,
      isMute: false,
      isNext: false,
      isPrev: false,
      activeSlide: 0,
      percentage: 0,
    };
  },

  watch: {
    isPause(newVal, oldVal) {
      if (newVal) {
        this.doProgress();
      }
    },
    isNext(newVal, oldVal) {
      return newVal;
    },
  },

  mounted() {
    this.doProgress();
  },

  updated() {
    this.onSwiper()
  },

  methods: {
    onSwiper(sw) {
      this.swiper = sw;
    },
    doProgress() {
      const bulletList = document.querySelectorAll(".swiper-pagination-bullet");
      bulletList.forEach((bullet) => {
        const progress = document.createElement("span");
        bullet.appendChild(progress);
        progress.className = "progress";
      });

      const progressList = document.querySelectorAll(".progress");
      for (let i = this.swiper.activeIndex; i < progressList.length; i++) {
        const timeout = () => {
          setTimeout(() => {
            let interval = setInterval(() => {
              if (!this.isPause) {
                if (
                  this.percentage <= 100 &&
                  this.swiper.activeIndex < progressList.length || this.swiper.activeIndex === 0
                ) {
                  this.percentage += 2;
                  progressList[i].style.width = `${this.percentage}%`;
                  this.activeSlide = this.swiper.activeIndex;
                  // console.log(this.percentage);
                } else {
                  this.percentage = 0;
                  clearInterval(interval);
                }
              }
            }, 60);
            if(this.isPrev){
              this.percentage = 0;
              clearInterval(interval);
            }
          }, 3200 * i);
        };
        if (this.isPause) {
          clearTimeout(timeout);
        } else {
          timeout();
        }
      }
    },
    next() {
      this.isNext = true;
      // console.log(this.swiper.activeIndex)
      const progressList = document.querySelectorAll(".progress");
      // this.percentage = 100;
      if (this.swiper.activeIndex < progressList.length - 1) {
        if (this.swiper.activeIndex < progressList.length) {
          progressList[this.swiper.activeIndex].style.width = "100%";
        }
      } else {
        this.getNewUserStories();
      }
    },
    prev() {
      this.isPrev = true;
      const progressList = document.querySelectorAll(".progress");
      console.log(this.swiper.activeIndex)
      if (this.swiper.activeIndex >= 0) {
        // this.percentage = 0;
        if (this.swiper.activeIndex < progressList.length) {
          // progressList[
          //   this.swiper.activeIndex - 1
          // ].style.width = `${this.percentage}%`;
          progressList[this.swiper.activeIndex].style.width = "0%";
          // this.doProgress();
        }
      } else {
        this.getNewUserStories();
      }
      setTimeout(() => {
        this.isPrev = false;
      }, 100);
    },

    pause() {
      this.isPause = !this.isPause;
      if (this.isPause) {
        this.swiper.autoplay.pause();
        console.log(this.swiper);
      } else {
        this.swiper.autoplay.resume();
      }
    },
    mute() {
      this.isMute = !this.isMute;
      console.log(this.isMute);
    },

    getNewUserStories() {
      const progressList = document.querySelectorAll(".progress");
      if (progressList.length - 1 === this.swiper.activeIndex) {
        console.log("load new user's stories");
        console.log(this.swiper.activeIndex);
        this.swiper.activeIndex = 0;
        this.percentage = 0;
        for (let i = 0; i < progressList.length; i++) {
          progressList[i].style.width = `${this.percentage}%`;
        }
        this.doProgress();
      } else {
        console.log("hello");
      }
    },
  },
});
</script>

<style>
.swiper-pagination-bullet {
  background-color: rgb(255, 255, 255);
}
</style>

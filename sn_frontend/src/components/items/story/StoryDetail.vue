<template>
  <div class="flex items-center justify-center h-full">
    <div
      class="relative border-2 w-[35%] h-full rounded-lg flex items-center justify-center"
    >
      <div
        v-if="isYourStory && !isFirstStory && !isOtherStory"
        class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
        :class="selectedYourStoryTheme?.textColor"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="yourStory[0]?.created_by?.get_avatar"
            alt=""
            class="rounded-full w-12 h-12"
          />
          <div class="flex gap-1 items-center">
            <span class="font-semibold text-lg">{{
              yourStory[0]?.created_by?.name
            }}</span>
            <span class="font-medium">{{
              yourStory[0]?.created_at_formatted
            }}</span>
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
          <StoryDropdown @openModal="openModal" :yourStory="yourStory[0]" />
          <DeleteStoryModalVue
            :show="isOpen"
            @closeModal="closeModal"
            @deleteStory="deleteStory"
          />
        </div>
      </div>
      <div
        v-else-if="
          isOtherStory &&
          isFirstStory &&
          !isYourStory &&
          !nextStories.length &&
          !prevStories.length &&
          !isNext &&
          currentStoryStore.activeStory
        "
        class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
        :class="selectedTheme?.textColor"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="currentStoryStore.currentStory[0]?.created_by?.get_avatar"
            alt=""
            class="rounded-full w-12 h-12"
          />
          <div class="flex gap-1 items-center">
            <span class="font-semibold text-lg">{{
              currentStoryStore.currentStory[0]?.created_by?.name
            }}</span>
            <span class="font-medium">{{
              currentStoryStore.currentStory[activeSlide]?.created_at_formatted
            }}</span>
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
          <StoryDropdown
            @openModal="openModal"
            :yourStory="currentStoryStore.currentStory[0]"
          />
          <DeleteStoryModalVue
            :show="isOpen"
            @closeModal="closeModal"
            @deleteStory="deleteStory(currentStoryStore.currentStory)"
          />
        </div>
      </div>
      <div
        v-else-if="nextStories.length > 0"
        class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
        :class="selectedNextStoryTheme?.textColor"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="nextStories[0]?.created_by?.get_avatar"
            alt=""
            class="rounded-full w-12 h-12"
          />
          <div class="flex gap-1 items-center">
            <span class="font-semibold text-lg">{{
              nextStories[0]?.created_by?.name
            }}</span>
            <span class="font-medium">{{
              nextStories[activeSlide]?.created_at_formatted
            }}</span>
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
          <StoryDropdown @openModal="openModal" :yourStory="nextStories[0]" />
          <DeleteStoryModalVue
            :show="isOpen"
            @closeModal="closeModal"
            @deleteStory="deleteStory(currentStoryStore.currentStory)"
          />
        </div>
      </div>
      <div
        v-else-if="prevStories.length > 0"
        class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
        :class="selectedPrevStoryTheme?.textColor"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="prevStories[0]?.created_by?.get_avatar"
            alt=""
            class="rounded-full w-12 h-12"
          />
          <div class="flex gap-1 items-center">
            <span class="font-semibold text-lg">{{
              prevStories[0]?.created_by?.name
            }}</span>
            <span class="font-medium">{{
              prevStories[activeSlide]?.created_at_formatted
            }}</span>
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
          <StoryDropdown @openModal="openModal" :yourStory="prevStories[0]" />
          <DeleteStoryModalVue
            :show="isOpen"
            @closeModal="closeModal"
            @deleteStory="deleteStory(currentStoryStore.currentStory)"
          />
        </div>
      </div>
      <div
        v-else-if="!isYourStory && !isFirstStory && isOtherStory"
        class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
        :class="selectedOtherStoryTheme?.textColor"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="userStories[0]?.created_by?.get_avatar"
            alt=""
            class="rounded-full w-12 h-12"
          />
          <div class="flex gap-1 items-center">
            <span class="font-semibold text-lg">{{
              userStories[0]?.created_by?.name
            }}</span>
            <span class="font-medium">{{
              userStories[0]?.created_at_formatted
            }}</span>
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
          <StoryDropdown @openModal="openModal" :yourStory="userStories[0]" />
          <DeleteStoryModalVue
            :show="isOpen"
            @closeModal="closeModal"
            @deleteStory="deleteStory"
          />
        </div>
      </div>
      <Swiper
        v-if="isYourStory && !isFirstStory && !isOtherStory"
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedYourStoryTheme?.background]"
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
          :data-swiper-autoplay="duration.toString()"
          v-for="story in yourStory"
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
              :class="[
                selectedYourStoryFont?.font,
                selectedYourStoryTheme?.textColor,
              ]"
            >
              {{ story.body }}
            </span>
          </div>
        </SwiperSlide>
        <SwiperStoryContainerButton
          @prev="prev"
          @next="next"
          :activeSlide="activeSlide"
        />
      </Swiper>
      <Swiper
        v-else-if="
          isOtherStory &&
          isFirstStory &&
          !isYourStory &&
          !nextStories.length &&
          !prevStories.length &&
          !isNext &&
          currentStoryStore.activeStory
        "
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedTheme?.background]"
        :centeredSlides="true"
        :centerInsufficientSlides="true"
        :centeredSlidesBounds="true"
        :simulate-touch="false"
        :keyboard="true"
        :watchSlidesProgress="true"
        :space-between="0"
        :speed="0"
        :setWrapperSize="true"
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
          :data-swiper-autoplay="duration.toString()"
          v-for="story in currentStoryStore?.currentStory"
          :key="story.id"
          class="overflow-hidden"
        >
          <div
            v-if="story.attachments"
            class="w-full h-full flex justify-center items-center"
            :style="{ backgroundColor: story?.theme }"
          >
            <img
              :src="story?.attachments[0]?.get_image"
              class="rounded-none w-full"
              :class="[story?.attachments[0]?.rotate]"
              :style="{ scale: story?.attachments[0]?.zoom_image }"
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
          @prev="prev"
          @next="next"
          :activeSlide="activeSlide"
        />
      </Swiper>
      <Swiper
        v-else-if="nextStories.length && !prevStories.length"
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedNextStoryTheme?.background]"
        :centeredSlides="true"
        :centerInsufficientSlides="true"
        :centeredSlidesBounds="true"
        :keyboard="true"
        :watchSlidesProgress="true"
        :space-between="0"
        :speed="0"
        :setWrapperSize="true"
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
          :data-swiper-autoplay="duration.toString()"
          v-for="story in nextStories"
          :key="story.id"
          class="overflow-hidden"
        >
          <div
            v-if="story.attachments"
            class="w-full h-full flex justify-center items-center"
            :style="{ backgroundColor: story?.theme }"
          >
            <img
              :src="story.attachments[0].get_image"
              class="rounded-none w-full"
              :class="[story.attachments[0].rotate]"
              :style="{ scale: story.attachments[0]?.zoom_image }"
              alt="img-story"
            />
          </div>
          <div v-else class="w-full flex justify-center items-center">
            <span
              class="text-2xl"
              :class="[
                selectedNextStoryFont?.font,
                selectedNextStoryTheme?.textColor,
              ]"
            >
              {{ story.body }}
            </span>
          </div>
        </SwiperSlide>
        <SwiperStoryContainerButton
          @prev="prev"
          @next="next"
          :activeSlide="activeSlide"
        />
      </Swiper>
      <Swiper
        v-else-if="prevStories.length && !nextStories.length"
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedPrevStoryTheme?.background]"
        :centeredSlides="true"
        :centerInsufficientSlides="true"
        :centeredSlidesBounds="true"
        :keyboard="true"
        :watchSlidesProgress="true"
        :simulate-touch="false"
        :space-between="0"
        :speed="0"
        :setWrapperSize="true"
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
          :data-swiper-autoplay="duration.toString()"
          v-for="story in prevStories"
          :key="story.id"
          class="overflow-hidden"
        >
          <div
            v-if="story?.attachments"
            class="w-full h-full flex justify-center items-center"
            :style="{ backgroundColor: story?.theme }"
          >
            <img
              :src="story?.attachments[0]?.get_image"
              class="rounded-none w-full"
              :class="[story?.attachments[0]?.rotate]"
              :style="{ scale: story?.attachments[0]?.zoom_image }"
              alt="img-story"
            />
          </div>
          <div v-else class="w-full flex justify-center items-center">
            <span
              class="text-2xl"
              :class="[
                selectedPrevStoryFont?.font,
                selectedPrevStoryTheme?.textColor,
              ]"
            >
              {{ story?.body }}
            </span>
          </div>
        </SwiperSlide>
        <SwiperStoryContainerButton
          @prev="prev"
          @next="next"
          :activeSlide="activeSlide"
        />
      </Swiper>
      <Swiper
        v-else-if="isOtherStory && !isFirstStory && !isYourStory"
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedOtherStoryTheme?.background]"
        :centeredSlides="true"
        :centerInsufficientSlides="true"
        :centeredSlidesBounds="true"
        :keyboard="true"
        :watchSlidesProgress="true"
        :simulate-touch="false"
        :space-between="0"
        :speed="0"
        :setWrapperSize="true"
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
          :data-swiper-autoplay="otherStoryDuration.toString()"
          v-for="story in userStories"
          :key="story.id"
          ><div
            v-if="story.attachments"
            class="w-full h-full flex justify-center items-center"
            :style="{ backgroundColor: story?.theme }"
            :class="[story?.attachments[0]?.rotate]"
          >
            <img
              :src="story?.attachments[0]?.get_image"
              :style="{ scale: story?.attachments[0]?.zoom_image }"
              class="rounded-none w-full"
              alt="img-story"
            />
          </div>
          <div
            v-else
            class="w-full h-full flex justify-center items-center"
            :class="[selectedOtherStoryTheme?.background]"
          >
            <span
              class="text-2xl"
              :class="[
                selectedOtherStoryFont?.font,
                selectedOtherStoryTheme?.textColor,
              ]"
            >
              {{ story.body }}
            </span>
          </div>
        </SwiperSlide>
        <SwiperStoryContainerButton
          @prev="prev"
          @next="next"
          :activeSlide="activeSlide"
        />
      </Swiper>
      <div
        class="text-white text-xl"
        v-else-if="!nextStories.length && !userStories.length"
      >
        <p>Đã xem hết tin</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { reactive } from "vue";

import { Swiper, SwiperSlide } from "swiper/vue";
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";
import { useToastStore } from "../../../stores/toast";
import { Autoplay, Mousewheel, Keyboard, Pagination } from "swiper/modules";
import StoryDropdown from "../../dropdown/StoryDropdown.vue";
import DeleteStoryModalVue from "../../modals/story/DeleteStoryModal.vue";

import {
  GlobeAsiaAustraliaIcon,
  PlayIcon,
  PauseIcon,
  SpeakerXMarkIcon,
  SpeakerWaveIcon,
} from "@heroicons/vue/24/solid";
import SwiperStoryContainerButton from "./SwiperStoryContainerButton.vue";

import "swiper/css/pagination";
import "swiper/css";
import themes from "../../../data/themes";
import fonts from "../../../data/fonts";

export default (await import("vue")).defineComponent({
  components: {
    Swiper,
    SwiperSlide,
    StoryDropdown,
    DeleteStoryModalVue,
    SwiperStoryContainerButton,
    GlobeAsiaAustraliaIcon,
    PlayIcon,
    PauseIcon,
    SpeakerXMarkIcon,
    SpeakerWaveIcon,
  },
  props: {
    isOtherStory: Boolean,
    userStories: Array,
    isYourStory: Boolean,
    yourStory: Object,
    isFirstStory: Boolean,
  },
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();
    const toastStore = useToastStore();
    const story = reactive({
      nextIndex: 0,
      prevIndex: 0,
    });
    return {
      story,
      userStore,
      currentStoryStore,
      toastStore,
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
      themes: themes,
      fonts: fonts,
      isOpen: false,
      nextStories: [],
      prevStories: [],
      index: 0,
    };
  },

  watch: {
    isNext: {
      handler(newVal) {
        return newVal;
      },
    },
    isPause: {
      handler(newVal) {
        return newVal;
      },
    },
  },

  computed: {
    selectedYourStoryTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.yourStory[this.activeSlide]?.theme
      )[0];
    },
    selectedYourStoryFont() {
      return this.fonts?.filter(
        (font) => font.name === this.yourStory[this.activeSlide]?.font
      )[0];
    },
    selectedNextStoryTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.nextStories[this.activeSlide]?.theme
      )[0];
    },
    selectedNextStoryFont() {
      return this.fonts?.filter(
        (font) => font.name === this.nextStories[this.activeSlide]?.font
      )[0];
    },
    selectedPrevStoryTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.prevStories[this.activeSlide]?.theme
      )[0];
    },
    selectedPrevStoryFont() {
      return this.fonts?.filter(
        (font) => font.name === this.prevStories[this.activeSlide]?.font
      )[0];
    },
    selectedTheme() {
      return this.themes?.filter(
        (theme) =>
          theme.name ===
          this.currentStoryStore?.currentStory[this.activeSlide]?.theme
      )[0];
    },
    selectedFont() {
      return this.fonts?.filter(
        (font) =>
          font.name ===
          this.currentStoryStore?.currentStory[this.activeSlide]?.font
      )[0];
    },
    duration() {
      if (this.isOtherStory && this.isFirstStory && !this.isYourStory) {
        return (
          this.currentStoryStore?.currentStory[this.activeSlide]?.duaration *
          1000
        );
      }
      if (this.userStories.length > 0) {
        return this.userStories[this.activeSlide]?.duaration * 1000;
      }
      if (this.yourStory.length > 0) {
        return this.yourStory[this.activeSlide]?.duaration * 1000;
      }
      if (this.nextStories.length > 0) {
        return this.nextStories[this.activeSlide]?.duaration * 1000;
      }
      if (this.prevStories.length > 0) {
        return this.prevStories[this.activeSlide]?.duaration * 1000;
      }
    },
    selectedOtherStoryTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.userStories[this.activeSlide]?.theme
      )[0];
    },
    selectedOtherStoryFont() {
      return this.fonts?.filter(
        (font) => font.name === this.userStories[this.activeSlide]?.font
      )[0];
    },
    otherStoryDuration() {
      return this.userStories[this.activeSlide]?.duaration * 1000;
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
      let length = 0;

      if (
        this.currentStoryStore.currentStory.length &&
        !this.isNext &&
        !this.isPrev
      ) {
        length = this.currentStoryStore.currentStory.length;
      } else if (this.yourStory.length && !this.isNext && !this.isPrev) {
        length = this.yourStory.length;
      } else if (this.nextStories.length && this.isNext) {
        length = this.nextStories.length;
      } else if (this.prevStories.length && this.isPrev) {
        length = this.prevStories.length;
      } else if (this.userStories.length && !this.isNext && !this.isPrev) {
        length = this.userStories.length;
      }

      const progressbar = document.querySelectorAll(
        ".swiper-pagination-progressbar-fill"
      );

      const pagination = document.querySelectorAll(".swiper-pagination");
      for (let i = 1; i <= length; i++) {
        const progressItem = document.createElement("span");
        pagination[0]?.appendChild(progressItem);
        progressItem.className = "progress-item";
      }

      const interval = setInterval(() => {
        if (
          this.percentage < 1 &&
          !this.isPause &&
          this.currentStoryStore.activeStory
        ) {
          this.activeSlide = this.swiper?.realIndex;
          this.percentage += (this.duration * 2) / 1000 / 1000 / length;

          progressbar[0]?.style?.setProperty(
            "transform",
            `scaleX(${this.percentage})`
          );

          // console.log(length)
        } else {
          this.percentage = 0;

          setTimeout(() => {
            this.next();
            if (!this.currentStoryStore.activeStory) {
              clearInterval(interval);
            }
          }, (this.duration + 100) * this.swiper.realIndex);
        }
      }, (this.duration * 2) / 100);
    },
    async next() {
      if (this.yourStory.length > 0 && !this.nextStories.length) {
        this.percentage = (this.activeSlide + 1) / this.yourStory.length;
      }
      if (this.nextStories.length > 0) {
        this.percentage = (this.activeSlide + 1) / this.nextStories.length;
      }
      if (this.prevStories.length > 0) {
        this.percentage = (this.activeSlide + 1) / this.prevStories.length;
      }
      if (this.userStories.length > 0 && !this.nextStories.length) {
        this.percentage = (this.activeSlide + 1) / this.userStories.length;
      }
      if (
        this.currentStoryStore.currentStory.length > 0 &&
        !this.nextStories.length
      ) {
        this.percentage =
          (this.activeSlide + 1) / this.currentStoryStore.currentStory.length;
      }

      this.$emit("next");
      this.isPause = false;
      this.story.nextIndex = this.swiper.realIndex + 1;

      if (
        (!this.nextStories.length &&
          this.story.nextIndex >
            this.currentStoryStore?.currentStory?.length - 1) ||
        (this.nextStories.length &&
          this.story.nextIndex > this.nextStories?.length - 1)
      ) {
        this.isNext = true;
      } else {
        this.isNext = false;
      }

      if (this.isNext) {
        this.isPrev = false;
        this.percentage = 0;
        this.nextStories = [];
        this.prevStories = [];
        this.index++;

        this.isNext = true;
        // console.log(this.nextStories);
        await axios
          .get(
            `/api/story/get-text-stories/${
              this.currentStoryStore.listId[
                this.currentStoryStore.currentStory[0].created_by.id ===
                this.userStore.user.id
                  ? this.index
                  : this.index + 1
              ]
            }/`
          )
          .then((res) => {
            if (res.data.stories.length) {
              res.data.stories.forEach((story) => {
                this.nextStories.unshift(story);
              });
            }
          })
          .catch((error) => {
            console.log(error);
          });

        await axios
          .get(
            `/api/story/get-media-stories/${
              this.currentStoryStore.listId[
                this.currentStoryStore.currentStory[0].created_by.id ===
                this.userStore.user.id
                  ? this.index
                  : this.index + 1
              ]
            }/`
          )
          .then((res) => {
            if (res.data.stories.length) {
              res.data.stories.forEach((story) => {
                this.nextStories.unshift(story);
              });
            }

            this.nextStories.sort(
              (a, b) => new Date(a.created_at) - new Date(b.created_at)
            );
          })
          .catch((error) => {
            console.log(error);
          });
        this.currentStoryStore.resetActiveStory();
        this.currentStoryStore.getActiveStory(
          this.nextStories[0]?.created_by?.id
        );
      }
    },
    async prev() {
      if (this.yourStory.length > 0) {
        this.percentage = (this.activeSlide - 1) / this.yourStory.length;
      }
      if (this.nextStories.length > 0) {
        this.percentage = (this.activeSlide - 1) / this.nextStories.length;
      }
      if (this.prevStories.length > 0) {
        this.percentage = (this.activeSlide - 1) / this.prevStories.length;
      }
      if (this.userStories.length > 0) {
        this.percentage = (this.activeSlide - 1) / this.userStories.length;
      }
      if (this.currentStoryStore.currentStory.length > 0) {
        this.percentage =
          (this.activeSlide - 1) / this.currentStoryStore.currentStory.length;
      }
      this.$emit("prev");
      this.isPause = false;
      this.story.prevIndex = this.swiper.realIndex;
      this.story.prevIndex--;

      if (this.story.prevIndex < 0) {
        this.isPrev = true;
      } else {
        this.isPrev = false;
      }
      console.log(this.story.prevIndex);

      if (this.isPrev) {
        this.isNext = false;
        this.prevStories = [];
        this.nextStories = [];
        console.log(this.index);
        await axios
          .get(
            `/api/story/get-text-stories/${
              this.currentStoryStore.listId[this.index - 1]
            }/`
          )
          .then((res) => {
            if (res.data.stories.length) {
              res.data.stories.forEach((story) => {
                this.prevStories.unshift(story);
              });
            }
          })
          .catch((error) => {
            console.log(error);
          });

        await axios
          .get(
            `/api/story/get-media-stories/${
              this.currentStoryStore.listId[this.index - 1]
            }/`
          )
          .then((res) => {
            if (res.data.stories.length) {
              res.data.stories.forEach((story) => {
                this.prevStories.unshift(story);
              });
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
      console.log(this.prevStories);
    },

    pause() {
      this.isPause = !this.isPause;
      console.log(this.isPause);
      if (this.isPause) {
        this.swiper.autoplay.pause();
      } else {
        this.swiper.autoplay.resume();
      }
    },
    mute() {
      this.isMute = !this.isMute;
      console.log(this.isMute);
    },

    openModal() {
      this.$emit("openModal", this.isOpen);
      this.isOpen = true;

      this.pause();
    },
    closeModal() {
      this.isOpen = false;
    },
    deleteStory(yourStory) {
      if (yourStory[0].body) {
        axios
          .delete(
            `/api/story/text-story/${
              yourStory[this.swiper.realIndex].id
            }/delete/`
          )
          .then((res) => {
            if (res.data.message === "text story deleted") {
              setTimeout(() => {
                this.closeModal();
              }, 1000);
              this.toastStore.showToast(
                3000,
                "Tin đã được xóa",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(-1);
              }, 3500);
            } else {
              this.toastStore.showToast(
                3000,
                "Xóa tin thất bại",
                "bg-rose-500 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        axios
          .delete(
            `/api/story/media-story/${
              yourStory[this.swiper.realIndex].id
            }/delete/`
          )
          .then((res) => {
            if (res.data.message === "text media deleted") {
              setTimeout(() => {
                this.closeModal();
              }, 1000);
              this.toastStore.showToast(
                3000,
                "Tin đã được xóa",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(-1);
              }, 3500);
            } else {
              this.toastStore.showToast(
                3000,
                "Xóa tin thất bại",
                "bg-rose-500 text-white"
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
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

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
            <span class="font-medium">{{ yourStory[0]?.created_at_formatted }}</span>
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
        v-else-if="!isYourStory && isFirstStory && isOtherStory"
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
            <span class="font-medium">{{ userStories[0]?.created_at_formatted }}</span>
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
        <SwiperSlide
          :data-swiper-autoplay="duration.toString()"
          v-for="story in yourStory"
          :key="story.id"
          class="overflow-hidden"
          ><div
            v-if="story.attachments"
            class="w-full h-full flex justify-center items-center"
            :style="{ backgroundColor: story?.theme }"
            :class="[story?.attachments[0]?.rotate]"
          >
            <img
              :src="userStore.user.avatar"
              :style="{scale: story?.attachments[0]?.zoom_image}"
              class="rounded-none"
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
        v-else-if="isOtherStory && isFirstStory && !isYourStory"
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedTheme?.background]"
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
        <SwiperSlide
          :data-swiper-autoplay="duration.toString()"
          v-for="story in currentStoryStore.currentStory"
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
              class="rounded-none"
              :class="[story.attachments[0].rotate]"
              :style="{ scale: story.attachments[0]?.zoom_image }"
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
        v-else-if="isOtherStory && !isFirstStory && !isYourStory"
        @swiper="onSwiper"
        class="detail-story h-full w-full"
        :class="[selectedOtherStoryTheme?.background]"
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
              :style="{scale: story?.attachments[0]?.zoom_image}"
              class="rounded-none"
              alt="img-story"
            />
          </div>
          <div v-else class="w-full h-full flex justify-center items-center" :class="[
                selectedOtherStoryTheme?.background,
              ]">
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
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
    return {
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
      if (this.isOtherStory && !this.isFirstStory && !this.isYourStory) {
        return this.userStories[this.activeSlide]?.duaration * 1000;
      }
      if (!this.isOtherStory && !this.isFirstStory && this.isYourStory) {
        return this.yourStory[this.activeSlide]?.duaration * 1000;
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
                  this.percentage < 100 &&
                  this.swiper.activeIndex < progressList.length
                ) {
                  this.percentage += 2;
                  progressList[i].style.width = `${this.percentage}%`;
                  this.activeSlide = this.swiper.activeIndex;
                } else {
                  this.percentage = 0;
                  clearInterval(interval);
                }
              }
            }, (this.duration * 2) / 100);
            // if (this.isPrev) {
            //   this.percentage = 0;
            //   clearInterval(interval);
            // }
          }, (this.duration + this.duration / 100) * i);
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
      console.log(this.swiper.activeIndex);
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

    openModal() {
      this.$emit("openModal", this.isOpen);
      this.isOpen = true;

      this.pause();
    },
    closeModal() {
      this.isOpen = false;
    },
    deleteStory(yourStory) {
      axios
        .delete(
          `/api/story/text-story/${
            yourStory[this.swiper.activeIndex].id
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
    },
  },
});
</script>

<style>
.swiper-pagination-bullet {
  background-color: rgb(255, 255, 255);
}
</style>

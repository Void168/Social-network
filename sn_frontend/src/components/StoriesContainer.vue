<template>
  <div>
    <Swiper
      :simulateTouch="false"
      :breakpoints="{
        '0': {
          slidesPerView: 2,
          spaceBetween: 10,
        },
        '320': {
          slidesPerView: 2,
          spaceBetween: 10,
        },
        '440': {
          slidesPerView: 3,
          spaceBetween: 20,
        },
        '640': {
          slidesPerView: 2,
          spaceBetween: 10,
        },
        '770': {
          slidesPerView: 3,
          spaceBetween: 20,
        },
        '1280': {
          slidesPerView: 4,
          spaceBetween: 20,
        },
        '1536': {
          slidesPerView: 5,
          spaceBetween: 20,
        },
      }"
    >
      <SwiperSlide
        ><div
          class="relative cursor-pointer dark:bg-slate-700 bg-slate-300 rounded-lg xs:h-[213px] h-[190px]"
          @click="openModal"
        >
          <img
            loading="lazy"
            :src="pageStore.pageId ? pageStore.pageActive.get_avatar : userStore.user.avatar"
            class="rounded-b-none h-[70%] w-full rounded-t-lg"
            alt="create-story"
          />
          <div class="flex justify-center items-center relative h-[30%]">
            <span class="absolute top-[-25%]">
              <PlusCircleIcon
                class="w-10 h-10 text-blue-500 rounded-full dark:bg-slate-700 bg-slate-300 p-1"
              />
            </span>
            <p class="font-semibold">Tạo tin</p>
          </div>
        </div></SwiperSlide
      >
      <SwiperSlide v-if="yourLastStory">
        <SkeletonLoadingStoryVue v-if="isLoading" />
        <div
          v-else
          class="relative cursor-pointer rounded-lg group"
          @click="getUserStories(yourLastStory?.created_by?.id)"
        >
          <img
          loading="lazy"
            :src="userStore.user.avatar"
            alt=""
            class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 ring-emerald-300 z-20"
          />
          <div
            class="relative xs:h-[213px] h-[190px] flex items-center justify-center overflow-hidden shadow-sm rounded-lg cursor-pointer"
          >
            <div
              alt="story-image"
              class="h-full w-full group-hover:scale-105 group-hover:rounded-lg absolute z-10 bg-cover transition flex items-center justify-center"
              :class="[selectedTheme?.background, selectedFont?.font]"
              v-if="yourLastStory?.body"
            >
              <span class="text-xs" :class="[selectedTheme?.textColor]">{{
                yourLastStory?.body
              }}</span>
            </div>
            <div
              v-else
              alt="story-image"
              class="h-full w-full group-hover:scale-105 group-hover:rounded-lg absolute z-10 bg-cover transition flex items-center justify-center"
              :style="{ backgroundColor: yourLastStory?.theme }"
              :class="
                yourLastStory?.attachments[0]?.get_video ? 'bg-black' : ''
              "
            >
              <img
              loading="lazy"
                v-if="yourLastStory?.attachments[0]?.get_image"
                :src="yourLastStory?.attachments[0]?.get_image"
                :class="[yourLastStory?.attachments[0]?.rotate]"
                :style="{ scale: yourLastStory?.attachments[0]?.zoom_image }"
                class="rounded-none"
                ref="image"
              />
              <video
                v-else
                muted
                class="rounded-none w-full shadow-none"
                ref="myVideo"
              >
                <source
                  :src="yourLastStory?.attachments[0]?.get_video"
                  type="video/mp4"
                />
              </video>
            </div>
          </div>
        </div>
      </SwiperSlide>
      <!-- <SwiperSlide>
        <SkeletonLoadingStoryVue />
      </SwiperSlide> -->
      <SwiperSlide
        v-for="story in setStory"
        :key="story.id"
        @click="getUserStories(story[0]?.created_by?.id)"
      >
        <SkeletonLoadingStoryVue v-if="isLoading" />
        <Story
          v-else
          :story="
            story.filter(
              (st) =>
                !st?.seen_by?.map((user) => user.id).includes(userStore.user.id)
            ).length
              ? story
                  .filter(
                    (st) =>
                      !st?.seen_by
                        ?.map((user) => user.id)
                        .includes(userStore.user.id)
                  )
                  .sort(
                    (a, b) => new Date(a.created_at) - new Date(b.created_at)
                  )[0]
              : story.sort(
                  (a, b) => new Date(a.created_at) - new Date(b.created_at)
                )[0]
          "
        />
      </SwiperSlide>
      <SwiperStoryContainerButton />
    </Swiper>
    <CreateStoryModal
      :show="isOpen"
      :isTextStory="isTextStory"
      :textStories="textStories"
      @closeModal="closeModal"
      @openTextStory="openTextStory"
      @closeTextStory="closeTextStory"
    />
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { useCurrentStoryStore } from "../stores/currentStory";
import { usePageStore } from "../stores/page";
import { Swiper, SwiperSlide } from "swiper/vue";
import { defineAsyncComponent } from "vue";

import { PlusCircleIcon } from "@heroicons/vue/24/solid";

import fonts from "../data/fonts";
import themes from "../data/themes";
import "swiper/css";

import SwiperStoryContainerButton from "./items/story/SwiperStoryContainerButton.vue";
import CreateStoryModal from "./modals/story/CreateStoryModal.vue";
import SkeletonLoadingStoryVue from "./loadings/SkeletonLoadingStory.vue";
import SkeletonLoadingContainer from "./loadings/SkeletonLoadingContainer.vue";

export default {
  components: {
    PlusCircleIcon,
    Story: defineAsyncComponent(() => import("./items/story/Story.vue")),
    Swiper,
    SwiperSlide,
    SwiperStoryContainerButton,
    CreateStoryModal,
    SkeletonLoadingStoryVue,
    SkeletonLoadingContainer,
  },
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();
    const pageStore = usePageStore()

    return {
      userStore,
      currentStoryStore,
      pageStore
    };
  },

  data() {
    return {
      isOpen: false,
      isTextStory: false,
      textStories: [],
      mediaStories: [],
      yourStories: [],
      setStory: [],
      firstStories: [],
      themes: themes,
      fonts: fonts,
      isLoading: false,
    };
  },

  computed: {
    yourLastStory() {
      return this.yourStories
        .filter((stories) => stories?.created_by?.id === this.userStore.user.id)
        .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))[0];
    },
    selectedTheme() {
      return this.themes?.filter(
        (theme) => theme.name === this.yourLastStory?.theme
      )[0];
    },
    selectedFont() {
      return this.fonts?.filter(
        (font) => font.name === this.yourLastStory?.font
      )[0];
    },
  },

  mounted() {
    this.getStories();
    this.currentStoryStore.resetActiveStory();
  },

  methods: {
    async getStories() {
      this.currentStoryStore.getCurrentUserId(this.userStore.user.id);
      this.isLoading = true;

      await axios
        .get("/api/story/text-stories/")
        .then((res) => {
          this.textStories = res.data;
          // console.log(this.textStories);

          this.textStories.forEach((textStory) => {
            this.yourStories.unshift(textStory);
          });
        })
        .catch((error) => {
          console.log(error);
        });

      await axios
        .get("/api/story/media-stories/")
        .then((res) => {
          this.mediaStories = res.data;
          // console.log(this.mediaStories);
          this.mediaStories.forEach((mediaStory) => {
            this.yourStories.unshift(mediaStory);
          });
          this.isLoading = false;
          this.getSetStories();
        })
        .catch((error) => {
          console.log(error);
        });

      this.getSetStories();
      this.yourStories = this.yourStories.sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
      );
    },
    getSetStories() {
      const resultAll = Object.groupBy(
        this.yourStories
          .filter((story) => story?.created_by?.id !== this.userStore.user.id)
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
        ({ created_by }) => created_by?.id
      );

      this.setStory = resultAll;

      // console.log(this.yourLastStory);
      const listId = this.yourStories
        .filter((story) => story?.created_by?.id !== this.userStore.user.id)
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .map((story) => story.created_by.id);
      const removeDuplicate = [...new Set(listId)];

      this.currentStoryStore.resetListId();
      this.currentStoryStore.getUserIdList(removeDuplicate);
    },
    async getUserStories(userId) {
      this.currentStoryStore.resetCurrentStory();
      this.currentStoryStore.resetActiveStory();

      await axios
        .get(`/api/story/get-text-stories/${userId}`)
        .then((res) => {
          res.data.stories.forEach((story) => {
            this.firstStories.unshift(story);
          });
        })
        .catch((error) => {
          console.log("error", error);
        });
      await axios
        .get(`/api/story/get-media-stories/${userId}`)
        .then((res) => {
          res.data.stories.forEach((story) => {
            this.firstStories.unshift(story);
          });
        })
        .catch((error) => {
          console.log("error", error);
        });

      this.currentStoryStore.getCurrentUserStory(this.firstStories);
      this.currentStoryStore.getActiveStory(
        this.currentStoryStore.currentStory[0]?.created_by?.id
      );

      setTimeout(() => {
        this.$router.push("/stories");
      }, 500);
    },
    openModal() {
      this.isOpen = true;
      this.isTextStory = false;
    },
    closeModal() {
      this.isOpen = false;
      this.isTextStory = false;
    },
    openTextStory() {
      this.isTextStory = true;
    },
    closeTextStory() {
      this.isTextStory = false;
    },
  },
};
</script>

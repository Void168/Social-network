<template>
  <div>
    <Swiper :slides-per-view="5" :space-between="20">
      <SwiperSlide
        ><div
          class="relative cursor-pointer bg-slate-700 rounded-lg h-[213px]"
          @click="openModal"
        >
          <img
            :src="userStore.user.avatar"
            class="rounded-b-none h-[70%] w-full"
            alt="create-story"
          />
          <div class="flex justify-center items-center relative h-[30%]">
            <span class="absolute top-[-25%]">
              <PlusCircleIcon
                class="w-10 h-10 text-blue-500 rounded-full bg-slate-700 p-1"
              />
            </span>
            <p class="font-semibold">Tạo tin</p>
          </div>
        </div></SwiperSlide
      >
      <SwiperSlide v-if="yourLastStory"
        ><div
          class="relative cursor-pointer rounded-lg group"
          @click="getUserStories"
        >
          <img
            :src="userStore.user.avatar"
            alt=""
            class="absolute top-4 left-4 w-10 h-10 rounded-full ring-4 ring-emerald-400 z-20"
          />
          <div
            class="relative h-[213px] flex items-center justify-center overflow-hidden shadow-sm rounded-lg cursor-pointer"
          >
            <div
              alt="story-image"
              class="h-full w-full group-hover:scale-105 group-hover:rounded-lg absolute z-10 bg-cover transition flex items-center justify-center"
              :class="[selectedTheme?.background, selectedFont?.font]"
            >
              <span class="text-xs" :class="[selectedTheme?.textColor]">{{
                yourLastStory?.body
              }}</span>
            </div>
          </div>
        </div></SwiperSlide
      >
      <SwiperSlide v-for="story in setStory" :key="story.id">
        <Story :story="story[0]" />
      </SwiperSlide>
      <SwiperStoryContainerButton />
    </Swiper>
    <CreateStoryModal
      :show="isOpen"
      :isTextStory="isTextStory"
      :yourStories="yourStories"
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
import Story from "./items/story/Story.vue";
import { Swiper, SwiperSlide } from "swiper/vue";

import { PlusCircleIcon } from "@heroicons/vue/24/solid";

import fonts from "../data/fonts";
import themes from "../data/themes";
import "swiper/css";

import SwiperStoryContainerButton from "./items/story/SwiperStoryContainerButton.vue";
import CreateStoryModal from "./modals/story/CreateStoryModal.vue";

export default {
  components: {
    PlusCircleIcon,
    Story,
    Swiper,
    SwiperSlide,
    SwiperStoryContainerButton,
    CreateStoryModal,
  },
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();

    return {
      userStore,
      currentStoryStore,
    };
  },

  data() {
    return {
      isOpen: false,
      isTextStory: false,
      yourStories: [],
      setStory: [],
      themes: themes,
      fonts: fonts,
    };
  },

  computed: {
    yourLastStory() {
      return this.yourStories.filter(
        (stories) => stories.created_by.id === this.userStore.user.id
      )[0];
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
    this.getTextStories();
  },

  methods: {
    getTextStories() {
      axios
        .get("/api/story/text-stories/")
        .then((res) => {
          this.yourStories = res.data.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          // console.log(this.yourStories);
          this.getSetStories();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getSetStories() {
      const result = Object.groupBy(
        this.yourStories.filter(
          (story) => story.created_by.id !== this.userStore.user.id
        ),
        ({ created_by }) => created_by.id
      );
      // console.log(result)
      this.setStory = result;
      // console.log(this.setStory);
    },
    getUserStories() {
      axios
        .get(`/api/story/get-text-stories/${this.userStore.user.id}`)
        .then((res) => {
          this.currentStoryStore.getCurrentUserStory(res.data.stories);
          setTimeout(() => {
            this.$router.push("/stories");
          }, 200);
        })
        .catch((error) => {
          console.log("error", error);
        });
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

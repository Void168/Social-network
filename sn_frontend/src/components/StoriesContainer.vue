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
            >
              <img
                :src="yourLastStory?.attachments[0]?.get_image"
                :class="[yourLastStory?.attachments[0]?.rotate]"
                :style="{ scale: yourLastStory?.attachments[0]?.zoom_image }"
                class="rounded-none"
                ref="image"
              />
            </div>
          </div>
        </div>
      </SwiperSlide>
      <SwiperSlide v-for="story in setStory" :key="story.id">
        <Story :story="story[0]" />
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
      textStories: [],
      mediaStories: [],
      yourStories: [],
      setStory: [],
      themes: themes,
      fonts: fonts,
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
  },

  methods: {
    getStories() {
      setTimeout(() => {
        axios
          .get("/api/story/text-stories/")
          .then((res) => {
            this.textStories = res.data.sort(
              (a, b) => new Date(a.created_at) - new Date(b.created_at)
            );
            // console.log(this.textStories);

            this.textStories.forEach((textStory) => {
              this.yourStories.unshift(textStory);
            });
          })
          .catch((error) => {
            console.log(error);
          });
      }, 100);

      setTimeout(() => {
        axios
          .get("/api/story/media-stories/")
          .then((res) => {
            this.mediaStories = res.data.sort(
              (a, b) => new Date(a.created_at) - new Date(b.created_at)
            );
            // console.log(this.mediaStories);
            this.mediaStories.forEach((mediaStory) => {
              this.yourStories.unshift(mediaStory);
            });

            this.getSetStories();
          })
          .catch((error) => {
            console.log(error);
          });
      }, 200);

      setTimeout(() => {
        this.getSetStories();
        this.yourStories = this.yourStories.sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
        console.log(this.yourStories);
      }, 300);
    },
    getSetStories() {
      const resultAll = Object.groupBy(
        this.yourStories
          .filter((story) => story?.created_by?.id !== this.userStore.user.id)
          .sort((a, b) => new Date(a.created_at) - new Date(b.created_at)),
        ({ created_by }) => created_by?.id
      );

      this.setStory = resultAll;
    },
    getUserStories() {
      axios
        .get(`/api/story/get-text-stories/${this.userStore.user.id}`)
        .then((res) => {
          this.currentStoryStore.resetCurrentStory()
          this.currentStoryStore.getCurrentUserStory(res.data.stories);
          setTimeout(() => {
            this.$router.push("/stories");
          }, 200);
        })
        .catch((error) => {
          console.log("error", error);
        });

      axios
        .get(`/api/story/get-media-stories/${this.userStore.user.id}`)
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

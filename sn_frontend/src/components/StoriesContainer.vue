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
            class="rounded-b-none h-[70%]"
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
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperSlide><Story /></SwiperSlide>
      <SwiperNavButton />
    </Swiper>
    <CreateStoryModal
      :show="isOpen"
      :isTextStory="isTextStory"
      @closeModal="closeModal"
      @openTextStory="openTextStory"
      @closeTextStory="closeTextStory"
    />
  </div>
</template>

<script>
import { useUserStore } from "../stores/user";
import Story from "./items/story/Story.vue";
import { PlusCircleIcon } from "@heroicons/vue/24/solid";
import { Swiper, SwiperSlide } from "swiper/vue";

import "swiper/css";

import SwiperNavButton from "./items/story/SwiperNavButton.vue";
import CreateStoryModal from "./modals/story/CreateStoryModal.vue";

export default {
  components: {
    PlusCircleIcon,
    Story,
    Swiper,
    SwiperSlide,
    SwiperNavButton,
    CreateStoryModal,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      isOpen: false,
      isTextStory: false,
    };
  },

  methods: {
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
    }
  },
};
</script>

<template>
  <div
    class="flex items-center justify-between absolute top-4 w-full h-16 p-4 z-20"
    :class="[selectedTheme?.textColor]"
  >
    <div class="flex gap-4 items-center">
      <img
      loading="lazy"
        :src="stories[0]?.created_by?.get_avatar"
        alt=""
        class="rounded-full w-12 h-12"
      />
      <div class="flex gap-1 items-center">
        <div class="flex gap-1 xm:items-center xm:flex-row flex-col">
          <span class="font-semibold xm:text-lg text-xs">{{
            stories[0]?.created_by?.name
          }}</span>
          <span class="font-medium xm:text-base text-xs">{{
            stories[this.currentStoryStore?.activeSlide]?.created_at_formatted
          }}</span>
        </div>
        <GlobeAsiaAustraliaIcon
          class="xm:w-5 xm:h-5 h-3 w-3"
          v-if="
            !stories[this.currentStoryStore?.activeSlide]?.is_private &&
            !stories[this.currentStoryStore?.activeSlide]?.only_me
          "
        />
        <UserGroupIcon
          class="xm:w-5 xm:h-5 h-3 w-3"
          v-else-if="
            stories[this.currentStoryStore?.activeSlide]?.is_private &&
            !stories[this.currentStoryStore?.activeSlide]?.only_me
          "
        />
        <LockClosedIcon
          class="xm:w-5 xm:h-5 h-3 w-3"
          v-else-if="
            !stories[this.currentStoryStore?.activeSlide]?.is_private &&
            stories[this.currentStoryStore?.activeSlide]?.only_me
          "
        />
      </div>
    </div>
    <div class="flex gap-2 items-center">
      <PauseIcon
        class="xm:w-6 xm:h-6 w-4 h-4 cursor-pointer"
        @click="$emit('pause')"
        v-if="!isPause"
      />
      <PlayIcon class="xm:w-6 xm:h-6 w-4 h-4 cursor-pointer" @click="$emit('pause')" v-else />
      <SpeakerWaveIcon
        class="xm:w-6 xm:h-6 w-4 h-4 cursor-pointer"
        @click="$emit('mute')"
        v-if="!isMute"
      />
      <SpeakerXMarkIcon
        class="xm:w-6 xm:h-6 w-4 h-4 cursor-pointer"
        @click="$emit('mute')"
        v-else
    />
      <StoryDropdown
        @openModal="openModal"
        :yourStory="stories[currentStoryStore.activeSlide]"
      />
      <DeleteStoryModalVue
        :show="isOpen"
        @closeModal="closeModal"
        @deleteStory="deleteStory(stories[currentStoryStore.activeSlide])"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
  PlayIcon,
  PauseIcon,
  SpeakerXMarkIcon,
  SpeakerWaveIcon,
} from "@heroicons/vue/24/solid";
import StoryDropdown from "../../dropdown/StoryDropdown.vue";
import DeleteStoryModalVue from "../../modals/story/DeleteStoryModal.vue";
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";
import { useToastStore } from "../../../stores/toast";

import themes from "../../../data/themes";
import fonts from "../../../data/fonts";

export default (await import("vue")).defineComponent({
  components: {
    StoryDropdown,
    DeleteStoryModalVue,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
    PlayIcon,
    PauseIcon,
    SpeakerXMarkIcon,
    SpeakerWaveIcon,
  },

  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();
    const toastStore = useToastStore();
    return {
      toastStore,
      userStore,
      currentStoryStore,
    };
  },

  props: {
    stories: Array,
    isPause: Boolean,
    isMute: Boolean,
  },

  data() {
    return {
      isOpen: false,
      themes: themes,
      fonts: fonts,
    };
  },

  computed: {
    selectedTheme() {
      return this.themes?.filter(
        (theme) =>
          theme.name === this.stories[this.currentStoryStore.activeSlide]?.theme
      )[0];
    },
  },

  methods: {
    openModal() {
      this.$emit("openModal", this.isOpen);
      this.isOpen = true;
    },
    closeModal() {
      this.isOpen = false;
    },
    deleteStory(yourStory) {
      if (yourStory?.body) {
        axios
          .delete(`/api/story/text-story/${yourStory?.id}/delete/`)
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
          .delete(`/api/story/media-story/${yourStory?.id}/delete/`)
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

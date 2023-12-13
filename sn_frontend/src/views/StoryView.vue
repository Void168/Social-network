<template>
  <div class="bg-slate-800 text-neutral-200 h-screen grid grid-cols-5 relative">
    <div
      class="col-span-1 bg-slate-800 overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
    >
      <div class="p-4 border-b border-slate-700 bg-slate-800 sticky top-0">
        <RouterLink to="/">
          <XMarkIcon
            class="text-neutral-200 h-10 w-10 cursor-pointer transition p-2 bg-slate-700 rounded-full hover:bg-slate-600"
          />
        </RouterLink>
      </div>
      <div class="p-4">
        <h2 class="text-2xl font-bold">Tin</h2>
        <div class="mt-4">
          <a href="#" class="text-emerald-400 hover:text-emerald-500"
            >Kho lưu trữ</a
          >
          &middot;
          <a href="#" class="text-emerald-400 hover:text-emerald-500"
            >Cài đặt</a
          >
        </div>
        <div class="my-4 flex flex-col space-y-4">
          <h2 class="text-xl font-semibold">Tin của bạn</h2>
          <div class="flex gap-3 items-center">
            <PlusIcon
              @click="openModal"
              class="text-emerald-300 h-16 w-16 cursor-pointer transition p-3 bg-slate-700 rounded-full hover:bg-slate-600"
            />
            <div class="flex flex-col space-y-1">
              <h4 class="font-semibold text-lg">Tạo tin</h4>
              <p class="text-neutral-400">Bạn có thể tạo ảnh hoặc viết gì đó</p>
            </div>
            <CreateStoryModal
              :show="isCreateStoryOpen"
              :isTextStory="isTextStory"
              @closeModal="closeModal"
              @openTextStory="openTextStory"
              @closeTextStory="closeTextStory"
            />
          </div>
        </div>
      </div>
      <div>
        <div class="">
          <h2 class="text-xl font-semibold ml-4">Tất cả tin</h2>
          <div v-for="n in 10" :key="n">
            <StoryBox />
          </div>
        </div>
      </div>
    </div>
    <div class="col-span-4 bg-slate-900 flex flex-col relative">
      <div class="py-4 h-full">
        <StoryDetail />
      </div>
      <div class="flex justify-center items-center gap-2">
        <input
          ref="replyStory"
          type="text"
          placeholder="Trả lời..."
          class="my-2 py-2 px-8 border text-lg border-gray-200 dark:bg-slate-700 dark:text-neutral-200 rounded-2xl"
        />
        <div class="flex gap-3" v-for="emoji in emojiList" :key="emoji.unicode">
          <div
            class="group p-2 rounded-full w-12 h-12 bg-gradient-to-t from-white via-emerald-500 to-green-500 flex justify-center items-center cursor-pointer"
          >
            <span
              :class="
                emoji.name === 'Like'
                  ? 'text-3xl mb-2 group-hover:scale-105'
                  : 'text-3xl group-hover:scale-105 mb-1'
              "
              >{{ emoji.unicode }}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCurrentStoryStore } from "../stores/currentStory";
import { RouterLink } from "vue-router";
import { XMarkIcon, PlusIcon } from "@heroicons/vue/24/solid";
import StoryBox from "../components/items/story/StoryBox.vue";
import StoryDetail from "../components/items/story/StoryDetail.vue";
import CreateStoryModal from "../components/modals/story/CreateStoryModal.vue";
import emojiStory from "../data/emoji";

export default {
  name: "StoryView",
  components: {
    RouterLink,
    StoryBox,
    StoryDetail,
    CreateStoryModal,
    XMarkIcon,
    PlusIcon,
  },
  setup() {
    const currentStoryStore = useCurrentStoryStore()

    return {
      currentStoryStore
    }
  },
  data() {
    return {
      isCreateStoryOpen: false,
      isTextStory: false,
      emojiList: emojiStory,
    };
  },

  methods: {
    openModal() {
      this.isCreateStoryOpen = true;
      this.isTextStory = false;
    },
    closeModal() {
      this.isCreateStoryOpen = false;
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

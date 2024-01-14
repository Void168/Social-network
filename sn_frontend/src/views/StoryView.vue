<template>
  <div class="bg-slate-800 text-neutral-200 h-screen grid lg:grid-cols-5 grid-cols-4 relative">
    <div
      class="md:col-span-1 md:block hidden bg-slate-800 overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
    >
      <div class="p-4 border-b border-slate-700 bg-slate-800 sticky top-0">
        <RouterLink to="/" class="w-10 block">
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
              class="text-emerald-300 2xl:h-16 2xl:w-16 xl:w-14 xl:h-[52px] xs:w-10 xs:h-[36px] cursor-pointer transition p-3 bg-slate-700 rounded-full hover:bg-slate-600"
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
        <div
          v-if="yourLastStory.length"
          @click="otherStory(yourLastStory[0]?.created_by.id)"
        >
          <div
            class="flex gap-3 items-center p-4 hover:bg-slate-700 rounded-lg cursor-pointer"
            :class="
              currentStoryStore.activeStory === yourLastStory[0]?.created_by.id
                ? 'bg-slate-700'
                : ''
            "
          >
            <img
              :src="userStore.user.avatar"
              alt="story-owner"
              class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 xs:w-10 xs:h-10 rounded-full"
            />
            <div class="flex flex-col space-y-2">
              <h3 class="text-lg font-semibold">{{ userStore.user.name }}</h3>
              <p class="flex gap-2">
                <span class="dark:text-neutral-400">{{
                  yourLastStory[yourLastStory.length - 1]?.created_at_formatted
                }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-semibold ml-4">Tất cả tin</h2>
        <div class="my-2">
          <div @click="firstStory">
            <div
              @click="
                otherStory(currentStoryStore?.currentStory[0]?.created_by.id)
              "
              v-if="
                currentStoryStore?.currentStory[0]?.created_by?.id !==
                yourLastStory[0]?.created_by?.id
              "
              class="flex gap-3 items-center py-4 px-8 hover:bg-slate-700 rounded-lg cursor-pointer"
              :class="
                currentStoryStore?.currentStory[0]?.created_by?.id ===
                currentStoryStore.activeStory
                  ? 'bg-slate-700'
                  : ''
              "
            >
              <img
                :src="
                  currentStoryStore?.currentStory[0]?.created_by?.get_avatar
                "
                alt="story-owner"
                class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 xs:w-10 xs:h-10 rounded-full ring-4"
                :class="
                  currentStoryStore?.currentStory[0]?.seen_by?.map(
                    (user) => user.id === userStore.user.id
                  )
                    ? 'ring-slate-500'
                    : 'ring-emerald-400'
                "
              />
              <div class="flex flex-col 2xl:space-y-2 w-full">
                <h3 class="xl:text-lg font-semibold">
                  {{ currentStoryStore?.currentStory[0]?.created_by?.name }}
                </h3>
                <p class="flex 2xl:gap-2 2xl:flex-row xl:text-base xs:text-sm flex-wrap flex-col w-full">
                  <span class="text-emerald-400"
                    >{{ currentStoryStore?.currentStory?.length }} thẻ mới</span
                  >
                  <span
                    >{{
                      currentStoryStore?.currentStory[0]?.created_at_formatted
                    }}
                    trước</span
                  >
                </p>
              </div>
            </div>
          </div>
          <div v-for="story in setStory" :key="story.id">
            <StoryBox
              :story="story"
              @otherStory="otherStory(story[0].created_by.id)"
              :isOtherStory="isOtherStory"
              :class="
                story[0]?.created_by?.id === userStories[0]?.created_by?.id
                  ? 'bg-slate-700'
                  : ''
              "
            />
          </div>
        </div>
      </div>
    </div>
    <div
      @click="expandListStories"
      class="absolute flex md:hidden left-0 z-20 inset-y-2/4 w-5 h-20 bg-slate-800 rounded-r-2xl"
      :class="isExpand ? 'translate-x-0' : 'translate-x-[300px]'"
    >
      <ChevronLeftIcon class="dark:text-slate-200" v-if="!isExpand" />
      <ChevronRightIcon class="dark:text-slate-200" v-else />
    </div>
    <div
      class="block md:hidden bg-slate-800 absolute w-[300px] z-50 h-full overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
      :class="isExpand ? '-translate-x-[300px]' : 'translate-x-0'"
    >
      <div class="p-4 border-b border-slate-700 bg-slate-800 sticky top-0">
        <RouterLink to="/" class="w-10 block">
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
              class="text-emerald-300 2xl:h-16 2xl:w-16 xl:w-14 xl:h-[52px] xs:w-10 xs:h-[36px] cursor-pointer transition p-3 bg-slate-700 rounded-full hover:bg-slate-600"
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
        <div
          v-if="yourLastStory.length"
          @click="otherStory(yourLastStory[0]?.created_by.id)"
        >
          <div
            class="flex gap-3 items-center p-4 hover:bg-slate-700 rounded-lg cursor-pointer"
            :class="
              currentStoryStore.activeStory === yourLastStory[0]?.created_by.id
                ? 'bg-slate-700'
                : ''
            "
          >
            <img
              :src="userStore.user.avatar"
              alt="story-owner"
              class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 xs:w-10 xs:h-10 rounded-full"
            />
            <div class="flex flex-col space-y-2">
              <h3 class="text-lg font-semibold">{{ userStore.user.name }}</h3>
              <p class="flex gap-2">
                <span class="dark:text-neutral-400">{{
                  yourLastStory[yourLastStory.length - 1]?.created_at_formatted
                }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-semibold ml-4">Tất cả tin</h2>
        <div class="my-2">
          <div @click="firstStory">
            <div
              @click="
                otherStory(currentStoryStore?.currentStory[0]?.created_by.id)
              "
              v-if="
                currentStoryStore?.currentStory[0]?.created_by?.id !==
                yourLastStory[0]?.created_by?.id
              "
              class="flex gap-3 items-center py-4 px-8 hover:bg-slate-700 rounded-lg cursor-pointer"
              :class="
                currentStoryStore?.currentStory[0]?.created_by?.id ===
                currentStoryStore.activeStory
                  ? 'bg-slate-700'
                  : ''
              "
            >
              <img
                :src="
                  currentStoryStore?.currentStory[0]?.created_by?.get_avatar
                "
                alt="story-owner"
                class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 xs:w-10 xs:h-10 rounded-full ring-4"
                :class="
                  currentStoryStore?.currentStory[0]?.seen_by?.map(
                    (user) => user.id === userStore.user.id
                  )
                    ? 'ring-slate-500'
                    : 'ring-emerald-400'
                "
              />
              <div class="flex flex-col 2xl:space-y-2 w-full">
                <h3 class="xl:text-lg font-semibold">
                  {{ currentStoryStore?.currentStory[0]?.created_by?.name }}
                </h3>
                <p class="flex 2xl:gap-2 2xl:flex-row xl:text-base xs:text-sm flex-wrap flex-col w-full">
                  <span class="text-emerald-400"
                    >{{ currentStoryStore?.currentStory?.length }} thẻ mới</span
                  >
                  <span
                    >{{
                      currentStoryStore?.currentStory[0]?.created_at_formatted
                    }}
                    trước</span
                  >
                </p>
              </div>
            </div>
          </div>
          <div v-for="story in setStory" :key="story.id">
            <StoryBox
              :story="story"
              @otherStory="otherStory(story[0].created_by.id)"
              :isOtherStory="isOtherStory"
              :class="
                story[0]?.created_by?.id === userStories[0]?.created_by?.id
                  ? 'bg-slate-700'
                  : ''
              "
            />
          </div>
        </div>
      </div>
    </div>
    <div
      class="md:col-span-1 md:hidden block bg-slate-800 overflow-y-auto scrollbar-corner-slate-200 scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
    >
      <div class="p-4 border-b border-slate-700 bg-slate-800 sticky top-0">
        <RouterLink to="/" class="w-10 block">
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
              class="text-emerald-300 2xl:h-16 2xl:w-16 xl:w-14 xl:h-[52px] xs:w-10 xs:h-[36px] cursor-pointer transition p-3 bg-slate-700 rounded-full hover:bg-slate-600"
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
        <div
          v-if="yourLastStory.length"
          @click="otherStory(yourLastStory[0]?.created_by.id)"
        >
          <div
            class="flex gap-3 items-center p-4 hover:bg-slate-700 rounded-lg cursor-pointer"
            :class="
              currentStoryStore.activeStory === yourLastStory[0]?.created_by.id
                ? 'bg-slate-700'
                : ''
            "
          >
            <img
              :src="userStore.user.avatar"
              alt="story-owner"
              class="2xl:w-16 2xl:h-16 xl:w-14 xl:h-14 xs:w-10 xs:h-10 rounded-full"
            />
            <div class="flex flex-col space-y-2">
              <h3 class="text-lg font-semibold">{{ userStore.user.name }}</h3>
              <p class="flex gap-2">
                <span class="dark:text-neutral-400">{{
                  yourLastStory[yourLastStory.length - 1]?.created_at_formatted
                }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-semibold ml-4">Tất cả tin</h2>
        <div class="my-2">
          <div @click="firstStory">
            <div
              @click="
                otherStory(currentStoryStore?.currentStory[0]?.created_by.id)
              "
              v-if="
                currentStoryStore?.currentStory[0]?.created_by?.id !==
                yourLastStory[0]?.created_by?.id
              "
              class="flex gap-3 items-center py-4 px-8 hover:bg-slate-700 rounded-lg cursor-pointer"
              :class="
                currentStoryStore?.currentStory[0]?.created_by?.id ===
                currentStoryStore.activeStory
                  ? 'bg-slate-700'
                  : ''
              "
            >
              <img
                :src="
                  currentStoryStore?.currentStory[0]?.created_by?.get_avatar
                "
                alt="story-owner"
                class="w-16 h-16 rounded-full ring-4"
                :class="
                  currentStoryStore?.currentStory[0]?.seen_by?.map(
                    (user) => user.id === userStore.user.id
                  )
                    ? 'ring-slate-500'
                    : 'ring-emerald-400'
                "
              />
              <div class="flex flex-col space-y-2">
                <h3 class="text-lg font-semibold">
                  {{ currentStoryStore?.currentStory[0]?.created_by?.name }}
                </h3>
                <p class="flex gap-2">
                  <span class="text-emerald-400"
                    >{{ currentStoryStore?.currentStory?.length }} thẻ mới</span
                  >
                  <span
                    >{{
                      currentStoryStore?.currentStory[0]?.created_at_formatted
                    }}
                    trước</span
                  >
                </p>
              </div>
            </div>
          </div>
          <div v-for="story in setStory" :key="story.id">
            <StoryBox
              :story="story"
              @otherStory="otherStory(story[0].created_by.id)"
              :isOtherStory="isOtherStory"
              :class="
                story[0]?.created_by?.id === userStories[0]?.created_by?.id
                  ? 'bg-slate-700'
                  : ''
              "
            />
          </div>
        </div>
      </div>
    </div>
    <div class="lg:col-span-4 md:col-span-3 col-span-4 bg-slate-900 flex flex-col relative h-screen">
      <div class="py-4 h-full">
        <Suspense>
          <StoryDetail
            :userStories="userStories"
            :isOtherStory="isOtherStory"
            :isYourStory="isYourStory"
            :yourStory="yourLastStory"
            :isFirstStory="isFirstStory"
            :isListSeenOpen="isListSeenOpen"
            @closeListSeen="closeListSeen"
          />
          <template #fallback> Loading... </template>
        </Suspense>
      </div>
      <div v-if="!isListSeenOpen && currentStoryStore.activeStoryId" class="flex justify-center items-center">
        <div
          class="flex sm:justify-center sm:px-0 px-6 items-center gap-2 md:max-w-max xs:max-w-96 xs:overflow-x-scroll md:overflow-hidden"
          v-if="currentStoryStore.activeStory !== userStore.user.id"
        >
          <input
            ref="replyStory"
            type="text"
            placeholder="Trả lời..."
            class="my-2 py-2 px-8 border text-lg border-gray-200 dark:bg-slate-700 dark:text-neutral-200 rounded-2xl lg:w-96 w-56"
          />
          <div
            class="flex gap-3"
            v-for="emoji in emojiList.slice(1, emojiList.length)"
            :key="emoji.utf"
          >
            <div
              class="group p-2 rounded-full lg:w-12 lg:h-12 md:w-10 md:h-10 xs:w-8 xs:h-8 bg-gradient-to-t from-white via-emerald-500 to-green-500 flex justify-center items-center cursor-pointer"
            >
              <span
                @click="sendReact(emoji.name, currentStoryStore.activeStoryId)"
                :class="
                  emoji.name === 'like'
                    ? 'lg:text-3xl md:text-xl mb-2 group-hover:scale-105'
                    : 'lg:text-3xl md:text-xl group-hover:scale-105 mb-1'
                "
                >{{ emoji.unicode }}</span
              >
            </div>
          </div>
        </div>
        <div
          @click="openListSeen"
          v-else
          class="flex justify-center items-center flex-col cursor-pointer"
        >
          <ChevronUpIcon class="w-8" />
          <p class="font-bold text-lg border-b pb-1">
            {{ yourLastStory[currentStoryStore.activeSlide]?.seen_by.length || 0 }}
            người xem
          </p>
          <div class="flex my-2 gap-1">
            <div
              v-for="user in yourLastStory[
                currentStoryStore.activeSlide
              ]?.seen_by.slice(0, 4)"
              :key="user.id"
            >
              <img :src="user.get_avatar" class="w-8 h-8 rounded-full" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../stores/user";
import { useCurrentStoryStore } from "../stores/currentStory";
import { RouterLink } from "vue-router";
import { XMarkIcon, PlusIcon, ChevronUpIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/vue/24/solid";
import StoryBox from "../components/items/story/StoryBox.vue";
import CreateStoryModal from "../components/modals/story/CreateStoryModal.vue";
import emojiStory from "../data/emoji";
import { defineAsyncComponent } from "vue";

export default {
  name: "StoryView",
  components: {
    RouterLink,
    StoryBox,
    StoryDetail: defineAsyncComponent(() =>
      import("../components/items/story/StoryDetail.vue")
    ),
    CreateStoryModal,
    XMarkIcon,
    PlusIcon,
    ChevronUpIcon,
    ChevronLeftIcon, ChevronRightIcon
  },
  setup() {
    const currentStoryStore = useCurrentStoryStore();
    const userStore = useUserStore();

    return {
      currentStoryStore,
      userStore,
    };
  },
  data() {
    return {
      isCreateStoryOpen: false,
      isTextStory: false,
      emojiList: emojiStory,
      yourStories: [],
      setStory: [],
      isOtherStory: false,
      userStories: [],
      userId: null,
      isFirstStory: false,
      isYourStory: false,
      userIdList: [],
      isListSeenOpen: false,
      activeStory: null,
      isExpand: false
    };
  },

  computed: {
    yourLastStory() {
      return this.yourStories
        .filter((stories) => stories.created_by.id === this.userStore.user.id)
        .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    },
  },

  beforeMount() {
    this.settingActiveStory();
    this.getActiveStory();
  },

  mounted() {
    this.getStories();
  },

  beforeUpdate() {
    this.getActiveStory();
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
    expandListStories(){
      this.isExpand = !this.isExpand
    },
    async getStories() {
      await axios
        .get("/api/story/text-stories/")
        .then((res) => {
          this.textStories = res.data.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
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
          this.mediaStories = res.data.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          this.mediaStories.forEach((mediaStory) => {
            this.yourStories.unshift(mediaStory);
          });

          this.getSetStories();
        })
        .catch((error) => {
          console.log(error);
        });

      setTimeout(() => {
        this.getSetStories();
        this.yourStories = this.yourStories.sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
      }, 300);
    },
    getSetStories() {
      const result = Object.groupBy(
        this.yourStories
          .filter(
            (story) =>
              story?.created_by?.id !== this.userStore.user.id &&
              story?.created_by?.id !==
                this.currentStoryStore?.currentStory[0]?.created_by?.id
          )
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
        ({ created_by }) => created_by.id
      );
      this.setStory = result;
    },
    settingActiveStory() {
      if (
        this.currentStoryStore?.currentStory?.userId ===
          this.yourLastStory[0]?.created_by?.id &&
        this.yourLastStory[0]?.created_by?.id ===
          this.userStories[0]?.created_by?.id
      ) {
        this.isFirstStory = false;
        this.isOtherStory = false;
        this.isYourStory = true;
      }
      if (
        this.currentStoryStore?.currentStory?.userId ===
        this.userStories[0]?.created_by?.id
      ) {
        this.isFirstStory = true;
        this.isOtherStory = true;
        this.isYourStory = false;
      }
    },
    firstStory() {
      this.isFirstStory = true;
    },
    async otherStory(userId) {
      this.currentStoryStore.getActiveStory(userId);
      this.userId = userId;
      this.$emit("otherStory");
      if (this.currentStoryStore.userId !== userId) {
        this.isFirstStory = false;
      } else {
        this.isFirstStory = true;
      }

      if (this.yourLastStory[0]?.created_by?.id === userId) {
        this.isOtherStory = false;
        this.isYourStory = true;
      } else {
        this.isOtherStory = true;
        this.isYourStory = false;
      }

      if (
        this.currentStoryStore.userId === this.yourLastStory[0]?.created_by?.id
      ) {
        this.isFirstStory = false;
      }

      this.userStories = [];

      await axios
        .get(`api/story/get-text-stories/${userId}/`)
        .then((res) => {
          if (this.userStories) {
            res.data.stories.forEach((textStory) => {
              this.userStories.unshift(textStory);
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });

      await axios
        .get(`api/story/get-media-stories/${userId}/`)
        .then((res) => {
          res.data.stories.forEach((mediaStory) => {
            this.userStories.unshift(mediaStory);
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getActiveStory() {
      await axios
        .get(
          `/api/story/get-detail-text-story/${this.currentStoryStore.activeStoryId}`
        )
        .then((res) => {
          if (!res.data.message) {
            this.activeStory = res.data;
          }
        })
        .catch((error) => console.log(error));

      await axios
        .get(
          `/api/story/get-detail-media-story/${this.currentStoryStore.activeStoryId}`
        )
        .then((res) => {
          if (!res.data.message) {
            this.activeStory = res.data;
          }})
        .catch((error) => console.log(error));
    },
    sendReact(typeOfReact, pk) {
      if (this.activeStory?.body) {
        axios
          .post(`/api/story/react-text-story/${pk}/${typeOfReact}/`)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        axios
          .post(`/api/story/react-media-story/${pk}/${typeOfReact}/`)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    openListSeen() {
      this.isListSeenOpen = true;
    },
    closeListSeen() {
      this.isListSeenOpen = false;
    },
  },
};
</script>

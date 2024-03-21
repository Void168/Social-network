<template>
  <div class="flex items-center justify-center h-full">
    <div
      class="relative border-2 xl:w-[500px] h-full xm:w-[400px] w-full rounded-lg flex items-center shadow-lg"
    >
      <Suspense>
        <SwiperStoryHeader
          v-if="isYourStory && !isFirstStory && !isOtherStory"
          :stories="yourStory"
          :isPause="isPause"
          :isMute="isMute"
          @pause="pause"
          @mute="mute"
        />
        <SwiperStoryHeader
          v-else-if="
            isOtherStory &&
            isFirstStory &&
            !isYourStory &&
            !nextStories.length &&
            !prevStories.length &&
            !isNext &&
            currentStoryStore.activeStory
          "
          :stories="currentStoryStore.currentStory"
          :isPause="isPause"
          :isMute="isMute"
          @pause="pause"
          @mute="mute"
        />
        <SwiperStoryHeader
          v-else-if="nextStories.length && !prevStories.length"
          :stories="nextStories"
          :isPause="isPause"
          :isMute="isMute"
          @pause="pause"
          @mute="mute"
        />
        <SwiperStoryHeader
          v-else-if="prevStories.length && !nextStories.length"
          :stories="prevStories"
          :isPause="isPause"
          :isMute="isMute"
          @pause="pause"
          @mute="mute"
        />
        <SwiperStoryHeader
          v-else-if="
            userStories.length &&
            !prevStories.length &&
            !nextStories.length &&
            currentStoryStore.listId.indexOf(
              this.currentStoryStore?.activeStory
            ) > 0
          "
          :stories="userStories"
          :isPause="isPause"
          :isMute="isMute"
          @pause="pause"
          @mute="mute"
        />
      </Suspense>
      <Suspense>
        <SwiperStory
          v-if="isYourStory && !isFirstStory && !isOtherStory"
          :stories="yourStory"
          :isPause="isPause"
          :isMute="isMute"
          :nextFunction="next"
          @next="next"
          @prev="prev"
        />
        <SwiperStory
          v-else-if="
            isOtherStory &&
            isFirstStory &&
            !isYourStory &&
            !nextStories.length &&
            !prevStories.length &&
            !isNext &&
            currentStoryStore.activeStory
          "
          :nextFunction="next"
          :stories="currentStoryStore?.currentStory"
          :isPause="isPause"
          :isMute="isMute"
          @next="next"
          @prev="prev"
        />
        <SwiperStory
          v-else-if="nextStories.length && !prevStories.length"
          :stories="nextStories"
          :isPause="isPause"
          :isMute="isMute"
          :nextFunction="next"
          @next="next"
          @prev="prev"
        />
        <SwiperStory
          v-else-if="prevStories.length && !nextStories.length"
          :stories="prevStories"
          :isPause="isPause"
          :isMute="isMute"
          :nextFunction="next"
          @next="next"
          @prev="prev"
        />
        <SwiperStory
          v-else-if="
            userStories.length &&
            !prevStories.length &&
            !nextStories.length &&
            currentStoryStore.listId.indexOf(
              this.currentStoryStore?.activeStory
            ) > 0
          "
          :stories="userStories"
          :isPause="isPause"
          :isMute="isMute"
          :nextFunction="next"
          @next="next"
          @prev="prev"
        />
        <div
          class="text-white text-xl flex justify-center items-center w-full"
          v-else-if="
            !nextStories.length &&
            !prevStories.length &&
            currentStoryStore.listId.indexOf(
              this.currentStoryStore?.activeStory
            ) < 0
          "
        >
          <p class="text-center">Đã xem hết tin</p>
        </div>
        <template #fallback>
          <SkeletonLoadingContainer
            class="flex justify-center items-center w-full"
          />
        </template>
      </Suspense>
      <Suspense>
        <MediaStoryTitle
          :stories="yourStory"
          v-if="isYourStory && !isFirstStory && !isOtherStory"
        />
        <MediaStoryTitle
          :stories="currentStoryStore?.currentStory"
          v-else-if="
            isOtherStory &&
            isFirstStory &&
            !isYourStory &&
            !nextStories.length &&
            !prevStories.length &&
            !isNext &&
            currentStoryStore.activeStory
          "
        />
        <MediaStoryTitle
          :stories="nextStories"
          v-else-if="nextStories.length && !prevStories.length"
        />
        <MediaStoryTitle
          :stories="prevStories"
          v-else-if="prevStories.length && !nextStories.length"
        />
        <MediaStoryTitle
          :stories="userStories"
          v-else-if="
            userStories.length &&
            !prevStories.length &&
            !nextStories.length &&
            currentStoryStore.listId.indexOf(
              this.currentStoryStore?.activeStory
            ) > 0
          "
        />
      </Suspense>
      <Suspense>
        <ListSeenUserStory
          @closeListSeen="$emit('closeListSeen')"
          :stories="yourStory"
          v-if="
            isListSeenOpen &&
            currentStoryStore.activeStory === userStore.user.id
          "
        />
      </Suspense>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { reactive } from "vue";

import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";
import { useToastStore } from "../../../stores/toast";
import { defineAsyncComponent } from "vue";
import SkeletonLoadingContainer from "../../loadings/SkeletonLoadingContainer.vue";

export default (await import("vue")).defineComponent({
  components: {
    SwiperStory: defineAsyncComponent(() => import("./SwiperStory.vue")),
    SwiperStoryHeader: defineAsyncComponent(() =>
      import("./SwiperStoryHeader.vue")
    ),
    ListSeenUserStory: defineAsyncComponent(() =>
      import("./ListSeenUserStory.vue")
    ),
    MediaStoryTitle: defineAsyncComponent(() =>
      import("./MediaStoryTitle.vue")
    ),
    SkeletonLoadingContainer,
  },
  props: {
    isOtherStory: Boolean,
    userStories: Array,
    isYourStory: Boolean,
    yourStory: Object,
    isFirstStory: Boolean,
    isListSeenOpen: Boolean,
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
    };
  },

  data() {
    return {
      isPause: false,
      isMute: false,
      isNext: false,
      isPrev: false,
      isOpen: false,
      nextStories: [],
      prevStories: [],
    };
  },

  methods: {
    async next() {
      this.isPause = false;
      this.story.nextIndex = this.currentStoryStore.activeSlide + 1;
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

      const index = this.currentStoryStore.listId.indexOf(
        this.currentStoryStore?.activeStory
      );

      if (this.isNext) {
        this.isPrev = false;
        this.nextStories = [];
        this.prevStories = [];

        await axios
          .get(
            `/api/story/get-text-stories/${
              this.currentStoryStore.listId[index + 1]
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
            console.log("Đã xem hết tin");
          });

        await axios
          .get(
            `/api/story/get-media-stories/${
              this.currentStoryStore.listId[index + 1]
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
            console.log("Đã xem hết tin");
          });

        this.currentStoryStore.resetActiveStory();
        this.currentStoryStore.getActiveStory(
          this.nextStories[0]?.created_by?.id
        );
        this.currentStoryStore.getActiveStoryId(this.nextStories[0]?.id);
      }
    },
    async prev() {
      this.index = this.currentStoryStore.listId.indexOf(
        this.currentStoryStore.activeStory
      );

      this.isPause = false;
      this.story.prevIndex = this.currentStoryStore.activeSlide;
      this.story.prevIndex--;

      if (this.story.prevIndex < 0) {
        this.isPrev = true;
      } else {
        this.isPrev = false;
      }

      if (this.isPrev) {
        this.isNext = false;
        this.prevStories = [];
        this.nextStories = [];
        this.index--;
        await axios
          .get(
            `/api/story/get-text-stories/${
              this.currentStoryStore.listId[this.index]
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
              this.currentStoryStore.listId[this.index]
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

        this.currentStoryStore.resetActiveStory();
        this.currentStoryStore.getActiveStory(
          this.prevStories[0]?.created_by?.id
        );
      }
    },

    pause() {
      this.isPause = !this.isPause;
    },
    mute() {
      this.isMute = !this.isMute;
    },
  },
});
</script>

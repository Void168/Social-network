<template>
  <div
    class="flex items-start absolute bottom-0 max-h-min p-4 z-50 w-full h-[90%] flex-col dark:bg-slate-800 rounded-lg"
  >
    <XMarkIcon
      class="absolute top-3 right-2 h-10 w-10 cursor-pointer p-2 hover:bg-neutral-600 rounded-full"
      @click="$emit('closeListSeen')"
    />
    <p
      class="pb-4 border-b border-slate-600 font-bold text-lg w-full text-center"
    >
      Chi tiết về tin
    </p>
    <div class="w-full">
      <TabGroup>
        <TabList class="flex space-x-1 rounded-xl p-1">
          <Tab
            v-for="emoji in emojiStory"
            as="template"
            :key="emoji.name"
            v-slot="{ selected }"
          >
            <button
              :class="[
                'w-full rounded-none py-2.5 font-medium leading-5 text-xl',
                ' focus:border-emerald-400 focus:border-b-2',
                selected
                  ? ' text-white shadow'
                  : 'text-blue-100 hover:bg-white/[0.12] hover:text-white',
              ]"
            >
              <span ref="status">{{ emoji.unicode || emoji.name }}</span>
            </button>
          </Tab>
        </TabList>

        <TabPanels class="mt-2">
          <div v-for="n in emojiStory.length" :key="n">
            <TabPanel
            v-if="n === 1"
              :class="['rounded-none p-3', 'ring-white/60 ring-offset-2']"
            >
            <div class="flex gap-3 items-center text-neutral-300/90">
              <EyeIcon class="w-6 h-5"/>
              <span class="font-bold">{{ stories[currentStoryStore.activeSlide]?.seen_by.length }} người xem</span>
            </div>
              <ul>
                <li
                  v-for="user in stories[currentStoryStore.activeSlide]?.seen_by"
                  :key="user.id"
                  class="relative rounded-md p-3 flex items-center justify-between"
                >
                  <div class="flex items-center gap-3">
                    <img
                      :src="user.get_avatar"
                      alt="avatar"
                      class="w-12 h-12 rounded-full"
                    />
                    <h3 class="text-sm font-medium leading-5">
                      {{ user.name }}
                    </h3>
                  </div>
                  <EllipsisHorizontalIcon
                    class="w-10 p-1 hover:bg-slate-600 rounded-full cursor-pointer"
                  />
                </li>
              </ul>
              <div class="flex items-center justify-center my-4">
                <p class="text-sm">Thông tin chi tiết về những người xem tin của bạn sẽ hiển thị ở đây.</p>
              </div>
            </TabPanel>
            <TabPanel
            v-else
              :class="['rounded-none p-3', 'ring-white/60 ring-offset-2']"
            >
              <ul>
                <li
                  v-for="user in stories[currentStoryStore.activeSlide]?.seen_by"
                  :key="user.id"
                  class="relative rounded-md p-3 flex items-center justify-between"
                >
                  <div class="flex items-center gap-3">
                    <img
                      :src="user.get_avatar"
                      alt="avatar"
                      class="w-12 h-12 rounded-full"
                    />
                    <h3 class="text-sm font-medium leading-5">
                      {{ user.name }}
                    </h3>
                  </div>
                  <EllipsisHorizontalIcon
                    class="w-10 p-1 hover:bg-slate-600 rounded-full cursor-pointer"
                  />
                </li>
              </ul>
              <div class="flex items-center justify-center my-4">
                <p class="text-sm">Thông tin chi tiết về những người xem tin của bạn sẽ hiển thị ở đây.</p>
              </div>
            </TabPanel>
          </div>
        </TabPanels>
      </TabGroup>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "../../../stores/user";
import { useCurrentStoryStore } from "../../../stores/currentStory";
import { XMarkIcon, EllipsisHorizontalIcon, EyeIcon } from "@heroicons/vue/24/solid";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import emojiStory from "../../../data/emoji";

export default (await import("vue")).defineComponent({
  components: {
    XMarkIcon,
    EllipsisHorizontalIcon,
    EyeIcon,
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
  },
  setup() {
    const userStore = useUserStore();
    const currentStoryStore = useCurrentStoryStore();
    return {
      userStore,
      currentStoryStore,
    };
  },

  props: {
    stories: Array,
  },

  data() {
    return {
      isOpen: false,
      emojiStory: emojiStory,
      emoji: null,
    };
  },
});
</script>

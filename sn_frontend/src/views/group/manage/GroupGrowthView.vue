<template>
  <div
    class="w-[60%] flex flex-col justify-center items-center mx-auto my-4 space-y-4"
  >
    <div class="flex justify-between items-center w-full">
      <Listbox v-model="selectedDistance">
        <div class="relative mt-1">
          <ListboxButton
            class="relative w-full cursor-default rounded-lg bg-white dark:bg-slate-700 py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm"
          >
            <span
              class="block truncate dark:text-neutral-200 font-semibold text-lg"
              >{{ selectedDistance.name }}</span
            >
            <span
              class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
            >
              <ChevronUpDownIcon
                class="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
            </span>
          </ListboxButton>

          <transition
            leave-active-class="transition duration-100 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <ListboxOptions
              class="absolute mt-1 max-h-60 min-w-max overflow-auto rounded-md bg-white dark:bg-slate-700 py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
            >
              <ListboxOption
                v-slot="{ active, selected }"
                v-for="distance in distances"
                :key="distance.name"
                :value="distance"
                as="template"
              >
                <li
                  :class="[
                    active
                      ? 'bg-emerald-100 text-emerald-900'
                      : 'text-gray-900 dark:text-neutral-200',
                    'relative cursor-default select-none py-2 pl-10 pr-4',
                  ]"
                >
                  <span
                    :class="[selected ? 'font-medium' : 'font-normal', 'block']"
                    >{{ distance.name }}</span
                  >
                  <span
                    v-if="selected"
                    class="absolute inset-y-0 left-0 flex items-center pl-3 text-emerald-600"
                  >
                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                  </span>
                </li>
              </ListboxOption>
            </ListboxOptions>
          </transition>
        </div>
      </Listbox>
      <div
        class="flex items-center px-4 py-2 font-semibold dark:bg-slate-700 rounded-lg cursor-pointer duration-75 dark:hover:bg-slate-600"
      >
        <ArrowDownTrayIcon class="w-6" />
        Tải xuống
      </div>
    </div>
    <div class="dark:bg-slate-800 w-full rounded-lg p-4 space-y-4">
      <div>
        <h3 class="text-lg font-semibold">
          Tổng số thành viên: {{ group.members_count }}
        </h3>
        <h5 class="text-sm text-neutral-400">{{ today }}</h5>
      </div>
      <TotalMember />
    </div>
    <div class="dark:bg-slate-800 w-full rounded-lg p-4 space-y-4">
      <div>
        <h3 class="text-lg font-semibold">
          Yêu cầu làm thành viên: {{ joinRequestsLength }}
        </h3>
        <h5
          class="text-sm text-neutral-400"
          v-if="selectedDistance.name === '7 ngày trước'"
        >
          {{ daySevenAgo }} - {{ today }}
        </h5>
        <h5
          class="text-sm text-neutral-400"
          v-if="selectedDistance.name === '28 ngày trước'"
        >
          {{ dayTwentyEightAgo }} - {{ today }}
        </h5>
        <h5
          class="text-sm text-neutral-400"
          v-if="selectedDistance.name === '60 ngày trước'"
        >
          {{ daySixtyAgo }} - {{ today }}
        </h5>
      </div>
      <JoinRequest
        :setJoinRequestLength="setJoinRequestLength"
        :selectedDays="selectedDistance.name"
      />
      <div class="flex justify-center items-center">
        <RouterLink
          :to="{ name: 'groupjoinrequest', params: { id: group.id } }"
          class="px-4 py-2 dark:bg-slate-600 rounded-lg max-w-max font-semibold cursor-pointer dark:hover:bg-slate-500 duration-75"
        >
          Xem tất cả yêu cầu làm thành viên
        </RouterLink>
      </div>
    </div>
    <div class="flex flex-col gap-4 w-full">
      <div class="dark:bg-slate-800 rounded-lg p-4 space-y-4">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold" v-if="selected === categories[0]">
              Bài viết: {{ postsLength }}
            </h3>
            <h3 class="text-lg font-semibold" v-if="selected === categories[1]">
              Bình luận: {{ commentsLength }}
            </h3>
            <h3 class="text-lg font-semibold" v-if="selected === categories[2]">
              Cảm xúc: {{ likesLength }}
            </h3>
            <h5
              class="text-sm text-neutral-400"
              v-if="selectedDistance.name === '7 ngày trước'"
            >
              {{ daySevenAgo }} - {{ today }}
            </h5>
            <h5
              class="text-sm text-neutral-400"
              v-if="selectedDistance.name === '28 ngày trước'"
            >
              {{ dayTwentyEightAgo }} - {{ today }}
            </h5>
            <h5
              class="text-sm text-neutral-400"
              v-if="selectedDistance.name === '60 ngày trước'"
            >
              {{ daySixtyAgo }} - {{ today }}
            </h5>
          </div>
          <div class="flex space-x-1 rounded-xl bg-slate-700 p-1">
            <div v-for="category in categories" :key="category">
              <button
                @click="getCategory(category)"
                :class="[
                  'min-w-max rounded-lg px-4 py-2 text-sm font-medium leading-5 ',
                  'ring-slate-600/60 focus:outline-none focus:ring-2 ',
                  selected === category
                    ? 'bg-white dark:bg-slate-500 dark:text-neutral-200 shadow'
                    : 'dark:text-neutral-200 hover:bg-white/[0.12] hover:text-white',
                ]"
              >
                {{ category }}
              </button>
            </div>
          </div>
        </div>
        <Post
          v-if="selected === categories[0]"
          :selectedDays="selectedDistance.name"
          :setPostsLength="setPostsLength"
        />
        <Comment
          v-if="selected === categories[1]"
          :selectedDays="selectedDistance.name"
          :setCommentsLength="setCommentsLength"
        />
        <Like
          v-if="selected === categories[2]"
          :selectedDays="selectedDistance.name"
          :setLikesLength="setLikesLength"
        />
      </div>
      <div class="dark:bg-slate-800 rounded-lg p-4 space-y-4">
        <div>
          <h3 class="text-lg font-semibold">
            Thành viên hoạt động: {{ group.members_count }}
          </h3>
          <h5
            class="text-sm text-neutral-400"
            v-if="selectedDistance.name === '7 ngày trước'"
          >
            {{ daySevenAgo }} - {{ today }}
          </h5>
          <h5
            class="text-sm text-neutral-400"
            v-if="selectedDistance.name === '28 ngày trước'"
          >
            {{ dayTwentyEightAgo }} - {{ today }}
          </h5>
          <h5
            class="text-sm text-neutral-400"
            v-if="selectedDistance.name === '60 ngày trước'"
          >
            {{ daySixtyAgo }} - {{ today }}
          </h5>
        </div>
        <ActiveMember />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

import TotalMember from "../../../components/items/group/chart/TotalMember.vue";
import JoinRequest from "../../../components/items/group/chart/JoinRequest.vue";
import Post from "../../../components/items/group/chart/Post.vue";
import Comment from "../../../components/items/group/chart/Comment.vue";
import Like from '../../../components/items/group/chart/Like.vue';
import ActiveMember from "../../../components/items/group/chart/ActiveMember.vue";

import {
  Listbox,
  ListboxLabel,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from "@headlessui/vue";
import {
  CheckIcon,
  ChevronUpDownIcon,
  ArrowDownTrayIcon,
} from "@heroicons/vue/20/solid";

export default {
  name: "groupgrowth",
  components: {
    TotalMember,
    JoinRequest,
    Post,
    Comment,
    Like,
    ActiveMember,
    Listbox,
    ListboxLabel,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
    CheckIcon,
    ChevronUpDownIcon,
    ArrowDownTrayIcon,
  },
  setup() {
    const categories = ["Bài viết", "Bình luận", "Cảm xúc"];
    const selected = ref(categories[0]);

    const distances = [
      { name: "7 ngày trước" },
      { name: "28 ngày trước" },
      { name: "60 ngày trước" },
    ];
    const selectedDistance = ref(distances[0]);

    let today = new Date();
    const dd = String(today.getDate()).padStart(2, "0");
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const yyyy = today.getFullYear();

    let timeFrom = (X) => {
      const day = new Date(new Date().getTime() - X * 24 * 60 * 60 * 1000);
      return day;
    };

    let daySevenAgo = timeFrom(6);
    const sevenDD = String(timeFrom(6).getDate()).padStart(2, "0");
    const sevenMM = String(timeFrom(6).getMonth() + 1).padStart(2, "0");
    const sevenYYYY = timeFrom(6).getFullYear();

    let dayTwentyEightAgo = timeFrom(27);
    const twentyEightDD = String(timeFrom(27).getDate()).padStart(2, "0");
    const twentyEightMM = String(timeFrom(27).getMonth() + 1).padStart(2, "0");
    const twentyEightYYYY = timeFrom(27).getFullYear();

    let daySixtyAgo = timeFrom(59);
    const sixtyDD = String(timeFrom(59).getDate()).padStart(2, "0");
    const sixtyMM = String(timeFrom(59).getMonth() + 1).padStart(2, "0");
    const sixtyYYYY = timeFrom(59).getFullYear();

    today = dd + " Tháng " + mm + ", " + yyyy;
    daySevenAgo = sevenDD + " Tháng " + sevenMM + ", " + sevenYYYY;
    dayTwentyEightAgo =
      twentyEightDD + " Tháng " + twentyEightMM + ", " + twentyEightYYYY;
    daySixtyAgo = sixtyDD + " Tháng " + sixtyMM + ", " + sixtyYYYY;

    return {
      today,
      selectedDistance,
      distances,
      daySevenAgo,
      dayTwentyEightAgo,
      daySixtyAgo,
      categories,
      selected,
    };
  },
  props: {
    group: Object,
  },

  data() {
    return {
      joinRequestsLength: 0,
      postsLength: 0,
      commentsLength: 0,
      likesLength: 0,
    };
  },

  methods: {
    setJoinRequestLength(data) {
      this.joinRequestsLength = data;
    },
    setPostsLength(data) {
      this.postsLength = data;
    },
    setCommentsLength(data) {
      this.commentsLength = data;
    },
    setLikesLength(data) {
      this.likesLength = data;
    },
    getCategory(data) {
      this.selected = data;
    },
  },
};
</script>

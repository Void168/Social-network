<template>
  <div
  v-if="isOpen"
    class="flex flex-col h-[480px] w-[400px] bg-slate-200 dark:bg-slate-500 rounded-t-lg"
  >
    <div
      class="h-16 border-b-2 border-slate-400 dark:border-slate-300 flex justify-between"
    >
      <div
        class="flex p-4 gap-2 items-center hover:bg-slate-600 hover:rounded-lg transition duration-75 cursor-pointer"
      >
        <img :src="friend.get_avatar" class="rounded-full h-10 w-10" />
        <span class="font-bold">{{ friend.name }}</span>
        <ChevronDownIcon class="w-6 h-6 rounded-full hover:bg-slate-600 p-1" />
      </div>
      <div class="flex gap-1 p-4">
        <VideoCameraIcon
          class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
        />
        <PhoneIcon
          class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
        />
        <MinusIcon
          @click="$emit('miniatureChat')"
          class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
        />
        <div @click="$emit('removeFriendChat')">
            <!-- v-on:click="closeConversationBubble" -->
            <XMarkIcon
              class="w-8 h-8 rounded-full hover:bg-slate-600 p-1 transition cursor-pointer"
            />
        </div>
      </div>
    </div>
    <div
      class="h-[346px] p-4 overflow-y-scroll scrollbar-none scrollbar scrollbar-corner-slate-200 hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 border border-gray-200 shadow-md dark:bg-slate-600 dark:border-slate-700 dark:text-neutral-200"
    >
      fgsgds
    </div>
    <div
      class="relative h-16 p-4 border-t-2 border-slate-400 dark:border-slate-300"
    >
      <span class="absolute right-12 p-4 top-2 z-10">
        <Popover class="relative">
          <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-y-1 opacity-0"
            enter-to-class="translate-y-0 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 opacity-100"
            leave-to-class="translate-y-1 opacity-0"
            ><PopoverPanel
              class="absolute z-10 bottom-10 right-0 shadow-2xl rounded-lg"
              @click="Pick"
            >
              <emoji-picker></emoji-picker>
            </PopoverPanel>
          </transition>

          <PopoverButton>
            <FaceSmileIcon class="w-6 h-6" />
          </PopoverButton>
        </Popover>
      </span>
      <form
        v-on:submit.prevent="submitForm"
        @keyup.enter="submitForm"
        class="flex items-center justify-between gap-1"
      >
        <div class="flex gap-1">
          <PlusCircleIcon
            class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
          />
          <PhotoIcon
            class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
          />
          <GifIcon
            class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
          />
        </div>
        <div class="relative flex items-center gap-2">
          <textarea
            v-model="body"
            class="w-full py-2 px-4 bg-gray-100 rounded-3xl resize-none"
            name=""
            id=""
            cols="30"
            rows="1"
            placeholder="Bạn muốn nói điều gì?"
          ></textarea>
          <button class="" type="submit">
            <PaperAirplaneIcon
              class="w-8 h-8 cursor-pointer rounded-full text-emerald-300 hover:bg-slate-600 transition p-1"
            />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { RouterLink } from "vue-router";

import {
  XMarkIcon,
  MinusIcon,
  PhoneIcon,
  VideoCameraIcon,
  ChevronDownIcon,
  PaperAirplaneIcon,
  PlusCircleIcon,
  PhotoIcon,
  GifIcon,
  FaceSmileIcon,
} from "@heroicons/vue/24/solid";

import "emoji-picker-element";

import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    RouterLink,
    Popover,
    PopoverButton,
    PopoverPanel,
    XMarkIcon,
    MinusIcon,
    PhoneIcon,
    VideoCameraIcon,
    ChevronDownIcon,
    PaperAirplaneIcon,
    PlusCircleIcon,
    PhotoIcon,
    GifIcon,
    FaceSmileIcon,
  },

  props: {
    friend: Object,
    conversation: Object,
  },

  data() {
    return {
      friendsChat: [],
      body: "",
      isOpen: true
    };
  },

  methods: {
    Pick() {
      document
        .querySelector("emoji-picker")
        .addEventListener("emoji-click", (event) => {
          this.body = this.body + event.detail.unicode;

          return this.body;
        });
    },
  },
});
</script>

<template>
  <div class="space-y-2 break-words">
    <div
      v-for="option in options"
      :key="option.id"
      class="p-2 flex justify-between items-center dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
      @click="$emit('getOption', option)"
    >
      <div class="flex gap-2 items-center w-[80%]">
        <EyeIcon
          class="xm:w-10 w-6 xm:p-2 p-1 rounded-full dark:bg-slate-600 bg-slate-100"
          v-if="option.id === 1"
        />
        <EyeSlashIcon class="xm:w-10 w-6 xm:p-2 p-1 rounded-full dark:bg-slate-600 bg-slate-100" v-else />
        <div class="flex flex-col gap-1">
          <h4 class="font-medium xm:text-base text-sm">{{ option.name }}</h4>
          <h5 class="xm:text-sm text-xs">{{ option.content }}</h5>
        </div>
      </div>
      <div class="relative sm:w-10 sm:h-10 h-6 w-6 rounded-full dark:bg-slate-600 bg-slate-200">
        <span
          class="absolute sm:w-5 sm:h-5 h-3 w-3 bg-emerald-500 rounded-full sm:top-[10px] sm:left-[10px] top-[6px] left-[6px]"
          v-if="selectedOption && option.id === 1"
        ></span>
        <span
          class="absolute sm:w-5 sm:h-5 h-3 w-3 bg-emerald-500 rounded-full sm:top-[10px] sm:left-[10px] top-[6px] left-[6px]"
          v-if="!selectedOption && option.id === 2"
        ></span>
      </div>
    </div>
    <div class="flex justify-end items-center gap-2">
      <button
        @click="$emit('toggle')"
        class="xm:px-4 xm:py-2 px-2 py-1 font-medium text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75 rounded-lg"
      >
        Hủy
      </button>
      <button
        @click="$emit('submit')"
        class="xm:px-4 xm:py-2 px-2 py-1 font-medium rounded-lg"
        :class="'text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75'"
      >
        Lưu
      </button>
    </div>
  </div>
</template>

<script>
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/20/solid";
export default (await import("vue")).defineComponent({
  components: {
    EyeIcon,
    EyeSlashIcon,
  },
  props: {
    options: Array,
    selectedOption: Boolean,
  },
});
</script>

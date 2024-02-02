<template>
  <div class="w-full space-y-2">
    <div
      v-for="option in options"
      :key="option.id"
      class="p-2 flex justify-between items-center dark:hover:bg-slate-700 rounded-lg duration-75 cursor-pointer"
      @click="$emit('getOption', option)"
    >
      <div class="flex gap-2 items-center">
        <EyeIcon
          class="w-10 p-2 rounded-full bg-slate-600"
          v-if="option.id === 1"
        />
        <EyeSlashIcon class="w-10 p-2 rounded-full bg-slate-600" v-else />
        <div class="flex flex-col gap-1">
          <h4 class="font-medium">{{ option.name }}</h4>
          <h5 class="text-sm">{{ option.content }}</h5>
        </div>
      </div>
      <div class="relative w-10 h-10 rounded-full dark:bg-slate-600">
        <span
          class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
          v-if="selectedOption && option.id === 1"
        ></span>
        <span
          class="absolute w-5 h-5 bg-emerald-500 rounded-full top-[10px] left-[10px]"
          v-if="!selectedOption && option.id === 2"
        ></span>
      </div>
    </div>
    <div class="flex justify-end items-center gap-2">
      <button
        @click="$emit('toggle')"
        class="px-4 py-2 font-medium text-emerald-500 dark:bg-slate-700 dark:hover:bg-slate-600 duration-75 rounded-lg"
      >
        Hủy
      </button>
      <button
        class="px-4 py-2 font-medium rounded-lg"
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

<template>
  <div
    class="w-full xs:min-h-[700px] xs:px-4"
  >
  <div class="lg:w-[80%] mx-auto gap-4 xs:my-6 bg-white dark:bg-slate-700 p-4 xs:rounded-md dark:text-neutral-200">
      <div class="flex justify-between items-center xm:flex-nowrap flex-wrap">
        <h2 class="text-xl font-semibold">File</h2>
        <div class="flex items-center xm:gap-4 gap-2 xm:flex-nowrap flex-wrap">
          <div class="relative w-full">
            <MagnifyingGlassIcon
              class="absolute top-[18px] left-2 sm:w-6 sm:h-6 vs:w-3 vs:h-3 dark:text-neutral-400"
            />
            <input
              ref="input"
              type="text"
              placeholder="Tìm kiếm file"
              class="w-full my-2 sm:py-2 sm:px-8 vs:py-1 vs:px-6 border border-gray-200 dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 rounded-2xl sm:text-base xs:text-sm"
            />
          </div>
          <div
            class="px-4 py-2 font-semibold text-emerald-400 dark:bg-slate-600 dark:hover:bg-slate-500 duration-75 cursor-pointer rounded-lg sm:text-base text-sm w-full text-center"
          >
            Tải file lên
          </div>
        </div>
      </div>
      <hr class="border border-slate-600 my-2"/>
      <div class="flex sm:flex-nowrap	flex-wrap gap-2 items-center px-4 my-4">
          <div class="flex justify-center items-center w-full dark:bg-slate-600 py-2 font-semibold  sm:text-base text-sm px-4 rounded-lg">
              TÊN FILE
          </div>
          <div class="flex justify-center items-center sm:max-w-max dark:bg-slate-600 py-2 font-semibold  sm:text-base text-sm px-4 w-full rounded-lg">
              LOẠI
          </div>
          <div class="flex justify-center items-center sm:max-w-max dark:bg-slate-600 py-2 font-semibold  sm:text-base text-sm px-4 w-full rounded-lg">
              LẦN SỬA ĐỔI GẦN ĐÂY
          </div>
      </div>
  </div>
  </div>
</template>

<script>
import { MagnifyingGlassIcon } from "@heroicons/vue/24/solid";

export default {
  name: "groupfile",
  components: {
    MagnifyingGlassIcon,
  },
};
</script>

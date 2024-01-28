<template>
  <div
    class="relative rounded-lg dark:bg-slate-700 dark:border-slate-600 border p-4"
  >
    <div class="flex items-center gap-2">
      <img
        src="https://s3.amazonaws.com/intanibase/iad_screenshots/1951/3523/6thumb.jpg"
        alt=""
        class="rounded-lg h-20 w-20"
      />
      <div class="flex flex-col space-y-2">
        <h4 class="font-semibold">Cats</h4>
        <h5 class="text-sm">Lần truy cập gần đây nhất: 5 giờ trước</h5>
      </div>
    </div>
    <div class="mt-4 flex items-center justify-center gap-2 w-full">
      <div class="flex items-center justify-center w-full">
        <button
          class="py-2 w-full dark:bg-slate-800 rounded-lg dark:hover:bg-slate-900 font-semibold duration-75"
        >
          Xem nhóm
        </button>
        <EllipsisHorizontalIcon class="w-10" />
      </div>
    </div>
  </div>
</template>

<script>
import { EllipsisHorizontalIcon } from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    EllipsisHorizontalIcon,
  },
});
</script>

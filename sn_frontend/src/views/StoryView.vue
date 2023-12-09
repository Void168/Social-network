<template>
  <div class="bg-slate-800 text-neutral-200 h-screen grid grid-cols-5">
    <div class="col-span-1 bg-slate-800">
      <div class="p-4 border-b border-slate-700">
        <RouterLink to="/">
          <XMarkIcon
            class="text-neutral-200 h-10 w-10 cursor-pointer transition p-2 bg-slate-700 rounded-full hover:bg-slate-600"
          />
        </RouterLink>
      </div>
      <div class="p-4">
        <h2 class="text-2xl font-bold">Tin</h2>
        <div class="mt-4">
          <a href="#" class="text-emerald-400 hover:text-emerald-500">Kho lưu trữ</a>
          &middot;
          <a href="#" class="text-emerald-400 hover:text-emerald-500">Cài đặt</a>
        </div>
        <div class="my-4 flex flex-col space-y-4">
          <h2 class="text-xl font-semibold">Tin của bạn</h2>
          <div class="flex gap-3 items-center">
            <PlusIcon
              class="text-emerald-300 h-16 w-16 cursor-pointer transition p-3 bg-slate-700 rounded-full hover:bg-slate-600"
            />
            <div class="flex flex-col space-y-1">
              <h4 class="font-semibold text-lg">Tạo tin</h4>
              <p class="text-neutral-400">Bạn có thể tạo ảnh hoặc viết gì đó</p>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div class="px-4 py-2">
          <h2 class="text-xl font-semibold">Tất cả tin</h2>
        </div>
      </div>
    </div>
    <div class="col-span-4 bg-slate-900"></div>
  </div>
</template>

<script>
import { RouterLink } from "vue-router";
import { XMarkIcon, PlusIcon } from "@heroicons/vue/24/solid";
export default {
  name: "StoryView",
  components: {
    RouterLink,
    XMarkIcon,
    PlusIcon,
  },
};
</script>

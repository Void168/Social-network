<template>
  <div class="relative rounded-lg dark:bg-slate-700 dark:border-slate-600 border">
    <img
      src="https://s3.amazonaws.com/intanibase/iad_screenshots/1951/3523/6thumb.jpg"
      alt=""
      class="w-full rounded-t-lg"
    />
    <div class="px-4 py-2 flex flex-col justify-between gap-4">
      <div>
        <h3 class="font-semibold text-lg">Cats</h3>
        <h4 class="">168K thành viên &middot; Hơn 10 bài viết/ngày</h4>
      </div>
      <div class="flex items-center justify-center">
        <button class="py-2 w-full dark:bg-slate-800 rounded-lg dark:hover:bg-slate-900 font-semibold duration-75">
          Tham gia nhóm
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default (await import("vue")).defineComponent({});
</script>

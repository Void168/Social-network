<template>
  <div
    class="absolute md:top-[-50px] top-[-50px] left-[-90px] group-hover:block hidden dark:text-slate-200 dark:bg-slate-800 bg-slate-200 min-w-max z-20 p-2 rounded-xl before:content-[''] before:w-0 before:h-0 before:border-l-[5px] before:border-r-[5px] before:border-t-[10px] before:dark:border-t-slate-800 before:border-l-transparent before:border-r-transparent before:top-10 before:inset-x-[50%] before:absolute before:border-t-slate-200"
  >
    <p class="flex gap-1">
      <span>Đã chia sẻ với</span>
      <span v-if="post.is_private === false && post.only_me === false"
        >công khai</span
      >
      <span v-if="post.is_private === true && post.only_me === false"
        >bạn bè</span
      >
      <span v-if="post.is_private === true && post.only_me === true"
        >chỉ mình tôi</span
      >
    </p>
  </div>
</template>

<script>
export default (await import("vue")).defineComponent({
  props: {
    post: Object,
  },
});
</script>

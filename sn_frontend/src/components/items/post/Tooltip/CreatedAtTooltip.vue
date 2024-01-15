<template>
  <div
    class="absolute md:top-[-50px] top-[-50px] left-[-30px] group-hover:block hidden dark:text-slate-200 dark:bg-slate-800 bg-slate-200 min-w-max z-20 p-2 rounded-xl before:content-[''] before:w-0 before:h-0 before:border-l-[5px] before:border-r-[5px] before:border-t-[10px] before:dark:border-t-slate-800 before:border-l-transparent before:border-r-transparent before:top-10 before:inset-x-[50%] before:absolute before:border-t-slate-200"
  >
    {{ post?.created_at?.slice(11, 19) }} ngày
    {{ post?.created_at?.slice(0, 10)?.split("-").reverse().join("-") }}
  </div>
</template>

<script>
export default (await import("vue")).defineComponent({
  props: {
    post: Object,
  },
});
</script>

<template>
    <div class="flex flex-col items-center">
        <div @click="$emit('chooseTheme')" class="rounded-full xm:h-24 xm:w-24 xs:h-16 xs:w-16 h-10 w-10 shadow-md cursor-pointer" :class="[color.background]"></div>
        <p class="dark:text-neutral-200 font-semibold xm:text-base text-xs">{{ color.name }}</p>
    </div>
</template>

<script>
export default (await import("vue")).defineComponent({
  props: {
    color: Object,
  },
});
</script>

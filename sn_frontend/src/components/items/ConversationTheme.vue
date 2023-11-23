<template>
    <div class="flex flex-col items-center">
        <div @click="$emit('chooseTheme')" class="rounded-full h-24 w-24 shadow-md cursor-pointer" :class="[color.background]"></div>
        <p class="dark:text-neutral-200 font-semibold">{{ color.name }}</p>
    </div>
</template>

<script>
export default (await import("vue")).defineComponent({
  props: {
    color: Object,
  },
});
</script>

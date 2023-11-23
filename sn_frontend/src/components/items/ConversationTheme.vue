<template>
    <div class="flex flex-col items-center">
        <div @click="chooseTheme" class="rounded-full h-24 w-24 shadow-md cursor-pointer" :class="[color.background, isChoose ? 'ring-2 ring-white' : '']"></div>
        <p class="dark:text-neutral-200 font-semibold">{{ color.name }}</p>
    </div>
</template>

<script>
export default (await import("vue")).defineComponent({
  props: {
    color: Object,
  },

  data() {
    return {
        isChoose: false
    }
  },

  methods: {
    chooseTheme() {
        this.isChoose = !this.isChoose
    }
  }
});
</script>

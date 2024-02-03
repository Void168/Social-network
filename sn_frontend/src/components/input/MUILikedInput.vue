<template>
  <div class="relative">
    <input
      class="p-4 w-full bg-gray-100 dark:bg-slate-800 rounded-lg resize-none border dark:border-slate-600"
      :placeholder="isFocus ? '' : `${placeholder}`"
      @focus="focusIn"
      @focusout="focusOut"
      :value="modelValue"
      :type="type"
      @input="$emit('update:modelValue', $event.target.value)"
      required
    />
    <span
      class="absolute left-4 text-xs top-1 text-emerald-400"
      v-if="isFocus"
      >{{ placeholder }}</span
    >
  </div>
</template>

<script>
export default {
  props: {
    placeholder: String,
    modelValue: String,
    type: String,
  },
  emits: ['update:modelValue'],
  data(){
    return {
      isFocus: false,
    }
  },

  methods: {
    focusIn(){
      this.isFocus = true
    }, 
    focusOut(){
      this.isFocus = false
    }
  },
};
</script>

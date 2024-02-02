<template>
  <div
    class="flex"
    :class="
      isOpen
        ? 'flex-col justify-start items-start gap-2'
        : 'items-center justify-between'
    "
  >
    <div class="space-y-1">
      <h3 class="text-lg font-semibold">{{ name }}</h3>
      <h5 class="text-sm" v-if="!isOpen">
        {{ selectedOption ? options[0]?.content : options[1]?.content }}
      </h5>
    </div>
    <PencilIcon
      v-if="!isOpen"
      @click="$emit('toggle')"
      class="w-8 dark:text-neutral-400 cursor-pointer p-1 rounded-full hover:dark:bg-slate-600 duration-75"
    />
    <div v-else class="w-full">
      <CustomListRadio
        :options="options"
        :selectedOption="selectedOption"
        @getOption="getOption"
        @click="$emit('getOption', option)"
        @toggle="$emit('toggle')"
        @submit="$emit('submit')"
      />
    </div>
  </div>
</template>

<script>
import { PencilIcon } from "@heroicons/vue/20/solid";
import CustomListRadio from "../../input/CustomListRadioButton.vue";

export default (await import("vue")).defineComponent({
  components:{
    PencilIcon,
    CustomListRadio
  },
  props: {
    name: String,
    group: Object,
    isOpen: Boolean,
    options: Array,
    selectedOption: Boolean,
  },

  data(){
    return {
      option: {}
    }
  },

  methods: {
    getOption(data){
      this.option = data
    }
  }
});
</script>

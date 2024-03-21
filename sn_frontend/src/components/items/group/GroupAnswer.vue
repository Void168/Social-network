<template>
  <div class="dark:text-neutral-200">
    <div class="flex justify-between items-center">
      <div>
        <h3>Câu hỏi {{ index }}</h3>
        <h4 class="font-bold">
          {{ question.body }}
        </h4>
      </div>
      <EllipsisHorizontalIcon
        class="w-10 p-1 rounded-full dark:hover:bg-slate-800 duration-75 cursor-pointer"
      />
    </div>
    <div class="my-2">
      <textarea
        @keyup="$emit('getAnswer', answer, index)"
        type="text"
        class="form-control w-full p-4 rounded-lg resize-none"
        rows="2"
        v-model="answer"
        placeholder="Viết câu trả lời..."
      ></textarea>
    </div>
  </div>
</template>

<script>
import { EllipsisHorizontalIcon } from "@heroicons/vue/24/solid";
export default (await import("vue")).defineComponent({
  components: {
    EllipsisHorizontalIcon,
  },
  props: {
    question: Object,
    index: Number,
  },
  data() {
    return {
      answer: "",
    };
  },
});
</script>

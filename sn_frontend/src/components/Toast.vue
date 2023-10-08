<template>
  <div
    v-if="store.isVisible"
    class="transition ease-in-out delay-500 duration-150 px-6 py-3 fixed right-8 rounded-xl shadow-xl"
    :class="store.classes"
  >
    {{ store.messages }}
  </div>
</template>

<script setup>
import { useToastStore } from "@/stores/toast";

const store = useToastStore();

return {
  store,
};
</script>

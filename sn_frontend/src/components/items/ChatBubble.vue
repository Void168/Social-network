<template>
  <div v-if="isOpen">
    <div class="relative group my-1">
        <XMarkIcon @click="closeConversationBubble" class="p-1 hidden dark:text-neutral-200 rounded-full dark:bg-slate-500 text-slate-700 group-hover:block w-6 h-6 absolute z-50 top-[-0.75rem]  right-[-0.25rem] cursor-pointer"/>
        <img :src="friend.get_avatar" class="w-12 h-12 rounded-full shadow-md cursor-pointer" @click="$emit('openChatWindow')"/>
    </div>
  </div>
</template>

<script>
import { XMarkIcon } from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    XMarkIcon,
  },

  props: {
    friend: Object,
  },

  data() {
    return {
      isOpen: true,
    };
  },

  methods: {
    closeConversationBubble() {
      this.isOpen = false;
      //   this.friendsChat = this.friendsChat?.pop(friend);
    },
  },
});
</script>

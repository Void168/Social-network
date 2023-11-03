<template id="card-template">
  <div class="card bg-gray-100 rounded-lg p-4 h-48 my-4 shadow-md">
    <div class="header">
      <div class="header-img skeleton" />
      <div
        class="title font-bold text-lg capitalize whitespace-nowrap"
        data-title
      >
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
      </div>
    </div>
    <div data-body>
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-text"></div>
    </div>
    <div class="flex mt-4">
      <HeartLike class="w-6 h-6 text-gray-300 skeleton-button" />
      <ChatBubbleOvalLeftIcon class="w-6 h-6 text-gray-300 skeleton-button" />
    </div>
  </div>
</template>

<script>
import {
  HeartIcon as HeartLike,
  ChatBubbleOvalLeftIcon,
} from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    HeartLike,
    ChatBubbleOvalLeftIcon,
  },
});
</script>

<style scoped>
.skeleton {
  opacity: 0.7;
  animation: skeleton-loading 1s linear infinite alternate;
}

.skeleton-text {
  width: 100%;
  height: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 0.125rem;
}

.skeleton-button {
  animation: skeleton-loading-text 1s linear infinite alternate;
}

.skeleton-text:last-child {
  margin-bottom: 0;
  width: 80%;
}

@keyframes skeleton-loading {
  0% {
    background-color: hsl(200, 20%, 70%);
  }

  100% {
    background-color: hsl(200, 20%, 95%);
  }
}

@keyframes skeleton-loading-text {
  0% {
    color: hsl(200, 20%, 70%);
  }

  100% {
    color: hsl(200, 20%, 95%);
  }
}

.header {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.header-img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 100%;
  margin-right: 1rem;
  flex-shrink: 0;
}

.title {
  word-wrap: none;
  text-overflow: ellipsis;
  overflow: hidden;
  flex-grow: 1;
}
</style>

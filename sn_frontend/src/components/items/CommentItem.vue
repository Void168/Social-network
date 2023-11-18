<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-start space-x-6 w-full">
        <img
          :src="comment.created_by.get_avatar"
          class="w-10 h-10 rounded-full"
        />
        <div
          class="flex justify-between border-none bg-gray-200 dark:bg-slate-700 dark:border-slate-800 dark:text-neutral-200 rounded-2xl w-full p-4"
        >
          <div>
            <p>
              <strong>
                <RouterLink
                  :to="{
                    name: 'profile',
                    params: { id: comment.created_by.id },
                  }"
                  >{{ comment.created_by.name }}</RouterLink
                >
              </strong>
            </p>
            <div class="flex gap-1">
              <p
                v-for="word in words"
                :key="word"
                :class="filteredTags.includes(word) ? 'text-emerald-400' : ''"
              >
                <RouterLink v-if="filteredTags.includes(word)" :to="{
                    name: 'profile',
                    params: { id: tags.filter((tag) => word.includes(tag.name))[0].id },
                  }">
                  {{ word }}
                </RouterLink>
                <span v-else>{{ word }}</span>
              </p>
            </div>
          </div>
          <p class="text-gray-600 dark:text-neutral-200">
            {{ comment.created_at_formatted }} trước
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  props: {
    comment: Object,
  },
  data() {
    return {
      tags: this.comment.tags,
      filteredTags: [],
    };
  },
  computed: {
    words() {
      return this.comment.body.split(" ");
    },
  },

  mounted() {
    this.checkTag();
  },

  methods: {
    checkTag() {
      const tagNames = this.tags.map((tag) => tag.name);
      tagNames.forEach((name) => {
        const filter = this.words.filter((word) => word.includes(name));
        this.filteredTags.push(...filter);
      });
    },
  },
  components: { RouterLink },
});
</script>

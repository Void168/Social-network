<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-start space-x-6 w-full">
        <img
          :src="comment.created_by.get_avatar"
          class="w-10 h-10 rounded-full"
        />
        <div class="flex justify-between border-none bg-gray-200 rounded-2xl w-full p-4">
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
            <p>{{ comment.body }}</p>
          </div>

          <p class="text-gray-600">{{ comment.created_at_formatted }} trước</p>
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
  components: { RouterLink },
});
</script>

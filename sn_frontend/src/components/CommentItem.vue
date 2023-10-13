<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-start space-x-6 w-full">
        <img
          src="https://i.pinimg.com/736x/fa/81/55/fa81555d2190e9c91a7d584ce7174a5f.jpg"
          class="w-[40px] rounded-full"
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

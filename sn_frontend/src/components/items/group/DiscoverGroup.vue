<template>
  <div class="relative rounded-lg dark:bg-slate-700 dark:border-slate-600 border">
    <RouterLink :to="{name: 'groupdetail', params: {id: group?.id}}">
      <img
        :src="group?.get_cover_image"
        alt=""
        class="w-full rounded-t-lg max-h-56"
      />
      <div class="px-4 py-2 flex flex-col justify-between gap-4">
        <div>
          <h3 class="font-semibold text-lg">{{ group?.name }}</h3>
          <h4 class="">{{ group?.members_count }} thành viên &middot; Hơn 10 bài viết/ngày</h4>
        </div>
      </div>
    </RouterLink>
    <div class="flex items-center justify-center px-4 py-2 ">
      <button class="py-2 w-full dark:bg-slate-800 rounded-lg dark:hover:bg-slate-900 font-semibold duration-75">
        Tham gia nhóm
      </button>
    </div>
  </div>
</template>

<script>
import { useToastStore } from "../../../stores/toast";
import { useUserStore } from "../../../stores/user";
import { RouterLink } from "vue-router";
export default (await import("vue")).defineComponent({
  components: {
    RouterLink
  },
  setup(){
    const userStore = useUserStore()
    const toastStore = useToastStore()

    return {
      userStore,
      toastStore
    }
  },
  props: {
    group: Object
  }
});
</script>

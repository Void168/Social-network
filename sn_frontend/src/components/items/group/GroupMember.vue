<template>
    <div class="dark:bg-slate-700 rounded-lg w-full flex xm:flex-row flex-col justify-between gap-2 xm:items-center p-4">
        <RouterLink
          :to="{
            name: 'profile',
            params: { id: member?.information?.id },
          }"
          class="flex items-center gap-2"
        >
          <img
          loading="lazy"
            :src="member?.information?.get_avatar"
            alt="admin-avatar"
            class="xm:w-16 xm:h-16 h-10 w-10 rounded-full"
          />
          <div>
            <h3 class="font-semibold">
              {{ member?.information?.name }}
            </h3>
            <h4 class="text-sm">Làm việc tại</h4>
          </div>
        </RouterLink>
        <div
        class="bg-emerald-600/40 text-emerald-300 font-semibold px-4 py-2 xm:text-base text-sm rounded-lg hover:bg-emerald-300/30 cursor-pointer text-center"
      >
        Thêm bạn bè
      </div>
    </div>
</template>

<script>
import { RouterLink } from "vue-router";
export default(await import("vue")).defineComponent({
    components: {
        RouterLink
    },
    props: {
        member: Object
    }
})
</script>

<template>
  <div
    class="dark:bg-slate-900 bg-slate-200 flex flex-col gap-4 relative items-center pt-6 py-12 px-6 w-[50%]"
  >
    <div v-for="n in 3" :key="n" class="dark:bg-slate-700 rounded-lg w-full flex justify-between items-center px-4 py-2">
      <div class="flex items-center gap-2">
        <img
          :src="userStore?.user?.avatar"
          alt="admin-avatar"
          class="w-16 h-16 rounded-full"
        />
        <div>
          <h3 class="font-semibold">
            {{ userStore?.user?.name }}
          </h3>
          <h4 class="text-sm">Làm việc tại</h4>
        </div>
      </div>
      <div class="bg-emerald-600/40 text-emerald-300 font-semibold px-4 py-2 rounded-lg hover:bg-emerald-300/30 cursor-pointer">Thêm bạn bè</div>
    </div>
    <div v-for="n in 3" :key="n" class="dark:bg-slate-700 rounded-lg px-4">
      <GroupPost />
    </div>
  </div>
</template>

<script>
import GroupPost from "../../components/items/group/GroupPost.vue";
import { useUserStore } from "../../stores/user";
export default {
  name: "groupsearch",
  components: {
    GroupPost,
  },

  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
};
</script>

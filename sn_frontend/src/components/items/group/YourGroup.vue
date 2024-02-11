<template>
  <div
    class="relative rounded-lg dark:bg-slate-700 dark:border-slate-600 border p-4"
  >
    <div class="flex items-center gap-2">
      <RouterLink
        :to="{ name: 'groupdetail', params: { id: yourGroup.id } }"
        @click="accessGroup"
      >
        <img
          :src="yourGroup.get_cover_image"
          alt=""
          class="rounded-lg h-20 w-20"
        />
      </RouterLink>
      <div class="flex flex-col space-y-2">
        <RouterLink
          @click="accessGroup"
          :to="{ name: 'groupdetail', params: { id: yourGroup.id } }"
          class="hover:underline"
        >
          <h4 class="font-semibold">{{ yourGroup.name }}</h4>
        </RouterLink>
        <h5 class="text-sm">Lần truy cập gần đây nhất: {{ currentMember.last_access_formatted }} trước</h5>
      </div>
    </div>
    <div class="mt-4 flex items-center justify-center gap-2 w-full">
      <div class="flex items-center justify-center w-full">
        <RouterLink
          :to="{ name: 'groupdetail', params: { id: yourGroup.id } }"
          class="w-full"
          @click="accessGroup"
        >
          <button
            class="py-2 w-full dark:bg-slate-800 rounded-lg dark:hover:bg-slate-900 font-semibold duration-75"
          >
            Xem nhóm
          </button>
        </RouterLink>
        <EllipsisHorizontalIcon class="w-10" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { EllipsisHorizontalIcon } from "@heroicons/vue/24/solid";
import { RouterLink } from "vue-router";
export default (await import("vue")).defineComponent({
  components: {
    EllipsisHorizontalIcon,
    RouterLink,
  },
  props: {
    yourGroup: Object,
  },

  data() {
    return {
      currentMember: {}
    }
  },

  mounted() {
    this.getCurrentMember()
  },

  methods: {
    accessGroup() {
      axios
        .post(`/api/group/${this.yourGroup.id}/last-access/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getCurrentMember() {
      axios
        .get(`/api/group/get-current-member/${this.yourGroup.id}/`)
        .then((res) => {
          this.currentMember = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

<template>
  <div class="flex flex-col items-center justify-center py-6 gap-4 w-[40%]">
    <div
      class="w-full dark:bg-slate-700 p-4 rounded-lg flex items-center justify-between"
    >
      <h3 class="text-lg font-semibold">Quy tắc nhóm</h3>
      <div
        @click="openModal"
        class="px-4 py-2 rounded-lg dark:hover:bg-slate-600 duration-75 cursor-pointer text-emerald-400 font-medium"
      >
        Tạo
      </div>
      <CreateRuleModal :show="isOpen" @closeModal="closeModal" />
    </div>
    <div v-if="rules.length" class="w-full dark:bg-slate-700 p-4 rounded-lg">
      <div v-for="rule in rules" :key="rule.id" class="flex gap-4">
        <GroupRule :rule="rule" :index="rules.indexOf(rule) + 1" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateRuleModal from "../../components/modals/group/CreateRuleModal.vue";
import { EllipsisHorizontalIcon } from "@heroicons/vue/24/solid";
import GroupRule from "../../components/items/group/GroupRule.vue";
export default {
  name: "grouprules",
  components: {
    CreateRuleModal,
    EllipsisHorizontalIcon,
    GroupRule,
  },
  props: {
    group: Object,
  },

  data() {
    return {
      isOpen: false,
      rules: [],
    };
  },

  mounted() {
    this.getRules();
  },

  methods: {
    openModal() {
      this.isOpen = true;
    },
    closeModal() {
      this.isOpen = false;
    },
    async getRules() {
      axios
        .get(`/api/group/${this.$route.params.id}/get-rules/`)
        .then((res) => {
          this.rules = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

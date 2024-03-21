<template>
  <div>
    <div class="flex gap-4">
      <span class="font-semibold">
        {{ index }}
      </span>
      <div class="flex flex-col space-y-2">
        <h3 class="font-semibold xm:text-base text-sm">{{ rule.name }}</h3>
        <h5 class="xm:text-sm text-xs dark:text-neutral-400 ">{{ rule.body }}</h5>
      </div>
      <RuleDropdown
        :rule="rule"
        @deleteRule="deleteRule"
        @updateRule="updateRule"
      />
    </div>
    <hr class="my-4 border dark:border-slate-600" />
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "../../../stores/toast";
import RuleDropdown from "../../dropdown/RuleDropdown.vue";
export default (await import("vue")).defineComponent({
  components: {
    RuleDropdown,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },
  props: {
    rule: Object,
    index: Number,
  },

  methods: {
    deleteRule(rule) {
      axios
        .post(`api/group/rule/${rule.id}/delete/`)
        .then((res) => {
          if (res.data.message) {
            this.toastStore.showToast(
              3500,
              "Đã xóa quy tắc",
              "bg-emerald-500 text-white"
            );
          }
        })
        .catch((error) => {
          console.log(error);
          this.toastStore.showToast(
            3500,
            "Xóa quy tắc thất bại",
            "bg-rose-500 text-white"
          );
        });
    },
    updateRule() {},
  },
});
</script>

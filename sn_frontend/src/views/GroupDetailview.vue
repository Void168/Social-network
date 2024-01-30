<template>
  <div>Hello</div>
</template>

<script>
import axios from "axios";
export default {
  name: "groupdetail",
  components: {},
  data() {
    return {};
  },

  mounted() {
    this.getGroupDetail();
  },

  methods: {
    async getGroupDetail() {
      await axios
        .get(`/api/group/${this.$route.params.id}/`)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

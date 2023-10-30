<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="bg-white border border-gray-200 rounded-lg h-[750px] px-2">
        <h3 class="text-xl p-3">Đoạn hội thoại ({{ conversations.length }})</h3>
        <div>
          <ConversationBox
            v-bind:conversations="conversations"
          />
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <div
        class="bg-white h-[750px] border-gray-200 rounded-lg flex justify-center items-center"
      >
        Chưa chọn đoạn hội thoại nào
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";
import ConversationBox from "../components/ConversationBox.vue";

export default (await import("vue")).defineComponent({
  name: "chat",
  components: {
    ConversationBox,
    RouterLink,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      conversations: [],
      body: "",
    };
  },
  mounted() {
    this.getConversations();
  },

  methods: {
    getConversations() {
      axios
        .get("/api/chat/")
        .then((res) => {
          this.conversations = res.data;
          console.log(this.conversations)
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

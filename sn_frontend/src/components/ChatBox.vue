<template>
  <div>
    <div class="bg-white border border-gray-200 rounded-lg">
      <div>
        <div class="p-4 flex justify-between items-center">
          <div class="flex items-center gap-2">
            <img
              :src="receivedUser.get_avatar"
              alt=""
              class="w-10 h-10 rounded-full"
            />
            <span class="font-bold">{{ receivedUser.name }}</span>
          </div>

          <span>Đang hoạt động</span>
        </div>
      </div>

      <hr />
      <div
        class="flex flex-col flex-grow p-4 overflow-y-auto h-[400px]"
      >
        <div v-if="recentConversation?.messages?.length > 0">
          <div
            v-for="message in listMessages"
            v-bind:key="message.id"
            :id="message.id"
          >
            <div
              class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div>
                <div
                  class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg"
                >
                  <p class="text-sm">
                    {{ message.body }}
                  </p>
                </div>
                <span class="text-xs text-gray-500 leading-none"
                  >{{ message.created_at_formatted }} trước</span
                >
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  alt=""
                  class="w-10 h-10 rounded-full"
                />
              </div>
            </div>
            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  alt=""
                  class="w-10 h-10 rounded-full"
                />
              </div>
              <div>
                <div
                  v-if="
                    recentConversation?.messages?.filter(
                      (user) => user.sent_to.id === userStore.user.id
                    )
                  "
                  v-bind:key="message.id"
                  class="mb-4"
                >
                  <div
                    class="bg-gray-200 p-3 rounded-r-lg rounded-bl-lg"
                    v-if="message.created_by !== chats[0]?.users[0].name"
                  >
                    <p class="text-sm">
                      {{ message.body }}
                    </p>
                  </div>
                  <span class="text-xs text-gray-500 leading-none"
                    >{{ message.created_at_formatted }} trước</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="bg-white h-[500px] flex justify-center items-center">
          Hãy bắt đầu nói chuyện với nhau
        </div>
      </div>
    </div>
    <div class="bg-white border border-gray-200 rounded-lg">
      <form v-on:submit.prevent="submitForm" @keyup.enter="submitForm">
        <div class="p-4">
          <textarea
            v-model="body"
            class="p-4 w-full bg-gray-100 rounded-lg"
            name=""
            id=""
            cols="30"
            rows="1"
            placeholder="Bạn muốn nói điều gì?"
          ></textarea>
        </div>
        <div class="p-4 border-t border-gray-100 flex justify-end">
          <button>Gửi</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ConversationBox from "../components/ConversationBox.vue";
import { useUserStore } from "../stores/user";
import { RouterLink } from "vue-router";

export default (await import("vue")).defineComponent({
  props: {
    chats: Array,
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
  },

  data() {
    return {
      receivedUser: {},
      listMessages: [],
      recentConversation: {},
      body: "",
    };
  },
  watch: {
    "$route.params.id": {
      handler: function () {
        this.getMessages();
      },
      deep: true,
      immediate: true,
    },
  },
  mounted() {
    this.getActiveConversation();
    this.getMessages()
  },
  methods: {
    getActiveConversation() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
        .then((res) => {
          this.recentConversation = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getMessages() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
        .then((res) => {
          this.recentConversation = res.data;
          this.listMessages = this.recentConversation.messages;
          let users = [];
          for (let i = 0; i < this.recentConversation.users.length; i++) {
            users.push(this.recentConversation.users[i]);
          }
          const filteredUser = users
            ?.map((user) => user.id)
            .filter((id) => id !== this.userStore.user.id);
          this.receivedUser = users.filter((user) => user.id === filteredUser[0])[0]
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      axios
        .post(`/api/chat/${this.recentConversation.id}/send/`, {
          body: this.body,
        })
        .then((res) => {
          console.log(res.data);
          this.recentConversation.messages.push(res.data);
          this.body = "";
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  components: { RouterLink, ConversationBox },
});
</script>

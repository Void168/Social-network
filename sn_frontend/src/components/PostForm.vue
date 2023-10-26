<template>
  <form v-on:submit.prevent="submitForm" method="post">
    <div class="p-4">
      <textarea
        v-model="body"
        class="p-4 w-full bg-gray-100 rounded-lg resize-none"
        cols="30"
        rows="4"
        placeholder="Bạn đang nghĩ gì?"
      ></textarea>
      <label>
        <input type="checkbox" v-model="is_private"> Riêng tư
      </label>
      <div
        id="preview"
        v-if="url"
        class="flex relative justify-center items-center w-full p-4 border-[1px] rounded-lg"
      >
        <img :src="url" class="w-full rounded-lg" />
        <span class="absolute top-5 right-5 cursor-pointer" @click="removeImage"
          ><svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-8 h-8"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </span>
      </div>
    </div>

    <div class="p-4 border-t border-gray-100 flex justify-between">
      <label for="doc">
        <div
          class="py-3 px-6 text-black bg-gray-400 font-semibold rounded-lg transition-colors hover:bg-gray-600 hover:text-white cursor-pointer"
        >
          <span>Chọn ảnh</span>
        </div>
        <input
          type="file"
          ref="file"
          id="doc"
          name="doc"
          hidden
          @change="onFileChange"
        />
      </label>

      <button>Đăng bài viết</button>
    </div>
  </form>
</template>
<script>
import axios from "axios";

export default {
  props: {
    user: Object,
    posts: Array,
  },

  data() {
    return {
      body: "",
      url: null,
      is_private: false
    };
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },

    removeImage() {
      this.url = null;
    },
    submitForm() {
      console.log("submitForm", this.body);

      let formData = new FormData();
      formData.append("image", this.$refs.file.files[0]);
      formData.append("body", this.body);
      formData.append("is_private", this.is_private)

      axios
        .post("/api/posts/create/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("data", res.data);

          this.posts.unshift(res.data);
          this.body = "";
          this.$refs.file.value = null;
          this.is_private = false
          this.url = null;

          if (this.user) {
            this.user.posts_count += 1;
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

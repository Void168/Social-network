<template>
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 xs:grid-cols-1 gap-4">
    <div class="main-left md:block xs:hidden">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Chỉnh sửa thông tin</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eaque
          delectus voluptatum sed ipsam, omnis voluptates et tempore temporibus
          hic harum veritatis eveniet, alias pariatur, at ad architecto cumque
          inventore illo. Lorem ipsum dolor sit amet, consectetur adipisicing
          elit. Beatae, nostrum harum facere necessitatibus esse dolorum! Cum
          provident, tenetur ipsa minus quam eos voluptas nostrum assumenda
          suscipit, dolor veritatis perspiciatis soluta.
        </p>
      </div>
    </div>

    <div class="main-right flex justify-center">
      <div class="p-12 bg-white border boder-gray-200 rounded-lg w-full">
        <template v-if="errors.length > 0">
          <div
            class="bg-rose-400 text-white text-center rounded-lg px-6 py-3 mb-4"
          >
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>
        </template>
        <form action="" class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label for="">Tên người dùng</label>
            <input
              v-model="form.name"
              type="text"
              placeholder="Họ và tên"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label for="">E-mail</label>
            <input
              type="email"
              v-model="form.email"
              placeholder="E-mail của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div class="flex flex-col">
            <label class="text-center">Ảnh đại diện</label>
            <input
              type="file"
              ref="file"
            />
          </div>
          <div class="flex items-center justify-center">
            <button class="w-full">Lưu thay đổi</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "../stores/user";

export default (await import("vue")).defineComponent({
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();

    return {
      toastStore,
      userStore,
    };
  },

  data() {
    return {
      form: {
        email: this.userStore.user.email,
        name: this.userStore.user.name,
        avatar: null,
      },

      errors: [],
    };
  },

  methods: {
    submitForm() {
      this.errors = [];

      if (this.form.email === "") {
        this.errors.push("E-mail trống");
      }

      if (this.form.name === "") {
        this.errors.push("Tên đăng nhập trống");
      }

      if (this.errors.length === 0) {
        let formData = new FormData()
        formData.append('avatar', this.$refs.file.files[0])
        formData.append('name', this.form.name)
        formData.append('email', this.form.email)

        axios
          .post("/api/edit-profile/", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
          })
          .then((res) => {
            if (res.data.message === "information updated") {
              this.toastStore.showToast(
                5000,
                "Đã lưu thông tin chỉnh sửa.",
                "bg-emerald-500 text-white"
              );

              this.userStore.setUserInfo({
                id: this.userStore.user.id,
                name: this.form.name,
                email: this.form.email,
                avatar: res.data.user.get_avatar
              });

              this.$router.go(-1);
            } else {
              this.toastStore.showToast(
                5000,
                `${res.data.message}`,
                "bg-rose-400 text-white"
              );
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
  },
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 xs:grid-cols-1 gap-4">
    <div class="main-left md:block xs:hidden">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Đăng ký</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eaque
          delectus voluptatum sed ipsam, omnis voluptates et tempore temporibus
          hic harum veritatis eveniet, alias pariatur, at ad architecto cumque
          inventore illo. Lorem ipsum dolor sit amet, consectetur adipisicing
          elit. Beatae, nostrum harum facere necessitatibus esse dolorum! Cum
          provident, tenetur ipsa minus quam eos voluptas nostrum assumenda
          suscipit, dolor veritatis perspiciatis soluta.
        </p>
        <p class="font-bold">
          Chưa có tài khoản?
          <RouterLink :to="{ name: 'signup' }" class="underline"
            >Bấm để tạo tài khoản</RouterLink
          >
        </p>
      </div>
    </div>

    <div class="main-right flex justify-center items-center">
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
            <label for="">E-mail</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="E-mail của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label for="">Mật khẩu</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="Mật khẩu của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div class="flex items-center justify-center">
            <button class="w-full">Đăng nhập</button>
          </div>
          <p class="font-bold md:hidden xs:block">
            Chưa có tài khoản?
            <a href="#" class="underline">Bấm để tạo tài khoản</a>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../stores/user";

export default {
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      errors: [],
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];

      if (this.form.email === "") {
        this.errors.push("E-mail trống");
      }

      if (this.form.password === "") {
        this.errors.push("Mật khẩu trống");
      }

      if (this.errors.length === 0) {
        await axios
          .post("/api/login/", this.form)
          .then((res) => {
            this.userStore.setToken(res.data);

            axios.defaults.headers.common["Authorization"] =
              "Bearer " + res.data.access;
          })
          .catch((error) => {
            console.log("error", error);

            this.errors.push(
              "E-mail hoặc mật khẩu không đúng! Hoặc người dùng chưa được đăng ký!"
            );
          });
      }

      if (this.errors.length === 0) {
        await axios
          .get("/api/me/")
          .then((res) => {
            this.userStore.setUserInfo(res.data);

            this.$router.push("/feed");
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
  },
};
</script>

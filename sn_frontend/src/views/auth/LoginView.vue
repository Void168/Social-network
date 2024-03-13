<template>
  <div
    class="max-w-7xl mx-auto flex justify-center items-center lg:py-4"
    :style="{ height: `${toastStore.height}px` }"
  >
    <div
      class="main-right lg:w-[60%] w-full h-full flex justify-center items-center dark:bg-[url('https://wallpapercave.com/wp/wp1912996.jpg')] bg-[url('https://media.istockphoto.com/photos/social-media-title-word-picture-id871280234?k=20&m=871280234&s=170667a&w=0&h=tENwfLyOFLpRr0HURw5MmYaFyMy89t-LrvGWdrOTUgU=')] bg-cover bg-center bg-no-repeat lg:rounded-lg"
    >
      <div
        class="md:p-12 p-4 dark:text-slate-200 text-black dark:border-slate-500 md:rounded-lg w-full h-full backdrop-blur-sm dark:bg-slate-900/60 bg-slate-900/20"
      >
        <template v-if="errors.length > 0">
          <div
            class="bg-rose-400 text-white text-center rounded-lg px-6 py-3 mb-4"
          >
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>
        </template>
        <div
          class="md:flex-none flex md:justify-normal justify-center items-center flex-col space-y-8"
        >
          <h1 class="font-bold md:text-6xl text-4xl">Đăng nhập</h1>
          <form
            action=""
            class="space-y-6 w-full"
            v-on:submit.prevent="submitForm"
          >
            <div>
              <label for="" class="text-lg font-semibold">E-mail</label>
              <input
                id="email-login"
                v-model="form.email"
                type="email"
                placeholder="E-mail của bạn"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-600 rounded-lg dark:text-slate-200 text-black"
              />
            </div>
            <div>
              <label for="" class="text-lg font-semibold">Mật khẩu</label>
              <input
                v-model="form.password"
                type="password"
                placeholder="Mật khẩu của bạn"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-600 rounded-lg dark:text-slate-200 text-black"
              />
            </div>

            <div class="flex items-center justify-center">
              <button class="w-full btn">
                {{ isLoading ? "Đang tải..." : "Đăng nhập" }}
              </button>
            </div>
          </form>
          <p class="font-bold md:text-lg dark:text-neutral-200">
            Chưa có tài khoản?
            <RouterLink :to="{ name: 'signup' }" class="underline"
              >Bấm để tạo tài khoản</RouterLink
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { useUserStore } from "../../stores/user";
import { useToastStore } from "../../stores/toast";

export default {
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
    };
  },

  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      errors: [],
      isLoading: false,
    };
  },
  methods: {
    async submitForm() {
      this.isLoading = true;
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
      } else {
        this.isLoading = false;
      }

      if (this.errors.length === 0) {
        await axios
          .get("/api/me/")
          .then((res) => {
            window.location = "/";
            this.userStore.setUserInfo(res.data);
            // this.isLoading = false
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        this.isLoading = false;
      }
    },
  },
};
</script>

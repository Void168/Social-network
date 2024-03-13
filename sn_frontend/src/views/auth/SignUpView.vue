<template>
  <div class="max-w-7xl mx-auto flex justify-center items-center lg:py-4" :style="{height: `${toastStore.height}px`}">
    <div class="main-right lg:w-[60%] w-full h-full flex justify-center items-center dark:bg-[url('https://wallpapercave.com/wp/wp1912996.jpg')] bg-[url('https://media.istockphoto.com/photos/social-media-title-word-picture-id871280234?k=20&m=871280234&s=170667a&w=0&h=tENwfLyOFLpRr0HURw5MmYaFyMy89t-LrvGWdrOTUgU=')] bg-cover bg-center bg-no-repeat lg:rounded-lg">
      <div class="md:p-12 p-4 dark:text-slate-200 text-black dark:border-slate-500 md:rounded-lg w-full h-full backdrop-blur-sm dark:bg-slate-900/60 bg-slate-900/20">
        <template v-if="errors.length > 0">
          <div
            class="bg-rose-400 text-white text-center rounded-lg px-6 py-3 mb-4"
          >
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>
        </template>
        <div class="md:flex-none flex md:justify-normal justify-center items-center flex-col space-y-4">
          <h1 class="md:hidden font-bold text-3xl"> Đăng nhập</h1>
          <form action="" class="space-y-6 w-full" v-on:submit.prevent="submitForm">
            <div>
              <label for="">Tên người dùng</label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Họ và tên"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-600 rounded-lg dark:text-slate-200 text-black"
              />
            </div>
            <div>
              <label for="">E-mail</label>
              <input
                id="email-signup"
                type="email"
                v-model="form.email"
                placeholder="E-mail của bạn"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-600 rounded-lg dark:text-slate-200 text-black"
              />
            </div>
            <div>
              <label for="">Mật khẩu</label>
              <input
                type="password"
                v-model="form.password1"
                placeholder="Mật khẩu của bạn"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-600 rounded-lg dark:text-slate-200 text-black"
              />
            </div>
            <div>
              <label for="">Nhập lại mật khẩu</label>
              <input
                type="password"
                v-model="form.password2"
                placeholder="Nhập lại mật khẩu"
                class="w-full mt-2 py-2 px-6 border border-gray-200 dark:bg-slate-600 rounded-lg dark:text-slate-200 text-black"
              />
            </div>
            <div class="flex items-center justify-center">
              <button class="w-full btn">Đăng ký</button>
            </div>
            <p class="font-bold md:hidden xs:block">
              Đã có tài khoản?
              <a href="#" class="underline">Bấm để đăng nhập</a>
            </p>
          </form>
          <p class="font-bold md:text-lg dark:text-neutral-200 md:block hidden">
            Đã có tài khoản?
            <RouterLink :to="{ name: 'signup' }" class="underline"
              >Bấm để đăng nhập</RouterLink
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";

export default {
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },

  data() {
    return {
      form: {
        email: "",
        name: "",
        password1: "",
        password2: "",
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

      if(this.form.name.includes("^[\w.@+-]+\Z") || /\s/.test(this.form.name))
      {
        this.errors.push("Tên chi cho phép chứa các ký tự . hoặc _");
      }
      if (this.form.password1 === "") {
        this.errors.push("Mật khẩu trống");
      }

      if (this.form.password1 !== this.form.password2) {
        this.errors.push("Mật khẩu nhập lại sai");
      }

      if (this.errors.length === 0) {
        axios
          .post("/api/signup/", this.form)
          .then((res) => {
            if (res.data.status === "success") {
              this.toastStore.showToast(
                5000,
                "Đăng ký thành công. Vui lòng xác thực e-mail.",
                "bg-emerald-500 text-white"
              );

              this.form.email = "";
              this.form.name = "";
              this.form.password1 = "";
              this.form.password2 = "";
            } else {
              this.toastStore.showToast(
                5000,
                "Đăng ký thất bại. Vui lòng thử lại",
                "bg-rose-400 text-white"
              );
              this.errors.push("Có thể e-mail đã được đăng ký");
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
  },
};
</script>

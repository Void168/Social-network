<template>
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 xs:grid-cols-1 gap-4">
    <div class="main-left md:block xs:hidden">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Đăng nhập</h1>
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
          Đã có tài khoản?
          <RouterLink :to="{ name: 'login' }" class="underline"
            >Bấm để đăng nhập</RouterLink
          >
        </p>
      </div>
    </div>

    <div class="main-right flex justify-center">
      <div class="p-12 bg-white border boder-gray-200 rounded-lg">
        <template v-if="errors.length > 0">
            <div class="bg-rose-400 text-white text-center rounded-lg px-6 py-3 mb-4">
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
          <div>
            <label for="">Mật khẩu</label>
            <input
              type="password"
              v-model="form.password1"
              placeholder="Mật khẩu của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label for="">Nhập lại mật khẩu</label>
            <input
              type="password"
              v-model="form.password2"
              placeholder="Nhập lại mật khẩu"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div class="flex items-center justify-center">
            <button class="w-full">Đăng ký</button>
          </div>
          <p class="font-bold md:hidden xs:block">
            Đã có tài khoản?
            <a href="#" class="underline">Bấm để đăng nhập</a>
          </p>
        </form>
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
            console.log(res.data)
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

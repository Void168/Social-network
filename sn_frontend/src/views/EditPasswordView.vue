<template>
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 xs:grid-cols-1 gap-4">
    <div class="main-left md:block xs:hidden">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Đổi mật khẩu</h1>
        <p class="mb-6 text-gray-500">Bạn có thể đổi mật khẩu tại đây</p>
      </div>
    </div>

    <div class="main-right flex justify-center">
      <div class="p-12 bg-white border boder-gray-200 rounded-lg w-full">
        <form action="" class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label for="">Mật khẩu cũ</label>
            <input
              v-model="form.old_password"
              type="password"
              placeholder="Nhập mật khẩu hiện tại"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <p class="text-rose-400 text-center rounded-lg">{{ errors[0] }}</p>

          <div>
            <label for="">Mật khẩu mới</label>
            <input
              v-model="form.new_password1"
              type="password"
              placeholder="Nhập mật khẩu mới"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <p class="text-rose-400 text-center rounded-lg">{{ errors[1] }}</p>

          <div>
            <label for="">Nhập lại mật khẩu mới</label>
            <input
              v-model="form.new_password2"
              type="password"
              placeholder="Nhập lại mật khẩu mới"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <p class="text-rose-400 text-center rounded-lg">{{ errors[2] }}</p>

          <div class="flex items-center justify-center">
            <button class="w-full btn">Lưu thay đổi</button>
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
        old_password: "",
        new_password1: "",
        new_password2: "",
      },

      errors: [],
    };
  },

  methods: {
    submitForm() {
      this.errors = [];

      if (this.form.old_password !== this.form.new_password1) {
        this.errors.push("Mật khẩu nhập cũ giống với mật khẩu mới");
      }

      if (this.form.new_password1 !== this.form.new_password2) {
        this.errors.push("Mật khẩu nhập lại không đúng");
      }

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("old_password", this.form.old_password);
        formData.append("new_password1", this.form.new_password1);
        formData.append("new_password2", this.form.new_password2);

        axios
          .post("/api/edit-password/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            if (res.data.message === "success") {
              this.toastStore.showToast(
                5000,
                "Đổi mật khẩu thành công. Vui lòng đăng nhập lại",
                "bg-emerald-500 text-white"
              );
              this.$router.push("/login");

              this.userStore.removeToken();
              console.log(this.errors)
            } else {
              const data = JSON.parse(res.data.message);

              for (const key in data) {
                this.errors.push(data[key][0].message);
              }
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

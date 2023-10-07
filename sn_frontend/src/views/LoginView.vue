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
          <RouterLink :to="{'name': 'signup'}" class="underline">Bấm để tạo tài khoản</RouterLink>
        </p>
      </div>
    </div>

    <div class="main-right flex justify-center items-center">
      <div class="p-12 bg-white border boder-gray-200 rounded-lg">
        <form action="" class="space-y-6">
          <div>
            <label for="">E-mail</label>
            <input
              type="email"
              placeholder="E-mail của bạn"
              class="w-full mt-2 py-2 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label for="">Mật khẩu</label>
            <input
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

<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <div
    class="dark:text-slate-200 dark:bg-slate-700 rounded-lg gap-6 p-4 mx-auto max-h-max lg:my-12 my-20"
    :class="isDeviceActive ? '2xl:w-[40%] sm:w-[60%] w-full' : 'lg:w-[70%]'"
  >
    <div class="flex justify-between items-center w-full mb-4">
      <h2 class="text-lg font-semibold">Xem trước trên máy tính</h2>
      <div class="flex gap-3">
        <ComputerDesktopIcon
          @click="$emit('computerActive')"
          class="w-6 cursor-pointer"
          :class="!isDeviceActive ? 'text-emerald-400' : ''"
        />
        <DevicePhoneMobileIcon
          @click="$emit('deviceActive')"
          class="w-6 cursor-pointer"
          :class="isDeviceActive ? 'text-emerald-400' : ''"
        />
      </div>
    </div>
    <div class="flex flex-col border dark:border-slate-600 w-full rounded-lg">
      <div
        class="relative flex justify-center w-full dark:bg-slate-800 rounded-lg"
        :class="
          isDeviceActive
            ? 'lg:h-[200px] md:h-[150px] h-[100px]'
            : 'lg:h-[350px] md:h-[300px] h-[200px]'
        "
      >
        <img
          src="@/assets/default-group-cover-image.jpg"
          alt="default-avatar"
          class="w-full h-full rounded-lg"
        />
      </div>
      <div class="my-6 px-8 space-y-2">
        <h1 class="text-3xl font-bold">
          {{ name || "Tên nhóm" }}
        </h1>
        <h4 class="dark:text-slate-400">
          Quyền riêng tư của nhóm &middot; <strong>1 thành viên</strong>
        </h4>
      </div>
      <hr class="border-slate-600 mx-4" />
      <div class="flex justify-between items-center px-2 py-4">
        <div class="flex gap-2 items-center max-h-max">
          <div
            class="px-4 py-2 dark:text-slate-300 font-semibold"
            :class="isDeviceActive ? 'hidden' : 'block'"
          >
            Giới thiệu
          </div>
          <div
            class="px-4 py-2 dark:text-slate-300 font-semibold"
            :class="isDeviceActive ? 'hidden' : 'block'"
          >
            Bài viết
          </div>
          <div
            class="px-4 py-2 dark:text-slate-300 font-semibold"
            :class="isDeviceActive ? 'hidden' : 'block'"
          >
            Thành viên
          </div>
          <div
            class="px-4 py-2 dark:text-slate-300 font-semibold"
            :class="isDeviceActive ? 'hidden' : 'block'"
          >
            Sự kiện
          </div>
        </div>
      </div>
      <div
        class="p-2 dark:bg-slate-800 rounded-b-lg flex gap-4"
        :class="isDeviceActive ? 'flex-col' : ''"
      >
        <div
          class="dark:bg-slate-700 bg-slate-200 p-2 rounded-lg flex flex-col space-y-4 h-fit"
          :class="isDeviceActive ? 'w-full' : 'w-[60%]'"
        >
          <div class="flex items-center w-full gap-2">
            <UserIcon
              class="w-10 dark:text-neutral-400 border-2 border-neutral-400 rounded-full p-1"
            />
            <div class="relative dark:bg-slate-800 h-10 w-full rounded-2xl">
              <span class="absolute top-2 left-4 dark:text-slate-400 w-full"
                >Bạn đang nghĩ gì</span
              >
            </div>
          </div>
          <div class="flex 2xl:flex-row flex-col justify-evenly items-center gap-2">
            <div class="flex items-center gap-2">
              <PhotoIcon class="w-6 dark:text-neutral-400" />
              <h3 class="dark:text-neutral-400 font-semibold">Ảnh/video</h3>
            </div>
            <div class="flex items-center gap-2">
              <TagIcon class="w-6 dark:text-neutral-400" />
              <h3 class="dark:text-neutral-400 font-semibold">
                Gắn thẻ người khác
              </h3>
            </div>
            <div class="flex items-center gap-2">
              <FaceSmileIcon class="w-6 dark:text-neutral-400" />
              <h3 class="dark:text-neutral-400 font-semibold">
                Feeling/activity
              </h3>
            </div>
          </div>
        </div>
        <div
          class="dark:bg-slate-700 bg-slate-200 p-2 rounded-lg h-fit"
          :class="isDeviceActive ? 'w-full' : 'w-[40%]'"
        >
          <h2 class="text-xl font-bold">Giới thiệu</h2>
          <div class="flex gap-2" v-if="privacy.name === 'Công khai'">
            <div class="flex flex-col justify-start">
                <GlobeAsiaAustraliaIcon class="w-6"/>
            </div>
            <div>
                <h3 class="font-semibold">{{ privacy.name }}</h3>
                <h4>Bất kỳ ai cũng có thể nhìn thấy mọi người trong nhóm và những gì họ đăng.</h4>
            </div>
          </div>
          <div class="flex gap-2" v-else>
            <div class="flex flex-col justify-start">
                <LockClosedIcon class="w-6"/>
            </div>
            <div>
                <h3 class="font-semibold">{{ privacy.name }}</h3>
                <h4>Chỉ thành viên mới nhìn thấy mọi người trong nhóm và những gì họ đăng.</h4>
            </div>
          </div>
          <div class="flex gap-2">
            <div class="flex flex-col justify-start" v-if="showOption.name === 'Hiển thị'">
                <EyeIcon class="w-6"/>
            </div>
            <div class="flex flex-col justify-start" v-else>
                <EyeSlashIcon class="w-6"/>
            </div>
            <div v-if="showOption.name === 'Hiển thị'">
                <h3 class="font-semibold">{{ showOption.name }}</h3>
                <h4>Ai cũng có thể tìm thấy nhóm này.</h4>
            </div>
            <div v-else>
                <h3 class="font-semibold">{{ showOption.name }}</h3>
                <h4>Chỉ thành viên mới tìm thấy nhóm này.</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  ComputerDesktopIcon,
  DevicePhoneMobileIcon,
  UserIcon,
  PhotoIcon,
  TagIcon,
  FaceSmileIcon,
  GlobeAsiaAustraliaIcon,
  EyeIcon,
  LockClosedIcon,
  EyeSlashIcon,
} from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    ComputerDesktopIcon,
    DevicePhoneMobileIcon,
    UserIcon,
    PhotoIcon,
    TagIcon,
    FaceSmileIcon,
    GlobeAsiaAustraliaIcon,
    EyeIcon,
    LockClosedIcon,
    EyeSlashIcon,
  },
  props: {
    isDeviceActive: Boolean,
    name: String,
    privacy: Object,
    showOption: Object,
  },
  emits: ["computerActive", "deviceActive"],
});
</script>

<template>
  <div
    class="dark:text-slate-200 dark:bg-slate-700 rounded-lg gap-6 p-4"
    :class="isDeviceActive ? 'w-[40%]' : 'w-[70%]'"
  >
    <div class="flex justify-between items-center w-full mb-2">
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
          :src="
            coverImageUrl ||
            'https://th.bing.com/th/id/OIP.o1n4kgruF-5cDCCx7jNYKQHaEo?pid=ImgDet&rs=1'
          "
          alt="default-avatar"
          class="w-full h-full"
        />
        <span
          v-if="!avatarUrl"
          class="absolute bottom-[-15px] z-10 w-40 h-40 rounded-full bg-slate-700/60"
        ></span>
        <img
          :src="
            avatarUrl ||
            'https://sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png'
          "
          alt="default-avatar"
          class="w-40 h-40 rounded-full absolute bottom-[-15px] bg-black"
        />
      </div>
      <div class="my-6">
        <h1 class="text-3xl font-bold text-center">
          {{ name || "Tên Trang" }}
        </h1>
        <h3 class="text-center text-lg">{{ biography || "" }}</h3>
      </div>
      <hr class="border-slate-600 mx-4" />
      <div class="flex justify-between items-center px-2 py-4">
        <div class="flex gap-2 items-center max-h-max">
          <div class="px-4 py-2 dark:text-slate-300 font-semibold">
            Bài viết
          </div>
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
            Người theo dõi
          </div>
          <div
            class="px-4 py-2 dark:text-slate-300 font-semibold"
            :class="isDeviceActive ? 'hidden' : 'block'"
          >
            Ảnh
          </div>
          <div
            class="px-4 py-2 dark:text-slate-300 font-semibold"
            :class="isDeviceActive ? 'hidden' : 'block'"
          >
            Video
          </div>
          <div class="px-4 py-2 dark:text-slate-300 font-semibold flex">
            <span>Xem thêm</span>
            <ChevronDownIcon class="w-6 p-1" />
          </div>
        </div>
        <div class="flex gap-2 items-center max-h-max">
          <div
            class="px-4 py-2 dark:text-slate-400 font-semibold dark:bg-slate-500/70 rounded-lg cursor-default"
          >
            Theo dõi
          </div>
          <div
            class="px-4 py-2 dark:text-slate-400 font-semibold dark:bg-slate-500/70 rounded-lg cursor-default"
          >
            Nhắn tin
          </div>
          <div
            class="px-4 py-2 dark:text-slate-400 font-semibold dark:bg-slate-500/70 rounded-lg cursor-default"
          >
            <EllipsisHorizontalIcon class="w-6" />
          </div>
        </div>
      </div>
      <div
        class="p-2 bg-slate-800 rounded-b-lg flex gap-4 h-72"
        :class="isDeviceActive ? 'flex-col' : ''"
      >
        <div
          class="bg-slate-700 p-2 rounded-lg flex flex-col space-y-4 h-fit"
          :class="isDeviceActive ? 'w-full' : 'w-[40%]'"
        >
          <h2 class="text-xl font-bold">Giới thiệu</h2>
          <div class="flex gap-1">
            <UserGroupIcon class="w-6 text-slate-400" />
            <span class="font-semibold">0 người theo dõi</span>
          </div>
          <div class="flex gap-1">
            <ExclamationCircleIcon class="w-6 text-slate-400" />
            <span class="font-semibold">Trang</span>
            <span>&middot;</span>
            <span>{{ type || "Hạng mục" }}</span>
          </div>
        </div>
        <div
          class="bg-slate-700 p-2 rounded-lg flex justify-between items-center h-fit"
          :class="isDeviceActive ? 'w-full' : 'w-[60%]'"
        >
          <h2 class="text-xl font-bold">Bài viết</h2>
          <div
            class="flex gap-1 px-4 py-2 dark:text-slate-200 font-semibold dark:bg-slate-600 rounded-lg cursor-default"
          >
            <span>Bộ lọc</span>
            <AdjustmentsHorizontalIcon class="w-6" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  AdjustmentsHorizontalIcon,
  ExclamationCircleIcon,
  EllipsisHorizontalIcon,
  ChevronDownIcon,
  ComputerDesktopIcon,
  DevicePhoneMobileIcon,
  UserGroupIcon
} from "@heroicons/vue/24/solid";

export default(await import("vue")).defineComponent({
  components: {
    AdjustmentsHorizontalIcon,
    ExclamationCircleIcon,
    EllipsisHorizontalIcon,
    ChevronDownIcon,
    ComputerDesktopIcon,
    DevicePhoneMobileIcon,
    UserGroupIcon,
  },
  props: {
    isDeviceActive: Boolean,
    coverImageUrl: String,
    avatarUrl: String,
    name: String,
    biography: String,
    type: String,
  },
  emits: ['computerActive', 'deviceActive']
});
</script>

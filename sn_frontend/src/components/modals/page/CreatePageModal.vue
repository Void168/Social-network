<template>
  <TransitionRoot appear as="template">
    <Dialog as="div" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto z-50">
        <div class="flex items-center justify-center text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full h-screen transform grid grid-cols-5 overflow-hidden bg-white dark:bg-slate-900 text-left align-middle shadow-xl transition-all"
            >
              <div
                class="lg:col-span-1 h-screen p-4 hidden bg-slate-800 dark:text-neutral-200 border-r-[1px] border-slate-700 lg:flex flex-col justify-between"
              >
                <div class="flex flex-col space-y-2">
                  <XMarkIcon
                    @click="$emit('closeCreatePageModal')"
                    class="h-8 w-8 p-1 mb-4 bg-slate-200 dark:bg-slate-600 rounded-full hover:bg-slate-300 dark:hover:bg-slate-500 transition duration-100 cursor-pointer"
                  />
                  <div class="flex gap-1">
                    <span>Trang</span>
                    <span>&middot;</span>
                    <span>Tạo trang</span>
                  </div>
                  <h1 class="text-2xl font-bold">Tạo trang</h1>
                  <h3 class="pr-4 text-lg">
                    Trang sẽ hiển thị thông tin về bạn để mọi người tìm hiểu
                    thêm. Hãy chắc chắn là Trang của bạn có mọi thông tin cần
                    thiết nhé.
                  </h3>
                  <div class="relative">
                    <input
                      v-model="name"
                      class="p-4 w-full bg-gray-100 dark:bg-slate-800 rounded-lg resize-none border dark:border-slate-600"
                      cols="30"
                      rows="4"
                      :placeholder="isNameFocus ? '' : 'Tên Trang (bắt buộc)'"
                      @focus="nameFocus"
                      @focusout="nameFocusOut"
                    />
                    <span
                      class="absolute left-4 text-xs top-1 text-emerald-400"
                      v-if="isNameFocus"
                      >Tên Trang (bắt buộc)</span
                    >
                  </div>
                  <h4 class="text-xs">
                    Dùng tên doanh nghiệp/thương hiệu/tổ chức của bạn hoặc tên
                    góp phần giải thích về Trang của bạn.
                    <span
                      class="text-emerald-500 hover:underline transition duration-75 cursor-pointer"
                      >Tìm hiểu thêm</span
                    >
                  </h4>
                  <div>Hạng mục</div>
                  <h4 class="text-xs">
                    Hãy nhập hạng mục mô tả chính xác nhất về bạn nhé.
                  </h4>
                  <div class="relative">
                    <textarea
                      v-model="biography"
                      class="p-4 w-full bg-gray-100 dark:bg-slate-800 rounded-lg resize-none border dark:border-slate-600"
                      cols="30"
                      rows="4"
                      :placeholder="
                        isBioFocus ? '' : 'Tiểu sử (Không bắt buộc)'
                      "
                      @focus="bioFocus"
                      @focusout="bioFocusOut"
                    ></textarea>
                    <span
                      class="absolute left-4 text-xs top-1 text-emerald-400"
                      v-if="isBioFocus"
                      >Tiểu sử (Không bắt buộc)</span
                    >
                  </div>
                  <h4 class="text-xs">
                    Hãy chia sẻ đôi nét về những gì bạn làm nhé.
                  </h4>
                </div>
                <div class="flex flex-col w-full gap-2">
                  <button
                    :class="
                      isDisabled
                        ? 'dark:bg-slate-600 py-2 rounded-lg font-semibold dark:text-slate-400'
                        : 'btn'
                    "
                    :disabled="name && type"
                  >
                    Tạo trang
                  </button>
                  <h4 class="text-xs text-center">
                    Bằng việc tạo Trang, bạn đồng ý với
                    <span
                      class="text-emerald-400 cursor-pointer hover:underline transition duration-75"
                      >Chính sách về Trang, Nhóm và Sự kiện</span
                    >
                  </h4>
                </div>
              </div>
              <div
                class="lg:col-span-4 col-span-5 justify-center flex flex-col items-center py-2"
              >
              <div class="dark:text-slate-200 dark:bg-slate-700 rounded-lg gap-6 p-4" :class="isDeviceActive ? 'w-[40%]' : 'w-[70%]'">
                  <div class="flex justify-between items-center w-full mb-2">
                    <h2 class="text-lg font-semibold">Xem trước trên máy tính</h2>
                    <div class="flex gap-3">
                      <ComputerDesktopIcon @click="computerActive" class="w-6 cursor-pointer" :class="!isDeviceActive ? 'text-emerald-400': ''"/>
                      <DevicePhoneMobileIcon @click="deviceActive" class="w-6 cursor-pointer" :class="isDeviceActive ? 'text-emerald-400': ''"/>
                    </div>
                  </div>
                  <div
                    class="flex flex-col border dark:border-slate-600 w-full rounded-lg"
                  >
                    <div
                      class="relative flex justify-center w-full dark:bg-slate-800 rounded-lg"
                      :class="isDeviceActive ? 'lg:h-[200px] md:h-[150px] h-[100px]' : 'lg:h-[350px] md:h-[300px] h-[200px]'"
                    >
                      <span
                        class="absolute bottom-[-15px] z-10 w-40 h-40 rounded-full bg-slate-700/60"
                      ></span>
                      <img
                        src="https://sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png"
                        alt="default-avatar"
                        class="w-40 h-40 rounded-full absolute bottom-[-15px]"
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
                        <div class="px-4 py-2 dark:text-slate-300 font-semibold" :class="isDeviceActive ? 'hidden' : 'block'">
                          Giới thiệu
                        </div>
                        <div class="px-4 py-2 dark:text-slate-300 font-semibold" :class="isDeviceActive ? 'hidden' : 'block'">
                          Người theo dõi
                        </div>
                        <div class="px-4 py-2 dark:text-slate-300 font-semibold" :class="isDeviceActive ? 'hidden' : 'block'">
                          Ảnh
                        </div>
                        <div class="px-4 py-2 dark:text-slate-300 font-semibold" :class="isDeviceActive ? 'hidden' : 'block'">
                          Video
                        </div>
                        <div
                          class="px-4 py-2 dark:text-slate-300 font-semibold flex"
                        >
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
                    <div class="p-2 bg-slate-800 rounded-b-lg flex gap-4 h-72" :class="isDeviceActive ? 'flex-col' : ''">
                      <div
                        class=" bg-slate-700 p-2 rounded-lg flex flex-col space-y-4 h-fit"
                        :class="isDeviceActive ? 'w-full' : 'w-[40%]'"
                      >
                        <h2 class="text-xl font-bold">Giới thiệu</h2>
                        <div class="flex gap-1">
                          <UserGroupIcon class="w-6 text-slate-400"/>
                          <span class="font-semibold">0 người theo dõi</span></div>
                        <div class="flex gap-1">
                          <ExclamationCircleIcon class="w-6 text-slate-400"/>
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
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import axios from "axios";

import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import {
  XMarkIcon,
  ComputerDesktopIcon,
  DevicePhoneMobileIcon,
  ChevronDownIcon,
  EllipsisHorizontalIcon,
  AdjustmentsHorizontalIcon,
  ExclamationCircleIcon,
  UserGroupIcon,
} from "@heroicons/vue/24/solid";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    XMarkIcon,
    ComputerDesktopIcon,
    DevicePhoneMobileIcon,
    ChevronDownIcon,
    EllipsisHorizontalIcon,
    AdjustmentsHorizontalIcon,
    ExclamationCircleIcon,
    UserGroupIcon
  },
  props: {
    isCreatePageOpen: Boolean,
  },

  data() {
    return {
      isNameFocus: false,
      isTypeFocus: false,
      isBioFocus: false,
      isDeviceActive: false,
      name: "",
      type: "",
      biography: "",
    };
  },

  computed: {
    isDisabled() {
      return !this.name.length && !this.type.length;
    },
  },

  mounted() {},

  methods: {
    nameFocus() {
      this.isNameFocus = true;
    },
    nameFocusOut() {
      this.isNameFocus = false;
    },
    bioFocus() {
      this.isBioFocus = true;
    },
    bioFocusOut() {
      this.isBioFocus = false;
    },
    computerActive(){
        this.isDeviceActive = false
    },
    deviceActive(){
        this.isDeviceActive = true
    },
  },
});
</script>

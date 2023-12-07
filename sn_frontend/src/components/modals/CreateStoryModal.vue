<template>
  <TransitionRoot @click="$emit('closeModal')" appear as="template">
    <Dialog as="div" class="relative z-10">
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
                class="col-span-1 bg-slate-800 dark:text-neutral-200 border-r-[1px] border-slate-700 flex flex-col justify-between"
              >
                <div>
                  <button
                    class="m-4 p-2 bg-slate-900 rounded-full hover:bg-slate-700"
                  >
                    <XMarkIcon
                      @click="$emit('closeModal')"
                      class="text-neutral-200 h-8 w-8 cursor-pointer transition"
                    />
                  </button>
                  <div class="flex justify-between items-center px-4">
                    <h2 class="text-2xl font-bold">Tin của bạn</h2>
                    <Cog8ToothIcon
                      class="text-neutral-200 h-10 w-10 cursor-pointer p-1 bg-slate-600 rounded-full hover:bg-slate-600 transition duration-100"
                    />
                  </div>
                  <div
                    class="flex gap-3 my-4 py-4 items-center border-b border-slate-700 px-4"
                  >
                    <img
                      :src="userStore.user.avatar"
                      alt="story-owner"
                      class="w-16 h-16 rounded-full shadow-lg"
                    />
                    <h3 class="text-xl font-semibold">
                      {{ userStore.user.name }}
                    </h3>
                  </div>
                  <div v-if="isTextStory">
                    <div class="p-4">
                      <textarea
                        v-model="body"
                        @keyup="getContent"
                        class="w-full py-2 pl-4 pr-8 bg-gray-100 border rounded-xl resize-none overflow-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
                        name=""
                        id=""
                        :rows="6"
                        cols="30"
                        placeholder="Bắt đầu nhập"
                      ></textarea>
                      <ChooseFontStory @getOption="getOption" class="w-full" />
                      <div
                        class="p-4 border mt-8 border-slate-700 rounded-lg h-48"
                      >
                        <h3 class="dark:text-neutral-200/70 text-lg">
                          Phông nền
                        </h3>
                        <div class="flex flex-wrap gap-2 my-4 justify-center">
                          <div v-for="theme in themes" :key="theme">
                            <div
                              @click="chooseTheme"
                              class="w-12 h-12 rounded-full cursor-pointer"
                              :class="[theme.background]"
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div
                    v-if="url"
                    class="p-4 flex gap-3 items-center font-semibold hover:bg-slate-700 rounded-lg mx-4 cursor-pointer"
                  >
                    <span
                      class="rounded-full bg-slate-600 p-1 w-12 h-12 flex items-center justify-center text-xl"
                      >Aa</span
                    >
                    <p class="text-xl">Thêm văn bản</p>
                  </div>
                </div>
                <div class="my-4 px-6 flex gap-2" v-if="isTextStory || url">
                  <div
                    @click="$emit('closeTextStory')"
                    class="flex justify-center py-2 px-4 w-[40%] dark:bg-slate-700 shadow-md rounded-lg font-semibold hover:bg-slate-600 transition duration-100 cursor-pointer"
                  >
                    <button @click="removeUrl" class="w-full">Bỏ</button>
                  </div>
                  <button
                    class="w-[60%] dark:bg-emerald-500 hover:bg-emerald-400 py-2 px-4 shadow-md rounded-lg font-semibold"
                  >
                    Chia sẻ lên tin
                  </button>
                </div>
              </div>
              <div
                class="col-span-4 flex items-center gap-6 py-12"
                :class="isTextStory ? 'justify-evenly' : 'justify-center'"
              >
                <div
                  v-if="!isTextStory && !url"
                  class="group relative flex flex-col space-y-2 justify-center items-center w-60 h-[360px] bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg cursor-pointer"
                >
                  <PhotoIcon
                    class="text-neutral-200 h-14 w-14 cursor-pointer p-3 bg-slate-600 shadow-transparent rounded-full hover:bg-slate-600 transition duration-100"
                  />
                  <div
                    class="w-full h-full bg-white top-[-8px] bg-opacity-25 absolute hidden group-hover:block rounded-lg"
                  >
                    <label for="story-image">
                      <input
                        type="file"
                        ref="story-image"
                        id="story-image"
                        name="story-image"
                        @change="chooseMedia"
                        class="w-full h-full opacity-0 cursor-pointer"
                      />
                    </label>
                  </div>
                  <h4 class="font-bold text-neutral-200">Tạo tin ảnh</h4>
                </div>
                <div
                  v-if="!isTextStory && !url"
                  class="group relative flex flex-col space-y-2 justify-center items-center w-60 h-[360px] bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-lg cursor-pointer"
                  @click="$emit('openTextStory')"
                >
                  <div
                    class="w-full h-full bg-white bg-opacity-25 absolute hidden group-hover:block rounded-lg"
                  ></div>
                  <span
                    class="flex justify-center items-center font-semibold text-xl shadow-transparent text-neutral-200 h-14 w-14 cursor-pointer p-1 bg-slate-600 rounded-full hover:bg-slate-600 transition duration-100"
                  >
                    Aa</span
                  >
                  <h4 class="font-bold text-neutral-200">
                    Tạo tin dạng văn bản
                  </h4>
                </div>
                <h3
                  v-if="isTextStory"
                  class="dark:text-neutral-200 font-semibold text-lg"
                >
                  Xem trước
                </h3>
                <div
                  v-if="isTextStory || url"
                  class="bg-slate-800 h-full w-[65%] rounded-xl p-4"
                >
                  <div
                    class="flex justify-center items-center bg-slate-900 h-full rounded-xl p-4"
                  >
                    <div
                      v-if="!url"
                      class="h-full bg-blue-500 w-[50%] rounded-xl flex justify-center items-center text-2xl font-semibold text-neutral-200/50"
                    >
                      {{ body || "Bắt đầu nhập" }}
                    </div>
                    <div
                      v-else
                      class="h-full w-[50%] border rounded-xl flex justify-center items-center text-2xl font-semibold text-neutral-200/50"
                      :style="{backgroundColor: color}"
                    >
                      <img
                        :src="url"
                        alt="story-url"
                        class="rounded-none w-full"
                        ref="myImage"
                      />
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
import { useUserStore } from "../../stores/user";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { XMarkIcon, Cog8ToothIcon, PhotoIcon } from "@heroicons/vue/24/solid";
import ChooseFontStory from "../dropdown/ChooseFontStory.vue";
import themes from "../../data/themes";
import ColorThief from "../../../node_modules/colorthief/dist/color-thief.mjs";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    ChooseFontStory,
    XMarkIcon,
    Cog8ToothIcon,
    PhotoIcon,
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  props: {
    isOpen: Boolean,
    isTextStory: Boolean,
  },

  data() {
    return {
      isMediaStory: false,
      body: "",
      themes: themes.reverse(),
      url: null,
      color: null,
    };
  },
  methods: {
    getOption() {},
    chooseTheme() {},
    chooseMedia(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
      setTimeout(() => {
        this.getColor();
      }, 50);
    },
    getColor() {
      const colorThief = new ColorThief();
      this.$nextTick(() => {
        let self = this;
        const img = self.$refs.myImage;

        if (img.complete) {
          const rgb = colorThief.getColor(img);
          this.color = `rgba(${rgb.toString()},0.8)`
          console.log(this.color)
        } else {
          img.addEventListener("load", function () {
            colorThief.getColor(img);
          });
        }
      });
    },
    removeUrl() {
        this.url = null
    }
  },
});
</script>

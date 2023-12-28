<template>
  <TransitionRoot appear as="template">
    <Dialog as="div" class="relative z-[100]">
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
                    @click="removeAll"
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
                      <form>
                        <textarea
                          v-model="body"
                          @keyup="getContent"
                          class="w-full py-2 pl-4 pr-8 bg-gray-100 border rounded-lg resize-none overflow-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
                          name=""
                          id=""
                          :rows="6"
                          cols="30"
                          placeholder="Bắt đầu nhập"
                        ></textarea>
                        <ChooseFontStory
                          class="w-full"
                          :fonts="fonts"
                          @getOption="getOption"
                        />
                        <div
                          class="p-2 border mt-8 border-slate-700 rounded-lg max-h-max"
                        >
                          <h3 class="dark:text-neutral-200/70 text-lg">
                            Phông nền
                          </h3>
                          <div class="flex flex-wrap gap-2 my-4">
                            <div v-for="theme in themes" :key="theme">
                              <div
                                @click="chooseTheme(theme)"
                                class="w-12 h-12 rounded-full cursor-pointer"
                                :class="[theme.background]"
                              ></div>
                            </div>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                  <div v-if="url" class="flex flex-col space-y-4">
                    <div
                      class="p-4 flex gap-3 items-center font-semibold hover:bg-slate-700 rounded-lg mx-4 cursor-pointer"
                    >
                      <span
                        class="rounded-full bg-slate-600 p-1 w-12 h-12 flex items-center justify-center text-xl"
                        >Aa</span
                      >
                      <p class="text-xl">Thêm văn bản</p>
                    </div>
                    <div
                      class="p-4 flex flex-col gap-3 items-start font-semibold"
                    >
                      <label for="caption" class="text-xl"> Tiêu đề </label>
                      <textarea
                        v-model="caption"
                        class="w-full py-2 pl-4 pr-8 bg-gray-100 border rounded-lg resize-none overflow-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
                        name="caption"
                        id="caption"
                        :rows="3"
                        cols="30"
                        placeholder="Nhập tiêu đề"
                      ></textarea>
                    </div>
                  </div>
                </div>
                <div class="my-4 px-6 flex gap-2" v-if="isTextStory || url">
                  <div
                    @click="$emit('closeTextStory')"
                    class="flex justify-center py-2 px-4 w-[40%] dark:bg-slate-700 shadow-md rounded-lg font-semibold hover:bg-slate-600 transition duration-100 cursor-pointer"
                  >
                    <button @click="removeAll" class="w-full">Bỏ</button>
                  </div>
                  <button
                    @click="submitForm"
                    class="w-[60%] dark:bg-emerald-500 hover:bg-emerald-400 py-2 px-4 shadow-md rounded-lg font-semibold"
                  >
                    Chia sẻ lên tin
                  </button>
                </div>
              </div>
              <div
                class="col-span-4 flex items-center gap-6 py-12"
                :class="
                  isTextStory || url ? 'justify-evenly' : 'justify-center'
                "
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
                        ref="story"
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
                  v-if="isTextStory || url"
                  class="dark:text-neutral-200 font-semibold text-lg"
                >
                  Xem trước
                </h3>
                <div
                  v-if="isTextStory || url"
                  class="bg-slate-800 h-full w-[65%] rounded-xl p-4"
                >
                  <div
                    class="flex justify-center flex-col items-center bg-slate-900 h-full rounded-xl p-4"
                  >
                    <div
                      v-if="!url"
                      :class="[
                        selectedFont.font,
                        selectedTheme.background,
                        body ? 'text-neutral-200' : 'text-neutral-200/60',
                      ]"
                      class="h-full bg-emerald-500 w-[50%] border-4 rounded-xl flex justify-center items-center text-2xl font-semibold"
                    >
                      <p
                        class="break-words w-full text-center px-12"
                        :class="[selectedTheme.textColor]"
                      >
                        {{ body || "Bắt đầu nhập" }}
                      </p>
                    </div>
                    <div
                      v-else
                      class="h-full w-[50%] flex justify-center items-center text-2xl font-semibold text-neutral-200/50"
                      :style="{
                        backgroundColor: color,
                        maskImage: `url(${url})`,
                        WebkitMaskImage: `url(${url})`,
                      }"
                    >
                      <img
                        :src="url"
                        alt="story-url"
                        class="rounded-none w-full cursor-pointer shadow-none"
                        :class="deg"
                        :style="{ scale: zoom + value / 50 }"
                        ref="myImage"
                        @click="editImage"
                      />
                    </div>
                    <div
                      class="text-neutral-200 text-lg mt-4 flex items-center gap-3"
                    >
                      <h3 v-if="!isRotate && url" class="px-2 py-1">
                        Chọn ảnh để cắt và xoay
                      </h3>
                      <div
                        v-if="isRotate"
                        class="flex gap-3 justify-center items-center"
                      >
                        <span>-</span>
                        <Slider
                          v-model="value"
                          class="w-96 h-1"
                          :tooltips="true"
                        />
                        <span>+</span>
                      </div>
                      <button
                        v-if="isRotate"
                        class="flex items-center gap-2 bg-slate-700 px-2 py-1 rounded-md"
                        @click="rotate"
                      >
                        <ArrowPathIcon class="w-6 h-6" />
                        <span>Xoay</span>
                      </button>
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
import { useUserStore } from "../../../stores/user";
import { useToastStore } from "../../../stores/toast";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import {
  XMarkIcon,
  Cog8ToothIcon,
  PhotoIcon,
  ArrowPathIcon,
} from "@heroicons/vue/24/solid";
import ChooseFontStory from "../../dropdown/ChooseFontStory.vue";
import themes from "../../../data/themes";
import fonts from "../../../data/fonts";
import ColorThief from "../../../../node_modules/colorthief/dist/color-thief.mjs";
import Slider from "@vueform/slider";

export default (await import("vue")).defineComponent({
  components: {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    Slider,
    ChooseFontStory,
    XMarkIcon,
    Cog8ToothIcon,
    PhotoIcon,
    ArrowPathIcon,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  props: {
    isOpen: Boolean,
    isTextStory: Boolean,
    textStories: Array,
  },

  data() {
    return {
      isMediaStory: false,
      isRotate: false,
      body: "",
      caption: "",
      url: null,
      is_private: false,
      only_me: false,
      color: null,
      fonts: fonts,
      selectedFont: {},
      selectedTheme: {},
      deg: null,
      toggle: 0,
      value: 25,
      zoom: 0.5,
      raw: null,
    };
  },

  computed: {
    themes() {
      return themes.reverse();
    },
  },

  methods: {
    getOption(selectedFont) {
      this.$emit("getOption", selectedFont);
      this.selectedFont = selectedFont;
    },
    chooseTheme(theme) {
      this.selectedTheme = theme;
    },
    async chooseMedia(e) {
      this.raw = this.$refs.story.files[0];
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
      await new Promise((resolve) => setTimeout(resolve, 200));
      this.getColor();
    },
    getColor() {
      const colorThief = new ColorThief();
      this.$nextTick(() => {
        let self = this;
        const img = self.$refs.myImage;

        if (img.complete) {
          const rgb = colorThief.getColor(img);
          this.color = `rgba(${rgb.toString()},1)`;
        } else {
          img.addEventListener("load", function () {
            colorThief.getColor(img);
          });
        }
      });
    },
    editImage() {
      this.isRotate = true;
    },
    rotate() {
      // let toggle = 0;
      this.toggle += 1;
      if (this.toggle === 4) {
        this.toggle = 0;
      }
      if (this.toggle === 1) {
        this.deg = "rotate-90";
      } else if (this.toggle === 2) {
        this.deg = "rotate-180";
      } else if (this.toggle === 3) {
        this.deg = "rotate-270";
      } else {
        this.deg = "rotate-0";
      }
    },

    removeAll() {
      this.url = null;
      this.color = null;
      this.body = "";
      this.selectedTheme = {};
      this.selectedFont = {};
      this.deg = "rotate-0";
      this.isRotate = false;
      this.zoom = 0.5;
    },
    submitForm() {
      if (this.isTextStory) {
        let formData = new FormData();

        formData.append("body", this.body);
        formData.append("is_private", this.is_private);
        formData.append("only_me", this.only_me);
        formData.append("theme", this.selectedTheme.name || "Cổ điển");
        formData.append("font", this.selectedFont.name || "Đơn giản");

        axios
          .post("/api/story/create-text-story/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            this.textStories.unshift(res.data);
            this.body = "";
            this.is_private = false;
            this.only_me = false;
            this.selectedFont = this.fonts[0];
            this.selectedTheme = this.themes[0];

            this.toastStore.showToast(
              2000,
              "Đã tạo tin",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 2500);
          })
          .catch((error) => {
            console.log("error", error);
          });
      }

      if (this.url) {
        let formData = new FormData();
        if (this.raw.name.includes(".png") || this.raw.name.includes(".jpg")) {
          formData.append("image", this.raw);
          formData.append("zoom_image", `${this.zoom + this.value / 50}`);
          formData.append("rotate", this.deg);
        } else {
          formData.append("video", this.raw);
        }

        formData.append("is_private", this.is_private);
        formData.append("only_me", this.only_me);
        formData.append("theme", this.color);
        formData.append("caption", this.caption);

        axios
          .post("/api/story/create-media-story/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            this.textStories.unshift(res.data);
            this.caption = "";
            this.is_private = false;
            this.only_me = false;
            this.color = null;
            this.url = null;
            this.raw = null;

            this.toastStore.showToast(
              2000,
              "Đã tạo tin",
              "bg-emerald-500 text-white"
            );
            setTimeout(() => {
              this.$router.go(0);
            }, 2500);
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
  },
});
</script>

<style src="@vueform/slider/themes/default.css"></style>

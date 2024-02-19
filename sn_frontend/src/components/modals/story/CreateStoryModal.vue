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
              <button
                @click="removeAll"
                class="m-4 p-2 bg-slate-900 rounded-full hover:bg-slate-700 lg:hidden absolute"
              >
                <XMarkIcon
                  @click="$emit('closeModal')"
                  class="text-neutral-200 h-8 w-8 cursor-pointer transition"
                />
              </button>
              <div
                class="lg:col-span-1 hidden bg-slate-800 dark:text-neutral-200 border-r-[1px] border-slate-700 lg:flex flex-col justify-between"
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
                    <h2 class="text-2xl font-bold min-w-max">Tin của bạn</h2>
                    <StoryPrivacySelector
                      @getOption="getOption"
                      :privacies="privacies"
                      v-model="privacy"
                      class="w-full"
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
                          @getFont="getFont"
                        />
                        <div
                          class="p-2 border mt-8 border-slate-700 rounded-lg max-h-max"
                        >
                          <h3 class="dark:text-neutral-200/70 text-lg">
                            Phông nền
                          </h3>
                          <div
                            class="flex flex-wrap gap-2 my-4 justify-center items-center"
                          >
                            <div v-for="theme in themes" :key="theme">
                              <div
                                @click="chooseTheme(theme)"
                                class="2xl:w-12 2xl:h-12 xl:h-10 xl:w-10 lg:w-8 lg:h-8 rounded-full cursor-pointer"
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
                    class="flex justify-center 2xl:py-2 2xl:px-4 py-1 px-2 w-[40%] dark:bg-slate-700 shadow-md rounded-lg font-semibold hover:bg-slate-600 transition duration-100 cursor-pointer"
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
                class="lg:col-span-4 col-span-5 flex lg:flex-row flex-col items-center gap-6 lg:py-12 lg:pt-0 py-6"
                :class="
                  isTextStory || url ? 'justify-evenly' : 'justify-center'
                "
              >
                <div
                  v-if="!isTextStory && !url"
                  class="group relative flex flex-col space-y-2 justify-center items-center xm:w-60 xm:h-[360px] xs:w-48 xs:h-[240px] bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg cursor-pointer"
                >
                  <PhotoIcon
                    class="text-neutral-200 h-14 w-14 cursor-pointer p-3 bg-slate-600 shadow-transparent rounded-full hover:bg-slate-600 transition duration-100"
                  />
                  <div
                    class="w-full h-full bg-white top-[-8px] bg-opacity-25 absolute hidden group-hover:block rounded-lg"
                  >
                    <label for="story-media">
                      <input
                        type="file"
                        ref="story"
                        id="story-media"
                        name="story-media"
                        @change="chooseMedia"
                        class="w-full h-full opacity-0 cursor-pointer"
                      />
                    </label>
                  </div>
                  <h4 class="font-bold text-neutral-200">Tạo tin ảnh</h4>
                </div>
                <div
                  v-if="!isTextStory && !url"
                  class="group relative flex flex-col space-y-2 justify-center items-center xm:w-60 xm:h-[360px] xs:w-48 xs:h-[240px] bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-lg cursor-pointer"
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
                  <h4 class="font-bold text-neutral-200 text-center">
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
                  class="bg-slate-800 h-full lg:w-[65%] xm:w-[80%] w-full rounded-xl p-4"
                >
                  <div
                    class="flex justify-center flex-col items-center bg-slate-900 h-full rounded-xl p-4 w-full"
                  >
                    <div
                      v-if="!url"
                      :class="[
                        selectedFont.font,
                        selectedTheme.background,
                        body ? 'text-neutral-200' : 'text-neutral-200/60',
                      ]"
                      class="h-full bg-emerald-500 2xl:w-[50%] xl:w-[70%] lg:w-[80%] sm:w-[60%] w-full border-4 rounded-xl flex justify-center items-center text-2xl font-semibold"
                    >
                      <p
                        class="break-words w-full text-center px-12"
                        :class="[selectedTheme.textColor]"
                      >
                        {{ body || "Bắt đầu nhập" }}
                      </p>
                    </div>
                    <div
                      v-else-if="url && isImage"
                      class="h-full 2xl:w-[50%] lg:w-[70%] sm:w-[60%] flex justify-center items-center text-2xl font-semibold text-neutral-200/50"
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
                      v-else
                      class="h-full w-[50%] flex justify-center items-center text-2xl font-semibold text-neutral-200/50 bg-black"
                    >
                      <video
                        autoplay
                        class="rounded-none w-full shadow-none"
                        :class="deg"
                        :style="{ scale: zoom + value / 50 }"
                        ref="myVideo"
                      >
                        <source :src="url" type="video/mp4" />
                      </video>
                    </div>
                    <div
                      v-if="isImage"
                      class="text-neutral-200 text-lg mt-4 flex items-center gap-3 w-full justify-center"
                    >
                      <h3 v-if="!isRotate && url" class="px-2 py-1">
                        Chọn ảnh để cắt và xoay
                      </h3>
                      <div
                        v-if="isRotate"
                        class="flex gap-3 justify-center items-center w-[50%] mx-auto"
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
                <div
                  class="bg-slate-800 dark:text-neutral-200 border-r-[1px] w-[90%] border-slate-700 flex justify-between lg:hidden overflow-x-scroll"
                >
                  <div class="flex">
                    <div v-if="isTextStory">
                      <div class="p-4">
                        <form class="flex">
                          <textarea
                            v-model="body"
                            @keyup="getContent"
                            class="lg:w-full py-2 pl-4 pr-8 bg-gray-100 border rounded-lg resize-none overflow-auto scrollbar-corner-slate-200 scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800"
                            name=""
                            id=""
                            :rows="3"
                            cols="30"
                            placeholder="Bắt đầu nhập"
                          ></textarea>
                          <ChooseFontStory
                            class="w-full"
                            :fonts="fonts"
                            @getFont="getFont"
                          />
                          <div
                            class="p-2 border border-slate-700 rounded-lg w-full"
                          >
                            <h3 class="dark:text-neutral-200/70 text-lg">
                              Phông nền
                            </h3>
                            <div
                              class="flex flex-wrap gap-2 justify-center items-center"
                            >
                              <div v-for="theme in themes" :key="theme">
                                <div
                                  @click="chooseTheme(theme)"
                                  class="2xl:w-12 2xl:h-12 xl:h-10 xl:w-10 lg:w-8 lg:h-8 h-4 w-4 rounded-full cursor-pointer"
                                  :class="[theme.background]"
                                ></div>
                              </div>
                            </div>
                          </div>
                        </form>
                      </div>
                    </div>
                    <div
                      v-if="url"
                      class="flex items-center justify-center space-y-4 p-4"
                    >
                      <div
                        class="p-4 flex flex-col justify-center gap-3 items-center font-semibold"
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
                  <div
                    class="my-4 px-6 flex flex-col justify-center items-center gap-2 w-full h-full"
                    v-if="isTextStory || url"
                  >
                    <div
                      @click="$emit('closeTextStory')"
                      class="flex justify-center 2xl:py-2 2xl:px-4 py-1 px-2 w-full dark:bg-slate-700 shadow-md rounded-lg font-semibold hover:bg-slate-600 transition duration-100 cursor-pointer"
                    >
                      <button @click="removeAll" class="w-full">Bỏ</button>
                    </div>
                    <button
                      @click="submitForm"
                      class="w-full dark:bg-emerald-500 hover:bg-emerald-400 py-2 px-4 shadow-md rounded-lg font-semibold"
                    >
                      <span class="md:block hidden">Chia sẻ lên tin</span>
                      <span class="md:hidden xs:block">Chia sẻ</span>
                    </button>
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
import StoryPrivacySelector from "../../dropdown/StoryPrivacySelector.vue";
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
    StoryPrivacySelector,
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
      isImage: false,
      privacies: [
        { name: "Công khai" },
        { name: "Bạn bè" },
        { name: "Chỉ mình tôi" },
      ],
      privacy: {},
    };
  },

  computed: {
    themes() {
      return themes.reverse();
    },
  },

  methods: {
    getFont(selectedFont) {
      this.$emit("getFont", selectedFont);
      this.selectedFont = selectedFont;
    },
    chooseTheme(theme) {
      this.selectedTheme = theme;
    },
    async chooseMedia(e) {
      this.raw = this.$refs.story.files[0];
      const file = e.target.files[0];
      if (
        this.raw.name.includes(".png") ||
        this.raw.name.includes(".jpg") ||
        this.raw.name.includes(".jpeg")
      ) {
        this.url = URL.createObjectURL(file);
        await new Promise((resolve) => setTimeout(resolve, 200));
        setTimeout(() => {
          this.getColor();
        }, 300);
        this.isImage = true;
      } else {
        this.url = URL.createObjectURL(file);
        this.isImage = false;
        setTimeout(() => {
          this.$refs.myVideo.volume = 0.1;
          console.log(typeof this.$refs.myVideo.duration);
        }, 50);
      }
    },
    async getColor() {
      if (
        this.raw.name.includes(".png") ||
        this.raw.name.includes(".jpg") ||
        this.raw.name.includes(".jpeg")
      ) {
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
      }
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
    getOption() {
      if (this.privacy.name === "Công khai") {
        this.is_private = false;
        this.only_me = false;
      }
      if (this.privacy.name === "Bạn bè") {
        this.is_private = true;
        this.only_me = false;
      }
      if (this.privacy.name === "Chỉ mình tôi") {
        this.is_private = true;
        this.only_me = true;
      }
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
        if (
          this.raw.name.includes(".png") ||
          this.raw.name.includes(".jpg") ||
          this.raw.name.includes(".jpeg")
        ) {
          formData.append("image", this.raw);
          formData.append("video", "");
          formData.append("zoom_image", `${this.zoom + this.value / 50}`);
          formData.append("rotate", this.deg);
          formData.append("duaration", 10);
        } else {
          formData.append("image", "");
          formData.append("zoom_image", `${this.zoom + this.value / 50}`);
          formData.append("rotate", this.deg);
          formData.append("video", this.raw);
          formData.append("duaration", this.$refs.myVideo.duration);
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

            if (
              this.raw?.name.includes(".png") ||
              this.raw?.name.includes(".jpg") ||
              this.raw?.name.includes(".jpeg")
            ) {
              this.toastStore.showToast(
                2000,
                "Đã tạo tin",
                "bg-emerald-500 text-white"
              );
            }

            if (
              (this.$refs.myVideo?.duration <= 20 &&
                !this.raw?.name.includes(".png")) ||
              !this.raw?.name.includes(".jpg") ||
              !this.raw?.name.includes(".jpeg")
            ) {
              this.toastStore.showToast(
                2000,
                "Đã tạo tin",
                "bg-emerald-500 text-white"
              );
              setTimeout(() => {
                this.$router.go(0);
              }, 2500);
            } else {
              this.toastStore.showToast(
                3000,
                "Video không được dài quá 20 giây",
                "bg-rose-500 text-white"
              );
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

<style src="@vueform/slider/themes/default.css"></style>

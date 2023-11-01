<template>
  <form v-on:submit.prevent="submitForm" method="post">
    <div class="p-4">
      <textarea
        v-model="body"
        class="p-4 w-full bg-gray-100 rounded-lg resize-none"
        cols="30"
        rows="4"
        placeholder="Bạn đang nghĩ gì?"
      ></textarea>
      <div class="flex justify-end items-center gap-3">
        <GlobeAsiaAustraliaIcon
          class="w-6 h-6"
          v-if="selection.name === 'Công khai'"
        />
        <UserGroupIcon
          class="w-6 h-6"
          v-else-if="selection.name === 'Bạn bè'"
        />
        <LockClosedIcon class="w-6 h-6" v-else />
        <Listbox v-model="selectedPrivacy" class="w-[20%]">
          <div class="relative mt-1 flex justify-end w-2/12">
            <ListboxButton
              class="relative flex justify-center w-full cursor-default rounded-lg font-semibold bg-gray-200 py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm"
            >
              <span class="block truncate">{{ selectedPrivacy.name }}</span>
              <span
                class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
              >
                <ChevronUpDownIcon
                  class="h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
              </span>
            </ListboxButton>

            <transition
              leave-active-class="transition duration-100 ease-in"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <ListboxOptions
                class="absolute mt-1 max-h-60 overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
              >
                <ListboxOption
                  v-slot="{ active, selected }"
                  v-for="selectOption in privacy"
                  :key="selectOption.name"
                  :value="selectOption"
                  as="template"
                  @click="getOption"
                >
                  <li
                    :class="[
                      active
                        ? 'bg-emerald-100 text-emerald-900'
                        : 'text-gray-900',
                      'relative cursor-default select-none py-2 pl-10 pr-4',
                    ]"
                  >
                    <span
                      :value="selection"
                      :class="[
                        selected ? 'font-medium' : 'font-normal',
                        'block truncate',
                      ]"
                      >{{ selectOption.name }}</span
                    >
                    <span
                      v-if="selected"
                      class="absolute inset-y-0 left-0 flex items-center pl-3 text-emerald-600"
                    >
                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                    </span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </transition>
          </div>
        </Listbox>
        
      </div>

      <div
        id="preview"
        v-if="url"
        class="flex relative justify-center items-center w-full p-4 border-[1px] rounded-lg"
      >
        <img :src="url" class="w-full rounded-lg" />
        <span class="absolute top-5 right-5 cursor-pointer" @click="removeImage"
          ><svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-8 h-8"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </span>
      </div>
    </div>

    <div class="p-4 border-t border-gray-100 flex justify-between">
      <label for="doc">
        <div
          class="py-3 px-6 text-black bg-gray-400 font-semibold rounded-lg transition-colors hover:bg-gray-600 hover:text-white cursor-pointer"
        >
          <span>Chọn ảnh</span>
        </div>
        <input
          type="file"
          ref="file"
          id="doc"
          name="doc"
          hidden
          @change="onFileChange"
        />
      </label>

      <button class="btn">Đăng bài viết</button>
    </div>
  </form>
</template>
<script>
import axios from "axios";
import {
  Listbox,
  ListboxLabel,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from "@headlessui/vue";
import {
  GlobeAsiaAustraliaIcon,
  UserGroupIcon,
  LockClosedIcon,
} from "@heroicons/vue/24/outline";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid";
import { ref } from "vue";

export default {
  components: {
    Listbox,
    ListboxLabel,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
    CheckIcon,
    ChevronUpDownIcon,
    GlobeAsiaAustraliaIcon,
    UserGroupIcon,
    LockClosedIcon,
  },
  setup() {
    const privacy = [
      { name: "Công khai" },
      { name: "Bạn bè" },
      { name: "Chỉ mình tôi" },
    ];
    const selectedPrivacy = ref(privacy[0]);

    return { selectedPrivacy };
  },
  props: {
    user: Object,
    posts: Array,
  },
  data() {
    return {
      body: "",
      url: null,
      is_private: false,
      only_me: false,
      privacy: [
        { name: "Công khai" },
        { name: "Bạn bè" },
        { name: "Chỉ mình tôi" },
      ],
      selection: "",
    };
  },
  mounted() {
    this.getOption();
  },
  methods: {
    getOption() {
      this.selection = this.selectedPrivacy;
      if (this.selection.name === "Công khai") {
        this.is_private = false;
        this.only_me = false;
      }
      if (this.selection.name === "Bạn bè") {
        this.is_private = true;
        this.only_me = false;
      }
      if (this.selection.name === "Chỉ mình tôi") {
        this.is_private = true;
        this.only_me = true;
      }
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },

    removeImage() {
      this.url = null;
    },
    submitForm() {
      console.log("submitForm", this.body);

      let formData = new FormData();
      formData.append("image", this.$refs.file.files[0]);
      formData.append("body", this.body);
      formData.append("is_private", this.is_private);
      formData.append("only_me", this.only_me);

      axios
        .post("/api/posts/create/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("data", res.data);

          this.posts.unshift(res.data);
          this.body = "";
          this.$refs.file.value = null;
          this.is_private = false;
          this.only_me = false;
          this.url = null;

          if (this.user) {
            this.user.posts_count += 1;
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
</script>

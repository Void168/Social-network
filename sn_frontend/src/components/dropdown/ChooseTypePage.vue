<template>
  <Combobox>
    <div class="relative mt-1">
      <div
        class="relative w-full cursor-default overflow-hidden rounded-lg bg-white dark:text-slate-200 dark:bg-slate-700 text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm"
      >
        <ComboboxInput
          class="w-full border-slate-500 border rounded-md py-2 pl-3 pr-10 text-sm leading-5 text-gray-900 dark:text-slate-200 dark:bg-slate-800 focus:ring-0"
          @change="query = $event.target.value"
          :displayValue="(type) => type.name"
        />
        <ComboboxButton
          class="absolute inset-y-0 right-0 flex items-center pr-2"
        >
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </ComboboxButton>
      </div>
      <TransitionRoot @after-leave="query = ''">
        <ComboboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto scrollbar-none hover:scrollbar-thin scrollbar-thumb-slate-400 scrollbar-track-slate-800 rounded-md bg-white dark:bg-slate-700 py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
        >
          <div
            v-if="filteredTypes.length === 0 && query !== ''"
            class="relative cursor-default select-none py-2 px-4 text-gray-700 dark:text-slate-200"
          >
            Không tìm thấy
          </div>
          <ComboboxOption
            v-for="type in filteredTypes"
            as="template"
            :key="type.id"
            :value="type"
            v-slot="{ selected, active }"
          >
            <li
              class="relative cursor-default select-none py-2 pl-10 pr-4"
              :class="{
                'bg-teal-600 text-white': active,
                'text-gray-900 dark:text-slate-200 dark:bg-slate-800': !active,
              }"
              @click="$emit('getOption')"
            >
              <span
                class="block truncate"
                :class="{
                  'font-medium': selected,
                  'font-normal': !selected,
                }"
              >
                {{ type.name }}
              </span>
              <span
                v-if="selected"
                class="absolute z-10 inset-y-0 left-0 flex items-center pl-3"
                :class="{
                  'text-white': active,
                  'text-teal-600': !active,
                }"
              >
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </TransitionRoot>
    </div>
  </Combobox>
</template>

<script>
import { ref } from "vue";
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from "@headlessui/vue";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid";

export default {
  components: {
    Combobox,
    ComboboxInput,
    ComboboxButton,
    ComboboxOptions,
    ComboboxOption,
    TransitionRoot,
    CheckIcon,
    ChevronUpDownIcon,
  },
  setup() {
    let selected = ref(null);
    let query = ref("");

    return {
      selected,
      query,
    };
  },

  props: {
    types: Array,
  },

  computed: {
    filteredTypes() {
      return this.query === ""
        ? this.types
        : this.types.filter((type) => {
            type.name
              .toLowerCase()
              .replace(/\s+/g, "")
              .normalize("NFD")
              .replace(/\p{Diacritic}/gu, "")
              .includes(
                this.query
                  .toLowerCase()
                  .replace(/\s+/g, "")
                  .normalize("NFD")
                  .replace(/\p{Diacritic}/gu, "")
              );
          });
    },
  },
};
</script>

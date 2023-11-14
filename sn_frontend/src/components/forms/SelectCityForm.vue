<template>
    <Combobox v-model="citySelected">
      <div class="relative mt-1">
        <div
          class="relative w-full cursor-default overflow-hidden rounded-lg bg-slate-200 dark:bg-slate-700 text-left shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm"
        >
          <ComboboxInput
            class="w-full border-none py-2 pl-3 pr-10 text-sm leading-5 bg-slate-200 dark:bg-slate-700 text-gray-900 dark:text-neutral-200 focus:ring-0"
            :displayValue="(city) => city.name"
            @change="query = $event.target.value"
          />
          <ComboboxButton
            class="absolute inset-y-0 right-0 flex items-center pr-2"
          >
            <ChevronUpDownIcon
              class="h-5 w-5 text-gray-400"
              aria-hidden="true"
            />
          </ComboboxButton>
        </div>
        <TransitionRoot
          leave="transition ease-in duration-100"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
          @after-leave="query = ''"
        >
          <ComboboxOptions
            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-slate-200 dark:bg-slate-700 py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
          >
            <div
              v-if="filteredCities.length === 0 && query !== ''"
              class="relative cursor-default select-none py-2 px-4 bg-slate-200 text-gray-700 dark:text-neutral-200"
            >
              Nothing found.
            </div>

            <ComboboxOption
              v-for="city in filteredCities"
              as="template"
              :key="city.latitude"
              :value="city"
              v-slot="{ selected, active }"
              v-on:click="$emit('selectCity')"
            >
              <li
                class="relative cursor-default select-none py-2 pl-10 pr-4"
                :class="{
                  'bg-teal-600 text-white': active,
                  'text-gray-900 dark:text-neutral-200': !active,
                }"
              >
                <span
                  class="block truncate"
                  :class="{ 'font-medium': selected, 'font-normal': !selected }"
                >
                  {{ city.name }}
                </span>
                <span
                  v-if="selected"
                  class="absolute inset-y-0 left-0 flex items-center pl-3"
                  :class="{ 'text-white': active, 'text-teal-600': !active }"
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
  props: {
    cities: Array,
    query: String,
    city: Object
  },
  data() {
    return {
        citySelected: this.city
    }
  },

  computed: {
    filteredCities() {
      return this.query === ""
        ? this.cities
        : this.cities.filter((city) =>
            city.name
              .toLowerCase()
              .replace(/\s+/g, "")
              .includes(this.query?.toLowerCase().replace(/\s+/g, ""))
          );
    },
  },

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
};
</script>

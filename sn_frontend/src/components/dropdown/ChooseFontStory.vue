<template>
  <Listbox v-model="selectedFont">
    <div class="relative mt-1 flex justify-end w-2/12">
      <ListboxButton
        class="relative flex items-center gap-4 w-full cursor-default rounded-lg bg-gray-200 dark:bg-slate-800 border dark:border-slate-700 dark:text-neutral-200 py-4 pl-3 lg:pr-10 text-left focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm"
      >
        <span class="text-lg">Aa</span>
        <span class="block truncate p-2 text-xl">{{
          selectedFont?.name || fonts[0].name
        }}</span>
        <span
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
        >
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>

      <transition
        leave-active-class="transition duration-100 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ListboxOptions
          class="absolute w-full top-20 z-50 mt-1 max-h-60 border overflow-auto rounded-md bg-white dark:bg-slate-800 dark:border-slate-700 dark:text-neutral-200 py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
        >
          <ListboxOption
            v-slot="{ active, selected }"
            v-for="font in fonts"
            :key="font.name"
            :value="font"
            as="template"
            @click="$emit('getFont', selectedFont)"
          >
            <li
              :class="[
                active
                  ? 'bg-emerald-100 text-emerald-900'
                  : 'text-gray-900 dark:text-neutral-200',
                'relative cursor-default select-none py-2 pl-10 pr-4',
              ]"
            >
              <span
                :value="selection"
                :class="[
                  selected ? 'font-medium' : 'font-normal',
                  'block truncate',
                ]"
                >{{ font.name }}</span
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
</template>

<script>
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
  props: {
    selection: Object,
    fonts: Object,
  },

  data() {
    return {
      selectedFont: {}
    }
  }
};
</script>

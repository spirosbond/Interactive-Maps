<template>
  <div class="flex justify-center items-center">
    <div
      class="bg-white rounded-lg shadow-lg p-4 w-80 border-b border-slate-200"
    >
      <button
        @click="toggleAccordion(1)"
        class="w-full flex justify-between items-center py-2 text-slate-800"
      >
        <span>Daylight Windows</span>
        <img
          :src="activeAccordion === 1 ? minusIcon : plusIcon"
          alt="Accordion Icon"
          class="text-slate-800 transition-transform duration-300 size-4"
        />
      </button>
      <div
        id="content"
        ref="content"
        class="max-h-0 overflow-hidden transition-all duration-300 ease-in-out"
      >
        <div class="pb-5 text-sm text-slate-500">
          <ul class="max-h-80 mt-4 overflow-y-auto">
            <li
              v-for="(time, index) in timeWindows"
              :key="index"
              class="flex justify-between items-center py-2 px-3 mb-2 mr-2 bg-gray-100 rounded-md shadow-sm"
            >
              <span class="text-gray-700">
                {{
                  new Date(time.start).toLocaleString("en-US", timeFormat)
                }}
                -
                {{
                  new Date(time.end).toLocaleString("en-US", timeFormat)
                }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import plusIcon from "~/assets/img/plus.svg";
import minusIcon from "~/assets/img/minus.svg";

// State for managing which accordion is active
const activeAccordion = ref(0);
// Accordion content. To be used in the toggleAccordion() function to change the DOM
const content = ref(null);

// Time windows data. Uses Composable that uses the backend api to pull all daylight windows
const timeWindows = useState("timeWindows", () => fetchDaylightWindows());

// Formatting dictionary for showing the windows nicely
const timeFormat = {
  day: "2-digit",
  month: "short",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false,
};

// Function called when the accordion is clicked. Manages Opening/Closing
const toggleAccordion = (index) => {
  if (activeAccordion.value === index) {
    activeAccordion.value = null; // Close accordion
    content.value.style.maxHeight = "0";
  } else {
    activeAccordion.value = index; // Open accordion
    content.value.style.maxHeight = content.value.scrollHeight + "px";
  }
};
</script>

<template>
  

<div class="flex justify-center items-center">
  <div class="bg-white rounded-lg shadow-lg p-4 w-80 border-b border-slate-200">
  <button @click="toggleAccordion(1)" class="w-full flex justify-between items-center py-2 text-slate-800">
    <span>Daylight Windows</span>
    <span id="icon-1" class="text-slate-800 transition-transform duration-300">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>

    </span>
  </button>
  <div id="content-1" class="max-h-0 overflow-hidden transition-all duration-300 ease-in-out">
    <div class="pb-5 text-sm text-slate-500">
      <ul
        class="max-h-80 mt-4 overflow-y-auto"
      >
        <li
          v-for="(time, index) in timeWindows"
          :key="index"
          class="flex justify-between items-center py-2 px-3 mb-2 mr-2 bg-gray-100 rounded-md shadow-sm"
        >
          <span class="text-gray-700">
            {{ new Date(time.start).toLocaleString("en-US",timeFormat)}} - {{ new Date(time.end).toLocaleString("en-US",timeFormat) }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</div>
</div>
</template>

<script setup lang="ts">

// Time windows data
const timeWindows = useState("timeWindows", () => "Loading...");
fetchDaylightWindows(timeWindows);
const timeFormat = {"day":"2-digit","month":"short","hour":"2-digit","minute":"2-digit","second":"2-digit","hour12":false}

// Adapted from: https://www.material-tailwind.com/docs/html/accordion
const toggleAccordion = (index) => {
    const content = document.getElementById(`content-${index}`);
    const icon = document.getElementById(`icon-${index}`);
 
    // SVG for Minus icon
    const minusSVG = `
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14" />
    </svg>`;
 
    // SVG for Plus icon
    const plusSVG = `
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>`;
 
    // Toggle the content's max-height for smooth opening and closing
    if (content.style.maxHeight && content.style.maxHeight !== '0px') {
      content.style.maxHeight = '0';
      icon.innerHTML = plusSVG;
    } else {
      content.style.maxHeight = content.scrollHeight + 'px';
      icon.innerHTML = minusSVG;
    }
  }
</script>

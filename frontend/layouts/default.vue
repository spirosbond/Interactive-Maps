<template>
  <div class="flex flex-col h-screen">
    <!-- <header class="bg-gray-800 text-white p-4">
      <h1 class="text-center text-2xl">Aerospacelab - Interactive Maps</h1>
    </header> -->
    <!-- <div class="flex flex-row w-full"> -->
        <AppTopBar></AppTopBar>
    <!-- </div> -->
    
      <!-- NuxtPage ensures the content here includes your MapView component -->
      <NuxtPage />
    <!-- <footer class="bg-gray-800 text-white text-center p-4">
      Footer Content
    </footer> -->
    <!-- <div class="flex flex-row w-full"> -->
    <AppFooter></AppFooter>
<!-- </div> -->
  </div>
</template>
<!-- 
<script setup>
// import AppTopBar from './AppTopBar.vue';
// import AppFooter from './AppFooter.vue';
</script> -->

<template>
    <div class="min-h-screen flex flex-col">
      <Navbar />
      <router-view class="flex-1" />
    </div>
  </template>
  
  <script>
  import Navbar from '/src/components/Director/Navbar.vue'
  
  export default {
    name: 'DirectorLayout',
    components: {
      Navbar
    }
  }
  </script>
  
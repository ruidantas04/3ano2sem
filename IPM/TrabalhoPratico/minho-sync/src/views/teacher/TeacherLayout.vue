<template>
    <div class="min-h-screen flex flex-col">
      <!-- Navbar sempre no topo -->
      <Navbar />
  
      <!-- Aqui ficam as páginas do diretor -->
      <router-view class="flex-1" />
    </div>
  </template>
  
  <script>
  import Navbar from '/src/components/teacher/Navbar.vue'
  
  export default {
    name: 'DirectorLayout',
    components: {
      Navbar
    }
  }
  </script>
  
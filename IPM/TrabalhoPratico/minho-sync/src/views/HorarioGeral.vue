<template>
  <div class="min-h-screen flex flex-col">
    <!-- Renderiza a navbar correta com base no tipo de usuário -->
    <DirectorNavbar v-if="userType === 'director'" />
    <TeacherNavbar v-else-if="userType === 'teacher'" />
    <StudentNavbar v-else-if="userType === 'student'" />
    <DefaultNavbar v-else />
    
    <!-- Conteúdo principal -->
    <main class="flex-1 p-6">
      <h1 class="text-2xl font-bold mb-4">Horário Geral</h1>
      
      <!-- Componente de horário -->
      <HorarioComponent />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DirectorNavbar from '../components/director/navbar.vue';
import TeacherNavbar from '../components/teacher/navbar.vue';
import StudentNavbar from '../components/student/navbar.vue';
import DefaultNavbar from '../components/Navbar.vue'; 
import HorarioComponent from '../components/Horario.vue';

const userType = ref(null);

// Função para obter o tipo de usuário do localStorage
onMounted(() => {
  userType.value = localStorage.getItem('userType') || null;
});
</script>
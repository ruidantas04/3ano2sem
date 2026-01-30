<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navbar baseada no tipo de usuário -->
    <DirectorNavbar v-if="userType === 'director'" />
    <TeacherNavbar v-else-if="userType === 'teacher'" />
    <StudentNavbar v-else-if="userType === 'student'" />
    <DefaultNavbar v-else />

    <!-- Conteúdo principal -->
    <div class="flex-1 flex items-center justify-center bg-gray-100 p-6">
      <div class="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
        <div class="text-9xl font-bold text-red-600 mb-4">404</div>
        <h1 class="text-2xl font-bold text-gray-800 mb-2">Página Não Encontrada</h1>
        <p class="text-gray-600 mb-6">Ops! A página que você está procurando não existe.</p>
        <div class="flex flex-col sm:flex-row justify-center gap-3">
          <button 
            @click="goToHomePage" 
            class="bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
          >
            <span class="flex items-center justify-center">
              Página Inicial
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import DirectorNavbar from '../components/director/navbar.vue';
import TeacherNavbar from '../components/teacher/navbar.vue';
import StudentNavbar from '../components/student/navbar.vue';
import DefaultNavbar from '../components/Navbar.vue'; 

const router = useRouter();
const userType = ref(null);
const hasUserType = ref(false);

onMounted(() => {
  const storedUserType = localStorage.getItem('userType');
  userType.value = storedUserType;
  hasUserType.value = !!storedUserType;
});
 

function goToHomePage() {
   if (userType.value === 'director') {
    router.push('/director/dashboard');
  } else if (userType.value === 'teacher') {
    router.push('/teacher/course');
  } else if (userType.value === 'student') {
    router.push('/student/schedule');
  } else {
    router.push('/schedule'); // Página pública de horário como fallback
  }
}
</script>
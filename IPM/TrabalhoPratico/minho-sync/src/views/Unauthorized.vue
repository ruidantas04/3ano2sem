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
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-red-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h1 class="text-2xl font-bold text-gray-800 mb-2">Acesso Não Autorizado</h1>
        <p class="text-gray-600 mb-6">Você não tem permissão para acessar esta página.</p>
        <button 
          @click="goToHomePage" 
          class="bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
        >
          Voltar para a página inicial
        </button>
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
const showDirectorNavbar = ref(false);
const showTeacherNavbar = ref(false);
const showStudentNavbar = ref(false);
const showDefaultNavbar = ref(false);

onMounted(() => {
  const storedUserType = localStorage.getItem('userType');
  userType.value = storedUserType;

  showDirectorNavbar.value = storedUserType === 'director';
  showTeacherNavbar.value = storedUserType === 'teacher';
  showStudentNavbar.value = storedUserType === 'student';
  showDefaultNavbar.value = !['director', 'teacher', 'student'].includes(storedUserType);
});

function goToHomePage() {
  // Redireciona para a página inicial apropriada com base no tipo de usuário
  if (userType.value === 'director') {
    router.push('/director/dashboard');
  } else if (userType.value === 'teacher') {
    router.push('/teacher/course');
  } else if (userType.value === 'student') {
    router.push('/student/schedule');
  } else {
    router.push('/login');
  }
}
</script>
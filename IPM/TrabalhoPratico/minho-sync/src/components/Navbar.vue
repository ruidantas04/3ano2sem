<template>
  <div class="pt-[20px] px-[20px] pb-[0px]">
    <nav class="bg-red text-white shadow-md rounded-lg">
      <div class="container mx-auto px-6 py-2">
        <div class="flex justify-between items-center h-12">
          <!-- Logo e título -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <div class="flex items-center justify-center mr-2">
                <img src="/images/logotipo_branco.png" alt="Logo" class="h-8 w-8"/>
              </div>
              <span class="font-bold text-xl">MinhoSync</span>
            </router-link>
          </div>

          <!-- Links de navegação -->
          <div class="hidden md:flex items-center space-x-6">
            <router-link to="/schedule" class="text-white  hover:text-gray-300 transition-colors duration-200" :class="{ 'font-bold': isActive('/schedule') }">Horário</router-link>
          </div>

          <!-- Ícones à direita -->
          <div class="hidden md:flex items-center space-x-4">
            <!-- Ícone de perfil -->
            <div class="relative" ref="profileMenu">
              <router-link to="/login" class="flex items-center">
                <div class="p-1 rounded-lg bg-white hover:bg-gray-300 transition-colors duration-200 focus:outline-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="black">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Menu mobile (hamburger) -->
          <div class="md:hidden">
            <button @click="toggleMobileMenu" class="p-1 rounded-full hover:bg-red-700 focus:outline-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Menu mobile expandido -->
        <div v-if="mobileMenuOpen" class="md:hidden">
          <div class="flex flex-col space-y-1">
            <router-link 
              to="/schedule" 
              class="py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200">
              Horario
            </router-link>
          
            <router-link 
              to="/login" 
              class="py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
            >
              Login
            </router-link>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const mobileMenuOpen = ref(false);
const showProfileMenu = ref(false);
const profileMenu = ref(null);
const userName = ref('');


// Verifica se a rota atual corresponde ao caminho fornecido
const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};

// Toggle para o menu mobile
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  if (mobileMenuOpen.value) {
    showProfileMenu.value = false;
  }
};

// Função para fechar o menu de perfil quando clicar fora dele
const handleClickOutside = (event) => {
  if (profileMenu.value && !profileMenu.value.contains(event.target)) {
    showProfileMenu.value = false;
  }
};

// Remover event listener quando o componente for desmontado
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>
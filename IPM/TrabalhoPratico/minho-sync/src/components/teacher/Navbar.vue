<template>
  <div class="pt-[20px] px-[20px] pb-[0px]">
    <nav class="bg-red-800 text-white shadow-md rounded-lg">
      <div class="container mx-auto px-6 py-2">
        <div class="flex justify-between items-center h-12">
          <!-- Logo e título -->
          <div class="flex items-center">
            <router-link to="/director" class="flex items-center">
              <div class="flex items-center justify-center mr-2">
                <img src="/images/logotipo_branco.png" alt="Logo" class="h-8 w-8"/>
              </div>
              <span class="font-bold text-xl">MinhoSync</span>
            </router-link>
          </div>

          <!-- Links de navegação -->
          <div class="hidden md:flex items-center space-x-6">
            <router-link 
              to="/teacher/schedule" 
              class="text-white hover:text-gray-300 transition-colors duration-200" 
              :class="{ 'font-bold': isActive('/teacher/manual-allocation') }"
            >
              Horário
            </router-link>
            <router-link 
              to="/teacher/request-form" 
              class="text-white hover:text-gray-300 transition-colors duration-200" 
              :class="{ 'font-bold': isActive('/teacher/requests') }"
            >
              Formúlario de Pedidos
            </router-link>
          </div>

          <!-- Ícones à direita -->
          <div class="hidden md:flex items-center space-x-4">
            <!-- Ícone de notificações -->
            <div class="relative" ref="notificationsMenu">
              <button 
                @click="toggleNotificationsMenu" 
                class="p-1 rounded-lg bg-white hover:bg-gray-300 transition-colors duration-200 focus:outline-none relative"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="black">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <!-- Badge de notificações -->
                <div v-if="notificationCount > 0" class="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {{ notificationCount }}
                </div>
              </button>
              
              <!-- Menu de notificações -->
              <div 
                v-if="showNotificationsMenu" 
                class="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg py-1 z-10"
              >
                <div class="px-4 py-2 text-red-600 font-medium border-b flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                  Notificações
                  <span v-if="notificationCount > 0" class="ml-2 bg-red-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {{ notificationCount }}
                  </span>
                </div>
                
                <!-- Lista de notificações -->
                <div class="max-h-80 overflow-y-auto">
                  <div 
                    v-for="(notification, index) in notifications" 
                    :key="index" 
                    class="border-b border-gray-100 last:border-b-0"
                  >
                    <a 
                      href="#" 
                      class="block px-4 py-3 hover:bg-gray-50 transition-colors duration-200"
                    >
                      <div class="flex justify-between items-center">
                        <div>
                          <p class="text-sm text-gray-800">{{ notification.message }}</p>
                          <p class="text-xs text-gray-500 mt-1">Pedido por: {{ notification.requestedBy }}</p>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </a>
                  </div>
                </div>
                
                <!-- Se não houver notificações -->
                <div v-if="notifications.length === 0" class="px-4 py-3 text-sm text-gray-500 text-center">
                  Não há notificações no momento.
                </div>
              </div>
            </div>

            <!-- Ícone de perfil / Logout -->
            <div class="relative" ref="profileMenu">
              <button 
                @click="toggleProfileMenu" 
                class="p-1 rounded-lg bg-white hover:bg-gray-300 transition-colors duration-200 focus:outline-none"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="black">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </button>
              
              <!-- Menu de perfil -->
              <div 
                v-if="showProfileMenu" 
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
              >
                <router-link 
                  to="/director/profile" 
                  class="flex items-center px-4 py-3 text-sm text-gray-800 hover:bg-gray-50 transition-colors duration-200"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Perfil
                </router-link>
                <a 
                  href="#" 
                  @click.prevent="logout" 
                  class="flex items-center px-4 py-3 text-sm text-gray-800 hover:bg-gray-50 transition-colors duration-200"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Sair
                </a>
              </div>
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
              to="/student/schedule" 
              class="py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
              :class="{ 'font-bold': isActive('/director/manual-allocation') }"
            >
              Horário
            </router-link>
            <router-link 
              to="/student/request-form" 
              class="py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
              :class="{ 'font-bold': isActive('/director/requests') }"
            >
              Formúlario de Pedidos
            </router-link>
            <router-link 
              to="/student/profile" 
              class="py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
            >
              Perfil
            </router-link>
            <a 
              href="#" 
              @click.prevent="logout" 
              class="py-2 px-4 rounded hover:bg-red-700 transition-colors duration-200"
            >
              Sair
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const mobileMenuOpen = ref(false);
const showProfileMenu = ref(false);
const showNotificationsMenu = ref(false);
const profileMenu = ref(null);
const notificationsMenu = ref(null);
const userName = ref('');

// Dados de notificações (simulados)
const notifications = ref([
 
]);

// Número de notificações
const notificationCount = ref(notifications.value.length);

// Verifica se a rota atual corresponde ao caminho fornecido
const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};

// Toggle para o menu mobile
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  if (mobileMenuOpen.value) {
    showProfileMenu.value = false;
    showNotificationsMenu.value = false;
  }
};

// Toggle para o menu de perfil
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
  if (showProfileMenu.value) {
    showNotificationsMenu.value = false;
  }
};

// Toggle para o menu de notificações
const toggleNotificationsMenu = () => {
  showNotificationsMenu.value = !showNotificationsMenu.value;
  if (showNotificationsMenu.value) {
    showProfileMenu.value = false;
  }
};

// Função para fechar os menus quando clicar fora deles
const handleClickOutside = (event) => {
  if (profileMenu.value && !profileMenu.value.contains(event.target)) {
    showProfileMenu.value = false;
  }
  if (notificationsMenu.value && !notificationsMenu.value.contains(event.target)) {
    showNotificationsMenu.value = false;
  }
};

// Função de logout
const logout = () => {
  // Limpar dados de autenticação
  localStorage.removeItem('token');
  localStorage.removeItem('userType');
  localStorage.removeItem('userId');
  localStorage.removeItem('userName');
  
  // Redirecionar para a página de login
  router.push('/login');
};

// Carregar nome do usuário do localStorage
const storedName = ref(localStorage.getItem('userName') || '');

onMounted(() => {
  // Adicionar event listener para fechar o menu quando clicar fora
  document.addEventListener('click', handleClickOutside);
});

// Remover event listener quando o componente for desmontado
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>
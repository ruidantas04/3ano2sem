<template>
  <div class="h-screen w-full flex flex-col md:flex-row">
    <!-- Coluna Esquerda (Fundo Vermelho) -->
    <div class="md:w-1/2 bg-red-700 text-white flex flex-col justify-between p-8">
          <!-- Topo -->
          <div>
            <h1 class="text-4xl font-bold mb-4">MinhoSync</h1>
            <p class="text-xl mb-4">O teu horário, sincronizado ao teu ritmo!</p>
          </div>

          <!-- Rodapé (citação) -->
          <div>
            <p class="italic text-sm">
              "O saber começa com a gestão eficiente dos turnos" - Socrátes
            </p>
          </div>
        </div>

    <!-- Coluna Direita (Fundo Branco) -->
    <div class="md:w-1/2 bg-white flex flex-col justify-center items-center p-8">
      <div class="w-full max-w-sm">
        <!-- Título e Subtítulo -->
        <h2 class="text-xl font-semibold mb-2">Entre na sua conta</h2>
        <p class="text-sm text-gray-500 mb-6">
          Faça a autenticação para entrar no sistema
        </p>

        <!-- Formulário de Login -->
        <form @submit.prevent="login" class="space-y-4">
          <!-- Removida a seleção de Role, pois será definida automaticamente -->
          
          <!-- Email -->
          <div>
            <label class="block text-gray-700 mb-1" for="email">Email</label>
            <input
              v-model="email"
              id="email"
              type="email"
              placeholder="ex: usuario@dominio.com"
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-gray-700 mb-1" for="password">Password</label>
            <input
              v-model="password"
              id="password"
              type="password"
              placeholder="Password"
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <!-- Botão Entrar -->
          <button
            type="submit"
            class="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded transition-colors duration-200"
          >
            Entrar no sistema
          </button>
        </form>

        <!-- Mensagem de Erro -->
        <div v-if="errorMessage" class="mt-4 text-red-500 text-center">
          {{ errorMessage }}
        </div>

        <!-- Rodapé -->
        <p class="mt-2 text-center text-xs text-gray-400">
          Todos direitos reservados ao MinhoSync
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const router = useRouter()

async function login() {
  errorMessage.value = ''
  isLoading.value = true

  let user = null; // Define user outside the try block
  try {
    if (email.value.trim().toLowerCase().endsWith('@alunos.uminho.pt')) {
      const response = await axios.get('http://localhost:3000/students', {
        params: { email: email.value, password: password.value }
      })
      user = response.data[0]
      if (user) {
        // Armazenar informações do usuário
        localStorage.setItem('token', 'student-token') // Simulação de token
        localStorage.setItem('userType', 'student')
        localStorage.setItem('userId', user.id)
        localStorage.setItem('userName', user.name)
        
        router.push('/student/schedule')
      } else {
        errorMessage.value = 'Credenciais inválidas. Tente novamente.'
      }
    } else {
      // Primeiro tenta o endpoint de diretores
      let response = await axios.get('http://localhost:3000/directors', {
        params: { email: email.value, password: password.value }
      })
      user = response.data[0]

      if (user) {
        // Armazenar informações do usuário
        localStorage.setItem('token', 'director-token') // Simulação de token
        localStorage.setItem('userType', 'director')
        localStorage.setItem('userId', user.id)
        localStorage.setItem('userName', user.name)
        
        router.push('/director/dashboard')
      } else {
        // Se não for diretor, tenta o endpoint de professores
        response = await axios.get('http://localhost:3000/teachers', {
          params: { email: email.value, password: password.value }
        })
        user = response.data[0]
        if (user) {
          // Armazenar informações do usuário
          localStorage.setItem('token', 'teacher-token') // Simulação de token
          localStorage.setItem('userType', 'teacher')
          localStorage.setItem('userId', user.id)
          localStorage.setItem('userName', user.name)
          
          router.push('/teacher/course')
        } else {
          errorMessage.value = 'Credenciais inválidas. Tente novamente.'
        }
      }
    }
  } catch (error) {
    errorMessage.value = 'Erro ao tentar fazer login.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

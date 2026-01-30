<template>
    <div class="p-6 font-sans bg-gray-50 min-h-screen">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-4">
          <img src="https://i.pravatar.cc/100?img=3" class="w-16 h-16 rounded-full" alt="Avatar">
          <h2 class="text-2xl font-bold text-gray-800">{{ aluno?.name?.split(' ')[0] }} S.</h2>
        </div>
        <div class="space-x-2">
          <button class="bg-red-700 text-white px-4 py-2 rounded-full hover:bg-red-800">Editar Perfil</button>
          <button @click="$router.back()" class="border border-red-700 text-red-700 px-4 py-2 rounded-full hover:bg-red-100">Voltar</button>
        </div>
      </div>
  
      <!-- Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Coluna esquerda -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Informações Pessoais -->
          <div class="bg-white rounded-lg shadow p-4">
            <h3 class="text-lg font-semibold mb-2">Informações Pessoais</h3>
            <p><strong>Nome:</strong> {{ aluno?.name }}</p>
            <p><strong>Idade:</strong> {{ aluno?.age }} Anos</p>
            <p><strong>Localização:</strong> {{ aluno?.location }}</p>
            <p><strong>Interesses:</strong> {{ aluno?.interests }}</p>
          </div>
  
          <!-- Objetivos -->
          <div class="bg-white rounded-lg shadow p-4">
            <h3 class="text-lg font-semibold mb-2">Objetivos e Desafios</h3>
            <p><strong>Objetivos:</strong> {{ aluno?.goals }}</p>
            <p><strong>Desafios:</strong> {{ aluno?.challenges }}</p>
            <p><strong>Soluções:</strong> {{ aluno?.solutions }}</p>
          </div>
  
          <!-- Citação -->
          <div class="bg-gray-100 italic text-sm text-gray-700 p-4 rounded shadow">
            “{{ aluno?.quote }}” - {{ aluno?.name?.split(' ')[0] }}
          </div>
        </div>
  
        <!-- Coluna direita -->
        <div class="bg-white rounded-lg shadow p-4 space-y-2">
          <h3 class="text-lg font-semibold mb-4">Detalhes Académicos</h3>
          <p><strong>Tipo:</strong> {{ aluno?.degreeType }}</p>
          <p><strong>Ano Atual:</strong> {{ aluno?.year }}º Ano</p>
          <p><strong>Média Atual:</strong> {{ aluno?.gpa }} Valores</p>
          <p><strong>Estatuto:</strong> {{ aluno?.status }}</p>
          <p><strong>Aluno Mecanográfico:</strong> {{ aluno?.studentCode }}</p>
          <p><strong>Email:</strong> {{ aluno?.email }}</p>
          <p><strong>UCs Inscritas no Semestre:</strong> {{ aluno?.coursesEnrolled }}</p>
          <button class="bg-red-700 text-white w-full py-2 mt-2 rounded hover:bg-red-800">Ver Horário</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const aluno = ref(null)
  
  onMounted(async () => {
    const id = route.params.studentId
    try {
      const res = await axios.get(`http://localhost:3000/students/${id}`)
      aluno.value = res.data
    } catch (err) {
      console.error('Erro ao buscar aluno:', err)
    }
  })
  </script>
  
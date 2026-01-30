<template>
    <div class="p-10 max-w-4xl mx-auto bg-white rounded shadow">
      <!-- Cabeçalho -->
      <div class="border-b pb-4 mb-6">
        <h2 class="text-2xl font-bold text-red-700">Pedido de Mudança de Turno</h2>
        <p class="text-sm text-gray-600 mt-1">
          Solicitação recebida em {{ pedido?.data || '...' }} -
          <span :class="{
            'text-yellow-500': pedido?.response === 'pending',
            'text-green-600': pedido?.response === 'ok',
            'text-red-500': pedido?.response === 'rejected'
          }">
            {{ mapStatus(pedido?.response) }}
          </span>
        </p>
      </div>
  
      <!-- Formulário -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Estudante</label>
          <input type="text" class="w-full p-2 border rounded bg-gray-100"
            :value="student ? `${student.name} (${student.email})` : 'Carregando...'" disabled />
        </div>
  
        <div>
          <label class="block text-sm font-medium text-gray-700">Assunto</label>
          <input type="text" class="w-full p-2 border rounded bg-gray-100" value="Mudança de Turno" disabled />
        </div>
  
        <div>
          <label class="block text-sm font-medium text-gray-700">Unidade Curricular</label>
          <input type="text" class="w-full p-2 border rounded bg-gray-100" :value="course?.name || '---'" disabled />
        </div>
  
        <div>
          <label class="block text-sm font-medium text-gray-700">Turno Atual</label>
          <input type="text" class="w-full p-2 border rounded bg-gray-100"
            :value="turnoAtual ? `${turnoAtual.name} (${formatHorario(turnoAtual)})` : '---'" disabled />
        </div>
  
        <div>
          <label class="block text-sm font-medium text-gray-700">Turno Pretendido</label>
          <input type="text" class="w-full p-2 border rounded bg-gray-100"
            :value="turnoPretendido ? `${turnoPretendido.name} (${formatHorario(turnoPretendido)})` : '---'" disabled />
        </div>
  
        <div>
          <label class="block text-sm font-medium text-gray-700">Motivo da Mudança</label>
          <textarea class="w-full p-2 border rounded bg-gray-100" rows="4" :value="pedido?.reason" disabled></textarea>
        </div>
      </div>
  
      <!-- Botões -->
      <div class="flex justify-end gap-4 mt-6">
        <button @click="atualizarStatus('rejected')"
          class="bg-gray-200 hover:bg-gray-300 text-red-700 font-semibold px-4 py-2 rounded">
          Rejeitar Pedido
        </button>
        <button @click="atualizarStatus('ok')"
          class="bg-red-700 hover:bg-red-800 text-white font-semibold px-4 py-2 rounded">
          Aprovar Pedido
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  
  export default {
    setup() {
      const route = useRoute()
      const router = useRouter()
      const pedidoId = route.params.id
  
      const pedido = ref(null)
      const student = ref(null)
      const turnoAtual = ref(null)
      const turnoPretendido = ref(null)
      const course = ref(null)
  
      const mapStatus = (status) => {
        if (status === 'ok') return 'Aprovado'
        if (status === 'rejected') return 'Rejeitado'
        return 'Pendente'
      }
  
      const formatHorario = (turno) => {
        return `${turno.day} ${turno.from}h-${turno.to}h`
      }
  
      const fetchPedido = async () => {
        try {
          const res = await axios.get(`http://localhost:3000/shiftRequests?id=${pedidoId}`)
          if (!res.data || res.data.length === 0) {
            throw new Error(`Pedido com ID ${pedidoId} não encontrado.`)
          }
  
          pedido.value = res.data[0]
  
          const studentRes = await axios.get(`http://localhost:3000/students/${pedido.value.studentId}`)
          student.value = studentRes.data
  
          const turnoPretendidoRes = await axios.get(`http://localhost:3000/shifts/${pedido.value.shiftId}`)
          turnoPretendido.value = turnoPretendidoRes.data
  
          if (pedido.value.fromShiftId) {
            const turnoAtualRes = await axios.get(`http://localhost:3000/shifts/${pedido.value.fromShiftId}`)
            turnoAtual.value = turnoAtualRes.data
          }
  
          const courseId = turnoPretendido.value?.courseId || turnoAtual.value?.courseId
          if (courseId) {
            const courseRes = await axios.get(`http://localhost:3000/courses/${courseId}`)
            course.value = courseRes.data
          }
        } catch (error) {
          console.error('Erro ao carregar pedido:', error)
        }
      }
  
      const atualizarStatus = async (novoStatus) => {
        try {
          await axios.patch(`http://localhost:3000/shiftRequests/${pedido.value.id}`, {
            response: novoStatus
          })
          pedido.value.response = novoStatus
          alert(`Pedido ${mapStatus(novoStatus)} com sucesso!`)
          router.push('/director/requests')
        } catch (err) {
          console.error('Erro ao atualizar o status do pedido:', err)
        }
      }
  
      onMounted(fetchPedido)
  
      return {
        pedido,
        student,
        turnoAtual,
        turnoPretendido,
        course,
        formatHorario,
        mapStatus,
        atualizarStatus
      }
    }
  }
  </script>
  
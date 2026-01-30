<template>
    <div class="notifications-container">
      <div v-if="loading" class="text-center py-4">
        <div class="animate-spin h-5 w-5 border-t-2 border-red-600 border-solid rounded-full mx-auto"></div>
        <p class="text-sm text-gray-500 mt-2">Carregando notificações...</p>
      </div>
      
      <div v-else-if="error" class="text-center py-4 text-red-600">
        <p>Erro ao carregar notificações</p>
      </div>
      
      <div v-else-if="notifications.length === 0" class="text-center py-4">
        <p class="text-sm text-gray-500">Não há notificações</p>
      </div>
      
      <template v-else>
        <div v-for="notification in notifications" :key="notification.id" 
             class="notification-item p-3 border-b border-gray-200 hover:bg-gray-50 transition-colors duration-150"
             :class="{ 'bg-gray-50': !notification.seen }">
          <div class="flex items-start">
            <div class="flex-shrink-0 mr-3">
              <!-- Ícone baseado no tipo de notificação -->
              <div v-if="notification.type === 'shiftRequest'" 
                   class="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div v-else-if="notification.type === 'classroomRequest'" 
                   class="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
            </div>
            
            <div class="flex-1">
              <div class="flex justify-between">
                <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                <span class="text-xs text-gray-500">{{ formatDate(notification.date) }}</span>
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ notification.message }}</p>
              
              <!-- Ações para notificações que precisam de resposta (apenas para o diretor) -->
              <div v-if="notification.requiresAction && userType === 'director'" class="mt-2 flex space-x-2">
                <button @click="approveRequest(notification)" 
                        class="px-3 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 transition-colors">
                  Aprovar
                </button>
                <button @click="rejectRequest(notification)" 
                        class="px-3 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition-colors">
                  Rejeitar
                </button>
              </div>
              
              <!-- Botão para marcar como lida -->
              <button v-if="!notification.seen" 
                      @click="markAsSeen(notification)" 
                      class="mt-2 text-xs text-gray-500 hover:text-gray-700">
                Marcar como lida
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed, watch } from 'vue';
  import axios from 'axios';
  
  const props = defineProps({
    userType: {
      type: String,
      required: true
    },
    userId: {
      type: Number,
      required: true
    }
  });
  
  const notifications = ref([]);
  const loading = ref(true);
  const error = ref(null);
  const shiftRequests = ref([]);
  const classroomRequests = ref([]);
  const students = ref([]);
  const teachers = ref([]);
  const shifts = ref([]);
  const classrooms = ref([]);
  
  // Buscar dados necessários
  onMounted(async () => {
    try {
      loading.value = true;
      
      // Buscar todos os dados necessários em paralelo
      const [
        shiftRequestsRes, 
        classroomRequestsRes, 
        studentsRes, 
        teachersRes, 
        shiftsRes, 
        classroomsRes
      ] = await Promise.all([
        axios.get('http://localhost:3000/shiftRequests'),
        axios.get('http://localhost:3000/classroomRequests'),
        axios.get('http://localhost:3000/students'),
        axios.get('http://localhost:3000/teachers'),
        axios.get('http://localhost:3000/shifts'),
        axios.get('http://localhost:3000/classrooms')
      ]);
      
      shiftRequests.value = shiftRequestsRes.data;
      classroomRequests.value = classroomRequestsRes.data;
      students.value = studentsRes.data;
      teachers.value = teachersRes.data;
      shifts.value = shiftsRes.data;
      classrooms.value = classroomsRes.data;
      
      // Gerar notificações com base nos dados
      generateNotifications();
      
    } catch (err) {
      console.error('Erro ao buscar dados:', err);
      error.value = err;
    } finally {
      loading.value = false;
    }
  });
  
  // Função para gerar notificações com base nos pedidos
  function generateNotifications() {
    const allNotifications = [];
    
    // Processar pedidos de turno
    shiftRequests.value.forEach(request => {
      const student = students.value.find(s => s.id === request.studentId);
      const shift = shifts.value.find(s => s.id === request.shiftId);
      const alternativeShift = request.alternativeShiftId 
        ? shifts.value.find(s => s.id === request.alternativeShiftId)
        : null;
      
      if (!student || !shift) return;
      
      const studentName = student.name || `Estudante #${student.id}`;
      const shiftName = shift.name || `Turno #${shift.id}`;
      const alternativeShiftName = alternativeShift 
        ? (alternativeShift.name || `Turno #${alternativeShift.id}`)
        : null;
      
      let title, message;
      let requiresAction = false;
      
      // Diferentes mensagens baseadas no tipo de usuário e status do pedido
      if (props.userType === 'director') {
        // Notificações para o diretor
        if (request.response === 'pending') {
          title = `Novo pedido de mudança de turno`;
          message = `${studentName} solicitou mudança do turno ${shiftName}${alternativeShiftName ? ` para ${alternativeShiftName}` : ''}.`;
          requiresAction = true;
        } else if (request.response === 'ok') {
          title = `Pedido de turno aprovado`;
          message = `Você aprovou o pedido de ${studentName} para mudar de turno.`;
        } else if (request.response === 'rejected') {
          title = `Pedido de turno rejeitado`;
          message = `Você rejeitou o pedido de ${studentName} para mudar de turno.`;
        }
      } else if (props.userType === 'student' && props.userId === request.studentId) {
        // Notificações para o estudante que fez o pedido
        if (request.response === 'pending') {
          title = `Pedido de mudança de turno pendente`;
          message = `Seu pedido para mudar do turno ${shiftName}${alternativeShiftName ? ` para ${alternativeShiftName}` : ''} está em análise.`;
        } else if (request.response === 'ok') {
          title = `Pedido de turno aprovado`;
          message = `Seu pedido para mudar do turno ${shiftName}${alternativeShiftName ? ` para ${alternativeShiftName}` : ''} foi aprovado.`;
        } else if (request.response === 'rejected') {
          title = `Pedido de turno rejeitado`;
          message = `Seu pedido para mudar do turno ${shiftName}${alternativeShiftName ? ` para ${alternativeShiftName}` : ''} foi rejeitado.`;
        }
      } else {
        // Não é relevante para este usuário
        return;
      }
      
      // Adicionar à lista de notificações
      allNotifications.push({
        id: `shift_${request.id}`,
        type: 'shiftRequest',
        title,
        message,
        date: new Date(), // Idealmente, usar a data real do pedido
        seen: props.userType === 'student' ? request.responseSeenByStudent : true,
        requiresAction,
        originalRequest: request
      });
    });
    
    // Processar pedidos de sala de aula
    classroomRequests.value.forEach(request => {
      const teacher = teachers.value.find(t => t.id === request.teacherId);
      const classroom = classrooms.value.find(c => c.id === request.classroomId);
      
      if (!teacher || !classroom) return;
      
      const teacherName = teacher.name || `Professor #${teacher.id}`;
      const classroomName = classroom.name || `Sala #${classroom.id}`;
      
      let title, message;
      let requiresAction = false;
      
      // Diferentes mensagens baseadas no tipo de usuário e status do pedido
      if (props.userType === 'director') {
        // Notificações para o diretor
        if (request.response === 'pending') {
          title = `Novo pedido de sala de aula`;
          message = `${teacherName} solicitou a sala ${classroomName}.`;
          requiresAction = true;
        } else if (request.response === 'ok') {
          title = `Pedido de sala aprovado`;
          message = `Você aprovou o pedido de ${teacherName} para a sala ${classroomName}.`;
        } else if (request.response === 'rejected') {
          title = `Pedido de sala rejeitado`;
          message = `Você rejeitou o pedido de ${teacherName} para a sala ${classroomName}.`;
        }
      } else if (props.userType === 'teacher' && props.userId === request.teacherId) {
        // Notificações para o professor que fez o pedido
        if (request.response === 'pending') {
          title = `Pedido de sala pendente`;
          message = `Seu pedido para a sala ${classroomName} está em análise.`;
        } else if (request.response === 'ok') {
          title = `Pedido de sala aprovado`;
          message = `Seu pedido para a sala ${classroomName} foi aprovado.`;
        } else if (request.response === 'rejected') {
          title = `Pedido de sala rejeitado`;
          message = `Seu pedido para a sala ${classroomName} foi rejeitado.`;
        }
      } else {
        // Não é relevante para este usuário
        return;
      }
      
      // Adicionar à lista de notificações
      allNotifications.push({
        id: `classroom_${request.id}`,
        type: 'classroomRequest',
        title,
        message,
        date: new Date(), // Idealmente, usar a data real do pedido
        seen: props.userType === 'teacher' ? request.responseSeenByTeacher : true,
        requiresAction,
        originalRequest: request
      });
    });
    
    // Ordenar notificações por data (mais recentes primeiro)
    allNotifications.sort((a, b) => b.date - a.date);
    
    notifications.value = allNotifications;
  }
  
  // Formatar data para exibição
  function formatDate(date) {
    if (!date) return '';
    
    const now = new Date();
    const diff = now - date;
    
    // Se for menos de 24 horas, mostrar "há X horas/minutos"
    if (diff < 24 * 60 * 60 * 1000) {
      const hours = Math.floor(diff / (60 * 60 * 1000));
      if (hours > 0) {
        return `há ${hours} ${hours === 1 ? 'hora' : 'horas'}`;
      }
      
      const minutes = Math.floor(diff / (60 * 1000));
      if (minutes > 0) {
        return `há ${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}`;
      }
      
      return 'agora mesmo';
    }
    
    // Caso contrário, mostrar a data formatada
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit'
    });
  }
  
  // Marcar notificação como lida
  async function markAsSeen(notification) {
    try {
      if (notification.type === 'shiftRequest') {
        const request = notification.originalRequest;
        
        if (props.userType === 'student') {
          // Atualizar no backend
          await axios.patch(`http://localhost:3000/shiftRequests/${request.id}`, {
            responseSeenByStudent: true
          });
          
          // Atualizar localmente
          const index = shiftRequests.value.findIndex(r => r.id === request.id);
          if (index !== -1) {
            shiftRequests.value[index].responseSeenByStudent = true;
          }
        }
      } else if (notification.type === 'classroomRequest') {
        const request = notification.originalRequest;
        
        if (props.userType === 'teacher') {
          // Atualizar no backend
          await axios.patch(`http://localhost:3000/classroomRequests/${request.id}`, {
            responseSeenByTeacher: true
          });
          
          // Atualizar localmente
          const index = classroomRequests.value.findIndex(r => r.id === request.id);
          if (index !== -1) {
            classroomRequests.value[index].responseSeenByTeacher = true;
          }
        }
      }
      
      // Atualizar a notificação localmente
      const index = notifications.value.findIndex(n => n.id === notification.id);
      if (index !== -1) {
        notifications.value[index].seen = true;
      }
      
      // Regenerar notificações
      generateNotifications();
    } catch (err) {
      console.error('Erro ao marcar notificação como lida:', err);
    }
  }
  
  // Aprovar pedido (apenas para diretor)
  async function approveRequest(notification) {
    if (props.userType !== 'director') return;
    
    try {
      if (notification.type === 'shiftRequest') {
        const request = notification.originalRequest;
        
        // Atualizar no backend
        await axios.patch(`http://localhost:3000/shiftRequests/${request.id}`, {
          response: 'ok'
        });
        
        // Atualizar localmente
        const index = shiftRequests.value.findIndex(r => r.id === request.id);
        if (index !== -1) {
          shiftRequests.value[index].response = 'ok';
        }
      } else if (notification.type === 'classroomRequest') {
        const request = notification.originalRequest;
        
        // Atualizar no backend
        await axios.patch(`http://localhost:3000/classroomRequests/${request.id}`, {
          response: 'ok'
        });
        
        // Atualizar localmente
        const index = classroomRequests.value.findIndex(r => r.id === request.id);
        if (index !== -1) {
          classroomRequests.value[index].response = 'ok';
        }
      }
      
      // Regenerar notificações
      generateNotifications();
    } catch (err) {
      console.error('Erro ao aprovar pedido:', err);
    }
  }
  
  // Rejeitar pedido (apenas para diretor)
  async function rejectRequest(notification) {
    if (props.userType !== 'director') return;
    
    try {
      if (notification.type === 'shiftRequest') {
        const request = notification.originalRequest;
        
        // Atualizar no backend
        await axios.patch(`http://localhost:3000/shiftRequests/${request.id}`, {
          response: 'rejected'
        });
        
        // Atualizar localmente
        const index = shiftRequests.value.findIndex(r => r.id === request.id);
        if (index !== -1) {
          shiftRequests.value[index].response = 'rejected';
        }
      } else if (notification.type === 'classroomRequest') {
        const request = notification.originalRequest;
        
        // Atualizar no backend
        await axios.patch(`http://localhost:3000/classroomRequests/${request.id}`, {
          response: 'rejected'
        });
        
        // Atualizar localmente
        const index = classroomRequests.value.findIndex(r => r.id === request.id);
        if (index !== -1) {
          classroomRequests.value[index].response = 'rejected';
        }
      }
      
      // Regenerar notificações
      generateNotifications();
    } catch (err) {
      console.error('Erro ao rejeitar pedido:', err);
    }
  }
  
  // Exportar contagem de notificações não lidas
  const unreadCount = computed(() => {
    return notifications.value.filter(n => !n.seen).length;
  });
  
  defineExpose({
    unreadCount
  });
  </script>
  
  <style scoped>
  .notifications-container {
    max-height: 400px;
    overflow-y: auto;
  }
  
  .notification-item {
    transition: background-color 0.2s ease;
  }
  
  .notification-item:last-child {
    border-bottom: none;
  }
  </style>
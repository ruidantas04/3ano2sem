<template>
    <div class="flex flex-col lg:flex-row w-full gap-4">
      <!-- Sidebar com estrutura hierárquica -->
      <div class="w-full lg:w-64 bg-white rounded-lg shadow p-4 overflow-y-auto" style="max-height: 80vh;">
        <h2 class="text-lg font-semibold mb-3">Horário Geral</h2>
        
        <div class="mb-2">
          <label class="flex items-center text-sm font-medium text-red-600">
            <input 
              type="checkbox" 
              class="mr-2 rounded"
              v-model="selectAllGlobal"
              @change="toggleAllShifts(selectAllGlobal)"
            >
            <span>Select All</span>
          </label>
        </div>
        
        <!-- Anos -->
        <div class="space-y-1">
          <div v-for="year in 3" :key="`year-${year}`" class="border-b border-gray-200">
            <div 
              class="flex items-center py-2 px-1 cursor-pointer hover:bg-gray-50"
              @click="toggleYear(year)"
            >
              <span class="transform" :class="{ 'rotate-180': !expandedYears.includes(year) }">
                ▼
              </span>
              <span class="ml-2 font-medium">{{ year }}<sup>{{ getOrdinalSuffix(year) }}</sup> year</span>
            </div>
            
            <!-- Semestres -->
            <div v-if="expandedYears.includes(year)" class="ml-4 space-y-1">
              <div v-for="semester in 2" :key="`sem-${year}-${semester}`">
                <div 
                  class="flex items-center py-2 px-1 cursor-pointer hover:bg-gray-50"
                  @click="toggleSemester(year, semester)"
                >
                  <span class="transform" :class="{ 'rotate-180': !expandedSemesters.includes(`${year}-${semester}`) }">
                    ▼
                  </span>
                  <span class="ml-2 font-medium">{{ semester }}<sup>{{ getOrdinalSuffix(semester) }}</sup> semester</span>
                </div>
                
                <!-- Disciplinas -->
                <div v-if="expandedSemesters.includes(`${year}-${semester}`)" class="ml-4 space-y-1">
                  <div v-for="course in getCoursesByYearAndSemester(year, semester)" :key="`course-${course.id}`">
                    <div 
                      class="flex items-center py-2 px-1 cursor-pointer hover:bg-gray-50"
                      @click="toggleCourse(course.id)"
                    >
                      <span class="transform" :class="{ 'rotate-180': !expandedCourses.includes(course.id) }">
                        ▼
                      </span>
                      <span class="ml-2">{{ course.abbreviation }}</span>
                    </div>
                    
                    <!-- Turnos -->
                    <div v-if="expandedCourses.includes(course.id)" class="ml-4 border-l-2 border-gray-200 pl-2">
                      <div class="py-2">
                        <label class="flex items-center text-sm font-medium text-red-600">
                          <input 
                            type="checkbox" 
                            class="mr-2 rounded"
                            :checked="areAllShiftsSelectedForCourse(course.id)"
                            @change="toggleAllShiftsForCourse(course.id, $event.target.checked)"
                          >
                          <span>Select All</span>
                        </label>
                      </div>
                      
                      <div v-if="getShiftsByCourse(course.id).length === 0" class="py-1 text-sm text-gray-500">
                        Nenhum turno disponível
                      </div>
                      
                      <div v-for="shift in getShiftsByCourse(course.id)" :key="`shift-${shift.id}`" class="py-1">
                        <label class="flex items-center text-sm">
                          <input 
                            type="checkbox" 
                            class="mr-2 rounded"
                            v-model="selectedShifts"
                            :value="shift.id"
                          >
                          {{ shift.type }}{{ shift.name }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Tabela de horário -->
      <div class="flex-1 bg-white rounded-lg shadow p-4 overflow-x-auto">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-600"></div>
        </div>
        
        <div v-else-if="error" class="text-red-600 p-4 text-center">
          {{ error }}
        </div>
        
        <table v-else class="w-full border-collapse">
          <thead>
            <tr>
              <th class="border border-gray-300 bg-gray-100 p-2 w-16">Hora</th>
              <th v-for="day in weekDays" :key="day" class="border border-gray-300 bg-gray-100 p-2">
                {{ day }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hour in hours" :key="hour">
              <td class="border border-gray-300 bg-gray-50 p-2 text-center font-medium">{{ hour }}:00</td>
              <td 
                v-for="day in weekDays" 
                :key="`${day}-${hour}`" 
                class="border border-gray-300 p-0 relative"
                style="height: 60px;"
              >
                <div 
                  v-for="shift in getVisibleShiftsAt(day, hour)" 
                  :key="shift.id"
                  class="absolute inset-0 m-0.5 rounded overflow-hidden border border-gray-200"
                  :style="{ 
                    top: '0px',
                    height: `${(shift.to - shift.from) * 60 - 2}px`,
                    backgroundColor: getYearColor(getCourseYear(shift.courseId))
                  }"
                >
                  <div class="p-1 text-xs">
                    <div class="font-bold"> - {{ shift.name }}</div>
                    <div>CP{{ shift.courseId }} - Sala ?</div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed, watch } from 'vue';
  import axios from 'axios';
  
  // Estado reativo
  const courses = ref([]);
  const shifts = ref([]);
  const teachers = ref([]);
  const students = ref([]);
  const classrooms = ref([]);
  const buildings = ref([]);
  
  // Estado da UI
  const expandedYears = ref([1, 2, 3]); // Todos os anos expandidos por padrão
  const expandedSemesters = ref(['1-1', '1-2', '2-1', '2-2', '3-1', '3-2']); // Todos os semestres expandidos
  const expandedCourses = ref([]); // Nenhuma disciplina expandida inicialmente
  const selectedShifts = ref([]); // IDs dos turnos selecionados
  const selectAllGlobal = ref(false); // Checkbox global Select All
  
  const weekDays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'];
  const hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];
  
  // Cores por ano
  const yearColors = {
    1: 'rgba(255, 245, 157, 0.7)', // Amarelo claro para 1º ano
    2: 'rgba(200, 230, 201, 0.7)', // Verde claro para 2º ano
    3: 'rgba(179, 229, 252, 0.7)'  // Azul claro para 3º ano
  };
  
  const loading = ref(true);
  const error = ref(null);
  
  // Observar mudanças nos turnos selecionados para atualizar o estado do checkbox global
  watch(selectedShifts, (newValue) => {
    selectAllGlobal.value = newValue.length === shifts.value.length;
  });
  
  // Métodos
  const fetchData = async () => {
    try {
      loading.value = true;
      
      // Fazer requisições para os endpoints específicos
      const [
        coursesResponse,
        shiftsResponse,
        teachersResponse,
        studentsResponse,
        classroomsResponse,
        buildingsResponse
      ] = await Promise.all([
        axios.get('http://localhost:3000/courses'),
        axios.get('http://localhost:3000/shifts'),
        axios.get('http://localhost:3000/teachers'),
        axios.get('http://localhost:3000/students'),
        axios.get('http://localhost:3000/classrooms'),
        axios.get('http://localhost:3000/buildings')
      ]);
      
      // Atribuir os dados às variáveis reativas
      courses.value = coursesResponse.data;
      shifts.value = shiftsResponse.data;
      teachers.value = teachersResponse.data;
      students.value = studentsResponse.data;
      classrooms.value = classroomsResponse.data;
      buildings.value = buildingsResponse.data;
      
      // Expandir todas as disciplinas para demonstração
      courses.value.forEach(course => {
        expandedCourses.value.push(course.id);
      });
      
      // Selecionar todos os turnos para demonstração
      selectedShifts.value = shifts.value.map(shift => shift.id);
      selectAllGlobal.value = true;
      
      loading.value = false;
    } catch (err) {
      console.error('Erro ao buscar dados:', err);
      error.value = 'Não foi possível carregar os dados. Verifique se o JSON server está em execução.';
      loading.value = false;
    }
  };
  
  // Métodos para a UI
  const toggleYear = (year) => {
    if (expandedYears.value.includes(year)) {
      expandedYears.value = expandedYears.value.filter(y => y !== year);
    } else {
      expandedYears.value.push(year);
    }
  };
  
  const toggleSemester = (year, semester) => {
    const key = `${year}-${semester}`;
    if (expandedSemesters.value.includes(key)) {
      expandedSemesters.value = expandedSemesters.value.filter(s => s !== key);
    } else {
      expandedSemesters.value.push(key);
    }
  };
  
  const toggleCourse = (courseId) => {
    if (expandedCourses.value.includes(courseId)) {
      expandedCourses.value = expandedCourses.value.filter(c => c !== courseId);
    } else {
      expandedCourses.value.push(courseId);
    }
  };
  
  const toggleAllShifts = (checked) => {
    if (checked) {
      // Selecionar todos os turnos
      selectedShifts.value = shifts.value.map(shift => shift.id);
    } else {
      // Desselecionar todos os turnos
      selectedShifts.value = [];
    }
  };
  
  const getCoursesByYearAndSemester = (year, semester) => {
    return courses.value.filter(course => course.year === year && course.semester === semester);
  };
  
  const getShiftsByCourse = (courseId) => {
    return shifts.value.filter(shift => shift.courseId === courseId);
  };
  
  const areAllShiftsSelectedForCourse = (courseId) => {
    const courseShifts = getShiftsByCourse(courseId);
    const courseShiftIds = courseShifts.map(shift => shift.id);
    return courseShiftIds.length > 0 && courseShiftIds.every(id => selectedShifts.value.includes(id));
  };
  
  const toggleAllShiftsForCourse = (courseId, checked) => {
    const courseShifts = getShiftsByCourse(courseId);
    const courseShiftIds = courseShifts.map(shift => shift.id);
    
    if (checked) {
      // Adicionar todos os turnos da disciplina que ainda não estão selecionados
      courseShiftIds.forEach(id => {
        if (!selectedShifts.value.includes(id)) {
          selectedShifts.value.push(id);
        }
      });
    } else {
      // Remover todos os turnos da disciplina
      selectedShifts.value = selectedShifts.value.filter(id => !courseShiftIds.includes(id));
    }
  };
  
  const getVisibleShiftsAt = (day, hour) => {
    // Retorna apenas os turnos selecionados que ocorrem no dia e hora especificados
    return shifts.value.filter(shift => {
      // Verificar se o turno está selecionado
      const isSelected = selectedShifts.value.includes(shift.id);
      
      // Verificar se o turno ocorre no dia e hora especificados
      const isCorrectDay = shift.day === convertDayName(day);
      const isWithinHourRange = hour >= shift.from && hour < shift.to;
      
      return isSelected && isCorrectDay && isWithinHourRange;
    });
  };
  
  const convertDayName = (portugueseDayName) => {
    const dayMap = {
      'Segunda-feira': 'Monday',
      'Terça-feira': 'Tuesday',
      'Quarta-feira': 'Wednesday',
      'Quinta-feira': 'Thursday',
      'Sexta-feira': 'Friday'
    };
    return dayMap[portugueseDayName];
  };
  
  const getCourseAbbreviation = (courseId) => {
    const course = courses.value.find(c => c.id === courseId);
    return course ? course.abbreviation : '';
  };
  
  const getCourseYear = (courseId) => {
    const course = courses.value.find(c => c.id === courseId);
    return course ? course.year : 1;
  };
  
  const getYearColor = (year) => {
    return yearColors[year] || 'rgba(224, 224, 224, 0.7)'; // Cinza claro como fallback
  };
  
  const getOrdinalSuffix = (num) => {
    if (num === 1) return 'st';
    if (num === 2) return 'nd';
    if (num === 3) return 'rd';
    return 'th';
  };
  
  // Lifecycle hooks
  onMounted(() => {
    fetchData();
  });
  </script>
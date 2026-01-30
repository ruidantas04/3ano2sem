<template>
    <div class="font-sans p-6 space-y-6">
        <!-- Título -->
        <h2 class="text-xl font-bold text-gray-800">Gestão de Pedidos</h2>

        <!-- Resumo -->
        <div class="flex flex-wrap justify-around gap-4">
            <div class="bg-gray-100 p-6 text-center rounded-xl w-64 shadow">
                <h3 class="text-lg font-semibold flex justify-center items-center gap-2">
                    <span>🗂️</span> Total de Pedidos
                </h3>
                <p class="text-2xl mt-2">{{ totalPedidos }}</p>
            </div>
            <div class="bg-gray-100 p-6 text-center rounded-xl w-64 shadow">
                <h3 class="text-lg font-semibold flex justify-center items-center gap-2">
                    <span>⏳</span> Pendentes
                </h3>
                <p class="text-2xl mt-2">{{ pendentes }}</p>
            </div>
            <div class="bg-gray-100 p-6 text-center rounded-xl w-64 shadow">
                <h3 class="text-lg font-semibold flex justify-center items-center gap-2">
                    <span>✔️</span> Aprovados
                </h3>
                <p class="text-2xl mt-2">{{ aprovados }}</p>
            </div>
            <div class="bg-gray-100 p-6 text-center rounded-xl w-64 shadow">
                <h3 class="text-lg font-semibold flex justify-center items-center gap-2">
                    <span>❌</span> Rejeitados
                </h3>
                <p class="text-2xl mt-2">{{ rejeitados }}</p>
            </div>
        </div>

        <!-- Filtro -->
        <div class="flex justify-end">
            <label for="filter" class="mr-2 font-medium">Filtrar por</label>
            <select id="filter" v-model="selectedFilter"
                class="border border-gray-300 rounded px-3 py-1 focus:outline-none focus:border-red-700">
                <option value="all">Todos</option>
                <option value="pendente">Pendentes</option>
                <option value="aprovado">Aprovados</option>
                <option value="rejeitado">Rejeitados</option>
            </select>
        </div>

        <!-- Tabela -->
        <div class="overflow-x-auto">
            <table class="w-full border-collapse rounded-lg shadow-sm">
                <thead>
                    <tr class="bg-red-800 text-white">
                        <th class="py-3 px-4">ID</th>
                        <th class="py-3 px-4">Nome</th>
                        <th class="py-3 px-4">Tipo</th>
                        <th class="py-3 px-4">Unidade Curricular</th>
                        <th class="py-3 px-4">Data</th>
                        <th class="py-3 px-4">Status</th>
                        <th class="py-3 px-4">Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="pedido in paginatedPedidos" :key="pedido.id" class="text-center border-b">
                        <td class="py-2 px-4">{{ pedido.id }}</td>
                        <td class="py-2 px-4">{{ pedido.nome }}</td>
                        <td class="py-2 px-4">{{ pedido.tipo }}</td>
                        <td class="py-2 px-4">{{ pedido.unidadeCurricular }}</td>
                        <td class="py-2 px-4">{{ pedido.data }}</td>
                        <td class="py-2 px-4 font-semibold" :class="{
                            'text-yellow-500': pedido.status === 'Pendente',
                            'text-green-500': pedido.status === 'Aprovado',
                            'text-red-500': pedido.status === 'Rejeitado'
                        }">
                            {{ pedido.status }}
                        </td>
                        <td class="py-2 px-4 space-x-2">
                            <button @click="rejeitarPedido(pedido)"
                                class="bg-red-600 hover:bg-red-700 text-white rounded-full px-2 py-1"
                                title="Rejeitar Pedido">❌</button>
                            <button @click="aprovarPedido(pedido)"
                                class="bg-green-600 hover:bg-green-700 text-white rounded-full px-2 py-1"
                                title="Aprovar Pedido">✔️</button>
                            <router-link v-if="pedido.id.startsWith('S')"
                                :to="`/director/requests/${pedido.id.slice(1)}`"
                                class="bg-red-600 hover:bg-red-700 text-white rounded-full px-3 py-1 font-bold"
                                title="Ver Pedido">+</router-link>
                        </td>

                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Paginação -->
        <div class="flex justify-between items-center text-sm text-gray-600 mt-2">
            <span>A mostrar {{ paginatedPedidos.length }} de {{ filteredPedidos.length }} resultados</span>
            <div class="space-x-1">
                <button v-for="page in totalPages" :key="page" @click="currentPage = page"
                    class="px-3 py-1 rounded border" :class="{
                        'bg-red-700 text-white': currentPage === page,
                        'hover:bg-gray-200': currentPage !== page
                    }">
                    {{ page }}
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            pedidos: [],
            selectedFilter: 'all',
            currentPage: 1,
            itemsPerPage: 5
        }
    },
    computed: {
        filteredPedidos() {
            if (this.selectedFilter === 'all') return this.pedidos
            return this.pedidos.filter(p =>
                p.status.toLowerCase() === this.selectedFilter.toLowerCase()
            )
        },
        paginatedPedidos() {
            const start = (this.currentPage - 1) * this.itemsPerPage
            return this.filteredPedidos.slice(start, start + this.itemsPerPage)
        },
        totalPedidos() {
            return this.pedidos.length
        },
        pendentes() {
            return this.pedidos.filter(p => p.status === 'Pendente').length
        },
        aprovados() {
            return this.pedidos.filter(p => p.status === 'Aprovado').length
        },
        rejeitados() {
            return this.pedidos.filter(p => p.status === 'Rejeitado').length
        },
        totalPages() {
            return Math.ceil(this.filteredPedidos.length / this.itemsPerPage)
        }
    },
    methods: {
        async fetchPedidos() {
            const [shiftsRes, roomsRes, studentsRes, teachersRes, shiftsList, coursesRes] = await Promise.all([
                axios.get('http://localhost:3000/shiftRequests'),
                axios.get('http://localhost:3000/classroomRequests'),
                axios.get('http://localhost:3000/students'),
                axios.get('http://localhost:3000/teachers'),
                axios.get('http://localhost:3000/shifts'),
                axios.get('http://localhost:3000/courses')
            ])

            const getStudentName = id => studentsRes.data.find(s => s.id === id)?.name || `Aluno #${id}`
            const getTeacherName = id => teachersRes.data.find(t => t.id === id)?.name || `Docente #${id}`
            const getCourseNameFromShift = shiftId => {
                const shift = shiftsList.data.find(s => s.id === shiftId)
                const course = coursesRes.data.find(c => c.id === shift?.courseId)
                return course ? course.name : `Turno ${shiftId}`
            }

            const shiftPedidos = shiftsRes.data.map(p => ({
                id: `S${p.id}`,
                nome: getStudentName(p.studentId),
                tipo: 'Mudança de Turno',
                unidadeCurricular: getCourseNameFromShift(p.shiftId),
                data: new Date().toLocaleDateString(),
                status: this.mapStatus(p.response)
            }))

            const salaPedidos = roomsRes.data.map(p => ({
                id: `C${p.id}`,
                nome: getTeacherName(p.teacherId),
                tipo: 'Pedido de Sala',
                unidadeCurricular: `Sala ${p.classroomId}`,
                data: new Date().toLocaleDateString(),
                status: this.mapStatus(p.response)
            }))

            this.pedidos = [...shiftPedidos, ...salaPedidos]
        },
        mapStatus(response) {
            if (response === 'ok') return 'Aprovado'
            if (response === 'rejected') return 'Rejeitado'
            return 'Pendente'
        },
        async aprovarPedido(pedido) {
            const isShift = pedido.id.startsWith('S')
            const endpoint = isShift ? 'shiftRequests' : 'classroomRequests'
            const realId = pedido.id.slice(1)

            try {
                await axios.patch(`http://localhost:3000/${endpoint}/${realId}`, {
                    response: 'ok'
                })
                pedido.status = this.mapStatus('ok')
            } catch (error) {
                console.error('Erro ao aprovar pedido:', error)
            }
        },

        async rejeitarPedido(pedido) {
            const isShift = pedido.id.startsWith('S')
            const endpoint = isShift ? 'shiftRequests' : 'classroomRequests'
            const realId = pedido.id.slice(1)

            try {
                await axios.patch(`http://localhost:3000/${endpoint}/${realId}`, {
                    response: 'rejected'
                })
                pedido.status = this.mapStatus('rejected')
            } catch (error) {
                console.error('Erro ao rejeitar pedido:', error)
            }
        }

    },
    mounted() {
        this.fetchPedidos()
    }
}
</script>
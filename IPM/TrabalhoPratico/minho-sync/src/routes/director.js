// src/router/diretor.js
const diretorRoutes = [
    {
      path: '/director',
      name: 'Director',
      component: () => import('../views/director/DirectorLayout.vue'),
      children: [
        { path: 'dashboard', name: 'DirectorDashboard', component: () => import('../views/director/Dashboard.vue') },
        { path: 'course/:courseId', name: 'DirectorCourse', component: () => import('../views/App.vue'), props: true },
        { path: 'course/:courseId/shift/:shiftId', name: 'DirectorShift', component: () => import('../views/App.vue'), props: true },
        { path: 'schedule', name: 'DirectorSchedule', component: () => import('../views/App.vue') },
        { path: 'student/:studentId', name: 'DirectorStudentProfile', component: () => import('../views/director/PerfilAluno.vue'), props: true },
        { path: 'manual-allocation', name: 'DirectorManualAllocation', component: () => import('../views/App.vue') },
        { path: 'requests', name: 'DirectorRequests', component: () => import('../views/director/Pedidos.vue') },
        { path: 'requests/:requestId', name: 'DirectorRequestDetails', component: () => import('../views/director/FormMud.vue'), props: true },
      ]
    }
  ]
  
  export default diretorRoutes
  
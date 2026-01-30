// src/router/alunos.js
const alunosRoutes = [
    {
      path: '/student',
      name: 'Student',
      component: () => import('../views/student/StudentLayout.vue'),
      children: [
        { path: 'profile', name: 'StudentProfile', component: () => import('../views/App.vue') },
        { path: 'schedule', name: 'StudentSchedule', component: () => import('../views/App.vue') },
        { path: 'request-form', name: 'StudentRequestForm', component: () => import('../views/App.vue') }
      ]
    }
  ]
  
  export default alunosRoutes
  
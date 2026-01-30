// src/router/professor.js
const professorRoutes = [
    {
      path: '/teacher',
      name: 'Teacher',
      component: () => import('../views/teacher/TeacherLayout.vue'),
      children: [
        { path: 'course/:courseId', name: 'TeacherCourse', component: () => import('../views/App.vue'), props: true },
        { path: 'course/:courseId/shift/:shiftId', name: 'TeacherShift', component: () => import('../views/App.vue'), props: true },
        { path: 'request-form', name: 'TeacherRequestForm', component: () => import('../views/App.vue') }
      ]
    }
  ]
  
  export default professorRoutes
  
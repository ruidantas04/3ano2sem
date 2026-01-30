import { createRouter, createWebHistory } from 'vue-router'
import directorRoutes from './director'
import studentRoutes from './student'
import teacherRoutes from './teacher'

// Define rota base e de login
const routes = [
  { path: '/', redirect: '/schedule' },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/schedule', name: 'Horário', component: () => import('../views/HorarioGeral.vue') },
  
  { path: '/unauthorized', name: 'Unauthorized', component: () => import('../views/Unauthorized.vue') },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('../views/NotFound.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...routes,
    ...directorRoutes,
    ...studentRoutes,
    ...teacherRoutes
  ],
})

// Guarda de navegação global
router.beforeEach((to, from, next) => {
  // Páginas que não requerem autenticação
  const publicPages = ['/login', '/schedule'];
  const authRequired = !publicPages.includes(to.path) && !to.path.startsWith('/schedule');
  const userType = localStorage.getItem('userType');
  
  // Se a rota requer autenticação e o usuário não está logado, redireciona para login
  if (authRequired && !localStorage.getItem('token')) {
    return next('/login');
  }
  
  // Verifica permissões baseadas no tipo de usuário apenas para rotas protegidas
  if (authRequired && userType) {
    // Verifica se o usuário está tentando acessar uma rota que não tem permissão
    if (to.path.startsWith('/director') && userType !== 'director') {
      return next('/unauthorized');
    }
    
    if (to.path.startsWith('/teacher') && userType !== 'teacher') {
      return next('/unauthorized');
    }
    
    if (to.path.startsWith('/student') && userType !== 'student') {
      return next('/unauthorized');
    }
  }
  
  // Se tudo estiver ok, permite a navegação
  next();
})

export default router
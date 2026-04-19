import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
    path: '/login',
    name: 'Login',
    component: () => import('../views/AuthPage.vue')
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/cameras',
      name: 'cameras',
      component: () => import('../views/CamerasView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('user-token'); // Or your auth logic
  
  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router

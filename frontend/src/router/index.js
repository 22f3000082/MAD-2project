import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '@/views/AdminDashboard.vue'

const routes = [
  {   
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
  // Add other routes here
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 
import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '@/views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component:  () => import('@/views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guest: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/customer/dashboard',
    name: 'CustomerDashboard',
    component: () => import('@/views/CustomerDashboard.vue'),
    meta: { requiresAuth: true, requiresCustomer: true }
  },
  {
    path: '/professional/dashboard',
    name: 'ProfessionalDashboard',
    component: () => import('@/views/ProfessionalDashboard.vue'),
    meta: { requiresAuth: true, requiresProfessional: true }
  },
  {
    path: '/service-request/:serviceId',
    name: 'ServiceRequest',
    component: () => import('@/views/ServiceRequest.vue'),
    meta: { requiresAuth: true, requiresCustomer: true }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (!token && to.meta.requiresAuth) {
    next("/login");  // Redirect to login if no token
  } else {
    next();  // Allow access if token exists
  }
  
  // Routes that require authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login')
      return
    }

    // Check role-specific requirements
    if (to.meta.requiresAdmin && user.role !== 'admin') {
      next('/')
      return
    }
    if (to.meta.requiresCustomer && user.role !== 'customer') {
      next('/')
      return
    }
    if (to.meta.requiresProfessional && user.role !== 'professional') {
      next('/')
      return
    }
  }

  // // Routes for guests only (login, register)
  // if (to.matched.some(record => record.meta.guest)) {
  //   if (token) {
  //     next(`/${user.role}/dashboard`)
  //     return
  //   }
  // }

  next()
})

export default router

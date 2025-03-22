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
  },
  {
    path: '/service-details/:serviceId',
    name: 'ServiceDetails',
    component: () => import('@/views/ServiceDetails.vue'),
    props: true,
    meta: { requiresAuth: true, requiresCustomer: true }
  },
  {
    path: '/professional/:id',
    name: 'ProfessionalProfile',
    component: () => import('@/views/ProfessionalProfile.vue'),
    props: true
  }
]


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// Navigation guard - simplified
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : {}
  
  // Handle routes requiring authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      console.log('Auth required but no token found')
      return next('/login')
    }
    
    // Check role-specific requirements
    if (to.meta.requiresAdmin && user.role !== 'admin') {
      return next('/')
    }
    
    if (to.meta.requiresCustomer && user.role !== 'customer') {
      return next('/')
    }
    
    if (to.meta.requiresProfessional && user.role !== 'professional') {
      return next('/')
    }
  }

  // Redirect logged-in users away from login page
  if (to.path === '/login' && token) {
    if (user.role === 'admin') return next('/admin/dashboard')
    if (user.role === 'customer') return next('/customer/dashboard')
    if (user.role === 'professional') return next('/professional/dashboard')
    return next('/')
  }
  next()
 
})


export default router
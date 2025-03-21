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
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : {}
  
  console.log('Navigation:', {
    to: to.path,
    hasToken: !!token,
    userRole: user.role,
    requiresAuth: to.matched.some(r => r.meta.requiresAuth),
    requiresAdmin: to.matched.some(r => r.meta.requiresAdmin)
  })
  
  // // Handle routes requiring authentication
  // if (to.matched.some(record => record.meta.requiresAuth)) {
  //   if (!token) {
  //     if (to.path !== '/login') { // Only redirect if not already on /login
  //       console.log('Auth required but no token found - redirecting to login')
  //       next('/login')
  //     } else {
  //       console.log('Already on login page, no need to redirect')
  //       next()
  //     }
  //     return
  //   }
    
    // Handle auth required routes
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!token) {
        console.log('Auth required but no token found - redirecting to login');
        return next('/login')
      }
    
    console.log('Checking role-specific requirements')
    console.log('User role:', user.role)
    
    // Check role-specific requirements
    if (to.meta.requiresAdmin && user.role !== 'admin') {
      console.log('Admin route access denied for non-admin user')
      next('/')
      return
    }
    
    if (to.meta.requiresCustomer && user.role !== 'customer') {
      console.log('Customer route access denied for non-customer user')
      next('/')
      return
    }
    
    if (to.meta.requiresProfessional && user.role !== 'professional') {
      console.log('Professional route access denied for non-professional user')
      next('/')
      return
    }
  }

  console.log('Navigation allowed to', to.path);
   next(); // Allow navigation
  // Guest routes (login/register) should redirect already logged-in users
  if (to.matched.some(record => record.meta.guest) && token) {
    // if (token && to.path === '/login') {
      console.log('User already logged in, avoiding unnecessary login navigation')
    if (user.role === 'customer') {
      next('/customer/dashboard')
    } else if (user.role === 'professional') {
      next('/professional/dashboard')
    } else if (user.role === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/')
    }
    return}
  });
 
    // next()
  
export default router
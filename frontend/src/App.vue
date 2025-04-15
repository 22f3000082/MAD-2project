<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <i class="fas fa-home me-2"></i>
          <span class="d-none d-sm-inline">A-Z Household Services</span>
          <span class="d-inline d-sm-none">A-Z Services</span>
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Search Bar - Visible for all users -->
          <div class="ms-auto me-3 navbar-search d-none d-md-block">
            <form @submit.prevent="searchServices" class="d-flex">
              <div class="input-group">
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="Search services..." 
                  v-model="searchQuery"
                  aria-label="Search services"
                >
                <button class="btn btn-light" type="submit">
                  <i class="fas fa-search"></i>
                </button>
              </div>
            </form>
          </div>

          <!-- Mobile Search Button -->
          <div class="d-md-none ms-auto me-2">
            <button 
              class="btn btn-outline-light" 
              type="button"
              @click="toggleMobileSearch">
              <i class="fas fa-search"></i>
            </button>
          </div>

          <!-- Guest Links -->
          <ul class="navbar-nav" v-if="!isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/services">
                <i class="fas fa-tools me-1"></i> Services
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">
                <i class="fas fa-sign-in-alt me-1"></i> Login
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">
                <i class="fas fa-user-plus me-1"></i> Register
              </router-link>
            </li>
          </ul>

          <!-- Authenticated User Links -->
          <ul class="navbar-nav" v-else>
            <!-- Admin Links -->
            <template v-if="userRole === 'admin'">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/dashboard">
                  <i class="fas fa-tachometer-alt me-1"></i> Dashboard
                </router-link>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                  <i class="fas fa-cogs me-1"></i> Manage
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/admin/services">
                      <i class="fas fa-tools me-1"></i> Services
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/admin/professionals">
                      <i class="fas fa-user-tie me-1"></i> Professionals
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/admin/customers">
                      <i class="fas fa-users me-1"></i> Customers
                    </router-link>
                  </li>
                </ul>
              </li>
            </template>

            <!-- Customer Links -->
            <template v-if="userRole === 'customer'">
              <li class="nav-item">
                <router-link class="nav-link" to="/customer/dashboard">
                  <i class="fas fa-tachometer-alt me-1"></i> Dashboard
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/customer/services">
                  <i class="fas fa-tools me-1"></i> Services
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/customer/my-requests">
                  <i class="fas fa-clipboard-list me-1"></i> My Requests
                </router-link>
              </li>
            </template>

            <!-- Professional Links -->
            <template v-if="userRole === 'professional'">
              <li class="nav-item">
                <router-link class="nav-link" to="/professional/dashboard">
                  <i class="fas fa-tachometer-alt me-1"></i> Dashboard
                </router-link>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                  <i class="fas fa-clipboard-check me-1"></i> Service Requests
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/professional/requests/new">
                      <i class="fas fa-bell me-1"></i> New Requests
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/professional/requests/ongoing">
                      <i class="fas fa-spinner me-1"></i> Ongoing Services
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/professional/requests/completed">
                      <i class="fas fa-check-circle me-1"></i> Completed Services
                    </router-link>
                  </li>
                </ul>
              </li>
            </template>

            <!-- User Profile & Logout -->
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <i class="fas fa-user-circle me-1"></i> {{ userName }}
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" :to="'/' + userRole + '/profile'">
                    <i class="fas fa-id-card me-1"></i> Profile
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" :to="'/' + userRole + '/settings'">
                    <i class="fas fa-cog me-1"></i> Settings
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                    <i class="fas fa-sign-out-alt me-1"></i> Logout
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Mobile Search Bar -->
    <div class="mobile-search-bar" v-if="showMobileSearch">
      <div class="container py-2">
        <form @submit.prevent="searchServices" class="d-flex">
          <div class="input-group">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Search services..." 
              v-model="searchQuery"
              aria-label="Search services"
              ref="mobileSearchInput"
            >
            <button class="btn btn-primary" type="submit">
              <i class="fas fa-search"></i>
            </button>
            <button class="btn btn-outline-secondary" type="button" @click="toggleMobileSearch">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Main Content -->
    <main class="container py-4">
      <transition name="fade" mode="out-in">
        <router-view></router-view>
      </transition>
    </main>

    <!-- Footer -->
    <footer class="bg-light py-4 mt-auto">
      <div class="container text-center">
        <p class="mb-0">&copy; {{ currentYear }} A-Z Household Services. All rights reserved.</p>
      </div>
    </footer>

    <!-- Add to Home Screen Component -->
    <AddToHomeScreen />
    
    <!-- App Update Notification -->
    <AppUpdate />
  </div>
</template>

<script>
import AddToHomeScreen from '@/components/AddToHomeScreen.vue'
import AppUpdate from '@/components/AppUpdate.vue'

export default {
  name: 'App',
  components: {
    AddToHomeScreen,
    AppUpdate
  },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      searchQuery: '',
      showMobileSearch: false
    }
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    },
    userRole() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.role || ''
    },
    userName() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.name || 'User'
    }
  },
  methods: {
    async searchServices() {
      if (this.searchQuery.trim()) {
        // Navigate to services page with search query
        if (this.userRole === 'customer') {
          await this.$router.push({
            path: '/customer/services',
            query: { search: this.searchQuery }
          })
        } else {
          await this.$router.push({
            path: '/services',
            query: { search: this.searchQuery }
          })
        }
        // Reset search query after navigation
        this.searchQuery = ''
        this.showMobileSearch = false
      }
    },
    async handleLogout() {
      try {
        // Clear local storage
        localStorage.removeItem('token')
        localStorage.removeItem('user')

        // Redirect to home page
        await this.$router.push('/')

        // Optional: Show success message
        // You might want to add a toast/notification system here
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
    toggleMobileSearch() {
      this.showMobileSearch = !this.showMobileSearch
      if (this.showMobileSearch) {
        this.$nextTick(() => {
          this.$refs.mobileSearchInput.focus()
        })
      }
    }
  }
}
</script>

<style>
/* Global Styles */
html, body {
  height: 100%;
}

body {
  display: flex;
  flex-direction: column;
  font-family: 'Poppins', sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1 0 auto;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Mobile Search Bar */
.mobile-search-bar {
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 56px;
  z-index: 1000;
}

/* Responsive Typography */
@media (max-width: 576px) {
  h1 {
    font-size: 1.75rem;
  }
  h2 {
    font-size: 1.5rem;
  }
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }
}

/* Tablet Optimizations */
@media (min-width: 577px) and (max-width: 991px) {
  .container {
    max-width: 100%;
  }
}

/* Card optimizations for mobile */
@media (max-width: 576px) {
  .card {
    margin-bottom: 1rem;
  }
  .card-body {
    padding: 1rem;
  }
}

/* Add bottom spacing for fixed position elements */
.navbar-fixed-bottom-spacer {
  height: 60px;
  display: none;
}
@media (max-width: 576px) {
  .navbar-fixed-bottom-spacer {
    display: block;
  }
}
</style>

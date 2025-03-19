<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <i class="fas fa-home me-2"></i>
          A-Z Household Services
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Guest Links -->
          <ul class="navbar-nav ms-auto" v-if="!isAuthenticated">
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
          <ul class="navbar-nav ms-auto" v-else>
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
                <router-link class="nav-link" to="/services">
                  <i class="fas fa-tools me-1"></i> Services
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/my-requests">
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
              <li class="nav-item">
                <router-link class="nav-link" to="/service-requests">
                  <i class="fas fa-clipboard-check me-1"></i> Service Requests
                </router-link>
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
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentYear: new Date().getFullYear()
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
    }
  }
}
</script>

<style>
/* Ensure footer stays at bottom */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* Custom navbar styling */
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: bold;
}

.nav-link {
  font-weight: 500;
}

.dropdown-item {
  padding: 0.5rem 1rem;
}

.dropdown-item i {
  width: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 991.98px) {
  .navbar-nav {
    padding: 1rem 0;
  }
  
  .dropdown-menu {
    border: none;
    padding: 0;
    margin: 0;
  }
  
  .dropdown-item {
    padding-left: 2rem;
  }
}
</style>

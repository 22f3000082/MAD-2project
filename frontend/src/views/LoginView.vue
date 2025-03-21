<template>
  <div class="login-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow">
            <div class="card-body p-4">
              <h2 class="text-center mb-4">Login</h2>

              <!-- Login Form -->
              <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                <!-- Email Field -->
                <div class="mb-3">
                  <label class="form-label">Email</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-envelope"></i>
                    </span>
                    <input
                      type="email"
                      class="form-control"
                      v-model="formData.email"
                      required
                      :class="{ 'is-invalid': errors.email }"
                      placeholder="Enter your email"
                      autocomplete="email"
                    >
                    <div class="invalid-feedback">{{ errors.email }}</div>
                  </div>
                </div>

                <!-- Password Field -->
                <div class="mb-4">
                  <label class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-lock"></i>
                    </span>
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      v-model="formData.password"
                      required
                      :class="{ 'is-invalid': errors.password }"
                      placeholder="Enter your password"
                      autocomplete="current-password"
                    >
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="togglePassword"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                    <div class="invalid-feedback">{{ errors.password }}</div>
                  </div>
                </div>

                <!-- Error Alert -->
                <div v-if="loginError" class="alert alert-danger" role="alert">
                  <i class="fas fa-exclamation-circle me-2"></i>
                  {{ loginError }}
                </div>

                <!-- Submit Button -->
                <div class="d-grid gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                    {{ isLoading ? 'Logging in...' : 'Login' }}
                  </button>
                </div>

                <!-- Register Link -->
                <p class="text-center mt-3">
                  Don't have an account?
                  <router-link to="/register">Register here</router-link>
                </p>
              </form>
            </div>
          </div>

          <!-- Role Information Cards -->
          <div class="row mt-4 g-3">
            <!-- <div class="col-md-4">
              <div class="card h-100 border-0 shadow-sm">
                <div class="card-body text-center">
                  <i class="fas fa-user-shield fa-2x text-primary mb-2"></i>
                  <h5 class="card-title">Admin</h5>
                  <p class="card-text small">Manage services and users</p>
                </div>
              </div>
            </div> -->
            <div class="col-md-4">
              <div class="card h-100 border-0 shadow-sm">
                <div class="card-body text-center">
                  <i class="fas fa-user fa-2x text-success mb-2"></i>
                  <h5 class="card-title">Customer</h5>
                  <p class="card-text small">Book and manage services</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100 border-0 shadow-sm">
                <div class="card-body text-center">
                  <i class="fas fa-user-tie fa-2x text-info mb-2"></i>
                  <h5 class="card-title">Professional</h5>
                  <p class="card-text small">Provide services</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services/api'

export default {
  name: 'LoginView',
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      errors: {},
      loginError: '',
      isLoading: false,
      showPassword: false
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    validateForm() {
      this.errors = {}
      let isValid = true

      if (!this.formData.email) {
        this.errors.email = 'Email is required'
        isValid = false
      } else if (!/\S+@\S+\.\S+/.test(this.formData.email)) {
        this.errors.email = 'Please enter a valid email address'
        isValid = false
      }

      if (!this.formData.password) {
        this.errors.password = 'Password is required'
        isValid = false
      }

      return isValid
    },
    async handleSubmit() {
      this.loginError = ''
      if (!this.validateForm()) {
        return
      }

      this.isLoading = true
      try {
        const response = await authService.login(this.formData)
        
        // Redirect based on user role
        switch (response.user.role) {
          case 'admin':
            await this.$router.push('/admin/dashboard')
            break
          case 'customer':
            await this.$router.push('/customer/dashboard')
            break
          case 'professional':
            if (!response.user.is_approved) {
              this.loginError = 'Your account is pending approval. Please wait for admin verification.'
              localStorage.removeItem('token')
              localStorage.removeItem('user')
              return
            }
            await this.$router.push('/professional/dashboard')
            break
          default:
            await this.$router.push('/')
        }
      } catch (error) {
        console.error('Login error:', error)
        if (error.response?.status === 401) {
          this.loginError = 'Invalid email or password'
        } else if (error.message) {
          this.loginError = error.message
        } else {
          this.loginError = 'Network error. Please check your connection and try again.'
        }
      } finally {
        this.isLoading = false
      }
    }
  },
  created() {
    // Clear any existing auth data on component mount
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  border: none;
  border-radius: 15px;
}

.form-control:focus,
.form-select:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn-primary {
  padding: 0.75rem;
  font-weight: 500;
}

.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.input-group .form-control {
  border-left: none;
}

.input-group .form-control:focus {
  border-left: 1px solid #80bdff;
}

.input-group .btn-outline-secondary {
  border-color: #ced4da;
}

.input-group .btn-outline-secondary:hover {
  background-color: #f8f9fa;
}

.invalid-feedback {
  font-size: 0.875rem;
}

/* Role cards styling */
.card-body i {
  opacity: 0.8;
}

.card-text {
  color: #6c757d;
}

/* Transition effects */
.alert {
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .col-md-4 {
    margin-bottom: 1rem;
  }
}
</style>

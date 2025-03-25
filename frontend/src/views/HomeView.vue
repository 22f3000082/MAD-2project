<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero bg-primary text-white py-5">
      <div class="container">
        <div class="row justify-content-center text-center">
          <div class="col-md-8">
            <h1 class="display-4 mb-4">Welcome to A-Z Household Services</h1>
            <p class="lead mb-4">Find and book professional services for your home with ease</p>
            <div class="d-flex justify-content-center gap-3">
              <router-link v-if="!isLoggedIn" to="/register" class="btn btn-light btn-lg">Get Started</router-link>
              <router-link v-else :to="dashboardRoute" class="btn btn-light btn-lg">Go to Dashboard</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services py-5">
      <div class="container">
        <h2 class="text-center mb-5">Our Services</h2>
        <div class="row g-4">
          <div v-for="service in services" :key="service.id" class="col-md-4">
            <service-card 
              :service="service"
              @click="handleServiceClick(service)"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-5">Why Choose Us</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="text-center">
              <i class="fas fa-check-circle fa-3x text-primary mb-3"></i>
              <h4>Verified Professionals</h4>
              <p>All our service providers are thoroughly vetted and verified</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="text-center">
              <i class="fas fa-clock fa-3x text-primary mb-3"></i>
              <h4>Quick Service</h4>
              <p>Get your service requests handled promptly</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="text-center">
              <i class="fas fa-star fa-3x text-primary mb-3"></i>
              <h4>Quality Assured</h4>
              <p>Rated and reviewed by our community</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import ServiceCard from '@/components/ServiceCard.vue'
import { serviceAPI } from '@/services/api'

export default {
  name: 'Home',
  components: {
    ServiceCard
  },
  data() {
    return {
      services: [],
      isLoading: false,
      error: null
    }
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    dashboardRoute() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return `/${user.role}/dashboard`
    }
  },
  methods: {
    async fetchServices() {
      try {
        console.log('HomeView: Fetching services...')
        this.loading = true
        
        // Use serviceAPI directly
        const services = await serviceAPI.getServices()
        
        if (services && services.length > 0) {
          console.log(`HomeView: Received ${services.length} services`)
          this.services = services
        } else {
          console.warn('No services returned, using fallback data')
          this.services = this.getFallbackServices()
          // Optionally show a warning to the user
        }
      } catch (error) {
        console.error('Error fetching services:', error)
        // Use fallback data instead of showing an error
        this.services = this.getFallbackServices()
      } finally {
        this.loading = false
      }
    },
    
    getFallbackServices() {
      // Same mock data as in ServicesList component
      return [
        {
          id: 1,
          name: 'Plumbing Service',
          description: 'Professional plumbing services including repairs, installations, and maintenance.',
          base_price: 500,
          time_required: 2,
          category: 'Plumbing'
        },
        {
          id: 2,
          name: 'Electrical Repair',
          description: 'Electrical installations, repairs and maintenance for your home.',
          base_price: 600,
          time_required: 3,
          category: 'Electrical'
        },
        {
          id: 3,
          name: 'House Cleaning',
          description: 'Complete house cleaning and sanitization services.',
          base_price: 400,
          time_required: 4,
          category: 'Cleaning'
        }
      ]
    },
    handleServiceClick(service) {
      if (!this.isLoggedIn) {
        this.$router.push('/login')
      } else {
        this.$router.push({
          name: 'ServiceRequest',
          params: { serviceId: service.id }
        })
      }
    }
  },
  created() {
    this.fetchServices()
  }
}
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
}

.services .card {
  transition: transform 0.2s;
  cursor: pointer;
}

.services .card:hover {
  transform: translateY(-5px);
}

.features i {
  transition: transform 0.2s;
}

.features .col-md-4:hover i {
  transform: scale(1.1);
}
</style>

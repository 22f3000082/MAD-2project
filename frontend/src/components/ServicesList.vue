<template>
  <div class="services-list">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading services...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
    </div>
    
    <div v-else class="row">
      <div v-for="service in services" :key="service.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ service.description }}</p>
            <p class="card-text"><strong>Price:</strong> ₹{{ service.base_price }}</p>
            <p class="card-text"><strong>Time Required:</strong> {{ service.time_required }} hours</p>
            <p class="card-text"><strong>Category:</strong> {{ service.category }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { serviceAPI } from '@/services/api';

export default {
  name: 'ServicesList',
  
  data() {
    return {
      services: [],
      loading: true,
      error: null,
      retryCount: 0
    }
  },
  
  created() {
    this.fetchServices();
  },
  
  methods: {
    async fetchServices() {
      try {
        this.loading = true;
        console.log('ServicesList: Fetching services...');
        
        // Directly use serviceAPI instead of imported getServices
        const services = await serviceAPI.getServices();
        
        if (services && services.length > 0) {
          console.log(`ServicesList: Received ${services.length} services`);
          this.services = services;
          this.error = null;
        } else {
          // Use fallback mock data if no services returned
          console.warn('No services returned, using fallback data');
          this.services = this.getFallbackServices();
          this.error = 'Using demo data - backend service unavailable';
        }
      } catch (error) {
        console.error('Error fetching services:', error);
        this.error = 'Failed to load services. Using demo data instead.';
        this.services = this.getFallbackServices();
        
        // Retry logic (up to 3 times)
        if (this.retryCount < 3) {
          this.retryCount++;
          console.log(`Retrying... Attempt ${this.retryCount}`);
          setTimeout(() => this.fetchServices(), 3000); // Retry after 3 seconds
        }
      } finally {
        this.loading = false;
      }
    },
    
    getFallbackServices() {
      // Return some fallback/mock service data if API fails
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
      ];
    }
  }
}
</script>

<style scoped>
.services-list {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.alert {
  margin-top: 2rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 500;
}

.card-text {
  font-size: 1rem;
  color: #6c757d;
}
</style>
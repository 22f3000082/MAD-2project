/* eslint-disable */
<template>
  <div class="service-request container">
    <h2 class="mb-4">Available Services</h2>
    
    <!-- Loading and Error States -->
    <div v-if="loading" class="alert alert-info">Loading services...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Service Categories -->
    <div v-if="!loading && !error" class="mb-4">
      <div class="category-filters">
        <button 
          v-for="category in categories"
          :key="category"
          class="btn btn-outline-primary me-2 mb-2"
          :class="{ active: selectedCategory === category }"
          @click="filterByCategory(category)">
          {{ category }}
        </button>
      </div>
    </div>

    <!-- Services Grid -->
    <div v-if="!loading && !error" class="row">
      <div v-for="service in filteredServices" 
           :key="service.id" 
           class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ service.description }}</p>
            <div class="service-details">
              <p><strong>Category:</strong> {{ service.category }}</p>
              <p><strong>Price:</strong> ${{ service.base_price }}</p>
              <p><strong>Duration:</strong> {{ service.time_required }} hour(s)</p>
            </div>
            <button 
              @click="createServiceRequest(service)"
              class="btn btn-primary"
              :disabled="loading">
              Request Service
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Request Form Modal -->
    <div class="modal fade" id="requestModal" tabindex="-1" ref="requestModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Service: {{ selectedService?.name }}</h5>
            <button type="button" class="close" data-dismiss="modal">&times;</button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitRequest">
              <div class="form-group">
                <label>Preferred Date</label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="requestForm.preferred_date"
                  :min="minDate"
                  required
                >
              </div>
              <div class="form-group">
                <label>Notes</label>
                <textarea 
                  class="form-control" 
                  v-model="requestForm.notes"
                  rows="3"
                ></textarea>
              </div>
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="submitting"
              >
                Submit Request
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { serviceAPI, customerAPI } from '@/services/api';

export default {
  data() {
    return {
      services: [],
      loading: true,
      error: null,
      selectedService: null,
      submitting: false,
      requestForm: {
        preferred_date: '',
        notes: ''
      },
      selectedCategory: null,
      categories: [
        'AC Repair',
        'Plumbing',
        'Electrical',
        'Carpentry',
        'Painting',
        'Cleaning',
        'Pest Control',
        'Appliance Repair',
        'Moving Services',
        'Gardening'
      ]
    }
  },

  computed: {
    minDate() {
      const today = new Date();
      return today.toISOString().split('T')[0];
    },
    filteredServices() {
      if (!this.selectedCategory) return this.services;
      return this.services.filter(service => 
        service.category === this.selectedCategory
      );
    }
  },

  async created() {
    await this.fetchServices();
  },

  methods: {
    async fetchServices() {
      try {
        this.loading = true;
        this.error = null;
        const response = await serviceAPI.getPublicServices();
        this.services = response.filter(service => service.is_active);
      } catch (err) {
        console.error('Error fetching services:', err);
        this.error = 'Unable to load services. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    filterByCategory(category) {
      this.selectedCategory = this.selectedCategory === category ? null : category;
    },

    async createServiceRequest(service) {
      try {
        const requestData = {
          service_id: service.id,
          pin_code: prompt('Please enter your PIN code:'),
          special_instructions: prompt('Any special instructions?') || ''
        };

        if (!requestData.pin_code) {
          alert('PIN code is required');
          return;
        }

        await customerAPI.createRequest(requestData);
        this.$toast.success('Service request created successfully!');
      } catch (err) {
        console.error('Error creating request:', err);
        this.$toast.error(err.message || 'Failed to create request');
      }
    },

    async submitRequest() {
      try {
        this.submitting = true;
        
        const requestData = {
          service_id: this.selectedService.id,
          preferred_date: this.requestForm.preferred_date,
          notes: this.requestForm.notes
        };

        await customerAPI.createServiceRequest(requestData);
        
        // // Hide modal and show success message
        // $(this.$refs.requestModal).modal('hide');
        // this.$toast.success('Service request submitted successfully!');
        
      } catch (err) {
        console.error('Error submitting request:', err);
        this.$toast.error(err.message || 'Failed to submit request');
      } finally {
        this.submitting = false;
      }
    }
  }
}
</script>

<style scoped>
.service-request {
  padding: 20px;
}

.card {
  height: 100%;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.service-details {
  margin: 15px 0;
}

.modal-dialog {
  max-width: 500px;
}

.category-filters {
  margin-bottom: 20px;
}

.btn.active {
  background-color: #007bff;
  color: white;
}
</style>

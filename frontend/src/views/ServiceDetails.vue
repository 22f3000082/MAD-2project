<template>
  <div class="service-details-page">
    <div class="container py-5">
      <div class="row">
        <div class="col-lg-8">
          <!-- Service Information -->
          <div class="card mb-4">
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading service details...</p>
              </div>

              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <div v-else>
                <h2 class="mb-3">{{ service.name }}</h2>
                
                <div class="d-flex justify-content-between align-items-center mb-4">
                  <span class="badge bg-primary fs-5 px-3 py-2">₹{{ service.base_price }}</span>
                  <div class="text-muted">
                    <i class="far fa-clock me-2"></i>
                    {{ service.time_required }} minutes
                  </div>
                </div>
                
                <div class="mb-4">
                  <h5>Description</h5>
                  <p>{{ service.description }}</p>
                </div>
                
                <div class="mb-4">
                  <h5>Category</h5>
                  <p>{{ service.category }}</p>
                </div>
                
                <div class="mb-4">
                  <h5>What's Included</h5>
                  <ul class="included-list">
                    <li v-for="(item, index) in serviceIncludes" :key="index">
                      <i class="fas fa-check text-success me-2"></i>
                      {{ item }}
                    </li>
                  </ul>
                </div>
                
                <div class="d-grid">
                  <button class="btn btn-primary btn-lg" @click="showRequestForm = true">
                    <i class="fas fa-shopping-cart me-2"></i>
                    Book This Service
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Reviews Section -->
          <div class="card">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Customer Reviews</h5>
              <span class="text-muted">{{ reviews.length }} reviews</span>
            </div>
            <div class="card-body">
              <div v-if="reviews.length === 0" class="text-center py-4">
                <i class="far fa-star fa-3x text-muted mb-3"></i>
                <h5>No Reviews Yet</h5>
                <p class="text-muted">Be the first to review this service!</p>
              </div>
              
              <div v-else>
                <div v-for="(review, index) in reviews" :key="index" class="review-item">
                  <div class="d-flex align-items-center mb-2">
                    <div class="stars me-2">
                      <i v-for="n in 5" :key="n"
                         class="fas fa-star"
                         :class="n <= review.rating ? 'text-warning' : 'text-muted'"></i>
                    </div>
                    <strong>{{ review.customer_name }}</strong>
                  </div>
                  <p class="mb-1">{{ review.remarks }}</p>
                  <small class="text-muted">{{ formatDate(review.date_created) }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4 mt-4 mt-lg-0">
          <!-- Service Request Form Card -->
          <div class="card mb-4 sticky-top" style="top: 20px">
            <div class="card-header bg-white">
              <h5 class="mb-0">Book This Service</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="submitRequest">
                <div class="mb-3">
                  <label for="requestPinCode" class="form-label">PIN Code</label>
                  <input
                    id="requestPinCode"
                    name="requestPinCode"
                    type="text"
                    class="form-control"
                    v-model="requestForm.pin_code"
                    required
                    pattern="[0-9]{6}"
                    placeholder="Enter 6-digit PIN code"
                  >
                </div>
                
                <div class="mb-3">
                  <label for="requestInstructions" class="form-label">Special Instructions</label>
                  <textarea
                    id="requestInstructions"
                    name="requestInstructions"
                    class="form-control"
                    v-model="requestForm.special_instructions"
                    rows="3"
                    placeholder="Any specific requirements..."
                  ></textarea>
                </div>
                
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary" :disabled="submitting">
                    <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                    Submit Request
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <!-- Related Services Card -->
          <div class="card">
            <div class="card-header bg-white">
              <h5 class="mb-0">Similar Services</h5>
            </div>
            <div class="card-body">
              <div v-if="relatedServices.length === 0" class="text-center py-3">
                <p class="text-muted mb-0">No similar services found</p>
              </div>
              
              <div v-else>
                <div v-for="relatedService in relatedServices" :key="relatedService.id" 
                     class="related-service-item" @click="navigateToService(relatedService.id)">
                  <h6>{{ relatedService.name }}</h6>
                  <div class="d-flex justify-content-between">
                    <span class="badge bg-primary">₹{{ relatedService.base_price }}</span>
                    <small>{{ relatedService.time_required }} minutes</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Request Success Modal -->
    <div class="modal fade" :class="{ show: showSuccessModal }" v-if="showSuccessModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Submitted</h5>
            <button type="button" class="btn-close" @click="showSuccessModal = false"></button>
          </div>
          <div class="modal-body text-center">
            <i class="fas fa-check-circle text-success fa-4x mb-3"></i>
            <h4>Service Request Submitted!</h4>
            <p>Your request for <strong>{{ service.name }}</strong> has been submitted successfully.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="goToRequests">
              View My Requests
            </button>
            <button type="button" class="btn btn-primary" @click="showSuccessModal = false">
              Continue Browsing
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { serviceAPI, customerAPI } from '@/services/api'

export default {
  name: 'ServiceDetails',
  props: {
    serviceId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      service: {},
      reviews: [],
      relatedServices: [],
      loading: true,
      error: null,
      submitting: false,
      showSuccessModal: false,
      requestForm: {
        service_id: null,
        pin_code: '',
        special_instructions: ''
      },
      // Sample data for what's included (could come from API)
      serviceIncludes: [
        'Professional service provider',
        'Standard service time',
        'Quality assurance',
        'Customer satisfaction guarantee'
      ]
    }
  },
  methods: {
    async fetchServiceDetails() {
      try {
        this.loading = true;
        this.error = null;
        
        const service = await serviceAPI.getServiceById(this.serviceId);
        this.service = service;
        
        // Set the service ID in the request form
        this.requestForm.service_id = this.service.id;
        
        // In a real app, you would fetch related services and reviews here
        this.fetchRelatedServices();
        this.fetchReviews();
        
        this.loading = false;
      } catch (error) {
        console.error('Error fetching service details:', error);
        this.error = 'Failed to load service details. Please try again.';
        this.loading = false;
      }
    },
    
    async fetchRelatedServices() {
      // This would normally be an API call to get related services based on category
      // For demo purposes we'll just wait and populate with sample data
      setTimeout(() => {
        this.relatedServices = [
          {
            id: 1,
            name: 'Basic Plumbing',
            base_price: 600,
            time_required: 60
          },
          {
            id: 2,
            name: 'Advanced Plumbing',
            base_price: 1200,
            time_required: 120
          },
          {
            id: 3,
            name: 'Emergency Plumbing',
            base_price: 1500,
            time_required: 90
          }
        ];
      }, 1000);
    },
    
    async fetchReviews() {
      // This would normally be an API call to get reviews for this service
      // For demo purposes we'll just wait and populate with sample data
      setTimeout(() => {
        this.reviews = [
          {
            id: 1,
            customer_name: 'John Doe',
            rating: 5,
            remarks: 'Excellent service! The professional was on time and did a great job.',
            date_created: '2023-09-15T10:30:00Z'
          },
          {
            id: 2,
            customer_name: 'Jane Smith',
            rating: 4,
            remarks: 'Good service overall. Would recommend to others.',
            date_created: '2023-09-10T14:45:00Z'
          },
          {
            id: 3,
            customer_name: 'Mike Johnson',
            rating: 3,
            remarks: 'Average service. Took longer than expected.',
            date_created: '2023-09-05T09:20:00Z'
          }
        ];
      }, 1000);
    },
    
    async submitRequest() {
      this.submitting = true;
      try {
        // Make sure the service_id is set
        this.requestForm.service_id = this.service.id;
        
        // Send the request to the API
        await customerAPI.createRequest(this.requestForm);
        
        // Reset the form
        this.requestForm = {
          service_id: this.service.id,
          pin_code: '',
          special_instructions: ''
        };
        
        // Show success message
        this.showSuccessModal = true;
        
      } catch (error) {
        console.error('Error submitting service request:', error);
        alert('Failed to submit service request: ' + (error.message || 'Unknown error'));
      } finally {
        this.submitting = false;
      }
    },
    
    navigateToService(serviceId) {
      // Navigate to the details page for another service
      this.$router.push(`/service-details/${serviceId}`);
    },
    
    goToRequests() {
      // Close the modal and navigate to requests page
      this.showSuccessModal = false;
      this.$router.push('/customer/dashboard');
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  },
  created() {
    this.fetchServiceDetails();
  }
}
</script>

<style scoped>
.service-details-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  overflow: hidden;
}

.included-list {
  list-style: none;
  padding-left: 0;
}

.included-list li {
  padding: 8px 0;
}

.review-item {
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.review-item:last-child {
  border-bottom: none;
}

.stars i {
  color: #e0e0e0;
}

.stars i.text-warning {
  color: #ffc107;
}

.related-service-item {
  padding: 12px;
  border-radius: 8px;
  background-color: #f8f9fa;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.related-service-item:hover {
  background-color: #e9ecef;
}

.related-service-item:last-child {
  margin-bottom: 0;
}

.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>

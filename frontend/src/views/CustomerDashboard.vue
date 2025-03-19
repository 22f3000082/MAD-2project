<template>
  <div class="customer-dashboard">
    <div class="container py-4">
      <!-- Welcome Section -->
      <div class="row mb-4">
        <div class="col-md-8">
          <h2>Welcome, {{ userName }}!</h2>
          <p class="text-muted">Manage your service requests and find services</p>
        </div>
        <div class="col-md-4 text-md-end">
          <button class="btn btn-primary" @click="showNewRequestModal = true">
            <i class="fas fa-plus me-2"></i>New Service Request
          </button>
        </div>
      </div>

      <!-- Search Services Section -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="card-title mb-3">Search Services</h5>
          <div class="row g-3">
            <div class="col-md-4">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fas fa-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  v-model="searchQuery.name"
                  placeholder="Service name..."
                  @input="searchServices"
                >
              </div>
            </div>
            <div class="col-md-4">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fas fa-map-marker-alt"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  v-model="searchQuery.pinCode"
                  placeholder="PIN code..."
                  @input="searchServices"
                >
              </div>
            </div>
            <div class="col-md-4">
              <select class="form-select" v-model="searchQuery.category" @change="searchServices">
                <option value="">All Categories</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Service Requests Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'active' }"
            @click.prevent="activeTab = 'active'"
            href="#"
          >
            Active Requests
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'completed' }"
            @click.prevent="activeTab = 'completed'"
            href="#"
          >
            Completed
          </a>
        </li>
      </ul>

      <!-- Service Requests List -->
      <div class="row g-4">
        <div v-if="filteredRequests.length === 0" class="col-12 text-center py-5">
          <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
          <h5>No service requests found</h5>
          <p class="text-muted">{{ activeTab === 'active' ? 'Create a new request to get started!' : 'No completed requests yet.' }}</p>
        </div>
        
        <div v-for="request in filteredRequests" :key="request.id" class="col-md-6">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="card-title mb-0">{{ request.service.name }}</h5>
                <span :class="getStatusBadgeClass(request.status)">
                  {{ request.status }}
                </span>
              </div>
              
              <div class="mb-3">
                <small class="text-muted">
                  <i class="fas fa-calendar me-2"></i>
                  Requested: {{ formatDate(request.created_at) }}
                </small>
                <br v-if="request.completed_at">
                <small v-if="request.completed_at" class="text-muted">
                  <i class="fas fa-check-circle me-2"></i>
                  Completed: {{ formatDate(request.completed_at) }}
                </small>
              </div>

              <div v-if="request.professional" class="mb-3">
                <strong>Professional:</strong>
                <span>{{ request.professional.professional_name }}</span>
              </div>

              <p class="card-text">{{ request.special_instructions || 'No special instructions' }}</p>

              <!-- Action Buttons -->
              <div class="d-flex justify-content-end gap-2">
                <button
                  v-if="request.status === 'pending' || request.status === 'assigned'"
                  class="btn btn-outline-danger btn-sm"
                  @click="closeRequest(request)"
                >
                  <i class="fas fa-times me-1"></i>
                  Close
                </button>
                <button
                  v-if="request.status === 'pending'"
                  class="btn btn-outline-primary btn-sm"
                  @click="editRequest(request)"
                >
                  <i class="fas fa-edit me-1"></i>
                  Edit
                </button>
                <button
                  v-if="request.status === 'completed' && !request.has_review"
                  class="btn btn-outline-success btn-sm"
                  @click="addReview(request)"
                >
                  <i class="fas fa-star me-1"></i>
                  Review
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- New Service Request Modal -->
    <div class="modal fade" :class="{ show: showNewRequestModal }" v-if="showNewRequestModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">New Service Request</h5>
            <button type="button" class="btn-close" @click="showNewRequestModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createRequest">
              <div class="mb-3">
                <label class="form-label">Service Type</label>
                <select class="form-select" v-model="newRequest.service_id" required>
                  <option value="">Select a service</option>
                  <option v-for="service in services" :key="service.id" :value="service.id">
                    {{ service.name }} - ₹{{ service.base_price }}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">PIN Code</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="newRequest.pin_code"
                  required
                  pattern="[0-9]{6}"
                  placeholder="Enter 6-digit PIN code"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Special Instructions</label>
                <textarea
                  class="form-control"
                  v-model="newRequest.special_instructions"
                  rows="3"
                  placeholder="Any specific requirements or details..."
                ></textarea>
              </div>

              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" @click="showNewRequestModal = false">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Create Request
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <div class="modal fade" :class="{ show: showReviewModal }" v-if="showReviewModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Review</h5>
            <button type="button" class="btn-close" @click="showReviewModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitReview">
              <div class="mb-3">
                <label class="form-label">Rating</label>
                <div class="star-rating">
                  <i
                    v-for="star in 5"
                    :key="star"
                    class="fas fa-star"
                    :class="{ active: star <= review.rating }"
                    @click="review.rating = star"
                  ></i>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Comments</label>
                <textarea
                  class="form-control"
                  v-model="review.remarks"
                  rows="3"
                  required
                  placeholder="Share your experience..."
                ></textarea>
              </div>

              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" @click="showReviewModal = false">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Submit Review
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { customerAPI, serviceAPI } from '@/services/api'

export default {
  name: 'CustomerDashboard',
  data() {
    return {
      userName: JSON.parse(localStorage.getItem('user'))?.name || 'Customer',
      activeTab: 'active',
      searchQuery: {
        name: '',
        pinCode: '',
        category: ''
      },
      services: [],
      categories: [],
      serviceRequests: [],
      showNewRequestModal: false,
      showReviewModal: false,
      isLoading: false,
      newRequest: {
        service_id: '',
        pin_code: '',
        special_instructions: ''
      },
      review: {
        rating: 0,
        remarks: ''
      },
      selectedRequest: null
    }
  },
  computed: {
    filteredRequests() {
      return this.serviceRequests.filter(request => {
        if (this.activeTab === 'active') {
          return ['pending', 'assigned', 'in_progress'].includes(request.status)
        } else {
          return ['completed', 'closed'].includes(request.status)
        }
      })
    }
  },
  methods: {
    async fetchServices() {
      try {
        const response = await serviceAPI.getServices()
        this.services = response
        this.categories = [...new Set(response.map(service => service.category))]
      } catch (error) {
        console.error('Error fetching services:', error)
      }
    },
    async fetchRequests() {
      try {
        const response = await customerAPI.getRequests()
        this.serviceRequests = response
      } catch (error) {
        console.error('Error fetching requests:', error)
      }
    },
    async searchServices() {
      try {
        const response = await serviceAPI.searchServices(this.searchQuery)
        this.services = response
      } catch (error) {
        console.error('Error searching services:', error)
      }
    },
    async createRequest() {
      this.isLoading = true
      try {
        await customerAPI.createRequest(this.newRequest)
        this.showNewRequestModal = false
        this.newRequest = { service_id: '', pin_code: '', special_instructions: '' }
        await this.fetchRequests()
      } catch (error) {
        console.error('Error creating request:', error)
      } finally {
        this.isLoading = false
      }
    },
    async closeRequest(request) {
      if (confirm('Are you sure you want to close this request?')) {
        try {
          await customerAPI.closeRequest(request.id)
          await this.fetchRequests()
        } catch (error) {
          console.error('Error closing request:', error)
        }
      }
    },
    editRequest(request) {
      // Implement edit functionality
      console.log('Edit request:', request)
    },
    addReview(request) {
      this.selectedRequest = request
      this.review = { rating: 0, remarks: '' }
      this.showReviewModal = true
    },
    async submitReview() {
      if (!this.selectedRequest) return

      this.isLoading = true
      try {
        await customerAPI.addReview(this.selectedRequest.id, this.review)
        this.showReviewModal = false
        await this.fetchRequests()
      } catch (error) {
        console.error('Error submitting review:', error)
      } finally {
        this.isLoading = false
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    getStatusBadgeClass(status) {
      const classes = {
        pending: 'badge bg-warning',
        assigned: 'badge bg-info',
        in_progress: 'badge bg-primary',
        completed: 'badge bg-success',
        closed: 'badge bg-secondary'
      }
      return classes[status] || 'badge bg-secondary'
    }
  },
  async created() {
    await Promise.all([
      this.fetchServices(),
      this.fetchRequests()
    ])
  }
}
</script>

<style scoped>
.customer-dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.star-rating {
  display: flex;
  gap: 0.5rem;
  font-size: 1.5rem;
}

.star-rating i {
  cursor: pointer;
  color: #dee2e6;
}

.star-rating i.active {
  color: #ffc107;
}

.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}

.badge {
  font-size: 0.8rem;
  padding: 0.5em 0.8em;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .text-md-end {
    text-align: left !important;
    margin-top: 1rem;
  }
}
</style>

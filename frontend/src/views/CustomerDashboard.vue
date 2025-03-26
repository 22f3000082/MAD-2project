<template>
  <div class="customer-dashboard">
    <div class="container py-4">
      <!-- Welcome Section -->
      <div class="row mb-4">
        <div class="col-md-8">
          <h2>Welcome, {{ userName }}!</h2>
          <p class="text-muted">Find services and manage your requests</p>
        </div>
        <div class="col-md-4 text-md-end">
          <button class="btn btn-primary" @click="showNewRequestModal = true">
            <i class="fas fa-plus me-2"></i>New Service Request
          </button>
        </div>
      </div>

      <!-- Main Navigation Tabs -->
      <ul class="nav nav-pills mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeSection === 'browse' }" 
             @click.prevent="activeSection = 'browse'" href="#">
            <i class="fas fa-search me-1"></i> Browse Services
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeSection === 'requests' }" 
             @click.prevent="activeSection = 'requests'" href="#">
            <i class="fas fa-list-alt me-1"></i> My Requests
          </a>
        </li>
      </ul>

      <!-- Browse Services Section -->
      <div v-if="activeSection === 'browse'">
        <div class="browse-services-container">
          <!-- Header with Stats -->
          <div class="services-header mb-4">
            <div class="row align-items-center">
              <div class="col-md-6">
                <h4>Browse Available Services</h4>
                <p class="text-muted mb-md-0">
                  <span v-if="!loading">{{ filteredServices.length }} services available</span>
                  <span v-else>Finding the best services for you...</span>
                </p>
              </div>
              <div class="col-md-6 text-md-end">
                <div class="btn-group">
                  <button class="btn btn-outline-primary" @click="refreshServices">
                    <i class="fas fa-sync-alt me-1"></i> Refresh
                  </button>
                  <button claFss="btn btn-outline-secondary" @click="toggleAdvancedSearch">
                    <i class="fas fa-sliders-h me-1"></i> Filters
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Enhanced Service Search Panel -->
          <ServiceSearchPanel 
            :initialParams="searchQuery" 
            :categories="categories"
            @search="handleSearch"
            :class="{ 'mb-4': true, 'collapsed': !showAdvancedSearch }"
          />

          <!-- Popular Categories Quick Filter -->
          <div class="category-chips mb-4">
            <button 
              v-for="category in popularCategories" 
              :key="category" 
              class="category-chip" 
              :class="{ active: searchQuery.category === category }"
              @click="quickFilterByCategory(category)"
            >
              <span>{{ category }}</span>
            </button>
            <button class="category-chip" @click="clearCategoryFilter">
              <i class="fas fa-times me-1"></i> Clear
            </button>
          </div>

          <!-- Error Alert -->
          <div v-if="error" class="alert alert-danger mb-4" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ error }}
            <button type="button" class="btn-close float-end" @click="error = null"></button>
          </div>

          <!-- Service List Component -->
          <ServiceList
            :services="filteredServices"
            :loading="loading"
            :hasMore="hasMoreServices"
            @view-details="selectService"
            @request-service="directRequestService"
            @load-more="loadMoreServices"
          />
        </div>
      </div>

      <!-- My Requests Section -->
      <div v-if="activeSection === 'requests'">
        <!-- Service Requests Tabs -->
        <ul class="nav nav-tabs mb-4">
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: activeTab === 'active' }"
              @click.prevent="activeTab = 'active'"
              href="#"
            >
              <i class="fas fa-spinner me-1"></i> Active Requests
              <span v-if="getActiveCount() > 0" class="badge rounded-pill bg-primary ms-1">
                {{ getActiveCount() }}
              </span>
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: activeTab === 'completed' }"
              @click.prevent="activeTab = 'completed'"
              href="#"
            >
              <i class="fas fa-check-circle me-1"></i> Service History
              <span v-if="getCompletedCount() > 0" class="badge rounded-pill bg-success ms-1">
                {{ getCompletedCount() }}
              </span>
            </a>
          </li>
        </ul>

        <!-- Service Requests List -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-2">Loading your requests...</p>
        </div>
        
        <div v-else-if="filteredRequests.length === 0" class="text-center py-5">
          <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
          <h5>No service requests found</h5>
          <p class="text-muted">
            {{ activeTab === 'active' ? 'Create a new request to get started!' : 'No completed requests yet.' }}
          </p>
          <button v-if="activeTab === 'active'" class="btn btn-primary mt-2" @click="showNewRequestModal = true">
            <i class="fas fa-plus me-2"></i>Create Service Request
          </button>
        </div>
        
        <div v-else class="row g-4">
          <div v-for="request in filteredRequests" :key="request.id" class="col-md-6">
            <div class="card h-100 shadow-sm" :class="{'border-warning': request.status === 'pending', 
                                                     'border-primary': request.status === 'in_progress',
                                                     'border-success': request.status === 'completed'}">
              <div class="card-header bg-transparent d-flex justify-content-between align-items-center">
                <span :class="getStatusBadgeClass(request.status)">
                  {{ request.status }}
                </span>
                <small class="text-muted">
                  <i class="fas fa-calendar me-1"></i> {{ formatDate(request.created_at, true) }}
                </small>
              </div>
              <div class="card-body">
                <h5 class="card-title mb-3">{{ request.service.name }}</h5>
                
                <div class="d-flex mb-3">
                  <div class="me-3">
                    <i class="fas fa-map-marker-alt text-muted me-1"></i> {{ request.pin_code }}
                  </div>
                  <div v-if="request.final_amount">
                    <i class="fas fa-money-bill-wave text-success me-1"></i> ₹{{ request.final_amount }}
                  </div>
                </div>

                <div v-if="request.professional" class="mb-3 p-2 bg-light rounded">
                  <div class="d-flex align-items-center">
                    <i class="fas fa-user-tie text-primary me-2 fa-lg"></i>
                    <div>
                      <strong>{{ request.professional.professional_name }}</strong>
                      <p class="text-muted mb-0 small">{{ request.professional.service_type }}</p>
                    </div>
                  </div>
                </div>

                <p v-if="request.special_instructions" class="card-text text-truncate mb-3" 
                   :title="request.special_instructions">
                  {{ request.special_instructions }}
                </p>

                <!-- Status update indicators -->
                <div class="mb-3 service-progress">
                  <div class="status-track d-flex justify-content-between">
                    <div class="status-point" :class="{'active': true}">
                      <i class="fas fa-plus-circle"></i>
                      <span>Created</span>
                    </div>
                    <div class="status-point" :class="{'active': ['in_progress', 'completed', 'closed'].includes(request.status)}">
                      <i class="fas fa-tools"></i>
                      <span>In Progress</span>
                    </div>
                    <div class="status-point" :class="{'active': ['completed', 'closed'].includes(request.status)}">
                      <i class="fas fa-check-circle"></i>
                      <span>Completed</span>
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="d-flex justify-content-end gap-2 mt-3">
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
                  <button
                    class="btn btn-outline-secondary btn-sm"
                    @click="viewRequestDetails(request)"
                  >
                    <i class="fas fa-eye me-1"></i>
                    Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Service Details Modal -->
    <div class="modal fade" :class="{ show: showServiceModal }" v-if="showServiceModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Service Details</h5>
            <button type="button" class="btn-close" @click="showServiceModal = false"></button>
          </div>
          <div class="modal-body" v-if="selectedService">
            <div class="service-details">
              <h4>{{ selectedService.name }}</h4>
              <div class="d-flex justify-content-between mb-3">
                <span class="badge bg-primary fs-5">₹{{ selectedService.base_price }}</span>
                <span class="text-muted"><i class="far fa-clock me-2"></i>{{ selectedService.time_required }} minutes</span>
              </div>
              <p>{{ selectedService.description }}</p>
              <div class="mb-3">
                <strong>Category:</strong> {{ selectedService.category }}
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showServiceModal = false">Close</button>
            <button type="button" class="btn btn-primary" @click="requestSelectedService">
              <i class="fas fa-plus me-1"></i> Request Service
            </button>
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
                <label for="serviceCategory" class="form-label">Service Category</label>
                <select id="serviceCategory" name="serviceCategory" class="form-select" v-model="newRequest.category">
                  <option value="">Select Category</option>
                  <option v-for="category in categories" :key="category" :value="category">
                    {{ category }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="pinCode" class="form-label">PIN Code</label>
                <input 
                  id="pinCode"
                  name="pinCode"
                  type="text"
                  class="form-control"
                  v-model="newRequest.pin_code"
                  required
                  pattern="[0-9]{6}"
                  placeholder="Enter 6-digit PIN code"
                >
              </div>
              <div class="mb-3">
                <label for="specialInstructions" class="form-label">Special Instructions</label>
                <textarea
                  id="specialInstructions"
                  name="specialInstructions"
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

    <!-- Enhanced Review Modal -->
    <div class="modal fade" :class="{ show: showReviewModal }" v-if="showReviewModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <ServiceReviewForm
            :requestId="selectedRequest?.id"
            :serviceName="selectedRequest?.service?.name"
            :serviceDate="selectedRequest?.completed_at"
            :professionalName="selectedRequest?.professional?.professional_name"
            @close="showReviewModal = false"
            @submitted="handleReviewSubmitted"
          />
        </div>
      </div>
    </div>

    <!-- Enhanced Request Details Modal -->
    <div class="modal fade" :class="{ show: showRequestDetailsModal }" v-if="showRequestDetailsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Details</h5>
            <button type="button" class="btn-close" @click="showRequestDetailsModal = false"></button>
          </div>
          <div class="modal-body" v-if="selectedRequest">
            <div class="row mb-4">
              <div class="col-md-6">
                <h5>{{ selectedRequest.service?.name }}</h5>
                <div :class="getStatusBadgeClass(selectedRequest.status)" class="mb-2 badge-lg">
                  {{ selectedRequest.status }}
                </div>
                <p class="text-muted">
                  <i class="fas fa-map-marker-alt me-2"></i>
                  PIN Code: {{ selectedRequest.pin_code }}
                </p>
                <p v-if="selectedRequest.final_amount" class="badge bg-success">
                  Final Amount: ₹{{ selectedRequest.final_amount }}
                </p>
              </div>
              <div class="col-md-6 text-md-end">
                <p class="mb-1"><strong>Requested:</strong> {{ formatDate(selectedRequest.created_at) }}</p>
                <p v-if="selectedRequest.accepted_at" class="mb-1">
                  <strong>Accepted:</strong> {{ formatDate(selectedRequest.accepted_at) }}
                </p>
                <p v-if="selectedRequest.completed_at" class="mb-1">
                  <strong>Completed:</strong> {{ formatDate(selectedRequest.completed_at) }}
                </p>
                <p v-if="selectedRequest.closed_at" class="mb-1">
                  <strong>Closed:</strong> {{ formatDate(selectedRequest.closed_at) }}
                </p>
              </div>
            </div>
            <!-- Service Request Timeline -->
            <div class="service-timeline mb-4">
              <h6>Service Timeline</h6>
              <div class="timeline">
                <div class="timeline-item">
                  <div class="timeline-marker bg-success"></div>
                  <div class="timeline-content">
                    <p class="mb-0"><strong>Request Created</strong></p>
                    <p class="text-muted small mb-0">{{ formatDate(selectedRequest.created_at) }}</p>
                  </div>
                </div>
                <div v-if="selectedRequest.accepted_at" class="timeline-item">
                  <div class="timeline-marker bg-primary"></div>
                  <div class="timeline-content">
                    <p class="mb-0"><strong>Professional Assigned</strong></p>
                    <p class="text-muted small mb-0">{{ formatDate(selectedRequest.accepted_at) }}</p>
                    <p v-if="selectedRequest.professional" class="small mb-0">
                      {{ selectedRequest.professional.professional_name }} was assigned to your request
                    </p>
                  </div>
                </div>
                <div v-if="selectedRequest.completed_at" class="timeline-item">
                  <div class="timeline-marker bg-info"></div>
                  <div class="timeline-content">
                    <p class="mb-0"><strong>Service Completed</strong></p>
                    <p class="text-muted small mb-0">{{ formatDate(selectedRequest.completed_at) }}</p>
                    <p v-if="selectedRequest.final_amount" class="small mb-0">
                      Service completed with final amount: ₹{{ selectedRequest.final_amount }}
                    </p>
                  </div>
                </div>
                <div v-if="selectedRequest.closed_at" class="timeline-item">
                  <div class="timeline-marker bg-secondary"></div>
                  <div class="timeline-content">
                    <p class="mb-0"><strong>Request Closed</strong></p>
                    <p class="text-muted small mb-0">{{ formatDate(selectedRequest.closed_at) }}</p>
                  </div>
                </div>
                <div v-if="selectedRequest.has_review" class="timeline-item">
                  <div class="timeline-marker bg-warning"></div>
                  <div class="timeline-content">
                    <p class="mb-0"><strong>Review Submitted</strong></p>
                    <div v-if="selectedRequest.review" class="mt-1">
                      <div class="star-rating small">
                        <i v-for="n in 5" :key="n" 
                          class="fas fa-star" 
                          :class="n <= selectedRequest.review.rating ? 'text-warning' : 'text-muted'"></i>
                      </div>
                      <p class="small mt-1 mb-0">{{ selectedRequest.review.remarks }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Special Instructions -->
            <div class="mb-4">
              <h6>Special Instructions</h6>
              <p class="p-3 bg-light rounded">{{ selectedRequest.special_instructions || 'No special instructions provided.' }}</p>
            </div>
            <!-- Professional Details -->
            <div v-if="selectedRequest.professional" class="mb-4">
              <h6>Professional Details</h6>
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ selectedRequest.professional.professional_name }}</h5>
                  <p class="text-muted mb-1">
                    <strong>Service Type:</strong> {{ selectedRequest.professional.service_type }}
                  </p>
                  <p class="text-muted mb-0">
                    <strong>Experience:</strong> {{ selectedRequest.professional.experience }} years
                  </p>
                </div>
              </div>
            </div>
            <!-- Action Buttons -->
            <div class="d-flex justify-content-end gap-2 mt-4">
              <button 
                v-if="selectedRequest.status === 'pending' || selectedRequest.status === 'assigned'"
                class="btn btn-danger" 
                @click="closeRequest(selectedRequest, true)">
                <i class="fas fa-times me-1"></i> Cancel Request
              </button>
              <button 
                v-if="selectedRequest.status === 'completed' && !selectedRequest.has_review"
                class="btn btn-warning" 
                @click="addReview(selectedRequest)">
                <i class="fas fa-star me-1"></i> Review Service
              </button>
              <button 
                class="btn btn-secondary" 
                @click="showRequestDetailsModal = false">
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { serviceAPI, customerAPI } from '@/services/api';
import ServiceSearchPanel from '@/components/ServiceSearchPanel.vue';
import ServiceList from '@/components/ServiceList.vue';
import ServiceReviewForm from '@/components/ServiceReviewForm.vue';

export default {
  name: 'CustomerDashboard',
  components: {
    ServiceSearchPanel,
    ServiceList,
    ServiceReviewForm
  },

  data() {
    const user = JSON.parse(localStorage.getItem('user')) || {};
    return {
      userName: user.name || user.username || 'Customer',
      activeSection: 'browse',
      activeTab: 'active',
      showServiceModal: false,
      showNewRequestModal: false,
      showReviewModal: false,
      showRequestDetailsModal: false,
      selectedService: null,
      selectedRequest: null,
      searchQuery: {
        name: '',
        category: '',
        pinCode: ''
      },
      services: [],
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
      ],
      serviceRequests: [],
      loading: false,
      error: null,
      newRequest: {
        service_id: '',
        pin_code: '',
        special_instructions: '',
        category: ''
      },
      isLoading: false,
      page: 1,
      hasMoreServices: true,
      showAdvancedSearch: false
    };
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
    },
    filteredServices() {
      if (!this.services.length) return [];
      return this.services.filter(service => {
        // Filter by name
        if (this.searchQuery.name && !service.name.toLowerCase().includes(this.searchQuery.name.toLowerCase())) {
          return false;
        }
        
        // Filter by category
        if (this.searchQuery.category && service.category !== this.searchQuery.category) {
          return false;
        }

        // Filter by PIN code if implemented
        if (this.searchQuery.pinCode && service.available_pin_codes) {
          if (!service.available_pin_codes.includes(this.searchQuery.pinCode)) {
            return false;
          }
        }
        return true;
      });
    }
  },

  methods: {
    async fetchServices() {
      try {
        this.loading = true;
        this.error = null;
        const response = await serviceAPI.getPublicServices();
        this.services = response || [];
      } catch (error) {
        console.error('Error fetching services:', error);
        this.error = 'Failed to load services. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async fetchServiceTypes() {
      try {
        this.loading = true;
        console.log('Fetching service categories from database...');
        const response = await serviceAPI.getServiceTypes();
        if (response && Array.isArray(response) && response.length > 0) {
          this.categories = response;
          console.log(`Received ${this.categories.length} service categories`);
        } else {
          console.warn('No service categories returned from API, using defaults');
          // Fallback to defaults if API returns empty array
          this.categories = [
            'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
            'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
          ];
        }
        this.loading = false;
      } catch (error) {
        console.error('Error fetching service categories:', error);
        // Fallback to defaults on error
        this.categories = [
          'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
          'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
        ];
        this.loading = false;
      }
    },

    async fetchRequests() {
      try {
        this.loading = true;
        console.log('Fetching customer requests...');
        const response = await customerAPI.getRequests();
        if (!response || !Array.isArray(response)) {
          console.warn('Invalid response format for customer requests:', response);
          this.serviceRequests = [];
        } else {
          console.log(`Retrieved ${response.length} requests for customer`);
          this.serviceRequests = response;
        }
      } catch (error) {
        console.error('Error fetching requests:', error);
        this.error = 'Failed to load service requests. Please try again.';
        this.serviceRequests = []; // Fallback to empty array
      } finally {
        this.loading = false;
      }
    },

    async refreshServices() {
      try {
        this.loading = true;
        this.error = null;
        await this.fetchServices();
        // Reset some search parameters but keep category if selected
        const category = this.searchQuery.category;
        this.searchQuery = { name: '', category, pinCode: '' };
      } catch (error) {
        console.error('Error refreshing services:', error);
        this.error = 'Failed to refresh services. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    toggleAdvancedSearch() {
      this.showAdvancedSearch = !this.showAdvancedSearch;
    },

    quickFilterByCategory(category) {
      if (this.searchQuery.category === category) {
        // If clicking the already selected category, clear it
        this.searchQuery.category = '';
      } else {
        this.searchQuery.category = category;
      }
      this.handleSearch(this.searchQuery);
    },

    clearCategoryFilter() {
      this.searchQuery.category = '';
      this.handleSearch(this.searchQuery);
    },

    async loadMoreServices() {
      if (this.loading || !this.hasMoreServices) return;
      
      try {
        this.loading = true;
        this.page += 1;
        
        // Call API with pagination parameters
        const moreServices = await serviceAPI.getServices({
          page: this.page,
          ...this.searchQuery
        });
        if (moreServices && moreServices.length) {
          this.services = [...this.services, ...moreServices];
          // Check if we've reached the end
          this.hasMoreServices = moreServices.length >= 10; // Assuming 10 per page
        } else {
          this.hasMoreServices = false;
        }
      } catch (error) {
        console.error('Error loading more services:', error);
        this.error = 'Failed to load more services.';
      } finally {
        this.loading = false;
      }
    },

    async createRequest() {
      this.isLoading = true;
      try {
        // Validate that we have either service_id or category
        if (!this.newRequest.service_id && !this.newRequest.category) {
          throw new Error("Please select a service category");
        }
        
        // Ensure pin_code is valid
        if (!this.newRequest.pin_code || !/^\d{6}$/.test(this.newRequest.pin_code)) {
          throw new Error("Please enter a valid 6-digit PIN code");
        }
        
        console.log('Submitting request with data:', this.newRequest);
        
        try {
          const response = await customerAPI.createRequest(this.newRequest);
          this.showNewRequestModal = false;
          this.newRequest = { service_id: '', pin_code: '', special_instructions: '', category: '' };
          this.activeSection = 'requests'; // Switch to requests tab
          await this.fetchRequests();
          alert('Service request created successfully!');
        } catch (apiError) {
          // Show more friendly error message with details from the backend
          if (apiError.message.includes('No service found in category')) {
            throw new Error(`We currently don't have service professionals for ${this.newRequest.category}. Please try a different category.`);
          } else {
            throw apiError;
          }
        }
      } catch (error) {
        console.error('Error creating request:', error);
        alert('Failed to create service request: ' + (error.message || 'Unknown error'));
      } finally {
        this.isLoading = false;
      }
    },

    async closeRequest(request, fromModal = false) {
      if (confirm('Are you sure you want to cancel this request?')) {
        try {
          this.isLoading = true;
          await customerAPI.closeRequest(request.id);
          await this.fetchRequests();
          if (fromModal) {
            this.showRequestDetailsModal = false;
          }
          alert('Request cancelled successfully.');
        } catch (error) {
          console.error('Error closing request:', error);
          alert('Failed to cancel request: ' + (error.message || 'Unknown error'));
        } finally {
          this.isLoading = false;
        }
      }
    },

    editRequest(request) {
      // Implement edit functionality (e.g., populate form with current values)
      this.newRequest = {
        service_id: request.service_id,
        pin_code: request.pin_code,
        special_instructions: request.special_instructions || '',
        category: request.category || ''
      };
      this.showNewRequestModal = true;
    },

    addReview(request) {
      this.selectedRequest = request;
      this.review = { rating: 0, remarks: '' };
      this.showReviewModal = true;
    },

    async submitReview() {
      try {
        this.isLoading = true;
        await customerAPI.addReview(this.selectedRequest.id, this.review);
        this.showReviewModal = false;
        this.review = { rating: 0, remarks: '' };
        await this.fetchRequests();
        alert('Review submitted successfully.');
      } catch (error) {
        console.error('Error submitting review:', error);
        alert('Failed to submit review: ' + (error.message || 'Unknown error'));
      } finally {
        this.isLoading = false;
      }
    },

    selectService(service) {
      this.selectedService = service;
      this.showServiceModal = true;
    },

    requestSelectedService() {
      this.newRequest.service_id = this.selectedService.id;
      this.showServiceModal = false;
      this.showNewRequestModal = true;
    },

    viewRequestDetails(request) {
      this.selectedRequest = request;
      this.showRequestDetailsModal = true;
    },

    formatDate(dateString, short = false) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      if (short) {
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric'
        });
      }
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    getStatusBadgeClass(status) {
      const classes = {
        pending: 'badge bg-warning',
        assigned: 'badge bg-info',
        in_progress: 'badge bg-primary',
        completed: 'badge bg-success',
        closed: 'badge bg-secondary',
        cancelled: 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    },

    handleSearch(params) {
      this.searchQuery = { ...params };
      this.page = 1;
      this.fetchServices();
    },

    directRequestService(service) {
      this.selectedService = service;
      this.showNewRequestModal = true;
      // Pre-populate the request form with the selected service
      this.newRequest.service_id = service.id;
    },

    handleReviewSubmitted() {
      this.showReviewModal = false;
      alert('Thank you for your review!');
      this.fetchRequests();
    },

    getActiveCount() {
      return this.serviceRequests.filter(request => 
        ['pending', 'assigned', 'in_progress'].includes(request.status)
      ).length;
    },

    getCompletedCount() {
      return this.serviceRequests.filter(request => 
        ['completed', 'closed'].includes(request.status)
      ).length;
    },

    async createServiceRequest(serviceId) {
      try {
        if (!this.newRequest.pin_code || !/^\d{6}$/.test(this.newRequest.pin_code)) {
          throw new Error('Please enter a valid 6-digit PIN code');
        }

        this.isLoading = true;
        await customerAPI.createRequest({
          service_id: serviceId,
          pin_code: this.newRequest.pin_code,
          special_instructions: this.newRequest.special_instructions
        });

        this.showNewRequestModal = false;
        this.fetchRequests();
        this.$toast.success('Service request created successfully');
      } catch (error) {
        console.error('Error creating request:', error);
        this.$toast.error(error.message || 'Failed to create request');
      } finally {
        this.isLoading = false;
      }
    }
  },

  async created() {
    try {
      console.log('CustomerDashboard created, loading data...');
      await Promise.all([
        this.fetchServices(),
        this.fetchServiceTypes(),
        this.fetchRequests()
      ]);
    } catch (error) {
      console.error('Error initializing dashboard:', error);
      this.error = 'Failed to load dashboard data. Please refresh the page.';
    }
  }
}
</script>

<style scoped>
.customer-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.service-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.nav-pills .nav-link,
.nav-tabs .nav-link {
  font-size: 1rem;
  cursor: pointer;
}

.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}

.star-rating {
  display: flex;
  gap: 5px;
}

.star-rating i {
  cursor: pointer;
  color: #e0e0e0;
}

.star-rating i.active {
  color: #ffc107;
}

/* Enhanced timeline and status styles */
.badge-lg {
  font-size: 1rem;
  padding: 0.5rem 0.75rem;
}

.service-progress {
  position: relative;
  margin: 15px 0;
}

.status-track {
  position: relative;
  height: 40px;
}

.status-track:before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  height: 2px;
  background-color: #e9ecef;
  z-index: 1;
}

.status-point {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #adb5bd;
}

.status-point i {
  background-color: white;
  border-radius: 50%;
  padding: 5px;
  font-size: 1rem;
}

.status-point span {
  font-size: 0.65rem;
  margin-top: 4px;
}

.status-point.active {
  color: #0d6efd;
}

.status-point.active i {
  color: #0d6efd;
}

.timeline {
  position: relative;
  padding-left: 40px;
}

.timeline-item {
  position: relative;
  padding-bottom: 25px;
}

.timeline-marker {
  position: absolute;
  left: -20px;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.timeline:before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: -12px;
  width: 2px;
  background-color: #e9ecef;
}

.timeline-content {
  background-color: #f8f9fa;
  padding: 10px 15px;
  border-radius: 5px;
}

.card-header .badge {
  font-size: 0.85rem;
  padding: 0.35rem 0.65rem;
}

/* Browse Services Section Styles */
.browse-services-container {
  margin-bottom: 2rem;
}

.services-header {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category-chip {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  color: #495057;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  transition: all 0.2s;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  box-shadow: none;
  outline: none;
}

.category-chip:hover {
  background-color: #e9ecef;
  color: #212529;
}

.category-chip.active {
  background-color: #0d6efd;
  color: white;
  border-color: #0d6efd;
}

/* Animation for collapsing search panel */
.collapsed {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}
</style>
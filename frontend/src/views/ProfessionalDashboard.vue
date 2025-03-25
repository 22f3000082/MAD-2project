<template>
  <div class="professional-dashboard">
    <div class="container py-4">
      <!-- Welcome Section -->
      <div class="row mb-4">
        <div class="col-lg-8">
          <h2>Welcome, {{ professionalName }}!</h2>
          <p class="text-muted">Manage your service assignments and view customer requests</p>
          
          <div class="stats-cards row g-3 mt-3">
            <div class="col-md-4">
              <div class="card bg-primary text-white">
                <div class="card-body">
                  <h6 class="card-title">Pending Requests</h6>
                  <h3 class="mb-0">{{ pendingRequests.length }}</h3>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-success text-white">
                <div class="card-body">
                  <h6 class="card-title">In Progress</h6>
                  <h3 class="mb-0">{{ inProgressRequests.length }}</h3>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-info text-white">
                <div class="card-body">
                  <h6 class="card-title">Completed</h6>
                  <h3 class="mb-0">{{ completedRequests.length }}</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4 mt-4 mt-lg-0">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Your Service Profile</h5>
              <div class="d-flex align-items-center mb-3">
                <div class="rating me-2">
                  <i v-for="i in 5" :key="i" class="fas fa-star" 
                     :class="i <= Math.round(profile.average_rating) ? 'text-warning' : 'text-muted'"></i>
                </div>
                <span>{{ profile.average_rating.toFixed(1) }} / 5 ({{ profile.total_reviews }} reviews)</span>
              </div>
              <p class="mb-1"><strong>Service:</strong> {{ profile.service_type }}</p>
              <p class="mb-1"><strong>Experience:</strong> {{ profile.experience }} years</p>
              <p class="mb-0"><strong>Status:</strong> 
                <span class="badge" :class="profile.is_approved ? 'bg-success' : 'bg-warning'">
                  {{ profile.is_approved ? 'Approved' : 'Pending Approval' }}
                </span>
              </p>
              <div class="mt-3">
                <button class="btn btn-outline-primary btn-sm" @click="showProfileModal = true">
                  <i class="fas fa-user-edit me-1"></i> View Full Profile
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Job Availability Toggle -->
      <div class="card mb-4">
        <div class="card-body d-flex justify-content-between align-items-center">
          <div>
            <h5 class="mb-0">Job Availability</h5>
            <p class="text-muted mb-0">Toggle your availability to receive new service requests</p>
          </div>
          <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" id="availabilitySwitch" v-model="isAvailable" @change="updateAvailability">
            <label class="form-check-label" for="availabilitySwitch">
              <span class="badge" :class="isAvailable ? 'bg-success' : 'bg-secondary'">
                {{ isAvailable ? 'Available' : 'Unavailable' }}
              </span>
            </label>
          </div>
        </div>
      </div>

      <!-- Requests Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'pending' }"
            @click.prevent="activeTab = 'pending'"
            href="#"
          >
            <i class="fas fa-clock me-1"></i> New Requests
            <span class="badge bg-danger ms-1" v-if="pendingRequests.length">{{ pendingRequests.length }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'assigned' }"
            @click.prevent="activeTab = 'assigned'"
            href="#"
          >
            <i class="fas fa-tools me-1"></i> In Progress
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'completed' }"
            @click.prevent="activeTab = 'completed'"
            href="#"
          >
            <i class="fas fa-check-circle me-1"></i> Completed
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'reviews' }"
            @click.prevent="activeTab = 'reviews'"
            href="#"
          >
            <i class="fas fa-star me-1"></i> My Reviews
          </a>
        </li>
      </ul>

      <!-- Loading State -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading service requests...</p>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="filteredRequests.length === 0 && activeTab !== 'reviews'" class="text-center py-5">
        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
        <h5>No service requests found</h5>
        <p class="text-muted">{{ getEmptyStateMessage() }}</p>
      </div>
      
      <!-- Service Requests List -->
      <div v-else-if="activeTab !== 'reviews'" class="row g-4">
        <div v-for="request in filteredRequests" :key="request.id" class="col-md-6">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <span :class="getStatusBadgeClass(request.status)">
                {{ request.status }}
              </span>
              <span class="text-muted small">
                <i class="fas fa-calendar me-1"></i>
                {{ formatDate(request.created_at) }}
              </span>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ request.service.name }}</h5>
              <p class="card-text">
                <strong>Customer:</strong> {{ request.customer.customer_name }}
              </p>
              <p class="card-text">
                <strong>Location:</strong> PIN Code {{ request.pin_code }}
              </p>
to it              <div class="mb-3">
                <!-- Indicate if this is a new customer request vs. assigned request -->
                <span v-if="isNewCustomerRequest(request)" class="badge bg-info mb-2">New Customer Request</span>
              </div>
              <div class="mb-3">
                <strong>Instructions:</strong> 
                <p class="small text-muted">{{ request.special_instructions || 'No special instructions provided.' }}</p>
              </div>
              <div class="mb-3">
                <!-- Actions for pending requests -->
                <template v-if="request.status === 'pending'">
                  <button @click="acceptRequest(request.id)" class="btn btn-success btn-sm me-2">
                    <i class="fas fa-check me-1"></i> Accept
                  </button>
                  <button @click="rejectRequest(request.id)" class="btn btn-danger btn-sm me-2">
                    <i class="fas fa-times me-1"></i> Reject
                  </button>
                </template>
                
                <!-- Actions for in-progress requests -->
                <button v-if="request.status === 'in_progress'" @click="completeRequest(request.id)" class="btn btn-primary btn-sm me-2">
                  <i class="fas fa-check-circle me-1"></i> Mark as Completed
                </button>
                
                <!-- View details button for all requests -->
                <button @click="viewRequestDetails(request)" class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-eye me-1"></i> Details
                </button>
              </div>
            </div>
            <div v-if="request.status === 'completed'" class="card-footer text-muted">
              <div v-if="request.review" class="mt-2">
                <strong>Customer Review:</strong>
                <div class="d-flex align-items-center">
                  <div class="rating me-2">
                    <i v-for="i in 5" :key="i" class="fas fa-star" 
                       :class="i <= request.review.rating ? 'text-warning' : 'text-muted'"></i>
                  </div>
                  <span>{{ request.review.remarks }}</span>
                </div>
              </div>
              <div v-else>
                <i class="fas fa-star-half-alt me-1"></i> Awaiting customer review
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews Tab Content -->
      <div v-if="activeTab === 'reviews'" class="reviews-tab">
        <div v-if="reviews.length === 0" class="text-center py-5">
          <i class="fas fa-star fa-3x text-muted mb-3"></i>
          <h5>No Reviews Yet</h5>
          <p class="text-muted">Complete service requests to receive customer reviews</p>
        </div>

        <div v-else class="card">
          <div class="card-header bg-white">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Customer Reviews</h5>
              <div class="rating-summary">
                <span class="badge bg-primary rounded-pill">
                  <i class="fas fa-star me-1"></i> {{ profile.average_rating.toFixed(1) }}/5
                </span>
              </div>
            </div>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <div v-for="review in reviews" :key="review.id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h6 class="mb-0">{{ review.customer_name }}</h6>
                    <small class="text-muted">{{ formatDate(review.date_created) }}</small>
                  </div>
                  <div class="rating">
                    <i v-for="i in 5" :key="i" class="fas fa-star" 
                       :class="i <= review.rating ? 'text-warning' : 'text-muted'"></i>
                  </div>
                </div>
                <p class="mb-0">{{ review.remarks }}</p>
                <small class="text-muted">Service: {{ review.service_name }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Request Details Modal -->
    <div class="modal fade" :class="{ show: showDetailsModal }" v-if="showDetailsModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Details</h5>
            <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
          </div>
          <div class="modal-body" v-if="selectedRequest">
            <div class="mb-3">
              <h6>Service Information</h6>
              <p class="mb-1"><strong>Service:</strong> {{ selectedRequest.service.name }}</p>
              <p class="mb-1"><strong>Price:</strong> ₹{{ selectedRequest.service.base_price }}</p>
              <p><strong>Status:</strong> 
                <span :class="getStatusBadgeClass(selectedRequest.status)">
                  {{ selectedRequest.status }}
                </span>
              </p>
            </div>
            
            <div class="mb-3">
              <h6>Customer Information</h6>
              <p class="mb-1"><strong>Name:</strong> {{ selectedRequest.customer.customer_name }}</p>
              <p class="mb-1"><strong>Phone:</strong> {{ selectedRequest.customer.phone }}</p>
              <p class="mb-1"><strong>PIN Code:</strong> {{ selectedRequest.pin_code }}</p>
              <p class="mb-0">
                <strong>Address:</strong> {{ selectedRequest.customer.address }}
              </p>
            </div>
            
            <div class="mb-3">
              <h6>Timeline</h6>
              <ul class="timeline">
                <li class="mb-2"><strong>Created:</strong> {{ formatDate(selectedRequest.created_at) }}</li>
                <li v-if="selectedRequest.accepted_at" class="mb-2">
                  <strong>Accepted:</strong> {{ formatDate(selectedRequest.accepted_at) }}
                </li>
                <li v-if="selectedRequest.completed_at" class="mb-2">
                  <strong>Completed:</strong> {{ formatDate(selectedRequest.completed_at) }}
                </li>
                <li v-if="selectedRequest.closed_at">
                  <strong>Closed:</strong> {{ formatDate(selectedRequest.closed_at) }}
                </li>
              </ul>
            </div>
            
            <div class="mb-0">
              <h6>Special Instructions</h6>
              <p class="mb-0">{{ selectedRequest.special_instructions || 'No special instructions provided.' }}</p>
            </div>

            <div v-if="selectedRequest.status === 'in_progress'" class="mt-3">
              <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                You must confirm that you have exited the customer location before marking the service as completed.
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="exitedLocation" v-model="selectedRequest.exited_location">
                <label class="form-check-label" for="exitedLocation">
                  <strong>I confirm that I have exited the customer location</strong>
                </label>
              </div>
            </div>
            
            <div v-if="selectedRequest.status === 'completed'" class="mt-3">
              <div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>
                You have marked this service as completed. Waiting for customer to close the service.
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDetailsModal = false">Close</button>
            
            <!-- Action buttons based on status -->
            <template v-if="selectedRequest && selectedRequest.status === 'pending'">
              <button @click="acceptRequest(selectedRequest.id, true)" class="btn btn-success">
                <i class="fas fa-check me-1"></i> Accept
              </button>
              <button @click="rejectRequest(selectedRequest.id, true)" class="btn btn-danger">
                <i class="fas fa-times me-1"></i> Reject
              </button>
            </template>
            
            <button v-if="selectedRequest && selectedRequest.status === 'in_progress'" 
                    @click="completeRequest(selectedRequest.id, true)" 
                    class="btn btn-primary"
                    :disabled="!selectedRequest.exited_location">
              <i class="fas fa-check-circle me-1"></i> Mark as Completed
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Modal -->
    <div class="modal fade" :class="{ show: showProfileModal }" v-if="showProfileModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Professional Profile</h5>
            <button type="button" class="btn-close" @click="showProfileModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-4 text-center mb-4 mb-md-0">
                <div class="avatar-container mb-3">
                  <img src="https://via.placeholder.com/150" alt="Profile" class="rounded-circle img-thumbnail">
                </div>
                <h4>{{ professionalName }}</h4>
                <div class="rating mb-2">
                  <i v-for="i in 5" :key="i" class="fas fa-star" 
                    :class="i <= Math.round(profile.average_rating) ? 'text-warning' : 'text-muted'"></i>
                  <span class="ms-1">{{ profile.average_rating.toFixed(1) }}/5</span>
                </div>
                <p class="badge bg-primary">{{ profile.service_type }}</p>
              </div>
              
              <div class="col-md-8">
                <div class="mb-3">
                  <h6>About Me</h6>
                  <p>{{ profile.description || 'No description provided.' }}</p>
                </div>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <h6>Experience</h6>
                    <p>{{ profile.experience }} years</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>Joined</h6>
                    <p>{{ formatDate(profile.date_created) }}</p>
                  </div>
                </div>
                
                <div class="mb-3">
                  <h6>Specialization</h6>
                  <p>{{ profile.service_type }}</p>
                </div>
                
                <div class="mb-3">
                  <h6>Contact Information</h6>
                  <p class="mb-1"><i class="fas fa-envelope me-2"></i> {{ profile.email }}</p>
                  <p class="mb-0"><i class="fas fa-phone me-2"></i> {{ profile.phone || 'Not provided' }}</p>
                </div>
              </div>
            </div>
            
            <hr>
            
            <div class="profile-edit-section">
              <h5 class="mb-3">Edit Profile</h5>
              <form @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea v-model="profileForm.description" class="form-control" rows="3"></textarea>
                </div>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Phone</label>
                    <input type="tel" v-model="profileForm.phone" class="form-control">
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Experience (years)</label>
                    <input type="number" v-model="profileForm.experience" class="form-control" min="0">
                  </div>
                </div>
                
                <div class="text-end">
                  <button type="submit" class="btn btn-primary" :disabled="updatingProfile">
                    <span v-if="updatingProfile" class="spinner-border spinner-border-sm me-1"></span>
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error state with more detailed information -->
    <div v-if="error" class="alert alert-danger mt-4">
      <h5><i class="fas fa-exclamation-triangle me-2"></i>Error Loading Dashboard</h5>
      <p>{{ error }}</p>
      <div class="mt-2">
        <button @click="resetError" class="btn btn-primary btn-sm me-2">
          <i class="fas fa-sync me-1"></i> Retry
        </button>
      </div>
    </div>

    <!-- Remove ProfessionalDiagnostics component -->

    <!-- Debug controls (only in development) -->
    <div v-if="isDevelopment" class="mt-4 p-3 bg-light rounded">
      <div class="d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Developer Tools</h5>
        <div>
          <button @click="refreshRequests" class="btn btn-primary btn-sm me-2">
            <i class="fas fa-sync me-1"></i> Refresh Requests
          </button>
          <button @click="refreshAllPendingRequests" class="btn btn-warning btn-sm">
            <i class="fas fa-search me-1"></i> Show All Pending Requests
          </button>
        </div>
      </div>
      
      <div class="mt-3">
        <h6>Debug Information:</h6>
        <div class="small">
          <p class="mb-1"><strong>Professional ID:</strong> {{ current_user?.id || 'Unknown' }}</p>
          <p class="mb-1"><strong>Service Type:</strong> {{ profile.service_type || 'Not specified' }}</p>
          <p class="mb-1"><strong>Assigned Requests:</strong> {{ serviceRequests.length }}</p>
          <p class="mb-1"><strong>Available Requests:</strong> {{ availableCustomerRequests.length }}</p>
          <p class="mb-1"><strong>API Errors:</strong> {{ error || 'None' }}</p>
        </div>
      </div>
      
      <!-- Debug section for all pending requests -->
      <div v-if="debugAllPendingRequests" class="mt-3">
        <h6>All Pending Requests in System:</h6>
        <div class="alert alert-info">
          <p class="mb-1">Total pending requests: {{ debugAllPendingRequests.total_count }}</p>
          <p class="mb-0">These are ALL pending requests in the system, regardless of service type.</p>
        </div>
        
        <div class="table-responsive">
          <table class="table table-sm table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Service</th>
                <th>Category</th>
                <th>Customer</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in debugAllPendingRequests.requests" :key="req.id">
                <td>{{ req.id }}</td>
                <td>{{ req.service_info?.name || 'Unknown' }}</td>
                <td>{{ req.service_info?.category || 'Unknown' }}</td>
                <td>{{ req.customer_info?.name || 'Unknown' }}</td>
                <td>{{ formatDate(req.created_at) }}</td>
                <td>
                  <button @click="forceAcceptRequest(req.id)" class="btn btn-success btn-sm">
                    Accept
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { professionalAPI } from '@/services/api';
// Remove ProfessionalDiagnostics import

export default {
  name: 'ProfessionalDashboard',
  components: {
    // Remove ProfessionalDiagnostics component registration
  },
  data() {
    return {
      professionalName: '',
      activeTab: 'pending',
      loading: true,
      serviceRequests: [],
      availableCustomerRequests: [], // For new requests
      profile: {
        service_type: '',
        experience: 0,
        average_rating: 0,
        total_reviews: 0,
        is_approved: false,
        description: '',
        email: '',
        phone: '',
        date_created: new Date().toISOString()
      },
      reviews: [],
      showDetailsModal: false,
      showProfileModal: false,
      selectedRequest: null,
      isAvailable: true,
      updatingProfile: false,
      profileForm: {
        description: '',
        phone: '',
        experience: 0
      },
      error: null,
      // Remove showDiagnostics property
      isDevelopment: process.env.NODE_ENV === 'development',
      current_user: null,
      debugAllPendingRequests: null,
    };
  },
  computed: {
    pendingRequests() {
      // Add proper return statement
      return [
        ...this.serviceRequests.filter(req => req.status === 'pending'),
        ...this.availableCustomerRequests
      ];
    },
    
    inProgressRequests() {
      return this.serviceRequests.filter(req => 
        req.status === 'in_progress' || req.status === 'assigned'
      ) || [];
    },
    
    completedRequests() {
      return this.serviceRequests.filter(req => 
        req.status === 'completed' || req.status === 'closed'
      ) || [];
    },
    
    filteredRequests() {
      switch(this.activeTab) {
        case 'pending':
          return this.pendingRequests;
        case 'assigned':
          return this.inProgressRequests;
        case 'completed':
          return this.completedRequests;
        default:
          return [];
      }
    }
  },
  created() {
    this.fetchData();
  },
  
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token');
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      
      // Store current user for debugging
      this.current_user = user;
      
      if (!token) {
        console.log('No authentication token found - redirecting to login');
        // Add a small delay to prevent navigation errors during component initialization
        setTimeout(() => {
          this.$router.push('/login');
        }, 100);
        return false;
      }
      
      if (user.role !== 'professional') {
        console.log('User is not a professional - redirecting');
        setTimeout(() => {
          this.$router.push('/login');
        }, 100);
        return false;
      }
      
      this.professionalName = user.name || 'Professional';
      return true;
    },
    
    async fetchData() {
      try {
        // Only proceed if authentication check passed
        if (!this.checkAuth()) {
          return;
        }
        
        this.loading = true;
        this.error = null;
        
        // Only fetch data if we have a token
        const token = localStorage.getItem('token')
        if (!token) {
          throw new Error('Authentication required')
        }
        
        await Promise.all([
          this.fetchProfile(),
          this.fetchRequests()
        ])
      } catch (error) {
        console.error('Dashboard data fetch error:', error)
        this.error = error.message || 'Failed to load dashboard data'
        
        // If token is missing or invalid, redirect to login
        if (error.message.includes('authentication') || error.message.includes('token')) {
          setTimeout(() => this.$router.push('/login'), 1000)
        }
      } finally {
        this.loading = false
      }
    },
    async fetchProfile() {
      try {
        const profileData = await professionalAPI.getProfile();
        this.profile = {
          ...this.profile,
          ...profileData
        };
        
        // Initialize profile form with current values
        this.profileForm.description = profileData.description || '';
        this.profileForm.phone = profileData.phone || '';
        this.profileForm.experience = profileData.experience || 0;
      } catch (error) {
        console.error('Failed to load profile data:', error);
        // Continue with default profile values
      }
    },
    async fetchRequests() {
      try {
        this.loading = true;
        
        // Clear previous data to avoid displaying stale information
        this.serviceRequests = [];
        this.availableCustomerRequests = [];
        
        // Debug auth token
        const token = localStorage.getItem('token');
        console.log('Using token for requests (first 10 chars):', token ? token.substring(0, 10) + '...' : 'No token');
        
        // Get all service requests assigned to this professional
        console.log('Fetching assigned service requests...');
        try {
          const requestsData = await professionalAPI.getAssignments();
          console.log('Assigned requests response:', requestsData);
          
          if (Array.isArray(requestsData)) {
            this.serviceRequests = requestsData.map(request => ({
              ...request,
              // Ensure these fields exist even if backend doesn't provide them
              service: request.service || { name: 'Unknown Service', base_price: 0 },
              customer: request.customer_name || { customer_name: 'Unknown Customer' }
            }));
            console.log(`Loaded ${this.serviceRequests.length} assigned service requests`);
          } else {
            console.error('Invalid response format for assigned requests:', requestsData);
          }
        } catch (assignmentError) {
          console.error('Error fetching assignments:', assignmentError);
          this.error = 'Failed to load your assigned service requests: ' + (assignmentError.message || 'Unknown error');
        }
        
        // Also get available customer requests that aren't assigned yet
        try {
          console.log('Fetching available service requests...');
          const availableRequests = await professionalAPI.getAvailableRequests();
          console.log('Available requests response:', availableRequests);
          
          if (Array.isArray(availableRequests)) {
            this.availableCustomerRequests = availableRequests.map(request => ({
              ...request,
              // Ensure these fields exist even if backend doesn't provide them
              service: request.service || { name: 'Unknown Service', base_price: 0 },
              customer: request.customer || { customer_name: 'Unknown Customer' },
              // Add a flag for UI differentiation
              isNewRequest: true
            }));
            console.log(`Loaded ${this.availableCustomerRequests.length} available customer requests`);
          } else {
            console.error('Invalid response format for available requests:', availableRequests);
          }
        } catch (error) {
          console.error('Failed to load available requests:', error);
          this.availableCustomerRequests = [];
        }
        
        // Sort requests by date (newest first)
        this.serviceRequests.sort((a, b) => {
          const dateA = a.created_at ? new Date(a.created_at) : new Date(0);
          const dateB = b.created_at ? new Date(b.created_at) : new Date(0);
          return dateB - dateA;
        });
        
        // Debug counts after loading
        console.log(`Pending: ${this.pendingRequests.length}, In progress: ${this.inProgressRequests.length}, Completed: ${this.completedRequests.length}`);
      } catch (error) {
        console.error('Failed to load service requests:', error);
        this.error = 'Failed to load service requests. Please try again later.';
      } finally {
        this.loading = false;
        
        // Fetch reviews with error handling
        this.fetchReviews();
      }
    },
    
    // Remove setupSampleData method and replace with resetError
    resetError() {
      this.error = null;
      this.fetchData();
    },
    
    // Add a helper method to check if a request is a new available request vs. already assigned
    isNewCustomerRequest(request) {
      // Check if it comes from availableCustomerRequests array or is flagged as a new request
      return request.isNewRequest || this.availableCustomerRequests.some(r => r.id === request.id);
    },
    
    // Add a fetchReviews method with proper error handling
    async fetchReviews() {
      try {
        console.log('Fetching professional reviews...');
        const reviewsData = await professionalAPI.getReviews();
        
        if (Array.isArray(reviewsData)) {
          this.reviews = reviewsData;
          console.log(`Loaded ${this.reviews.length} reviews`);
        } else {
          console.error('Invalid reviews response format:', reviewsData);
          this.reviews = [];
        }
      } catch (error) {
        console.error('Failed to load reviews:', error);
        this.reviews = []; // Set to empty array on error
      }
    },
    
    async acceptRequest(requestId, closeModal = false) {
      try {
        this.loading = true;
        
        console.log(`Attempting to accept service request ${requestId}`);
        
        // Get the request either from service requests or available requests
        let request = this.serviceRequests.find(r => r.id === requestId);
        if (!request) {
          request = this.availableCustomerRequests.find(r => r.id === requestId);
        }
        
        if (!request) {
          throw new Error('Request not found');
        }
        
        // Check if the request can be accepted
        if (request.status !== 'pending') {
          alert('This request cannot be accepted in its current state.');
          return;
        }
        
        // Accept the request - log the API calls
        console.log(`Calling API to update status of request ${requestId} to in_progress`);
        await professionalAPI.updateStatus(requestId, 'in_progress');
        console.log('Status update API call completed successfully');
        
        // Refresh data
        await this.fetchData();
        
        if (closeModal) {
          this.showDetailsModal = false;
        }
        
        // Show success notification
        alert('Service request accepted successfully. You can find it in the "In Progress" tab.');
      } catch (error) {
        console.error('Error accepting request:', error);
        alert('Failed to accept request: ' + (error.message || 'Unknown error'));
      } finally {
        this.loading = false;
      }
    },
    
    async rejectRequest(requestId, closeModal = false) {
      if (confirm('Are you sure you want to reject this request?')) {
        try {
          this.loading = true;
          
          // Get the request either from service requests or available requests
          let request = this.serviceRequests.find(r => r.id === requestId);
          if (!request) {
            request = this.availableCustomerRequests.find(r => r.id === requestId);
          }
          
          if (!request) {
            throw new Error('Request not found');
          }
          
          // Check if the request can be rejected
          if (request.status !== 'pending' && request.status !== 'available') {
            alert('This request cannot be rejected in its current state.');
            return;
          }
          
          // Get rejection reason first
          const reason = prompt('Please provide a reason for rejection (optional):');
          
          // Reject the request
          await professionalAPI.updateStatus(requestId, 'rejected');
          
          // Add rejection reason if provided
          if (reason && reason.trim()) {
            await professionalAPI.addRejectionReason(requestId, reason);
          }
          
          // Refresh data
          await this.fetchData();
          
          if (closeModal) {
            this.showDetailsModal = false;
          }
          
          alert('Service request has been rejected.');
        } catch (error) {
          console.error('Error rejecting request:', error);
          alert('Failed to reject request: ' + (error.message || 'Unknown error'));
        } finally {
          this.loading = false;
        }
      }
    },

    async completeRequest(requestId, closeModal = false) {
      try {
        this.loading = true;
        
        const request = this.serviceRequests.find(r => r.id === requestId);
        if (!request) {
          throw new Error('Request not found');
        }
        
        // Check if the request is in progress
        if (request.status !== 'in_progress' && request.status !== 'assigned') {
          alert('Only in-progress requests can be marked as completed.');
          return;
        }
        
        let locationExitConfirmed = false;
        
        // Check if location exit is confirmed
        if (closeModal && this.selectedRequest) {
          // Use the modal's exit confirmation checkbox
          if (!this.selectedRequest.exited_location) {
            alert('You must confirm you have exited the customer location before completing the service.');
            this.loading = false;
            return;
          }
          locationExitConfirmed = true;
        } else {
          // If not in modal, ask for confirmation
          if (confirm('Have you exited the customer location? This is required before completing the service.')) {
            locationExitConfirmed = true;
          } else {
            this.loading = false;
            return;
          }
        }
        
        // Confirm location exit first
        if (locationExitConfirmed) {
          await professionalAPI.confirmLocationExit(requestId);
          
          // Now complete the request
          await professionalAPI.updateStatus(requestId, 'completed');
          
          // Refresh data
          await this.fetchData();
          
          if (closeModal) {
            this.showDetailsModal = false;
          }
          
          alert('Service request marked as completed successfully. The customer will be notified to close the service.');
        }
      } catch (error) {
        console.error('Error completing request:', error);
        alert('Failed to complete the request: ' + (error.message || 'Unknown error'));
      } finally {
        this.loading = false;
      }
    },
    
    viewRequestDetails(request) {
      // Add the exited_location property if needed
      this.selectedRequest = {
        ...request,
        exited_location: request.exited_location || false
      };
      this.showDetailsModal = true;
    },

    async updateAvailability() {
      try {
        await professionalAPI.updateAvailability(this.isAvailable);
        alert(`You are now ${this.isAvailable ? 'available' : 'unavailable'} for new service requests.`);
      } catch (error) {
        console.error('Error updating availability:', error);
        // Revert to previous state if there was an error
        this.isAvailable = !this.isAvailable;
      }
    },

    async updateProfile() {
      try {
        this.updatingProfile = true;
        await professionalAPI.updateProfile(this.profileForm);
        
        // Update local profile data
        this.profile.description = this.profileForm.description;
        this.profile.phone = this.profileForm.phone;
        this.profile.experience = this.profileForm.experience;
          
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
      } finally {
        this.updatingProfile = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },

    getStatusBadgeClass(status) {
      const classes = {
        pending: 'badge bg-warning',
        rejected: 'badge bg-danger',
        in_progress: 'badge bg-primary',
        assigned: 'badge bg-info',
        completed: 'badge bg-success',
        closed: 'badge bg-secondary'
      };
      return classes[status] || 'badge bg-secondary';
    },

    getEmptyStateMessage() {
      if (this.activeTab === 'pending') {
        return 'No new service requests available at the moment. Check back later.';
      } else if (this.activeTab === 'assigned') {
        return 'You have no active service assignments.';
      } else {
        return 'You have not completed any service requests yet.';
      }
    },

    // Add a specific method for refreshing requests
    async refreshRequests() {
      try {
        console.log("Manually refreshing requests...");
        this.loading = true;
        
        // First check the professional's profile and service type
        const profileData = await professionalAPI.getProfile();
        console.log("Professional profile:", profileData);
        
        // Then fetch customer requests
        await this.fetchRequests();
        
        console.log("Refresh completed");
      } catch (error) {
        console.error("Error refreshing requests:", error);
        this.error = `Error refreshing: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    // Method to see ALL pending requests in the system
    async refreshAllPendingRequests() {
      try {
        this.loading = true;
        console.log("Fetching ALL pending requests (debug mode)");
        
        const result = await professionalAPI.getAllPendingRequests();
        this.debugAllPendingRequests = result;
        
        console.log("All pending requests:", this.debugAllPendingRequests);
      } catch (error) {
        console.error("Error fetching all pending requests:", error);
        this.error = `Error: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    // Method to force-accept a request even if it doesn't match service type
    async forceAcceptRequest(requestId) {
      if (confirm(`Are you sure you want to accept request #${requestId}?`)) {
        try {
          this.loading = true;
          
          console.log(`Force-accepting request ${requestId}...`);
          await professionalAPI.updateStatus(requestId, 'in_progress');
          
          alert(`Request #${requestId} accepted successfully!`);
          
          // Refresh both regular requests and debug data
          await this.fetchRequests();
          await this.refreshAllPendingRequests();
        } catch (error) {
          console.error("Error force-accepting request:", error);
          alert(`Error: ${error.message}`);
        } finally {
          this.loading = false;
        }
      }
    },
  },
  mounted() {
    // Don't call fetchData here since we're doing it in created/checkAuth
  }
};
</script>

<style scoped>
.professional-dashboard {
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

.nav-tabs .nav-link {
  cursor: pointer;
  padding: 0.75rem 1rem;
}

.badge {
  padding: 0.5em 0.8em;
  font-weight: 500;
}

.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}

.rating {
  display: inline-block;
}

.rating .fas {
  color: #e0e0e0;
}

.rating .fas.text-warning {
  color: #ffc107;
}

.timeline {
  list-style: none;
  padding-left: 0;
}

.timeline li {
  position: relative;
  padding-left: 1.5rem;
}

.timeline li:before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.5rem;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: #0d6efd;
}

.avatar-container {
  width: 150px;
  height: 150px;
  margin: 0 auto;
}

.avatar-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.form-check-input[type="checkbox"] {
  width: 1.25em;
  height: 1.25em;
}

.list-group-item {
  border-left: none;
  border-right: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .stats-cards {
    margin-top: 1.5rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
}

/* Add new styles */
.alert {
  border-radius: 0.5rem;
}

.alert-info {
  background-color: rgba(13, 202, 240, 0.1);
  border-color: rgba(13, 202, 240, 0.2);
  color: #055160;
}

.alert-warning {
  background-color: rgba(255, 193, 7, 0.1);
  border-color: rgba(255, 193, 7, 0.2);
  color: #664d03;
}

.alert-success {
  background-color: rgba(25, 135, 84, 0.1);
  border-color: rgba(25, 135, 84, 0.2);
  color: #0f5132;
}

/* Animation for new items */
@keyframes highlight {
  0% { background-color: rgba(25, 135, 84, 0.2); }
  100% { background-color: transparent; }
}

.highlight-new {
  animation: highlight 2s ease-out;
}

.customer-avatar img {
  object-fit: cover;
  border: 2px solid #fff;
}

/* Add styling for new customer request badges */
.badge.bg-info {
  background-color: #0dcaf0 !important;
  color: #fff;
  font-weight: 500;
  padding: 0.4em 0.7em;
  margin-bottom: 8px;
  display: inline-block;
}
</style>
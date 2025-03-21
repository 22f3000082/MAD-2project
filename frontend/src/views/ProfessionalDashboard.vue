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
                <span>{{ profile.average_rating }} / 5 ({{ profile.total_reviews }} reviews)</span>
              </div>
              <p class="mb-1"><strong>Service:</strong> {{ profile.service_type }}</p>
              <p class="mb-1"><strong>Experience:</strong> {{ profile.experience }} years</p>
              <p class="mb-0"><strong>Status:</strong> 
                <span class="badge" :class="profile.is_approved ? 'bg-success' : 'bg-warning'">
                  {{ profile.is_approved ? 'Approved' : 'Pending Approval' }}
                </span>
              </p>
            </div>
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
      </ul>

      <!-- Loading State -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading service requests...</p>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="filteredRequests.length === 0" class="text-center py-5">
        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
        <h5>No service requests found</h5>
        <p class="text-muted">{{ getEmptyStateMessage() }}</p>
      </div>
      
      <!-- Service Requests List -->
      <div v-else class="row g-4">
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
              <div class="mb-3">
                <strong>Instructions:</strong>
                <p class="mb-0">{{ request.special_instructions || 'No special instructions' }}</p>
              </div>
              
              <div class="d-flex justify-content-end gap-2">
                <!-- Actions for pending requests -->
                <template v-if="request.status === 'pending'">
                  <button @click="acceptRequest(request.id)" class="btn btn-success btn-sm">
                    <i class="fas fa-check me-1"></i> Accept
                  </button>
                  <button @click="rejectRequest(request.id)" class="btn btn-danger btn-sm">
                    <i class="fas fa-times me-1"></i> Reject
                  </button>
                </template>
                
                <!-- Actions for in-progress requests -->
                <button v-if="request.status === 'in_progress'" @click="completeRequest(request.id)" class="btn btn-primary btn-sm">
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
                    class="btn btn-primary">
              <i class="fas fa-check-circle me-1"></i> Mark as Completed
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { professionalAPI } from '@/services/api';

export default {
  name: 'ProfessionalDashboard',
  setup() {
    // State
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const professionalName = ref(user.name || 'Professional');
    const activeTab = ref('pending');
    const loading = ref(true);
    const serviceRequests = ref([]);
    const profile = ref({
      service_type: '',
      experience: 0,
      average_rating: 0,
      total_reviews: 0,
      is_approved: false
    });
    const showDetailsModal = ref(false);
    const selectedRequest = ref(null);

    // Computed properties
    const pendingRequests = computed(() => 
      serviceRequests.value.filter(req => req.status === 'pending')
    );
    
    const inProgressRequests = computed(() => 
      serviceRequests.value.filter(req => req.status === 'in_progress' || req.status === 'assigned')
    );
    
    const completedRequests = computed(() => 
      serviceRequests.value.filter(req => req.status === 'completed' || req.status === 'closed')
    );
    
    const filteredRequests = computed(() => {
      if (activeTab.value === 'pending') {
        return pendingRequests.value;
      } else if (activeTab.value === 'assigned') {
        return inProgressRequests.value;
      } else if (activeTab.value === 'completed') {
        return completedRequests.value;
      }
      return [];
    });

    // Methods
    const fetchData = async () => {
      loading.value = true;
      try {
        const [requestsData, profileData] = await Promise.all([
          professionalAPI.getAssignments(),
          professionalAPI.getProfile()
        ]);
        serviceRequests.value = requestsData;
        profile.value = profileData;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        loading.value = false;
      }
    };

    const acceptRequest = async (requestId, closeModal = false) => {
      try {
        await professionalAPI.updateStatus(requestId, 'in_progress');
        await fetchData();
        if (closeModal) {
          showDetailsModal.value = false;
        }
      } catch (error) {
        console.error('Error accepting request:', error);
      }
    };

    const rejectRequest = async (requestId, closeModal = false) => {
      if (confirm('Are you sure you want to reject this request?')) {
        try {
          await professionalAPI.updateStatus(requestId, 'rejected');
          await fetchData();
          if (closeModal) {
            showDetailsModal.value = false;
          }
        } catch (error) {
          console.error('Error rejecting request:', error);
        }
      }
    };

    const completeRequest = async (requestId, closeModal = false) => {
      try {
        await professionalAPI.updateStatus(requestId, 'completed');
        await fetchData();
        if (closeModal) {
          showDetailsModal.value = false;
        }
      } catch (error) {
        console.error('Error completing request:', error);
      }
    };

    const viewRequestDetails = (request) => {
      selectedRequest.value = request;
      showDetailsModal.value = true;
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const getStatusBadgeClass = (status) => {
      const classes = {
        pending: 'badge bg-warning',
        rejected: 'badge bg-danger',
        in_progress: 'badge bg-primary',
        assigned: 'badge bg-info',
        completed: 'badge bg-success',
        closed: 'badge bg-secondary'
      };
      return classes[status] || 'badge bg-secondary';
    };

    const getEmptyStateMessage = () => {
      if (activeTab.value === 'pending') {
        return 'No new service requests available at the moment. Check back later.';
      } else if (activeTab.value === 'assigned') {
        return 'You have no active service assignments.';
      } else {
        return 'You have not completed any service requests yet.';
      }
    };

    // Lifecycle hooks
    onMounted(fetchData);

    return {
      professionalName,
      activeTab,
      loading,
      serviceRequests,
      profile,
      pendingRequests,
      inProgressRequests,
      completedRequests,
      filteredRequests,
      showDetailsModal,
      selectedRequest,
      acceptRequest,
      rejectRequest,
      completeRequest,
      viewRequestDetails,
      formatDate,
      getStatusBadgeClass,
      getEmptyStateMessage
    };
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .stats-cards {
    margin-top: 1.5rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
}
</style>

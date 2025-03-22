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
        <!-- Enhanced Service Search using the new component -->
        <ServiceSearchPanel 
          :initialParams="searchQuery" 
          @search="handleSearch"
        />

        <!-- Service List using the new component -->
        <ServiceList
          :services="filteredServices"
          :loading="loading"
          :hasMore="hasMoreServices"
          @view-details="selectService"
          @request-service="directRequestService"
          @load-more="loadMoreServices"
        />
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
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-2">Loading your requests...</p>
        </div>
        
        <div v-else-if="filteredRequests.length === 0" class="text-center py-5">
          <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
          <h5>No service requests found</h5>
          <p class="text-muted">{{ activeTab === 'active' ? 'Create a new request to get started!' : 'No completed requests yet.' }}</p>
        </div>
        
        <div v-else class="row g-4">
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
                    Cancel
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
                <label for="serviceType" class="form-label">Service Type</label>
                <select id="serviceType" name="serviceType" class="form-select" v-model="newRequest.service_id" required>
                  <option value="">Select a service</option>
                  <option v-for="service in services" :key="service.id" :value="service.id">
                    {{ service.name }} - ₹{{ service.base_price }}
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
          <ServiceRequestDetail
            :request="selectedRequest"
            @close="showRequestDetailsModal = false"
            @updated="handleRequestUpdated"
            @review="addReview"
            @cancel="closeRequest"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { customerAPI, serviceAPI } from '@/services/api'
import ServiceSearchPanel from '@/components/ServiceSearchPanel.vue'
import ServiceList from '@/components/ServiceList.vue'
import ServiceReviewForm from '@/components/ServiceReviewForm.vue'
import ServiceRequestDetail from '@/components/ServiceRequestDetail.vue'

export default {
  name: 'CustomerDashboard',
  components: {
    ServiceSearchPanel,
    ServiceList,
    ServiceReviewForm,
    ServiceRequestDetail
  },
  data() {
    return {
      userName: JSON.parse(localStorage.getItem('user'))?.name || 'Customer',
      activeSection: 'browse', // 'browse' or 'requests'
      activeTab: 'active', // For requests: 'active' or 'completed'
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
      showServiceModal: false,
      showRequestDetailsModal: false,
      isLoading: false,
      loading: false, // General loading state
      newRequest: {
        service_id: '',
        pin_code: '',
        special_instructions: ''
      },
      review: {
        rating: 0,
        remarks: ''
      },
      selectedRequest: null,
      selectedService: null,
      error: null,
      hasMoreServices: false,
      page: 1,
      limit: 9
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
        console.log('CustomerDashboard: Fetching services...');
        const response = await serviceAPI.getServices();
        console.log(`CustomerDashboard: Received ${response.length} services`);
        this.services = response;
        this.loading = false;
      } catch (error) {
        console.error('CustomerDashboard: Error fetching services:', error);
        this.error = 'Failed to load services. Please try again.';
        this.loading = false;
        
        // Retry after a delay in case of network issues
        setTimeout(() => {
          if (this.services.length === 0) {
            console.log('Retrying service fetch...');
            this.fetchServices();
          }
        }, 3000);
      }
    },
    async fetchServiceTypes() {
      try {
        console.log('CustomerDashboard: Fetching service types...');
        const response = await serviceAPI.getServiceTypes();
        console.log(`CustomerDashboard: Received ${response.length} service types`);
        this.categories = response;
      } catch (error) {
        console.error('CustomerDashboard: Error fetching service types:', error);
        this.error = 'Failed to load service categories. Please try again.';
      }
    },
    async fetchRequests() {
      try {
        this.loading = true;
        const response = await customerAPI.getRequests();
        this.serviceRequests = response;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching requests:', error);
        this.error = 'Failed to load service requests. Please try again.';
        this.loading = false;
      }
    },
    async searchServices() {
      // You can implement additional search logic here if needed
      // For now, we'll just use the computed filteredServices property
    },
    async createRequest() {
      this.isLoading = true;
      try {
        await customerAPI.createRequest(this.newRequest);
        this.showNewRequestModal = false;
        this.newRequest = { service_id: '', pin_code: '', special_instructions: '' };
        this.activeSection = 'requests'; // Switch to requests tab
        await this.fetchRequests();
        alert('Service request created successfully!');
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
        special_instructions: request.special_instructions || ''
      };
      this.showNewRequestModal = true;
    },
    addReview(request) {
      this.selectedRequest = request;
      this.review = { rating: 0, remarks: '' };
      this.showReviewModal = true;
      if (this.showRequestDetailsModal) {
        this.showRequestDetailsModal = false;
      }
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
    
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
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
    // Enhanced search method using the new search panel
    handleSearch(params) {
      this.searchQuery = { ...params };
      this.page = 1;
      this.fetchServices();
    },
    
    // Method to directly request a service from the service list
    directRequestService(service) {
      this.selectedService = service;
      this.showNewRequestModal = true;
      
      // Pre-populate the request form with the selected service
      this.newRequest.service_id = service.id;
    },
    
    // Load more services for pagination
    loadMoreServices() {
      this.page += 1;
      this.fetchMoreServices();
    },
    
    // Fetch additional services for pagination
    // async fetchMoreServices() {
    //   try {
    //     const response = await serviceAPI.getServices({
    //       ...this.searchQuery,
    //       page: this.page,
    //       limit: this.limit
    //     });
        
    //     if (response.length > 0) {
    //       this.services = [...this.services, ...response];
    //       this.hasMoreServices = response.length === this.limit;
    //     } else {
    //       this.hasMoreServices = false;
    //     }
    //   } catch (error) {
    //     console.error('Error fetching more services:', error);
    //   }
    // },
    
    // Handle review submission
    handleReviewSubmitted() {
      this.showReviewModal = false;
      this.fetchRequests();
      alert('Thank you for your review!');
    },
    
    // Handle request updated
    handleRequestUpdated() {
      this.fetchRequests();
    }
  },
  async created() {
    await Promise.all([
      this.fetchServices(),
      this.fetchServiceTypes(),
      this.fetchRequests()
    ]);
  }
}
</script>
<!--  -->
Add styling as needed
<!-- <style scoped> -->
/* .customer-dashboard { */
  /* background-color: #f8f9fa; */
  /* min-height: 100vh; */
/* } */
/*  */
/* .service-card { */
  /* transition: transform 0.2s, box-shadow 0.2s; */
/* } */
/*  */
/* .service-card:hover { */
        /* this.showNewRequestModal = false; */
        /* this.newRequest = { service_id: '', pin_code: '', special_instructions: '' }; */
        /* this.activeSection = 'requests'; // Switch to requests tab */
        /* await this.fetchRequests(); */
        /* alert('Service request created successfully!'); */
      /* } catch (error) { */
        /* console.error('Error creating request:', error); */
        /* alert('Failed to create service request: ' + (error.message || 'Unknown error')); */
      /* } finally { */
        /* this.isLoading = false; */
      /* } */
    /* }, */
    /* async closeRequest(request, fromModal = false) { */
      /* if (confirm('Are you sure you want to cancel this request?')) { */
        /* try { */
          /* this.isLoading = true; */
          /* await customerAPI.closeRequest(request.id); */
          /* await this.fetchRequests(); */
          /* if (fromModal) { */
            /* this.showRequestDetailsModal = false; */
          /* } */
          /* alert('Request cancelled successfully.'); */
        /* } catch (error) { */
          /* console.error('Error closing request:', error); */
          /* alert('Failed to cancel request: ' + (error.message || 'Unknown error')); */
        /* } finally { */
          /* this.isLoading = false; */
        /* } */
      /* } */
    /* }, */
    /* editRequest(request) { */
      /* // Implement edit functionality (e.g., populate form with current values) */
      /* this.newRequest = { */
        /* service_id: request.service_id, */
        /* pin_code: request.pin_code, */
        /* special_instructions: request.special_instructions || '' */
      /* }; */
      /* this.showNewRequestModal = true; */
    /* }, */
    /* addReview(request) { */
      /* this.selectedRequest = request; */
      /* this.review = { rating: 0, remarks: '' }; */
      /* this.showReviewModal = true; */
      /* if (this.showRequestDetailsModal) { */
        /* this.showRequestDetailsModal = false; */
      /* } */
    /* }, */
    /* async submitReview() { */
      /* try { */
        /* this.isLoading = true; */
        /* await customerAPI.addReview(this.selectedRequest.id, this.review); */
        /* this.showReviewModal = false; */
        /* this.review = { rating: 0, remarks: '' }; */
        /* await this.fetchRequests(); */
        /* alert('Review submitted successfully.'); */
      /* } catch (error) { */
        /* console.error('Error submitting review:', error); */
        /* alert('Failed to submit review: ' + (error.message || 'Unknown error')); */
      /* } finally { */
        /* this.isLoading = false; */
      /* } */
    /* }, */
    /*  */
    /* selectService(service) { */
      /* this.selectedService = service; */
      /* this.showServiceModal = true; */
    /* }, */
    /*  */
    /* requestSelectedService() { */
      /* this.newRequest.service_id = this.selectedService.id; */
      /* this.showServiceModal = false; */
      /* this.showNewRequestModal = true; */
    /* }, */
    /*  */
    /* viewRequestDetails(request) { */
      /* this.selectedRequest = request; */
      /* this.showRequestDetailsModal = true; */
    /* }, */
    /*  */
    /* formatDate(dateString) { */
      /* if (!dateString) return 'N/A'; */
      /* const date = new Date(dateString); */
      /* return date.toLocaleString('en-US', { */
        /* year: 'numeric', */
        /* month: 'short', */
        /* day: 'numeric', */
        /* hour: '2-digit', */
        /* minute: '2-digit' */
      /* }); */
    /* }, */
    /*  */
    /* getStatusBadgeClass(status) { */
      /* const classes = { */
        /* pending: 'badge bg-warning', */
        /* assigned: 'badge bg-info', */
        /* in_progress: 'badge bg-primary', */
        /* completed: 'badge bg-success', */
        /* closed: 'badge bg-secondary', */
        /* cancelled: 'badge bg-danger' */
      /* }; */
      /* return classes[status] || 'badge bg-secondary'; */
    /* } */
  /* }, */
  /* async created() { */
    /* await Promise.all([ */
      /* this.fetchServices(), */
      /* this.fetchServiceTypes(), */
      /* this.fetchRequests() */
    /* ]); */
  /* } */
/* } */
/* 
<!-- </script>  -->

<!-- Add styling as needed -->
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

.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.timeline-marker {
  position: absolute;
  left: -30px;
  top: 5px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
}

.timeline:before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: -23px;
  width: 2px;
  background-color: #e9ecef;
}
</style>
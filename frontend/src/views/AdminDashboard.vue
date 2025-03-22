<template>
  <div class="admin-dashboard">
    <!-- Top Stats Cards -->
    <div class="container-fluid py-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading dashboard data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger">
        <i class="fas fa-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-outline-danger btn-sm ms-3" @click="loadDashboardData">
          <i class="fas fa-sync-alt"></i> Retry
        </button>
      </div>

      <div v-else>
        <div class="row g-4 mb-4">
          <div class="col-xl-3 col-sm-6">
            <div class="card bg-primary text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title mb-0">Total Users</h6>
                    <h2 class="mt-2 mb-0">{{ stats.totalUsers }}</h2>
                  </div>
                  <div class="icon-shape bg-white text-primary rounded-circle">
                    <i class="fas fa-users fa-2x"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-3 col-sm-6">
            <div class="card bg-success text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title mb-0">Active Services</h6>
                    <h2 class="mt-2 mb-0">{{ stats.activeServices }}</h2>
                  </div>
                  <div class="icon-shape bg-white text-success rounded-circle">
                    <i class="fas fa-tools fa-2x"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-3 col-sm-6">
            <div class="card bg-warning text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title mb-0">Pending Approvals</h6>
                    <h2 class="mt-2 mb-0">{{ stats.pendingApprovals }}</h2>
                  </div>
                  <div class="icon-shape bg-white text-warning rounded-circle">
                    <i class="fas fa-clock fa-2x"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-3 col-sm-6">
            <div class="card bg-danger text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title mb-0">Blocked Users</h6>
                    <h2 class="mt-2 mb-0">{{ stats.blockedUsers }}</h2>
                  </div>
                  <div class="icon-shape bg-white text-danger rounded-circle">
                    <i class="fas fa-ban fa-2x"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content Tabs -->
        <div class="card">
          <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
              <li class="nav-item" v-for="tab in tabs" :key="tab.id">
                <a class="nav-link" :class="{ active: currentTab === tab.id }" 
                   @click="currentTab = tab.id" href="#">
                  <i :class="tab.icon"></i> {{ tab.name }}
                </a>
              </li>
            </ul>
          </div>
          <div class="card-body">
            <!-- Users Management Tab -->
            <div v-if="currentTab === 'users'" class="users-management">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="d-flex gap-2">
                  <input id="userSearchInput" name="userSearch" v-model="userSearch" type="text" class="form-control" 
                         placeholder="Search users...">
                  <select id="userTypeFilter" name="userTypeFilter" v-model="userTypeFilter" class="form-select">
                    <option value="">All Users</option>
                    <option value="professional">Professionals</option>
                    <option value="customer">Customers</option>
                    <option value="pending">Pending Approval</option>
                  </select>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-outline-primary" @click="refreshUsers">
                    <i class="fas fa-sync-alt"></i> Refresh
                  </button>
                </div>
              </div>

              <div v-if="pendingApprovals.length > 0" class="alert alert-warning mb-4">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>{{ pendingApprovals.length }} professional{{ pendingApprovals.length > 1 ? 's' : '' }}</strong> pending approval
              </div>

              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in filteredUsers" :key="user.id" 
                        :class="{'table-warning': user.role === 'professional' && !user.is_approved}">
                      <td>{{ user.id }}</td>
                      <td>{{ user.name }}</td>
                      <td>{{ user.email }}</td>
                      <td>
                        <span class="badge" 
                              :class="user.role === 'professional' ? 'bg-info' : 'bg-secondary'">
                          {{ user.role }}
                        </span>
                      </td>
                      <td>
                        <span v-if="user.role === 'professional' && !user.is_approved" 
                              class="badge bg-warning">Pending Approval</span>
                        <span v-else class="badge" 
                              :class="user.is_blocked ? 'bg-danger' : 'bg-success'">
                          {{ user.is_blocked ? 'Blocked' : 'Active' }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group">
                          <button v-if="user.role === 'professional' && !user.is_approved"
                                  class="btn btn-sm btn-success" 
                                  @click="approveUser(user.id)">
                            <i class="fas fa-check"></i> Approve
                          </button>
                          <button class="btn btn-sm" 
                                  :class="user.is_blocked ? 'btn-success' : 'btn-danger'"
                                  @click="toggleUserBlock(user)">
                            <i class="fas" :class="user.is_blocked ? 'fa-unlock' : 'fa-ban'"></i>
                            {{ user.is_blocked ? 'Unblock' : 'Block' }}
                          </button>
                          <button class="btn btn-sm btn-info" @click="viewUserDetails(user)">
                            <i class="fas fa-eye"></i> View
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Services Management Tab -->
            <div v-if="currentTab === 'services'" class="services-management">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="d-flex gap-2">
                  <input id="serviceSearchInput" name="serviceSearch" v-model="serviceSearch" type="text" class="form-control" 
                         placeholder="Search services...">
                </div>
                <button class="btn btn-primary" @click="showNewServiceModal">
                  <i class="fas fa-plus"></i> New Service
                </button>
              </div>

              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Base Price</th>
                      <th>Time Required</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="service in filteredServices" :key="service.id">
                      <td>{{ service.id }}</td>
                      <td>{{ service.name }}</td>
                      <td>₹{{ service.basePrice }}</td>
                      <td>{{ service.timeRequired }}</td>
                      <td>
                        <span class="badge" 
                              :class="service.status === 'active' ? 'bg-success' : 'bg-danger'">
                          {{ service.status }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group">
                          <button class="btn btn-sm btn-warning" @click="editService(service)">
                            <i class="fas fa-edit"></i> Edit
                          </button>
                          <button class="btn btn-sm btn-danger" @click="deleteService(service.id)">
                            <i class="fas fa-trash"></i> Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Analytics Tab -->
            <div v-if="currentTab === 'analytics'" class="analytics">
              <div class="row">
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-body">
                      <h5 class="card-title">Service Requests by Status</h5>
                      <canvas ref="requestsChart"></canvas>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-body">
                      <h5 class="card-title">User Registration Trend</h5>
                      <canvas ref="usersChart"></canvas>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- New/Edit Service Modal -->
    <div class="modal fade" id="serviceModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingService ? 'Edit' : 'New' }} Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveService">
              <div class="mb-3">
                <label for="serviceName" class="form-label">Service Name</label>
                <input id="serviceName" name="serviceName" v-model="serviceForm.name" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label for="serviceDescription" class="form-label">Description</label>
                <textarea id="serviceDescription" name="serviceDescription" v-model="serviceForm.description" class="form-control" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label for="serviceBasePrice" class="form-label">Base Price (₹)</label>
                <input id="serviceBasePrice" name="serviceBasePrice" v-model="serviceForm.basePrice" type="number" class="form-control" required>
              </div>
              <div class="mb-3">
                <label for="serviceTimeRequired" class="form-label">Time Required (hours)</label>
                <input id="serviceTimeRequired" name="serviceTimeRequired" v-model="serviceForm.timeRequired" type="number" class="form-control" required>
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div class="modal fade" id="userDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">User Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <div class="row">
              <div class="col-md-6">
                <h6>Basic Information</h6>
                <table class="table">
                  <tr>
                    <th>Name:</th>
                    <td>{{ selectedUser.name }}</td>
                  </tr>
                  <tr>
                    <th>Email:</th>
                    <td>{{ selectedUser.email }}</td>
                  </tr>
                  <tr>
                    <th>Role:</th>
                    <td>{{ selectedUser.role }}</td>
                  </tr>
                  <tr>
                    <th>Status:</th>
                    <td>{{ selectedUser.status }}</td>
                  </tr>
                </table>
              </div>
              <div class="col-md-6" v-if="selectedUser.role === 'professional'">
                <h6>Professional Details</h6>
                <table class="table">
                  <tr>
                    <th>Service Type:</th>
                    <td>{{ selectedUser.serviceType }}</td>
                  </tr>
                  <tr>
                    <th>Experience:</th>
                    <td>{{ selectedUser.experience }} years</td>
                  </tr>
                  <tr>
                    <th>Rating:</th>
                    <td>
                      <div class="stars">
                        <i v-for="n in 5" :key="n"
                           class="fas fa-star"
                           :class="n <= selectedUser.rating ? 'text-warning' : 'text-muted'"></i>
                        ({{ selectedUser.rating }}/5)
                      </div>
                    </td>
                  </tr>
                </table>
              </div>
            </div>
            <div class="mt-4" v-if="selectedUser.role === 'professional'">
              <h6>Recent Reviews</h6>
              <div class="reviews-list">
                <div v-for="review in selectedUser.reviews" :key="review.id" class="review-item">
                  <div class="stars mb-1">
                    <i v-for="n in 5" :key="n"
                       class="fas fa-star"
                       :class="n <= review.rating ? 'text-warning' : 'text-muted'"></i>
                  </div>
                  <p class="mb-1">{{ review.comment }}</p>
                  <small class="text-muted">{{ review.date }}</small>
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
import { ref, onMounted, computed } from 'vue'
import { Modal } from 'bootstrap'
import Chart from 'chart.js/auto'
import { adminAPI } from '@/services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    // State
    const stats = ref({
      totalUsers: 0,
      activeServices: 0,
      pendingApprovals: 0,
      blockedUsers: 0
    })
    const users = ref([])
    const services = ref([])
    const currentTab = ref('users')
    const userSearch = ref('')
    const serviceSearch = ref('')
    const userTypeFilter = ref('')
    const serviceForm = ref({
      name: '',
      description: '',
      basePrice: '',
      timeRequired: ''
    })
    const editingService = ref(null)
    const selectedUser = ref(null)
    const requestsChart = ref(null)
    const usersChart = ref(null)
    const loading = ref(false)
    const error = ref(null)

    // Tabs configuration
    const tabs = [
      { id: 'users', name: 'Users Management', icon: 'fas fa-users' },
      { id: 'services', name: 'Services', icon: 'fas fa-tools' },
      { id: 'analytics', name: 'Analytics', icon: 'fas fa-chart-bar' }
    ]

    // Computed properties
    const pendingApprovals = computed(() => 
      users.value.filter(user => user.role === 'professional' && !user.is_approved)
    );

    const filteredUsers = computed(() => {
      return users.value.filter(user => {
        const matchesSearch = (user.name || '').toLowerCase().includes(userSearch.value.toLowerCase()) ||
                             (user.email || '').toLowerCase().includes(userSearch.value.toLowerCase());
        
        if (userTypeFilter.value === 'pending') {
          return matchesSearch && user.role === 'professional' && !user.is_approved;
        } else {
          const matchesType = !userTypeFilter.value || user.role === userTypeFilter.value;
          return matchesSearch && matchesType;
        }
      });
    });

    const filteredServices = computed(() => {
      return services.value.filter(service =>
        service.name.toLowerCase().includes(serviceSearch.value.toLowerCase())
      )
    })

    // Methods
    const loadDashboardData = async () => {
      loading.value = true;
      error.value = null;
      try {
        console.log('Loading dashboard data...');
        // Debug token information
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No authentication token found. Please login again.');
        }
        console.log(`Token exists: ${token.substring(0, 10)}...`);
        
        // Load users data first - if this fails, we know authentication is an issue
        const usersData = await adminAPI.getUsers();
        console.log(`Loaded ${usersData.length} users successfully`);
        users.value = usersData;

        try {
          // Now try to load services
          const servicesData = await adminAPI.getServices();
          console.log(`Loaded ${servicesData.length} services successfully`);
          services.value = servicesData;
        } catch (servicesError) {
          console.error('Error loading services:', servicesError);
          // Don't fail completely, just show users without services
          services.value = [];
        }

        // Update dashboard stats
        updateStats();
        loading.value = false;
      } catch (err) {
        console.error('Error loading dashboard data:', err);
        error.value = err.message || 'Failed to load dashboard data. Please try again.';
        loading.value = false;
      }
    };

    const updateStats = () => {
      stats.value = {
        totalUsers: users.value.length,
        activeServices: services.value.filter(s => s.is_active !== false).length,
        pendingApprovals: pendingApprovals.value.length,
        blockedUsers: users.value.filter(u => u.is_blocked).length
      }
    }

    const showNewServiceModal = () => {
      editingService.value = null
      serviceForm.value = {
        name: '',
        description: '',
        basePrice: '',
        timeRequired: ''
      }
      new Modal(document.getElementById('serviceModal')).show()
    }

    const editService = (service) => {
      editingService.value = service
      serviceForm.value = { ...service }
      new Modal(document.getElementById('serviceModal')).show()
    }

    const saveService = async () => {
      try {
        if (editingService.value) {
          await adminAPI.updateService(editingService.value.id, serviceForm.value)
        } else {
          await adminAPI.createService(serviceForm.value)
        }
        await loadDashboardData()
        new Modal(document.getElementById('serviceModal')).hide()
      } catch (error) {
        console.error('Error saving service:', error)
      }
    }

    const deleteService = async (serviceId) => {
      if (confirm('Are you sure you want to delete this service?')) {
        try {
          await adminAPI.deleteService(serviceId)
          await loadDashboardData()
        } catch (error) {
          console.error('Error deleting service:', error)
        }
      }
    }

    const approveUser = async (userId) => {
      try {
        if (confirm('Are you sure you want to approve this professional?')) {
          await adminAPI.approveUser(userId);
          alert('Professional approved successfully');
          await loadDashboardData();
        }
      } catch (error) {
        console.error('Error approving user:', error);
        alert('Failed to approve professional: ' + (error.message || 'Unknown error'));
      }
    };

    const toggleUserBlock = async (user) => {
      try {
        if (user.is_blocked) {
          // Unblock user
          if (confirm('Are you sure you want to unblock this user?')) {
            await adminAPI.unblockUser(user.id);
            alert('User unblocked successfully');
          }
        } else {
          // Block user with reason
          const reason = prompt('Please enter a reason for blocking this user:', 'Violation of terms of service');
          if (reason) {
            await adminAPI.blockUser(user.id, reason);
            alert('User blocked successfully');
          }
        }
        await loadDashboardData();
      } catch (error) {
        console.error('Error toggling user block status:', error);
        alert('Operation failed: ' + error.message);
      }
    };

    const viewUserDetails = (user) => {
      selectedUser.value = user
      new Modal(document.getElementById('userDetailsModal')).show()
    }

    const initCharts = () => {
      // Requests Chart
      const requestsCtx = document.querySelector('#requestsChart')
      if (requestsCtx) {
        requestsChart.value = new Chart(requestsCtx, {
          type: 'bar',
          data: {
            labels: ['Pending', 'In Progress', 'Completed', 'Cancelled'],
            datasets: [{
              label: 'Service Requests',
              data: [12, 19, 3, 5],
              backgroundColor: [
                'rgba(255, 206, 86, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)'
              ],
              borderColor: [
                'rgba(255, 206, 86, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)'
              ],
              borderWidth: 1
            }]
          }
        })
      }

      // Users Chart
      const usersCtx = document.querySelector('#usersChart')
      if (usersCtx) {
        usersChart.value = new Chart(usersCtx, {
          type: 'line',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
              label: 'New Users',
              data: [65, 59, 80, 81, 56, 55],
              fill: false,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            }]
          }
        })
      }
    }

    const refreshUsers = async () => {
      loading.value = true;
      error.value = null;
      try {
        const userData = await adminAPI.getUsers();
        users.value = userData;
        updateStats();
      } catch (error) {
        console.error('Error refreshing users:', error);
        error.value = error.message || 'Failed to refresh users';
      } finally {
        loading.value = false;
      }
    };

    // Lifecycle hooks
    onMounted(() => {
      console.log('AdminDashboard mounted - loading data...');
      loadDashboardData();
      // Initialize charts after a delay to ensure DOM is ready
      setTimeout(() => {
        initCharts();
      }, 1000);
    });

    return {
      stats,
      users,
      services,
      currentTab,
      tabs,
      userSearch,
      serviceSearch,
      userTypeFilter,
      serviceForm,
      editingService,
      selectedUser,
      filteredUsers,
      filteredServices,
      pendingApprovals,
      loading,
      error,
      showNewServiceModal,
      editService,
      saveService,
      deleteService,
      approveUser,
      toggleUserBlock,
      viewUserDetails,
      refreshUsers,
      loadDashboardData
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.icon-shape {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 1.5rem;
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.table th {
  font-weight: 600;
  background-color: #f8f9fa;
}

.reviews-list {
  max-height: 300px;
  overflow-y: auto;
}

.review-item {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.review-item:last-child {
  border-bottom: none;
}

.stars {
  color: #ffc107;
}

.btn-group {
  gap: 0.25rem;
}

.modal-body {
  max-height: 80vh;
  overflow-y: auto;
}

.table-warning {
  background-color: rgba(255, 193, 7, 0.1);
}

.alert-warning {
  border-left: 4px solid #ffc107;
}
</style>

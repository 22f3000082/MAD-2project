<template>
  <div class="container mt-4">
    <h2>Admin Dashboard</h2>
    
    <!-- Users Management -->
    <div class="card mb-4">
      <div class="card-header">
        <h3>Users Management</h3>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td>
                  <span :class="user.is_blocked ? 'text-danger' : 'text-success'">
                    {{ user.is_blocked ? 'Blocked' : 'Active' }}
                  </span>
                </td>
                <td>
                  <button 
                    class="btn btn-sm"
                    :class="user.is_blocked ? 'btn-success' : 'btn-danger'"
                    @click="toggleBlockUser(user.id)"
                  >
                    {{ user.is_blocked ? 'Unblock' : 'Block' }}
                  </button>
                  <button 
                    v-if="user.role === 'professional' && !user.is_approved"
                    class="btn btn-sm btn-primary ms-2"
                    @click="approveProfessional(user.id)"
                  >
                    Approve
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Services Management -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h3>Services Management</h3>
        <button class="btn btn-primary" @click="showAddServiceModal">
          Add New Service
        </button>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Base Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="service in services" :key="service.id">
                <td>{{ service.name }}</td>
                <td>${{ service.base_price }}</td>
                <td>
                  <button class="btn btn-sm btn-warning me-2" @click="editService(service)">
                    Edit
                  </button>
                  <button class="btn btn-sm btn-danger" @click="deleteService(service.id)">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Service Modal -->
    <div class="modal fade" id="serviceModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingService ? 'Edit' : 'Add' }} Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveService">
              <div class="mb-3">
                <label class="form-label">Service Name</label>
                <input v-model="serviceForm.name" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Base Price</label>
                <input v-model="serviceForm.base_price" type="number" class="form-control" required>
              </div>
              <button type="submit" class="btn btn-primary">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Modal } from 'bootstrap'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      users: [],
      services: [],
      serviceForm: {
        name: '',
        base_price: ''
      },
      editingService: null,
      serviceModal: null
    }
  },
  mounted() {
    this.fetchUsers()
    this.fetchServices()
    this.serviceModal = new Modal(document.getElementById('serviceModal'))
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/api/admin/users')
        this.users = response.data
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    },
    async fetchServices() {
      try {
        const response = await axios.get('/api/admin/services')
        this.services = response.data
      } catch (error) {
        console.error('Error fetching services:', error)
      }
    },
    async toggleBlockUser(userId) {
      try {
        await axios.post(`/api/admin/users/${userId}/toggle-block`)
        this.fetchUsers()
      } catch (error) {
        console.error('Error toggling user block status:', error)
      }
    },
    async approveProfessional(profId) {
      try {
        await axios.post(`/api/admin/professionals/${profId}/approve`)
        this.fetchUsers()
      } catch (error) {
        console.error('Error approving professional:', error)
      }
    },
    showAddServiceModal() {
      this.editingService = null
      this.serviceForm = { name: '', base_price: '' }
      this.serviceModal.show()
    },
    editService(service) {
      this.editingService = service
      this.serviceForm = { ...service }
      this.serviceModal.show()
    },
    async saveService() {
      try {
        if (this.editingService) {
          await axios.put(`/api/admin/services/${this.editingService.id}`, this.serviceForm)
        } else {
          await axios.post('/api/admin/services', {
            ...this.serviceForm,
            admin_id: 1 // Replace with actual admin ID from auth
          })
        }
        this.serviceModal.hide()
        this.fetchServices()
      } catch (error) {
        console.error('Error saving service:', error)
      }
    },
    async deleteService(serviceId) {
      if (confirm('Are you sure you want to delete this service?')) {
        try {
          await axios.delete(`/api/admin/services/${serviceId}`)
          this.fetchServices()
        } catch (error) {
          console.error('Error deleting service:', error)
        }
      }
    }
  }
}
</script> 
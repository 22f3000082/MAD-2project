<template>
  <div class="professional-profile-page">
    <div class="container py-5">
      <!-- Loading state -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading professional profile...</p>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger">
        <i class="fas fa-exclamation-triangle me-2"></i>
        {{ error }}
      </div>
      
      <!-- Content when loaded -->
      <div v-else class="row">
        <!-- Profile Information -->
        <div class="col-lg-4 mb-4">
          <div class="card profile-card">
            <div class="card-body text-center">
              <div class="profile-image mb-3">
                <img src="https://via.placeholder.com/150" alt="Professional" class="rounded-circle img-thumbnail">
              </div>
              <h3>{{ profile.professional_name }}</h3>
              
              <!-- Edit Profile Section -->
              <div v-if="editMode">
                <form @submit.prevent="updateProfile">
                  <div class="form-group mb-3">
                    <label>Description</label>
                    <textarea 
                      v-model="form.description" 
                      class="form-control" 
                      rows="3"
                    ></textarea>
                  </div>

                  <div class="form-group mb-3">
                    <label>Phone</label>
                    <input 
                      v-model="form.phone" 
                      type="tel" 
                      class="form-control"
                    >
                  </div>

                  <div class="form-group mb-3">
                    <label>Experience (years)</label>
                    <input 
                      v-model="form.experience" 
                      type="number" 
                      class="form-control"
                      min="0"
                    >
                  </div>

                  <div class="btn-group w-100">
                    <button 
                      type="submit" 
                      class="btn btn-primary"
                      :disabled="loading"
                    >
                      Save Changes
                    </button>
                    <button 
                      type="button" 
                      class="btn btn-secondary"
                      @click="cancelEdit"
                      :disabled="loading"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>

              <!-- View Profile Section -->
              <div v-else>
                <p class="text-muted">{{ profile.description || 'No description available.' }}</p>
                <hr>
                <div class="text-start">
                  <p class="mb-2"><strong><i class="fas fa-briefcase me-2"></i>Experience:</strong> {{ profile.experience }} years</p>
                  <p class="mb-2"><strong><i class="fas fa-phone me-2"></i>Phone:</strong> {{ profile.phone || 'Not provided' }}</p>
                  <p class="mb-2"><strong><i class="fas fa-calendar-check me-2"></i>Joined:</strong> {{ formatDate(profile.date_created) }}</p>
                  <button 
                    @click="editMode = true" 
                    class="btn btn-primary mt-3 w-100"
                  >
                    Edit Profile
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Reviews Section -->
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header bg-white">
              <h4 class="mb-0">Reviews</h4>
            </div>
            <div class="card-body">
              <!-- Reviews content here -->
              <div v-if="!profile.reviews || profile.reviews.length === 0" class="text-center py-4">
                <p class="text-muted">No reviews yet</p>
              </div>
              <div v-else>
                <!-- Reviews list here -->
                <div class="list-group list-group-flush">
                  <div v-for="review in profile.reviews" :key="review.id" class="list-group-item">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                      <div>
                        <h6 class="mb-0">{{ review.customer_name || 'Customer' }}</h6>
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
          
          <!-- Service Statistics -->
          <div class="card mt-4">
            <div class="card-header bg-white">
              <h4 class="mb-0">Service Statistics</h4>
            </div>
            <div class="card-body">
              <div class="row g-4">
                <div class="col-sm-4">
                  <div class="stat-card bg-light p-3 text-center rounded">
                    <div class="stat-icon mb-2">
                      <i class="fas fa-check-circle fa-2x text-success"></i>
                    </div>
                    <h5>{{ profile.completed_services || 0 }}</h5>
                    <p class="text-muted mb-0">Services Completed</p>
                  </div>
                </div>
                <div class="col-sm-4">
                  <div class="stat-card bg-light p-3 text-center rounded">
                    <div class="stat-icon mb-2">
                      <i class="fas fa-star fa-2x text-warning"></i>
                    </div>
                    <h5>{{ profile.average_rating?.toFixed(1) || '0.0' }}</h5>
                    <p class="text-muted mb-0">Average Rating</p>
                  </div>
                </div>
                <div class="col-sm-4">
                  <div class="stat-card bg-light p-3 text-center rounded">
                    <div class="stat-icon mb-2">
                      <i class="fas fa-users fa-2x text-primary"></i>
                    </div>
                    <h5>{{ profile.total_customers || 0 }}</h5>
                    <p class="text-muted mb-0">Customers Served</p>
                  </div>
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
import { professionalAPI } from '@/services/api'

export default {
  name: 'ProfessionalProfile',
  
  data() {
    return {
      profile: null,
      loading: false,
      error: null,
      editMode: false,
      form: {
        description: '',
        phone: '',
        experience: '',
        availability: []
      }
    }
  },

  created() {
    this.fetchProfile()
  },

  methods: {
    async fetchProfile() {
      this.loading = true
      try {
        // Fetch profile data
        const data = await professionalAPI.getProfile()
        this.profile = data
        
        // Fetch reviews if not included in profile data
        if (!this.profile.reviews) {
          const reviews = await professionalAPI.getReviews()
          this.profile.reviews = reviews || []
        }
        
        this.form = {
          description: data.description || '',
          phone: data.phone || '',
          experience: data.experience || '',
          availability: data.availability || []
        }
      } catch (err) {
        this.error = err.message || 'Failed to load profile'
        console.error('Error fetching profile:', err)
      } finally {
        this.loading = false
      }
    },

    async updateProfile() {
      this.loading = true
      try {
        await professionalAPI.updateProfile(this.form)
        this.profile = { ...this.profile, ...this.form }
        this.editMode = false
        this.$toast?.success('Profile updated successfully') || alert('Profile updated successfully')
      } catch (err) {
        this.$toast?.error(err.message || 'Failed to update profile') || alert('Failed to update profile: ' + (err.message || ''))
        console.error('Error updating profile:', err)
      } finally {
        this.loading = false
      }
    },

    cancelEdit() {
      this.editMode = false
      this.form = {
        description: this.profile.description || '',
        phone: this.profile.phone || '',
        experience: this.profile.experience || '',
        availability: this.profile.availability || []
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.professional-profile-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.profile-card {
  border-radius: 15px;
}

.profile-image {
  width: 150px;
  height: 150px;
  margin: 0 auto;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.list-group-item {
  transition: background-color 0.2s;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.availability-grid {
  display: flex;
  gap: 10px;
  overflow-x: auto;
}

.day-column {
  flex: 1;
  min-width: 100px;
  text-align: center;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
}

.day-header {
  background-color: #f8f9fa;
  padding: 8px;
  font-weight: 500;
}

.day-availability {
  padding: 15px 8px;
}

.day-availability.is-available {
  background-color: #d4edda;
  color: #155724;
}

.day-availability:not(.is-available) {
  background-color: #f8d7da;
  color: #721c24;
}

.stat-card {
  transition: transform 0.2s;
  border-radius: 10px;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.stat-icon {
  color: #6c757d;
}
</style>

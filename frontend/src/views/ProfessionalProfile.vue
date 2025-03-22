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
              <div class="d-flex justify-content-center mb-3">
                <div class="rating">
                  <i v-for="n in 5" :key="n" class="fas fa-star" 
                    :class="n <= profile.average_rating ? 'text-warning' : 'text-muted'"></i>
                  <span class="ms-1">{{ profile.average_rating }}/5 ({{ profile.total_reviews }} reviews)</span>
                </div>
              </div>
              <span class="badge bg-primary rounded-pill mb-3">{{ profile.service_type }}</span>
              <p class="text-muted">{{ profile.description || 'No description available.' }}</p>
              <hr>
              <div class="text-start">
                <p class="mb-2"><strong><i class="fas fa-briefcase me-2"></i>Experience:</strong> {{ profile.experience }} years</p>
                <p class="mb-2"><strong><i class="fas fa-calendar-check me-2"></i>Joined:</strong> {{ formatDate(profile.date_created) }}</p>
                <p class="mb-0"><strong><i class="fas fa-check-circle me-2"></i>Status:</strong>
                  <span :class="profile.is_available ? 'text-success' : 'text-secondary'">
                    {{ profile.is_available ? 'Available for Work' : 'Currently Unavailable' }}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Reviews Section -->
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header bg-white">
              <h4 class="mb-0">Customer Reviews</h4>
            </div>
            <div class="card-body p-0">
              <div v-if="reviews.length === 0" class="text-center py-5">
                <i class="fas fa-star fa-3x text-muted mb-3"></i>
                <h5>No Reviews Yet</h5>
                <p class="text-muted">This professional hasn't received any reviews yet.</p>
              </div>
              
              <div v-else class="list-group list-group-flush">
                <div v-for="review in reviews" :key="review.id" class="list-group-item p-3">
                  <div class="d-flex justify-content-between mb-2">
                    <div>
                      <h5 class="mb-0">{{ review.customer_name }}</h5>
                      <small class="text-muted">{{ formatDate(review.date_created) }}</small>
                    </div>
                    <div class="rating">
                      <i v-for="n in 5" :key="n" class="fas fa-star" 
                        :class="n <= review.rating ? 'text-warning' : 'text-muted'"></i>
                    </div>
                  </div>
                  <p class="mb-1">{{ review.remarks }}</p>
                  <small class="text-muted">Service: {{ review.service_name }}</small>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Availability Calendar (for demonstration) -->
          <div class="card mt-4">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h4 class="mb-0">Availability</h4>
              <div>
                <button class="btn btn-outline-primary btn-sm" @click="requestService" :disabled="!profile.is_available">
                  <i class="fas fa-calendar-plus me-1"></i> Request Service
                </button>
              </div>
            </div>
            <div class="card-body">
              <div v-if="!profile.is_available" class="alert alert-warning">
                <i class="fas fa-exclamation-circle me-2"></i>
                This professional is currently unavailable for new service requests.
              </div>
              
              <!-- Simple weekly availability display -->
              <div class="availability-grid">
                <div v-for="day in availabilityCalendar" :key="day.name" class="day-column">
                  <div class="day-header">{{ day.name }}</div>
                  <div class="day-availability" :class="{ 'is-available': day.available }">
                    {{ day.available ? 'Available' : 'Unavailable' }}
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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'ProfessionalProfile',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const professionalId = route.params.id;
    
    const profile = ref({});
    const reviews = ref([]);
    const loading = ref(true);
    const error = ref(null);
    
    // Sample availability calendar
    const availabilityCalendar = ref([
      { name: 'Monday', available: true },
      { name: 'Tuesday', available: true },
      { name: 'Wednesday', available: true },
      { name: 'Thursday', available: true },
      { name: 'Friday', available: true },
      { name: 'Saturday', available: false },
      { name: 'Sunday', available: false }
    ]);
    
    const fetchProfileData = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`/api/professionals/${professionalId}`);
        profile.value = response.data;
        
        // Fetch reviews for this professional
        const reviewsResponse = await axios.get(`/api/professionals/${professionalId}/reviews`);
        reviews.value = reviewsResponse.data;
      } catch (err) {
        console.error('Error fetching professional profile:', err);
        error.value = 'Failed to load professional profile. Please try again.';
      } finally {
        loading.value = false;
      }
    };
    
    const requestService = () => {
      // Navigate to service request form with this professional pre-selected
      router.push({
        path: '/service-request',
        query: { professional: professionalId }
      });
    };
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric', 
        month: 'long', 
        day: 'numeric'
      });
    };
    
    onMounted(fetchProfileData);
    
    return {
      profile,
      reviews,
      loading,
      error,
      availabilityCalendar,
      requestService,
      formatDate
    };
  }
};
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
</style>

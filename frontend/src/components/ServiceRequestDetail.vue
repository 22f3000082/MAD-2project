<template>
  <div class="service-request-detail">
    <div class="modal-header">
      <h5 class="modal-title">Request Details</h5>
      <button type="button" class="btn-close" @click="close"></button>
    </div>
    
    <div class="modal-body" v-if="request">
      <div v-if="editMode" class="edit-form">
        <form @submit.prevent="saveChanges">
          <div class="mb-3">
            <label class="form-label">Service</label>
            <input type="text" class="form-control" :value="request.service?.name" disabled>
          </div>
          
          <div class="mb-3">
            <label class="form-label">PIN Code</label>
            <input 
              type="text" 
              class="form-control" 
              v-model="editedRequest.pin_code"
              pattern="[0-9]{6}"
              required
            >
          </div>
          
          <div class="mb-3">
            <label class="form-label">Special Instructions</label>
            <textarea 
              class="form-control" 
              rows="3" 
              v-model="editedRequest.special_instructions"
            ></textarea>
          </div>
          
          <div class="mb-3" v-if="request.status === 'completed'">
            <label class="form-label">Request Completion</label>
            <div class="form-check">
              <input 
                class="form-check-input" 
                type="checkbox" 
                v-model="editedRequest.is_completed"
                id="isCompletedCheck"
              >
              <label class="form-check-label" for="isCompletedCheck">
                Mark as completed
              </label>
            </div>
          </div>
          
          <div class="text-end">
            <button type="button" class="btn btn-secondary me-2" @click="cancelEdit">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              Save Changes
            </button>
          </div>
        </form>
      </div>
      
      <div v-else class="view-mode">
        <div class="request-details">
          <h4>{{ request.service?.name }}</h4>
          
          <div class="mb-3">
            <span :class="getStatusBadgeClass(request.status)">
              {{ request.status }}
            </span>
          </div>
          
          <div class="mb-3">
            <h6>Request Timeline</h6>
            <div class="timeline">
              <div class="timeline-item">
                <div class="timeline-marker bg-primary"></div>
                <div class="timeline-content">
                  <div class="timeline-heading">
                    <h6 class="mb-0">Request Created</h6>
                    <small>{{ formatDate(request.created_at) }}</small>
                  </div>
                </div>
              </div>
              
              <div v-if="request.accepted_at" class="timeline-item">
                <div class="timeline-marker bg-info"></div>
                <div class="timeline-content">
                  <div class="timeline-heading">
                    <h6 class="mb-0">Request Accepted</h6>
                    <small>{{ formatDate(request.accepted_at) }}</small>
                  </div>
                </div>
              </div>
              
              <div v-if="request.completed_at" class="timeline-item">
                <div class="timeline-marker bg-success"></div>
                <div class="timeline-content">
                  <div class="timeline-heading">
                    <h6 class="mb-0">Service Completed</h6>
                    <small>{{ formatDate(request.completed_at) }}</small>
                  </div>
                </div>
              </div>
              
              <div v-if="request.closed_at" class="timeline-item">
                <div class="timeline-marker bg-secondary"></div>
                <div class="timeline-content">
                  <div class="timeline-heading">
                    <h6 class="mb-0">Request Closed</h6>
                    <small>{{ formatDate(request.closed_at) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="mb-3" v-if="request.professional">
            <h6>Professional Details</h6>
            <p class="mb-1"><strong>Name:</strong> {{ request.professional.professional_name }}</p>
            <p class="mb-1"><strong>Phone:</strong> {{ request.professional.phone || 'N/A' }}</p>
            <p class="mb-0">
              <a href="#" class="text-decoration-none" @click.prevent="viewProfessionalProfile(request.professional.id)">
                <i class="fas fa-external-link-alt me-1"></i> View Profile
              </a>
            </p>
          </div>
          
          <div class="mb-3">
            <h6>Service Details</h6>
            <p class="mb-1"><strong>PIN Code:</strong> {{ request.pin_code }}</p>
            <p class="mb-1"><strong>Base Price:</strong> ₹{{ request.service?.base_price }}</p>
            <p class="mb-1"><strong>Final Amount:</strong> 
              {{ request.final_amount ? `₹${request.final_amount}` : 'To be determined' }}
            </p>
            <p class="mb-1"><strong>Service Time:</strong> {{ request.service?.time_required }} minutes</p>
          </div>
          
          <div class="mb-3">
            <h6>Special Instructions</h6>
            <p class="mb-0">{{ request.special_instructions || 'No special instructions provided.' }}</p>
          </div>
          
          <div class="mb-4" v-if="request.review">
            <h6>Your Review</h6>
            <div class="review-box p-3 bg-light rounded">
              <div class="stars mb-2">
                <i v-for="n in 5" :key="n"
                   class="fas fa-star"
                   :class="n <= request.review.rating ? 'text-warning' : 'text-muted'"></i>
              </div>
              <p class="mb-1">{{ request.review.remarks }}</p>
              <small class="text-muted">{{ formatDate(request.review.date_created) }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" @click="close">Close</button>
      
      <div class="action-buttons">
        <button 
          v-if="canEdit"
          type="button" 
          class="btn btn-primary me-2" 
          @click="toggleEditMode">
          <i class="fas fa-edit me-1"></i> {{ editMode ? 'Cancel Edit' : 'Edit Request' }}
        </button>
        
        <button 
          v-if="canAddReview"
          type="button" 
          class="btn btn-success me-2" 
          @click="openReviewForm">
          <i class="fas fa-star me-1"></i> Add Review
        </button>
        
        <button 
          v-if="canCancel"
          type="button" 
          class="btn btn-danger" 
          @click="confirmCancel">
          <i class="fas fa-times me-1"></i> Cancel Request
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { customerAPI } from '@/services/api';

export default {
  name: 'ServiceRequestDetail',
  props: {
    request: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'updated', 'review', 'cancel'],
  setup(props, { emit }) {
    const router = useRouter();
    const editMode = ref(false);
    const saving = ref(false);
    const editedRequest = reactive({
      pin_code: '',
      special_instructions: '',
      is_completed: false
    });

    // Computed properties for action button visibility
    const canEdit = computed(() => {
      return props.request && ['pending', 'assigned'].includes(props.request.status);
    });
    
    const canAddReview = computed(() => {
      return props.request && 
             props.request.status === 'completed' && 
             !props.request.review;
    });
    
    const canCancel = computed(() => {
      return props.request && 
             ['pending', 'assigned', 'in_progress'].includes(props.request.status);
    });

    // Initialize edit form with current values
    const initializeForm = () => {
      if (props.request) {
        editedRequest.pin_code = props.request.pin_code || '';
        editedRequest.special_instructions = props.request.special_instructions || '';
        editedRequest.is_completed = props.request.status === 'completed';
      }
    };

    // Toggle edit mode
    const toggleEditMode = () => {
      if (!editMode.value) {
        initializeForm();
      }
      editMode.value = !editMode.value;
    };

    // Cancel editing
    const cancelEdit = () => {
      editMode.value = false;
    };

    // Save changes to the service request
    const saveChanges = async () => {
      saving.value = true;
      try {
        const updatedData = {
          pin_code: editedRequest.pin_code,
          special_instructions: editedRequest.special_instructions
        };
        
        // If the user is marking the request as completed
        if (editedRequest.is_completed && props.request.status !== 'completed') {
          await customerAPI.closeRequest(props.request.id);
        } else {
          await customerAPI.updateRequest(props.request.id, updatedData);
        }
        
        // Exit edit mode and notify parent component
        editMode.value = false;
        saving.value = false;
        emit('updated');
      } catch (error) {
        console.error('Error updating request:', error);
        alert('Failed to update request: ' + (error.message || 'Unknown error'));
        saving.value = false;
      }
    };

    // Open the review form
    const openReviewForm = () => {
      emit('review', props.request);
    };

    // Cancel the service request
    const confirmCancel = () => {
      if (confirm('Are you sure you want to cancel this service request?')) {
        emit('cancel', props.request);
      }
    };

    // Close the detail view
    const close = () => {
      emit('close');
    };

    // View professional profile
    const viewProfessionalProfile = (professionalId) => {
      router.push(`/professional/${professionalId}`);
    };

    // Helper to format dates
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

    // Helper to get status badge class
    const getStatusBadgeClass = (status) => {
      const classes = {
        pending: 'badge bg-warning',
        assigned: 'badge bg-info',
        in_progress: 'badge bg-primary',
        completed: 'badge bg-success',
        closed: 'badge bg-secondary',
        cancelled: 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    };

    return {
      editMode,
      saving,
      editedRequest,
      canEdit,
      canAddReview,
      canCancel,
      toggleEditMode,
      cancelEdit,
      saveChanges,
      openReviewForm,
      confirmCancel,
      close,
      viewProfessionalProfile,
      formatDate,
      getStatusBadgeClass
    };
  }
};
</script>

<style scoped>
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

.stars i {
  color: #e0e0e0;
}

.stars i.text-warning {
  color: #ffc107;
}

.review-box {
  border-left: 4px solid #ffc107;
}
</style>

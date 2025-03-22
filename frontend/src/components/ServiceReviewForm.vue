<template>
  <div class="service-review-form">
    <div class="modal-header">
      <h5 class="modal-title">Review Your Service</h5>
      <button type="button" class="btn-close" @click="close"></button>
    </div>
    <div class="modal-body">
      <div class="service-summary mb-4 p-3 bg-light rounded">
        <div class="d-flex align-items-center mb-2">
          <div class="service-icon me-3">
            <i class="fas fa-tools fa-2x text-primary"></i>
          </div>
          <div>
            <h5 class="mb-0">{{ serviceName }}</h5>
            <p class="mb-0 text-muted">{{ formatDate(serviceDate) }}</p>
          </div>
        </div>
        <div v-if="professionalName" class="mt-2">
          <span class="text-muted">Professional:</span> {{ professionalName }}
        </div>
      </div>
      
      <form @submit.prevent="submitReview">
        <div class="mb-4">
          <label class="form-label d-block">Rating</label>
          <div class="rating-container d-flex flex-column align-items-center">
            <div class="stars mb-2">
              <i v-for="star in 5" 
                 :key="star" 
                 class="fas fa-star fa-2x" 
                 :class="{ 'text-warning': star <= rating, 'text-muted': star > rating }"
                 @click="rating = star"></i>
            </div>
            <div class="rating-text">
              {{ getRatingText() }}
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label for="reviewRemarks" class="form-label">Your Feedback</label>
          <textarea
            id="reviewRemarks"
            class="form-control"
            v-model="remarks"
            rows="4"
            placeholder="Share your experience with this service..."
            required
          ></textarea>
          <div class="form-text">Your review helps other customers and improves our service.</div>
        </div>
        
        <div class="mb-4">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="recommendService" id="recommendCheck">
            <label class="form-check-label" for="recommendCheck">
              I would recommend this service to others
            </label>
          </div>
        </div>
        
        <div class="text-end">
          <button type="button" class="btn btn-secondary me-2" @click="close">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary" :disabled="submitDisabled || submitting">
            <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
            Submit Review
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { customerAPI } from '@/services/api';

export default {
  name: 'ServiceReviewForm',
  props: {
    requestId: {
      type: [Number, String],
      required: true
    },
    serviceName: {
      type: String,
      default: 'Service'
    },
    serviceDate: {
      type: String,
      default: null
    },
    professionalName: {
      type: String,
      default: ''
    }
  },
  emits: ['close', 'submitted'],
  setup(props, { emit }) {
    const rating = ref(0);
    const remarks = ref('');
    const recommendService = ref(true);
    const submitting = ref(false);
    
    const submitDisabled = computed(() => {
      return rating.value === 0 || !remarks.value.trim();
    });
    
    const getRatingText = () => {
      const ratingTexts = [
        'Select a rating',
        'Poor',
        'Fair',
        'Good',
        'Very Good',
        'Excellent'
      ];
      return ratingTexts[rating.value] || 'Select a rating';
    };
    
    const submitReview = async () => {
      if (submitDisabled.value) return;
      
      submitting.value = true;
      try {
        const reviewData = {
          rating: rating.value,
          remarks: remarks.value,
          recommended: recommendService.value
        };
        
        await customerAPI.addReview(props.requestId, reviewData);
        emit('submitted');
      } catch (error) {
        console.error('Error submitting review:', error);
        alert('Failed to submit review: ' + (error.message || 'Unknown error'));
      } finally {
        submitting.value = false;
      }
    };
    
    const close = () => {
      emit('close');
    };
    
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    };
    
    return {
      rating,
      remarks,
      recommendService,
      submitting,
      submitDisabled,
      getRatingText,
      submitReview,
      close,
      formatDate
    };
  }
};
</script>

<style scoped>
.stars {
  cursor: pointer;
  user-select: none;
}

.stars i {
  margin: 0 5px;
  transition: all 0.2s;
}

.stars i:hover {
  transform: scale(1.2);
}

.stars i.text-warning {
  color: #ffc107;
}

.stars i.text-muted {
  color: #e0e0e0;
}

.rating-text {
  font-weight: 500;
  min-height: 24px;
}

.service-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(13, 110, 253, 0.1);
}
</style>

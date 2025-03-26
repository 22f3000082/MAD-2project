<template>
  <div>
    <div class="modal-header">
      <h5 class="modal-title">Rate Your Service</h5>
      <button type="button" class="btn-close" @click="$emit('close')"></button>
    </div>
    <div class="modal-body">
      <div class="service-review-form">
        <div class="text-center mb-4">
          <h5>{{ serviceName }}</h5>
          <p class="text-muted small">
            Completed on {{ formatDate(serviceDate) }} by {{ professionalName }}
          </p>
        </div>
        
        <form @submit.prevent="submitReview">
          <!-- Star Rating Component -->
          <div class="mb-4 text-center">
            <label class="form-label d-block">Your Rating</label>
            <div class="star-rating">
              <span 
                v-for="star in 5" 
                :key="star" 
                class="star-rating-item"
                :class="{ 'selected': star <= rating }"
                @click="setRating(star)"
                @mouseover="hoverRating = star"
                @mouseleave="hoverRating = 0"
              >
                <!-- Replace Font Awesome with Unicode stars for better compatibility -->
                <span class="star-icon" :class="{ 
                  'text-warning': star <= (hoverRating || rating),
                  'text-muted': star > (hoverRating || rating)
                }">★</span>
              </span>
            </div>
            <div class="rating-text mt-2">
              {{ getRatingText() }}
            </div>
            <div class="text-danger" v-if="validationErrors.rating">
              {{ validationErrors.rating }}
            </div>
          </div>
          
          <!-- Comments Field -->
          <div class="mb-4">
            <label for="reviewRemarks" class="form-label">Your Comments</label>
            <textarea
              id="reviewRemarks"
              v-model="remarks"
              class="form-control"
              rows="4"
              placeholder="Share your experience with this service professional..."
            ></textarea>
            <div class="text-danger" v-if="validationErrors.remarks">
              {{ validationErrors.remarks }}
            </div>
          </div>
          
          <!-- Submit Button -->
          <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-secondary me-2" @click="$emit('close')">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1"></span>
              Submit Review
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { customerAPI } from '@/services/api';

export default {
  name: 'ServiceReviewForm',
  props: {
    requestId: {
      type: Number,
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
      default: 'Professional'
    }
  },
  
  data() {
    return {
      rating: 0,
      hoverRating: 0,
      remarks: '',
      isSubmitting: false,
      validationErrors: {
        rating: '',
        remarks: ''
      }
    };
  },
  
  methods: {
    setRating(value) {
      this.rating = value;
      this.validationErrors.rating = '';
    },
    
    getRatingText() {
      const texts = [
        'Select a rating',
        'Poor',
        'Fair',
        'Good',
        'Very Good',
        'Excellent'
      ];
      return texts[this.rating] || texts[0];
    },
    
    validateForm() {
      let isValid = true;
      this.validationErrors = {
        rating: '',
        remarks: ''
      };
      
      if (!this.rating || this.rating < 1) {
        this.validationErrors.rating = 'Please select a rating';
        isValid = false;
      }
      
      if (!this.remarks.trim()) {
        this.validationErrors.remarks = 'Please provide some comments about your experience';
        isValid = false;
      } else if (this.remarks.length < 5) {
        this.validationErrors.remarks = 'Comments must be at least 5 characters';
        isValid = false;
      }
      
      return isValid;
    },
    
    async submitReview() {
      try {
        if (!this.validateForm()) {
          return;
        }
        
        this.isSubmitting = true;
        
        const reviewData = {
          rating: this.rating,
          remarks: this.remarks
        };
        
        await customerAPI.addReview(this.requestId, reviewData);
        
        // Clear form and emit event
        this.rating = 0;
        this.remarks = '';
        this.$emit('submitted');
      } catch (error) {
        console.error('Error submitting review:', error);
        alert('Failed to submit review: ' + (error.message || 'Unknown error'));
      } finally {
        this.isSubmitting = false;
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.star-rating {
  display: flex;
  justify-content: center;
  gap: 8px;
  font-size: 1.75rem;
}

.star-rating-item {
  cursor: pointer;
  transition: transform 0.1s;
}

.star-rating-item:hover {
  transform: scale(1.2);
}

.star-rating-item.selected {
  transform: scale(1.1);
}

.star-icon {
  display: inline-block;
  font-size: 1.75rem;
  line-height: 1;
}

.rating-text {
  font-weight: 500;
  height: 1.5rem; /* Fixed height to prevent layout shifts */
}

.text-warning {
  color: #ffc107 !important;
}

.text-muted {
  color: #dee2e6 !important;
}
</style>

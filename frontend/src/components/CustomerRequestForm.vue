<template>
  <div class="request-form">
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading services...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
      <button class="btn btn-outline-danger btn-sm ms-3" @click="loadServices">
        <i class="fas fa-sync-alt"></i> Retry
      </button>
    </div>
    
    <form v-else @submit.prevent="submitRequest" class="needs-validation" novalidate>
      <div class="mb-3">
      </div>
      
      <div class="mb-3">
        <label for="pinCode" class="form-label">PIN Code</label>
        <input 
          type="text" 
          class="form-control" 
          id="pinCode" 
          v-model="requestData.pin_code" 
          required 
          pattern="[0-9]{6}"
          :class="{ 'is-invalid': validationErrors.pin_code }"
        >
        <div class="invalid-feedback">{{ validationErrors.pin_code || 'Please enter a valid 6-digit PIN code' }}</div>
      </div>
      
      <div class="mb-3">
        <label for="instructions" class="form-label">Special Instructions (Optional)</label>
        <textarea 
          class="form-control" 
          id="instructions" 
          v-model="requestData.special_instructions" 
          rows="3"
        ></textarea>
      </div>
      
      <div class="d-grid">
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Submitting...' : 'Submit Request' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { serviceAPI, customerAPI } from '@/services/api';

export default {
  name: 'CustomerRequestForm',
  props: {
    // Optionally allow specifying a default service
    defaultServiceId: {
      type: [Number, String],
      default: null
    }
  },
  emits: ['request-submitted', 'request-failed'],
  setup(props, { emit }) {
    const services = ref([]);
    const loading = ref(true);
    const error = ref('');
    const isSubmitting = ref(false);
    
    const requestData = reactive({
      service_id: props.defaultServiceId || '',
      pin_code: '',
      special_instructions: ''
    });
    
    const validationErrors = reactive({
      service_id: '',
      pin_code: '',
      special_instructions: ''
    });
    
    const selectedService = computed(() => {
      if (!requestData.service_id) return null;
      return services.value.find(service => service.id == requestData.service_id);
    });
    
    // Validate form
    const validateForm = () => {
      let isValid = true;
      
      // Reset errors
      Object.keys(validationErrors).forEach(key => {
        validationErrors[key] = '';
      });
      
      // Validate service ID
      if (!requestData.service_id) {
        validationErrors.service_id = 'Please select a service';
        isValid = false;
      }
      
      // Validate PIN code
      if (!requestData.pin_code) {
        validationErrors.pin_code = 'PIN code is required';
        isValid = false;
      } else if (!/^\d{6}$/.test(requestData.pin_code)) {
        validationErrors.pin_code = 'PIN code must be 6 digits';
        isValid = false;
      }
      
      return isValid;
    };
    
    // Submit request
    const submitRequest = async () => {
      if (!validateForm()) return;
      
      isSubmitting.value = true;
      
      try {
        const response = await customerAPI.createRequest(requestData);
        console.log('Service request created:', response);
        
        // Reset form
        requestData.service_id = '';
        requestData.pin_code = '';
        requestData.special_instructions = '';
        
        // Emit success event
        emit('request-submitted', response);
      } catch (err) {
        console.error('Failed to create service request:', err);
        emit('request-failed', err.message || 'Failed to create service request');
      } finally {
        isSubmitting.value = false;
      }
    };
    
    onMounted(loadServices);
    
    return {
      services,
      loading,
      error,
      requestData,
      validationErrors,
      isSubmitting,
      selectedService,
      loadServices,
      submitRequest
    };
  }
}
</script>

<style scoped>
.service-details {
  font-size: 0.9rem;
}
</style>

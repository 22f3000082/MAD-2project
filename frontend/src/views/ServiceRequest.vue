/* eslint-disable */
<template>
    <div>
      <h1>Service Request</h1>
    </div>
  </template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { serviceAPI, customerAPI } from '@/services/api';

export default {
  setup() {
    const route = useRoute(); // Initialize route here
    const service = ref(null);
    const loading = ref(true);
    const error = ref(null);
    
    const fetchServiceDetails = async (serviceId) => {
      try {
        loading.value = true;
        error.value = null;
        console.log(`ServiceRequest: Fetching details for service ID ${serviceId}`);
        
        // Try first the specific service endpoint
        try {
          const serviceData = await serviceAPI.getServiceById(serviceId);
          service.value = serviceData;
        } catch (specificError) {
          console.error('ServiceRequest: Failed to get specific service, trying services list:', specificError);
          
          // Fallback: get all services and find the one we need
          const services = await serviceAPI.getServices();
          service.value = services.find(s => s.id === parseInt(serviceId));
          
          if (!service.value) {
            throw new Error('Service not found');
          }
        }
        
        console.log('ServiceRequest: Successfully loaded service:', service.value);
        loading.value = false;
      } catch (err) {
        console.error('ServiceRequest: Error fetching service:', err);
        error.value = err.message || 'Failed to load service details';
        loading.value = false;
      }
    };
    
    onMounted(() => {
      const serviceId = route.params.serviceId;
      fetchServiceDetails(serviceId);
    });
    
    return {
      service,
      loading,
      error
    };
  }
}
</script>

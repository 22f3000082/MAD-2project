<template>
  <div class="register-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow">
            <div class="card-body p-4">
              <h2 class="text-center mb-4">Register</h2>
              <div v-if="error" class="alert alert-danger">{{ error }}</div>
              
              <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                <div class="mb-3">
                  <label for="fullName" class="form-label">Full Name</label>
                  <input type="text" id="fullName" name="fullName" class="form-control" v-model="formData.name" required :class="{ 'is-invalid': errors.name }">
                  <div class="invalid-feedback">{{ errors.name }}</div>
                </div>

                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" id="username" name="username" class="form-control" v-model="formData.username" required :class="{ 'is-invalid': errors.username }">
                  <div class="invalid-feedback">{{ errors.username }}</div>
                </div>

                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" id="email" name="email" class="form-control" v-model="formData.email" required :class="{ 'is-invalid': errors.email }">
                  <div class="invalid-feedback">{{ errors.email }}</div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" id="password" name="password" class="form-control" v-model="formData.password" required :class="{ 'is-invalid': errors.password }">
                  <div class="invalid-feedback">{{ errors.password }}</div>
                </div>
                
                <div class="mb-4">
                  <label class="form-label">Register as:</label>
                  <div class="d-flex gap-4">
                    <div class="form-check">
                      <input class="form-check-input" type="radio" v-model="formData.role" value="customer" id="roleCustomer">
                      <label class="form-check-label" for="roleCustomer">Customer</label>
                    </div>
                    <div class="form-check">
                      <input class="form-check-input" type="radio" v-model="formData.role" value="professional" id="roleProfessional">
                      <label class="form-check-label" for="roleProfessional">Service Professional</label>
                    </div>
                  </div>
                </div>
                
                <div v-if="formData.role === 'professional'">
                  <div class="mb-3">
                    <label class="form-label">Service Type</label>
                    <select class="form-select" v-model="formData.service_type" required>
                      <option value="">Select a service type</option>
                      <option v-for="service in service_types" :key="service" :value="service">{{ service }}</option>
                    </select>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Experience (years)</label>
                    <input type="number" class="form-control" v-model="formData.experience" min="0" required>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" v-model="formData.description" rows="3"></textarea>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Upload Documents</label>
                    <input type="file" multiple class="form-control" @change="handleFileUpload">
                  </div>
                </div>
                
                <div v-if="formData.role === 'customer'">
                  <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input type="tel" class="form-control" v-model="formData.phone" required>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Address</label>
                    <textarea class="form-control" v-model="formData.address" required></textarea>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">PIN Code</label>
                    <input type="text" class="form-control" v-model="formData.pin_code" required pattern="[0-9]{6}">
                  </div>
                </div>
                
                <div class="d-grid gap-2">
                  <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? 'Registering...' : 'Register' }}</button>
                </div>
                
                <p class="text-center mt-3">
                  Already have an account? <router-link to="/login">Login here</router-link>
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import router from '@/router';
import ServiceList from '../components/ServiceList.vue';

export default {
  name: 'RegisterView',
  data() {
    return {
      // Define service_types in data section to make it reactive
      service_types: [
        'AC Repair',
        'Plumbing',
        'Electrical',
        'Carpentry',
        'Painting',
        'Cleaning',
        'Pest Control',
        'Appliance Repair',
        'Moving Services',
        'Gardening'
      ]
    };
  },
  setup() {
    const loading = ref(false);
    const error = ref('');
    const services = ref([]);
    
    const formData = reactive({
      name: '', username: '', email: '', password: '', role: '', service_type: '', // Changed from service_types to service_type (singular)
      experience: '', description: '', phone: '', address: '', pin_code: '',
      documents: []
    });
    
    const errors = reactive({});
    
    const fetchServiceTypes = async () => {
    };
    
    const handleFileUpload = (event) => {
      formData.documents = Array.from(event.target.files);
    };
    
    const handleSubmit = async () => {
      try {
        loading.value = true;
        error.value = '';
        
        // Clear previous errors
        Object.keys(errors).forEach(key => errors[key] = '');
        
        // Basic validation
        if (!formData.name) errors.name = 'Name is required';
        if (!formData.username) errors.username = 'Username is required';
        if (!formData.email) errors.email = 'Email is required';
        if (!formData.password) errors.password = 'Password is required';
        if (!formData.role) errors.role = 'Role is required';
        
        // Role-specific validation
        if (formData.role === 'professional') {
          if (!formData.service_type) errors.service_type = 'Service type is required'; // Updated from service_types to service_type
          if (!formData.experience) errors.experience = 'Experience is required';
        } else if (formData.role === 'customer') {
          if (!formData.phone) errors.phone = 'Phone is required';
          if (!formData.address) errors.address = 'Address is required';
          if (!formData.pin_code) errors.pin_code = 'PIN code is required';
        }
        
        // Check if there are any errors
        if (Object.values(errors).some(error => error)) {
          return;
        }
        
        const formDataToSend = new FormData();
        
        // Append all form data
        Object.keys(formData).forEach(key => {
          if (key === 'documents') {
            formData.documents.forEach(file => {
              formDataToSend.append('documents', file);
            });
          } else {
            formDataToSend.append(key, formData[key]);
          }
        });
        
        const response = await axios.post('http://localhost:8080/auth/register', 
          formDataToSend,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Accept': 'application/json'
            },
            withCredentials: true
          }
        );
        
        console.log('Registration successful:', response.data);
        
        // Show success message
        error.value = '';
        alert('Registration successful! Please login to continue.');
        
        // Redirect to login page
        router.push('/login');
      } catch (err) {
        console.error('Registration error:', err);
        error.value = err.response?.data?.message || err.response?.data?.error || 'Registration failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };
    
    onMounted(fetchServiceTypes);
    
    return { formData, errors, loading, error, services, handleSubmit, handleFileUpload, fetchServiceTypes };
  }
};
</script>

<style scoped>
.register-container { background-color: #f8f9fa; min-height: 100vh; padding-top: 2rem; }
.card { border-radius: 15px; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); }
.btn-primary { padding: 0.75rem; font-weight: 500; }
.invalid-feedback { font-size: 0.875rem; }
</style>

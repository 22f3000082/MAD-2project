import axios from 'axios'
import router from '@/router'

// Create axios instance with custom config
const api = axios.create({
  baseURL: 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true // Important for CORS with credentials
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('Response error:', error.response?.data || error.message)
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Unauthorized - clear storage and redirect to login
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          router.push('/login')
          break
        case 403:
          // Forbidden - redirect to home
          router.push('/')
          break
        case 500:
          console.error('Server error:', error.response.data)
          break
      }
      // Return the error message from the backend if available
      if (error.response.data && error.response.data.message) {
        return Promise.reject(new Error(error.response.data.message))
      }
    }
    return Promise.reject(error)
  }
)

// API Services
// API Services
export const authService = {
  async register(userData) {
    try {
      // Ensure professionals have a selected service type
      if (userData.role === 'professional' && !userData.service_type) {
        throw new Error("Professionals must select a service type.");
      }

      console.log('Sending registration data:', userData);

      const response = await api.post('/auth/register', userData);

      console.log('Registration response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error.response?.data || error.message);

      // Capture and return specific backend errors
      throw error.response?.data || { message: "Registration failed. Please try again." };
    }
  },

  async login(credentials) {
    try {
      console.log('Attempting login:', credentials)
      const response = await api.post('/auth/login', credentials)
      console.log('Login response:', response.data)
      if (response.data.token) {
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        // Redirect based on user role
        const user = response.data.user
        router.push(`/${user.role}/dashboard`)
      }
      return response.data
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message)
      throw error
    }
  },

  async logout() {
    try {
      await api.post('/auth/logout')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    } catch (error) {
      console.error('Logout error:', error.response?.data || error.message)
      // Still clear local storage and redirect even if API call fails
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
  },

  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }
}

export const serviceAPI = {
  async getServices(params = {}) {
    try {
      // hiihihih
      const response = await api.get('/api/admin/services', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching services:', error)
      throw error
    }
  },
  async mounted() {
    try {
      this.services = await this.searchServices();
      console.log("Services loaded:", this.services);
    } catch (error) {
      console.error("Failed to load services:", error);
    }
  },

  async getServiceById(id) {
    try {
      const response = await api.get(`/api/services/${id}`)
      return response.data
    } catch (error) {
      console.error('Error fetching service:', error)
      throw error
    }
  }
}
  // async searchServices(params) {
  //   try {
  //     const response = await api.get('/api/services/search', { params })
  //     return response.data
  //   } catch (error) {
  //     console.error('Error searching services:', error)
  //     throw error
  //   }
  // },


export const customerAPI = {
  async getRequests() {
    try {
      const response = await api.get('/api/customer/requests')
      return response.data
    } catch (error) {
      console.error('Error fetching requests:', error)
      throw error
    }
  },

  async createRequest(data) {
    try {
      const response = await api.post('/api/customer/requests', data)
      return response.data
    } catch (error) {
      console.error('Error creating request:', error)
      throw error
    }
  },

  async updateRequest(requestId, data) {
    try {
      const response = await api.put(`/api/customer/requests/${requestId}`, data)
      return response.data
    } catch (error) {
      console.error('Error updating request:', error)
      throw error
    }
  },

  async closeRequest(requestId) {
    try {
      const response = await api.put(`/api/customer/requests/${requestId}/close`)
      return response.data
    } catch (error) {
      console.error('Error closing request:', error)
      throw error
    }
  },

  async addReview(requestId, reviewData) {
    try {
      const response = await api.post(`/api/customer/requests/${requestId}/review`, reviewData)
      return response.data
    } catch (error) {
      console.error('Error adding review:', error)
      throw error
    }
  }
}

export const professionalAPI = {
  async getAssignments(status = null) {
    try {
      const params = status ? { status } : {}
      const response = await api.get('/api/professional/assignments', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching assignments:', error)
      throw error
    }
  },

  async updateStatus(requestId, status) {
    try {
      const response = await api.put(`/api/professional/requests/${requestId}`, { status })
      return response.data
    } catch (error) {
      console.error('Error updating status:', error)
      throw error
    }
  },

  async getProfile() {
    try {
      const response = await api.get('/api/professional/profile')
      return response.data
    } catch (error) {
      console.error('Error fetching profile:', error)
      throw error
    }
  },

  async updateProfile(data) {
    try {
      const response = await api.put('/api/professional/profile', data)
      return response.data
    } catch (error) {
      console.error('Error updating profile:', error)
      throw error
    }
  }
}

export const adminAPI = {
  async getUsers(role = null) {
    try {
      const params = role ? { role } : {}
      const response = await api.get('/api/admin/users', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching users:', error)
      throw error
    }
  },

  async approveUser(userId) {
    try {
      const response = await api.post(`/api/admin/users/${userId}/approve`)
      return response.data
    } catch (error) {
      console.error('Error approving user:', error)
      throw error
    }
  },

  async blockUser(userId) {
    try {
      const response = await api.post(`/api/admin/users/${userId}/block`)
      return response.data
    } catch (error) {
      console.error('Error blocking user:', error)
      throw error
    }
  },

  async getServices() {
    try {
      const response = await api.get('/api/admin/services')
      return response.data
    } catch (error) {
      console.error('Error fetching services:', error)
      throw error
    }
  },

  async createService(serviceData) {
    try {
      console.log('Creating service with data:', serviceData);
      const response = await api.post('/api/admin/services', serviceData);
      console.log('Service created:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error creating service:', error.response?.data || error);
      throw error;
    }
  },

  async updateService(serviceId, serviceData) {
    try {
      const response = await api.put(`/api/admin/services/${serviceId}`, serviceData)
      return response.data
    } catch (error) {
      console.error('Error updating service:', error)
      throw error
    }
  },

  async deleteService(serviceId) {
    try {
      const response = await api.delete(`/api/admin/services/${serviceId}`)
      return response.data
    } catch (error) {
      console.error('Error deleting service:', error)
      throw error
    }
  }
}

export default api

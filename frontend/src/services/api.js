import axios from 'axios'
import router from '@/router'

// Create axios instance with custom config
const api = axios.create({
  baseURL: 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json'
    // 'Accept': 'application/json'
  },
  withCredentials: true // Important for CORS with credentials
})

// Request interceptor
// api.interceptors.request.use(
//   config => {
//     const token = localStorage.getItem('token')
//     if (token) {
//       // Format token properly - token may already have 'Bearer ' prefix
//       const authToken = token.startsWith('Bearer ') ? token : `Bearer ${token}`
//       config.headers['Authorization'] = authToken
//       console.log(`Request to ${config.url} with token: ${authToken.substring(0, 20)}...`)
//     } else {
//       console.warn(`No token found for request to: ${config.url}`)
//     }
//     return config
//   },
//   error => {
//     console.error('Request error:', error)
//     return Promise.reject(error)
//   }
// )
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => Promise.reject(error));


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
        // Store auth data - ensure token is saved correctly
        const token = response.data.token
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        // Verify token was saved correctly
        const savedToken = localStorage.getItem('token')
        console.log(`Token saved successfully: ${savedToken ? 'Yes' : 'No'}`)
        console.log(`Saved token (first 15 chars): ${savedToken ? savedToken.substring(0, 15) : 'None'}`)
        
        // Debug: Check the localStorage item immediately
        console.log('localStorage.token:', localStorage.getItem('token'))
        console.log('localStorage.user:', localStorage.getItem('user'))

        // Get target route path
        const targetPath = `/${response.data.user.role}/dashboard`
        
        // Short delay to ensure token is saved before redirection
        setTimeout(() => {
          // Only navigate if not already on target page
          // if (router.currentRoute.path !== targetPath) {
            router.push(targetPath).catch(err => {
              if (err.name !== 'NavigationDuplicated') {
                console.error('Navigation error:', err)
              }
            })
          }
        , 500)
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

      // Only navigate if not already on login page
      if (router.currentRoute.path !== '/login') {
      router.push('/login').catch(err => {
          if (err.name !== 'NavigationDuplicated') {
            console.error('Navigation error:', err)
          }
        })
      }
    } catch (error) {
      console.error('Logout error:', error.response?.data || error.message)
      // Still clear local storage and redirect even if API call fails
      localStorage.removeItem('token')
      localStorage.removeItem('user')

      // Only navigate if not already on login page
      if (router.currentRoute.path !== '/login') {
      router.push('/login').catch(err => {
          if (err.name !== 'NavigationDuplicated') {
            console.error('Navigation error:', err)
          }
        })
      }
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
      console.log('Fetching professional assignments', status ? `with status: ${status}` : '')
      const params = status ? { status } : {}
      const response = await api.get('/api/professional/assignments', { params })
      console.log('Received assignments:', response.data.length)
      return response.data
    } catch (error) {
      console.error('Error fetching assignments:', error)
      throw error
    }
  },

  async updateStatus(requestId, status) {
    try {
      console.log(`Updating request ${requestId} status to ${status}`)
      const response = await api.put(`/api/professional/requests/${requestId}`, { status })
      console.log('Status update response:', response.data)
      return response.data
    } catch (error) {
      console.error('Error updating status:', error)
      throw error
    }
  },

  async getProfile() {
    try {
      console.log('Fetching professional profile')
      const response = await api.get('/api/professional/profile')
      console.log('Retrieved profile data')
      return response.data
    } catch (error) {
      console.error('Error fetching profile:', error)
      throw error
    }
  },

  async updateProfile(data) {
    try {
      console.log('Updating professional profile with data:', data)
      const response = await api.put('/api/professional/profile', data)
      console.log('Profile update response:', response.data)
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
      // Make sure token is present in localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('Token not found in localStorage');
      }
    
      // console.log(`Fetching users with token: ${token ? token.substring(0, 15) + '...' : 'No token!'}`)
      
      const params = role ? { role } : {}
      // Add a small delay to ensure token is available
      // await new Promise(resolve => setTimeout(resolve, 300))
      
      const response = await api.get('/api/admin/users'
        , { params,
        headers: {
          'Authentication-Token': `Bearer${token}`  // Add token explicitly to request
          // Authorization: `Bearer ${localStorage.getItem('token')}`,
        }
    })
      console.log('Users response:', response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching users:', error.response?.data || error.message)
      if (error.response && error.response.status === 401) {
        // Handle unauthorized error specifically
        console.log('Unauthorized. Please check your token.');
      } else {
      throw error
    }
  }
  },


  async approveUser(userId) {
    try {
      console.log(`Approving professional with ID: ${userId}`);
      const response = await api.post(`/api/admin/professionals/${userId}/approve`);
      console.log('Professional approved:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error approving user:', error);
      throw error;
    }
  },

  async blockUser(userId, reason = 'Violation of terms of service') {
    try {
      console.log(`Blocking user with ID: ${userId}, reason: ${reason}`);
      const response = await api.post(`/api/admin/users/${userId}/block`, { reason });
      console.log('User blocked:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error blocking user:', error);
      throw error;
    }
  },

  async unblockUser(userId) {
    try {
      console.log(`Unblocking user with ID: ${userId}`);
      const response = await api.post(`/api/admin/users/${userId}/unblock`);
      console.log('User unblocked:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error unblocking user:', error);
      throw error;
    }
  },

  async getServices() {
    try {
      // Make sure token is present in localStorage
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('Token not found in localStorage');
      }
      console.log(`Fetching services with token: ${token ? token.substring(0, 15) + '...' : 'No token!'}`)
      
      // Add a small delay to ensure token is available
      await new Promise(resolve => setTimeout(resolve, 300))
      
      const response = await api.get('/api/admin/services', {
        headers: {
          'Authentication-Token': `Bearer ${token}`  // Add token explicitly to request
        }
      })
      console.log('Services response:', response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching services:', error.response?.data || error.message)
      throw error
    }
  },

  // async getService(serviceId) {
  //   try {
  //     const response = await api.get(`/api/admin/services/${serviceId}`)
  //     return response.data
  //   } catch (error) {
  //     console.error('Error fetching service:', error)
  //     throw error
  //   }
  // },

  async createService(serviceData) {
    try {
        // Convert field names to snake_case for backend compatibility
        const formattedData = {
            name: serviceData.name,
            description: serviceData.description,
            base_price: Number(serviceData.basePrice), // Ensure number type
            time_required: Number(serviceData.timeRequired), // Ensure number type
            category: serviceData.category
        };

        console.log('Creating service with formatted data:', formattedData);
        
        const response = await api.post('/api/admin/services', formattedData);
        console.log('Service created:', response.data);

            
        // // Display a success flash message
        // const flashContainer = document.getElementById('flash-messages');
        // const flashMessage = document.createElement('div');
        // flashMessage.classList.add('flash-message');
        // flashMessage.textContent = 'Service created successfully!';
        // flashContainer.appendChild(flashMessage);
    
        // // Auto-hide the message after a few seconds
        // setTimeout(() => {
        //   flashMessage.remove();
        // }, 3000)
        return response.data;
        } catch (error) {
        console.error('Error creating service:', error.response?.data || error);
        
        // Handle specific validation errors
        if (error.response?.status === 400) {
            throw new Error(`Validation error: ${error.response.data.message || 'Invalid data'}`);
        }
        
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
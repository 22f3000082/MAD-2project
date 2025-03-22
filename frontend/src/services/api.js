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

// Request interceptor - fixed
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    // Flask-Security expects raw token without 'Bearer' prefix
    config.headers['Authentication-Token'] = token;
    
    // Add Authorization header too for APIs that might expect it
    // config.headers['Authorization'] = `Bearer ${token}`;
    
    console.log(`Request to ${config.url} with token: ${token.substring(0, 15)}...`);
  } else {
    console.warn(`No token found for request to: ${config.url}`);
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
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        // Simplified navigation
        const path = `/${response.data.user.role}/dashboard`
        router.push(path).catch(err => {
          console.error('Navigation error:', err)
        })
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
  // async getServices(params = {}) {
  //   try {
  //     const token = localStorage.getItem('token');
  //     if (!token) {
  //       throw new Error('No authentication token found');
  //     }

  //     const response = await api.get('/api/service-types', { 
  //       params,
  //       headers: {
  //         'Authentication-Token': token
  //       }
  //     });
  //     return response.data;
  //   } catch (error) {
  //     console.error('Error fetching services:', error)
  //     throw error;
  //   }
  // },

  async getServiceById(id) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await api.get(`/api/services/${id}`, {
        headers: {
          'Authentication-Token': token
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching service:', error)
      throw error;
    }
  },
  
  // Add a new method to fetch service types directly
  async getServiceTypes() {
    try {
      const response = await api.get('/api/service-types');
      return response.data;
    } catch (error) {
      console.error('Error fetching service types:', error);
      throw error;
    }
  },
  
  // Enhanced getServices method with pagination and filtering
  async getServices(params = {}) {
    try {
      const queryParams = { ...params };
      
      // Format price range if provided
      if (queryParams.priceMin) queryParams.price_min = queryParams.priceMin;
      if (queryParams.priceMax) queryParams.price_max = queryParams.priceMax;
      if (queryParams.sortBy) queryParams.sort_by = queryParams.sortBy;
      
      // Clean up params
      delete queryParams.priceMin;
      delete queryParams.priceMax;
      delete queryParams.sortBy;
      
      const response = await api.get('/api/admin/services', { params: queryParams });
      return response.data;
    } catch (error) {
      console.error('Error fetching services:', error);
      throw error;
    }
  }
}

export const customerAPI = {
  // async getRequests() {
  //   try {
  //     const response = await api.get('/api/customer/requests')
  //     return response.data
  //   } catch (error) {
  //     console.error('Error fetching requests:', error)
  //     throw error
  //   }
  // },

  async createRequest(data) {
    try {
      const response = await api.post('/api/customer/requests', data)
      return response.data
    } catch (error) {
      console.error('Error creating request:', error)
      throw error
    }
  },

  // async updateRequest(requestId, data) {
  //   try {
  //     const response = await api.put(`/api/customer/requests/${requestId}`, data)
  //     return response.data
  //   } catch (error) {
  //     console.error('Error updating request:', error)
  //     throw error
  //   }
  // },

  async closeRequest(requestId) {
    try {
      const response = await api.put(`/api/customer/requests/${requestId}/close`)
      return response.data
    } catch (error) {
      console.error('Error closing request:', error)
      throw error
    }
  },

  
  // Enhanced updateRequest method with additional parameters
  async updateRequest(requestId, data) {
    try {
      const response = await api.put(`/api/customer/requests/${requestId}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating request:', error);
      throw error;
    }
  },
  
  // Enhanced addReview method with additional parameters
  async addReview(requestId, reviewData) {
    try {
      const response = await api.post(`/api/customer/requests/${requestId}/review`, reviewData);
      return response.data;
    } catch (error) {
      console.error('Error adding review:', error);
      throw error;
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
  },
  
  async getReviews() {
    try {
      console.log('Fetching professional reviews')
      const response = await api.get('/api/professional/reviews')
      console.log('Retrieved reviews:', response.data.length)
      return response.data
    } catch (error) {
      console.error('Error fetching reviews:', error)
      throw error
    }
  },
  
  async updateAvailability(isAvailable) {
    try {
      console.log(`Updating availability to: ${isAvailable}`)
      const response = await api.put('/api/professional/availability', { is_available: isAvailable })
      console.log('Availability update response:', response.data)
      return response.data
    } catch (error) {
      console.error('Error updating availability:', error)
      throw error
    }
  },
  
  async confirmLocationExit(requestId) {
    try {
      console.log(`Confirming exit for request: ${requestId}`)
      const response = await api.post(`/api/professional/requests/${requestId}/exit-location`)
      console.log('Location exit confirmation response:', response.data)
      return response.data
    } catch (error) {
      console.error('Error confirming location exit:', error)
      throw error
    }
  }
}

export const adminAPI = {
  async getUsers(role = null) {
    try {
      console.log('Fetching users...');
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const params = role ? { role } : {};
      const response = await api.get('/api/admin/users', { params });
      
      // Ensure users have the 'name' property for display
      return response.data.map(user => {
        if (!user.name) {
          // Set a fallback name if none is provided
          user.name = user.username || `User ${user.id}`;
        }
        return user;
      });
    } catch (error) {
      console.error('Error fetching users:', error.response?.data || error.message);
      if (error.response?.status === 401) {
        console.log('Unauthorized. Please check your token.');
      }
      throw error;
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
      console.log('Fetching services...');
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await api.get('/api/admin/services');
      console.log('Services response:', response.data); // Add debugging
      
      // If backend already sends camelCase fields, return directly
      if (response.data && Array.isArray(response.data)) {
        // Make sure each service has the expected format
        return response.data.map(service => ({
          id: service.id,
          name: service.name,
          description: service.description || '',
          basePrice: service.basePrice || service.base_price,
          timeRequired: service.timeRequired || service.time_required,
          category: service.category || 'General',
          status: service.is_active !== false ? 'active' : 'inactive'
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Error fetching services:', error.response?.data || error.message);
      throw error;
    }
  },

  async createService(serviceData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const formattedData = {
        name: serviceData.name,
        description: serviceData.description,
        base_price: Number(serviceData.basePrice),
        time_required: Number(serviceData.timeRequired),
        category: serviceData.category || 'General'
      };

      const response = await api.post('/api/admin/services', formattedData, {
        headers: {
          'Authentication-Token': token
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating service:', error.response?.data || error);
      if (error.response?.status === 400) {
        throw new Error(`Validation error: ${error.response.data.message || 'Invalid data'}`);
      }
      throw error;
    }
  },

  async updateService(serviceId, serviceData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await api.put(`/api/admin/services/${serviceId}`, serviceData, {
        headers: {
          'Authentication-Token': token
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error updating service:', error);
      throw error;
    }
  },

  async deleteService(serviceId) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await api.delete(`/api/admin/services/${serviceId}`, {
        headers: {
          'Authentication-Token': token
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error deleting service:', error);
      throw error;
    }
  }
}

export default api
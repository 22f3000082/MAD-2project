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

// Add this interceptor at the top of your api.js
api.interceptors.request.use(config => {
  // Define routes that don't need authentication
  const publicRoutes = [
    '/auth/login', 
    '/auth/register', 
    '/auth/logout', 
    '/api/service-types', 
    '/api/services',
    '/api/services/public',
    '/api/customer/services'  // Add this as a public route
  ];
  
  // Check if the current request URL is for a public route
  const isPublicRoute = publicRoutes.some(route => config.url.includes(route));
  
  const token = localStorage.getItem('token');
  if (token) {
    // Flask-Security expects raw token without 'Bearer' prefix
    config.headers['Authentication-Token'] = token;
    
    // Only log non-sensitive requests to avoid exposing tokens in logs
    if (!config.url.includes('/auth/')) {
      console.log(`Request to ${config.url} with token available`);
    }
  } else if (!isPublicRoute) {
    console.warn(`No token found for request to: ${config.url}`);
    
    // Only redirect if the request is not already for a public route
    // and we're not on a public page
    const publicPaths = ['/login', '/register', '/'];
    if (!publicPaths.includes(window.location.pathname)) {
      console.log('Redirecting to login due to missing token');
      window.location.href = '/login';
    }
  }
  return config;
}, error => Promise.reject(error));

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    // Specific handling for CORS errors
    if (error.message === 'Network Error') {
      console.error('CORS or Network error detected:', error);
      console.log('Request details:', error.config?.url, error.config?.method);
      
      // Log available request headers for debugging
      if (error.config?.headers) {
        console.log('Request headers:', Object.keys(error.config.headers).map(k => `${k}: ${error.config.headers[k]}`));
      }
      
      return Promise.reject(new Error('Network error - This might be due to CORS issues or server unavailability.'));
    }
    
    console.error('Response error:', error.response?.data || error.message);
    
    if (error.response) {
      // Get current route before switch statement
      const currentPath = router.currentRoute.value?.path || router.currentRoute?.path;
      
      switch (error.response.status) {
        case 401:
          // Unauthorized - clear storage and redirect to login only if not already on login page
          console.log('401 Unauthorized response - clearing auth and redirecting');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          
          if (currentPath !== '/login') {
            router.push('/login').catch(err => {
              if (err.name !== 'NavigationDuplicated') {
                console.error('Navigation error when redirecting to login:', err);
              }
            });
          } else {
            console.log('Already on login page, not redirecting');
          }
          break;
        
        case 403:
          router.push('/');
          break;
          
        case 500:
          console.error('Server error:', error.response.data);
          break;
          
        default:
          // Handle other status codes
          break;
      }

      // Return the error message from the backend if available
      if (error.response.data?.message) {
        return Promise.reject(new Error(error.response.data.message));
      }
    }
    return Promise.reject(error);
  }
);

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
      // Check if credentials is empty or invalid
      if (!credentials || !credentials.email || !credentials.password) {
        console.error('Invalid login credentials:', credentials);
        throw new Error('Email and password are required');
      }
      
      console.log(`Attempting login for user: ${credentials.email}`);
      const response = await api.post('/auth/login', credentials);
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        // Simplified navigation
        const path = `/${response.data.user.role}/dashboard`;
        console.log(`Login successful, navigating to: ${path}`);
        router.push(path).catch(err => {
          console.error('Navigation error:', err);
        });
      }
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  },

  async logout() {
    try {
      await api.post('/auth/logout')
      localStorage.removeItem('token')
      localStorage.removeItem('user')

      // Only navigate if not already on login page
      if (router.currentRoute.value.path !== '/login') {
        // Use catch with explicit handling for NavigationDuplicated
        router.push('/login').catch(err => {
          // Only print errors other than NavigationDuplicated
          if (err.name !== 'NavigationDuplicated') {
            console.error('Navigation error:', err)
          }
        })
      }
    } catch (error) {
      console.error('Logout error:', error.response?.data || error.message)
      // Still clear local storage even if API call fails
      localStorage.removeItem('token')
      localStorage.removeItem('user')

      // Only navigate if not already on login page
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login').catch(err => {
          // Only print errors other than NavigationDuplicated
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
      console.log('Calling API for service categories...');
      
      // Try the dedicated service-types endpoint
      try {
        const response = await api.get('/api/service-types');
        console.log('Service types API response:', response.data);
        
        if (Array.isArray(response.data) && response.data.length > 0) {
          return response.data;
        } else {
          console.warn('Service types endpoint returned empty array or invalid data');
        }
      } catch (error) {
        console.error('Service types endpoint failed:', error.message);
      }
      
      // If the above fails, try the debug endpoint as fallback
      try {
        const debugResponse = await api.get('/api/debug/service-types');
        console.log('Debug service types response:', debugResponse.data);
        
        if (debugResponse.data.default_categories && 
            Array.isArray(debugResponse.data.default_categories) && 
            debugResponse.data.default_categories.length > 0) {
          return debugResponse.data.default_categories;
        }
      } catch (debugError) {
        console.error('Debug service types endpoint failed:', debugError.message);
      }
      
      // Final fallback: return hardcoded list
      console.warn('Falling back to hardcoded service types');
      return [
        'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
        'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
      ];
    } catch (error) {
      console.error('Error fetching service types:', error);
      // Return default categories instead of throwing
      return [
        'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
        'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
      ];
    }
  },
  
  async getServices() {
    try {
      console.log('Fetching services...');
      // Try multiple endpoints with fallback mechanism
      try {
        // First try the public services endpoint
        const response = await api.get('/api/services/public');
        console.log('Got services from public endpoint:', response.data.length);
        return response.data;
      } catch (error) {
        console.warn('Public services endpoint failed, trying customer endpoint:', error.message);
        
        try {
          // Then try customer services endpoint
          const customerResponse = await api.get('/api/customer/services');
          console.log('Got services from customer endpoint:', customerResponse.data.length);
          return customerResponse.data;
        } catch (error) {
          console.warn('Customer services endpoint failed, trying admin endpoint:', error.message);
          
          // Finally try admin services endpoint
          const adminResponse = await api.get('/api/admin/services');
          console.log('Got services from admin endpoint:', adminResponse.data.length);
          return adminResponse.data;
        }
      }
    } catch (error) {
      console.error('Error fetching services:', error);
      // Return empty array instead of throwing to prevent UI breaks
      return [];
    }
  },
  
  // Enhanced version of getPublicServices with multiple fallbacks
  async getPublicServices() {
    try {
      console.log('Fetching public services for customers...');
      
      // Try the dedicated public endpoint first
      try {
        const response = await api.get('/api/services/public');
        console.log(`Received ${response.data.length} public services from public endpoint`);
        return formatServiceData(response.data);
      } catch (publicError) {
        console.warn('Public services endpoint failed, trying regular services endpoint:', publicError.message);
        
        // Try the general services endpoint second
        try {
          const generalResponse = await api.get('/api/services');
          console.log(`Received ${generalResponse.data.length} services from general endpoint`);
          return formatServiceData(generalResponse.data);
        } catch (generalError) {
          console.warn('General services endpoint failed, trying customer services endpoint:', generalError.message);
          
          // Try customer-specific endpoint third
          try {
            const customerResponse = await api.get('/api/customer/services');
            console.log(`Received ${customerResponse.data.length} services from customer endpoint`);
            return formatServiceData(customerResponse.data);
          } catch (customerError) {
            console.warn('Customer services endpoint failed, trying admin endpoint as last resort:', customerError.message);
            
            // Last resort - try admin endpoint but only return active services
            const adminResponse = await api.get('/api/admin/services');
            console.log(`Received ${adminResponse.data.length} services from admin endpoint`);
            const activeServices = adminResponse.data.filter(service => 
              service.is_active === true || service.status === 'active'
            );
            console.log(`Filtered down to ${activeServices.length} active services`);
            return formatServiceData(activeServices);
          }
        }
      }
    } catch (error) {
      console.error('All attempts to fetch services failed:', error);
      throw new Error('Unable to load services. Please try again later.');
    }
  }
}

// Helper function to standardize service data format
function formatServiceData(services) {
  return services.map(service => ({
    id: service.id,
    name: service.name,
    description: service.description || '',
    base_price: service.base_price || service.basePrice || 0,
    time_required: service.time_required || service.timeRequired || 0,
    category: service.category || 'General',
    is_active: service.is_active !== false // Default to active if not specified
  }));
}

export const customerAPI = {
  async createRequest(data) {
    try {
      console.log('Creating service request with data:', data);
      
      // Validate the data before sending to server
      if (!data.pin_code) {
        throw new Error('PIN code is required');
      }
      
      if (!data.service_id && !data.category) {
        throw new Error('Either service_id or category is required');
      }
      
      const response = await api.post('/api/customer/requests', data);
      console.log('Service request created successfully:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error creating request:', error);
      // Enhanced error reporting
      if (error.response?.data?.error) {
        console.error('Backend error:', error.response.data.error);
        throw new Error(error.response.data.error);
      }
      throw error;
    }
  },
  
  async getRequests() {
    try {
      console.log('Fetching customer requests...');
      const response = await api.get('/api/customer/requests');
      console.log(`Received ${response.data.length} customer requests`);
      return response.data;
    } catch (error) {
      console.error('Error fetching customer requests:', error);
      // Add more detailed logging for debugging
      if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
      }
      throw error;
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
  },

  async getAvailableServices() {
    try {
      console.log('Fetching available services...');
      const response = await api.get('/api/customer/services');
      return response.data.map(service => ({
        id: service.id,
        name: service.name,
        description: service.description,
        base_price: service.base_price,
        time_required: service.time_required,
        category: service.category
      }));
    } catch (error) {
      console.error('Error fetching services:', error);
      throw error;
    }
  },
}

export const professionalAPI = {
  async getAssignments(status = null) {
    try {
      // Check auth token before making request
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No authentication token found for getAssignments call');
        throw new Error('No authentication token found');
      }
      
      console.log('Fetching professional assignments', status ? `with status: ${status}` : '');
      const params = status ? { status } : {};
      
      // Add debugging to trace the exact API call
      console.log(`API call URL: /api/professional/assignments`, params);
      
      // Use standard timeout of 30 seconds
      const response = await api.get('/api/professional/assignments', { 
        params,
        headers: {
          'Authentication-Token': token
        },
        timeout: 30000
      });
      
      // Log the full response for debugging
      console.log(`Received assignments response:`, response);
      console.log(`Response data:`, response.data);
      
      // Always return an array, even if the response is irregular
      if (!response.data) {
        console.error('Empty response data for assignments');
        return [];
      }
      
      // Validate response data structure
      if (Array.isArray(response.data)) {
        // Enhance response data to ensure all needed fields exist
        return response.data.map(req => {
          // Add default values if the required fields are missing
          if (!req.service) {
            console.warn(`Assignment ${req.id} is missing service data`);
            req.service = { name: 'Unknown Service', base_price: 0 };
          }
          
          if (!req.customer) {
            console.warn(`Assignment ${req.id} is missing customer data`);
            req.customer = { customer_name: 'Unknown Customer' };
          }
          
          return req;
        });
      }
      
      console.error('Unexpected response format:', response.data);
      return [];
    } catch (error) {
      console.error('Error fetching assignments:', error);
      // Return empty array instead of throwing to prevent dashboard from breaking
      return [];
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
      // Check auth token before making request
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      
      console.log('Fetching professional profile');
      const response = await api.get('/api/professional/profile');
      console.log('Retrieved profile data');
      return response.data;
    } catch (error) {
      console.error('Error fetching profile:', error);
      // Return basic profile instead of throwing to prevent dashboard from breaking
      return {
        professional_name: 'Professional',
        service_type: 'Not specified',
        description: '',
        experience: 0,
        is_approved: false,
        average_rating: 0,
        total_reviews: 0
      };
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
      // Check auth token before making request
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      
      console.log('Fetching professional reviews');
      const response = await api.get('/api/professional/reviews');
      console.log('Retrieved reviews:', response.data.length);
      return response.data;
    } catch (error) {
      console.error('Error fetching reviews:', error);
      // Return empty array instead of throwing
      return [];
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
  },
  
  /* eslint-disable no-dupe-keys */
  // Fetch ALL available service requests from the database
  async getAvailableRequests() {
    try {
      // Check auth token before making request
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No authentication token found for getAvailableRequests call');
        throw new Error('No authentication token found');
      }
      
      console.log('Fetching available service requests');
      console.log(`API call URL: /api/professional/available-requests`);
      
      // Try to get requests from the primary endpoint
      let response;
      try {
        response = await api.get('/api/professional/available-requests', {
          headers: {
            'Authentication-Token': token
          },
          timeout: 30000
        });
        console.log(`Primary endpoint returned ${response.data?.length || 0} requests`);
      } catch (primaryError) {
        console.error('Primary endpoint failed, trying fallback:', primaryError);
        
        // If primary endpoint fails, try the debug endpoint
        response = await api.get('/api/professional/all-pending-requests', {
          headers: {
            'Authentication-Token': token
          },
          timeout: 30000
        });
        
        // Transform the response to match expected format
        if (response.data?.requests) {
          console.log(`Fallback endpoint returned ${response.data.requests.length} requests`);
          response.data = response.data.requests;
        }
      }
      
      // Log the full response for debugging
      console.log(`Received available requests:`, response.data);
      
      // Provide sensible defaults for missing data
      if (Array.isArray(response.data)) {
        return response.data.map(req => {
          // Create consistent request objects
          const enhancedRequest = {
            ...req,
            // Ensure service object exists
            service: req.service || req.service_info || { 
              name: 'Unknown Service', 
              base_price: 0,
              description: ''
            },
            // Ensure customer object exists
            customer: req.customer || req.customer_info || { 
              customer_name: 'Customer',
              phone: 'Available after accepting'
            },
            // Add UI flags
            isNewRequest: true
          };
          
          return enhancedRequest;
        });
      }
      
      console.error('Unexpected response format for available requests:', response.data);
      return [];
    } catch (error) {
      console.error('Error fetching available requests:', error);
      // Return empty array instead of throwing
      return [];
    }
  },
  
  // Add a new method to get ALL pending requests (for debugging)
  async getAllPendingRequests() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      
      console.log('Fetching ALL pending service requests (debug)');
      const response = await api.get('/api/professional/all-pending-requests', {
        headers: {
          'Authentication-Token': token
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error fetching all pending requests:', error);
      return { total_count: 0, requests: [] };
    }
  },
  
  /* eslint-enable no-dupe-keys */

  async addRejectionReason(requestId, reason) {
    try {
      console.log(`Adding rejection reason for request ${requestId}: ${reason}`);
      
      // Enhanced error handling and logging
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Authentication required');
      }
      
      // Make sure request has proper payload format
      const payload = { reason };
      
      // Add explicit timeout and headers
      const response = await api.post(`/api/professional/requests/${requestId}/reject-reason`, payload, {
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': token
        },
        timeout: 10000
      });
      
      console.log('Rejection reason added:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error adding rejection reason:', error);
      // Provide more detailed error for debugging
      if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
      }
      throw error;
    }
  },
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
          base_price: service.base_price || service.basePrice,
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
        base_price: Number(serviceData.base_price),
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

  async update_service(serviceId, serviceData) {
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

  async deleteService(service_id) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await api.delete(`/api/admin/services/${service_id}`, {
            headers: {
                'Authentication-Token': token
            }
        });
        // return response.data;
      
      
        // Check response status
        if (response.data.status === 'deactivated') {
            return {
                success: true,
                wasDeactivated: true,
                message: response.data.message
            };
        }

        return {
            success: true,
            wasDeactivated: false,
            message: response.data.message
        };
      
    } catch (error) {
        console.error('Error deleting service:', error);
        throw new Error(error.response?.data?.message || 'Failed to delete service');
    }
},
  
  async getServiceRequests(params = {}) {
    try {
      console.log('Fetching service requests...');
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await api.get('/api/admin/requests', { params });
      console.log(`Retrieved ${response.data.length} service requests`);
      return response.data;
    } catch (error) {
      console.error('Error fetching service requests:', error.response?.data || error.message);
      throw error;
    }
  },

  // async deleteService(service_id) {
  //   try {
  //       const token = localStorage.getItem('token');
  //       if (!token) {
  //           throw new Error('Authentication required');
  //       }

  //       const response = await api.delete(`/api/admin/services/${service_id}`, {
  //           headers: {
  //               'Authentication-Token': token
  //           }
  //       });

  //       return response.data;
  //   } catch (error) {
  //       console.error('Delete service error:', error.response || error);
  //       throw new Error(error.response?.data?.message || 'Failed to delete service');
  //   }
  // }
}

// Export individual functions for components that import them directly
export const getServices = async () => {
  return serviceAPI.getServices();
};

export const getProfile = async () => {
  return professionalAPI.getProfile();
};

export const getAssignments = async () => {
  return professionalAPI.getAssignments();
};

export const getReviews = async () => {
  return professionalAPI.getReviews();
};

export const getAvailableRequests = async () => {
  return professionalAPI.getAvailableRequests();
};

export default api
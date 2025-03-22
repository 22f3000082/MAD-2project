<template>
  <div class="service-list">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading services...</p>
    </div>
    
    <div v-else-if="services.length === 0" class="text-center py-5">
      <i class="fas fa-search fa-3x text-muted mb-3"></i>
      <h5>No services found</h5>
      <p class="text-muted">{{ emptyMessage }}</p>
    </div>
    
    <div v-else class="row g-4">
      <div v-for="service in services" :key="service.id" class="col-md-4">
        <div class="card h-100 service-card">
          <div class="card-body">
            <div class="service-category mb-2">
              <span class="badge bg-light text-dark">{{ service.category }}</span>
            </div>
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ truncateDescription(service.description) }}</p>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="price">₹{{ service.base_price }}</span>
              <span class="time text-muted"><i class="far fa-clock me-1"></i>{{ service.time_required }} min</span>
            </div>
            
            <div class="d-grid gap-2">
              <button class="btn btn-outline-primary" @click="viewDetails(service)">
                <i class="fas fa-info-circle me-1"></i> View Details
              </button>
              <button class="btn btn-primary" @click="requestService(service)">
                <i class="fas fa-calendar-plus me-1"></i> Book Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="hasMore && !loading" class="text-center mt-4">
      <button class="btn btn-outline-primary" @click="loadMore">
        <i class="fas fa-sync me-1"></i> Load More
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ServiceList',
  props: {
    services: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    hasMore: {
      type: Boolean,
      default: false
    },
    emptyMessage: {
      type: String,
      default: 'Try adjusting your search criteria'
    }
  },
  emits: ['view-details', 'request-service', 'load-more'],
  setup(props, { emit }) {
    const truncateDescription = (description) => {
      if (!description) return '';
      return description.length > 80 
        ? description.substring(0, 80) + '...' 
        : description;
    };
    
    const viewDetails = (service) => {
      emit('view-details', service);
    };
    
    const requestService = (service) => {
      emit('request-service', service);
    };
    
    const loadMore = () => {
      emit('load-more');
    };
    
    return {
      truncateDescription,
      viewDetails,
      requestService,
      loadMore
    };
  }
};
</script>

<style scoped>
.service-card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.card-title {
  font-weight: 600;
}

.price {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0d6efd;
}

.service-category {
  position: relative;
}
</style>

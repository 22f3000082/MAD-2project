<template>
  <div class="service-list">
    <!-- Empty State -->
    <div v-if="!loading && (!services || services.length === 0)" class="text-center py-5">
      <div class="empty-state">
        <i class="fas fa-search fa-3x text-muted mb-3"></i>
        <h5>No services found</h5>
        <p class="text-muted">Try adjusting your search filters</p>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-else-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Finding services for you...</p>
    </div>
    
    <!-- Service Grid -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div v-for="service in services" :key="service.id" class="col">
        <div class="card h-100 service-card">
          <div class="card-category-badge" :style="{ backgroundColor: getCategoryColor(service.category) }">
            {{ service.category }}
          </div>
          
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <h5 class="card-title">{{ service.name }}</h5>
              <span class="price-badge">₹{{ service.base_price }}</span>
            </div>
            
            <div class="service-meta my-3">
              <span class="meta-item"><i class="far fa-clock me-1"></i> {{ service.time_required || 60 }} mins</span>
              <span class="meta-item" v-if="service.rating">
                <i class="fas fa-star text-warning me-1"></i> {{ service.rating }}
              </span>
            </div>
            
            <p class="card-text service-description">{{ service.description || 'No description available' }}</p>
            
            <div class="service-features mt-3" v-if="service.features && service.features.length">
              <span v-for="feature in service.features" :key="feature" class="feature-badge">
                {{ feature }}
              </span>
            </div>
          </div>
          
          <div class="card-footer bg-transparent border-0">
            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary flex-grow-1" @click="$emit('view-details', service)">
                <i class="fas fa-info-circle me-1"></i> Details
              </button>
              <button class="btn btn-primary flex-grow-1" @click="$emit('request-service', service)">
                <i class="fas fa-plus me-1"></i> Request
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Load More Button -->
    <div v-if="!loading && hasMore && services.length > 0" class="text-center mt-4">
      <button class="btn btn-outline-primary" @click="$emit('load-more')">
        <i class="fas fa-spinner me-1"></i> Load More Services
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
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    hasMore: {
      type: Boolean,
      default: false
    }
  },
  emits: ['view-details', 'request-service', 'load-more'],
  setup() {
    // Category color mapping for visual variety
    const categoryColors = {
      'AC Repair': '#4CAF50',
      'Plumbing': '#2196F3',
      'Electrical': '#FFC107',
      'Carpentry': '#795548',
      'Painting': '#9C27B0',
      'Cleaning': '#03A9F4',
      'Pest Control': '#F44336',
      'Appliance Repair': '#FF9800',
      'Moving Services': '#607D8B',
      'Gardening': '#8BC34A'
    };
    
    const getCategoryColor = (category) => {
      return categoryColors[category] || '#9E9E9E'; // Default gray
    };
    
    return {
      getCategoryColor
    };
  }
};
</script>

<style scoped>
.service-card {
  border: none;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.card-category-badge {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 0.75rem;
  padding: 0.35rem 0.8rem;
  color: white;
  border-bottom-left-radius: 8px;
}

.price-badge {
  
  background-color: #e3f2fd;
  color: #011646;
  padding: 0.35rem 0.7rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 1rem;
}

.service-meta {
  display: flex;
  gap: 12px;
  font-size: 0.85rem;
  color: #6c757d;
}

.meta-item {
  display: flex;
  align-items: center;
}

.service-description {
  height: 3em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #6c757d;
}

.service-features {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.feature-badge {
  font-size: 0.7rem;
  background-color: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: #495057;
}

.empty-state {
  padding: 3rem 1rem;
  background-color: #f8f9fa;
  border-radius: 12px;
}

.card-footer {
  padding: 1rem;
}

.btn {
  border-radius: 6px;
  padding: 0.5rem 1rem;
}
</style>

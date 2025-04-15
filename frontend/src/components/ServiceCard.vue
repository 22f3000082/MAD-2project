<template>
  <div class="card h-100 shadow-sm" @click="$emit('click')">
    <div class="card-body text-center">
      <div class="service-icon mb-3">
        <i :class="['fas', serviceIcon, 'fa-3x', 'text-primary']"></i>
      </div>
      <h3 class="card-title">{{ service.name }}</h3>
      <p class="card-text text-muted">{{ service.description }}</p>
      <div class="d-flex justify-content-between align-items-center mt-3">
        <span class="text-primary fw-bold">₹{{ service.base_price }}</span>
        <span class="badge bg-light text-dark">{{ service.time_required }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ServiceCard',
  props: {
    service: {
      type: Object,
      required: true,
      validator: (service) => {
        return service.name && service.base_price !== undefined
      }
    }
  },
  computed: {
    serviceIcon() {
      // Map service types to Font Awesome icons
      const iconMap = {
        'cleaning': 'fa-broom',
        'plumbing': 'fa-wrench',
        'electrical': 'fa-bolt',
        'carpentry': 'fa-hammer',
        'painting': 'fa-paint-roller',
        'gardening': 'fa-leaf',
        'default': 'fa-tools'
      }
      // return iconMap[this.service.type?.toLowerCase()] || iconMap.default
      return iconMap[this.service.type ? this.service.type.toLowerCase() : 'default'];

    }
  }
}
</script>

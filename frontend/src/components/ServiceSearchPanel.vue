<template>
  <div class="service-search-panel">
    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <h5 class="card-title mb-3">Find Services</h5>
        <div class="row g-3">
          <div class="col-md-4">
            <div class="input-group">
              <span class="input-group-text">
                <i class="fas fa-search"></i>
              </span>
              <input
                type="text"
                class="form-control"
                v-model="searchParams.name"
                placeholder="Service name..."
                @input="emitSearch"
              >
            </div>
          </div>
          <div class="col-md-4">
            <div class="input-group">
              <span class="input-group-text">
                <i class="fas fa-map-marker-alt"></i>
              </span>
              <input
                type="text"
                class="form-control"
                v-model="searchParams.pinCode"
                placeholder="PIN code..."
                @input="emitSearch"
              >
            </div>
          </div>
          <div class="col-md-4">
            <select class="form-select" v-model="searchParams.category" @change="emitSearch">
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="mt-3">
          <div class="accordion" id="accordionFilters">
            <div class="accordion-item border-0">
              <h2 class="accordion-header" id="headingAdvanced">
                <button class="accordion-button collapsed p-0 bg-transparent shadow-none" type="button" 
                        data-bs-toggle="collapse" data-bs-target="#collapseAdvanced" 
                        aria-expanded="false" aria-controls="collapseAdvanced">
                  <small>Advanced Filters</small>
                </button>
              </h2>
              <div id="collapseAdvanced" class="accordion-collapse collapse" 
                   aria-labelledby="headingAdvanced" data-bs-parent="#accordionFilters">
                <div class="accordion-body px-0 pt-3">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">Price Range</label>
                      <div class="d-flex gap-2">
                        <input type="number" class="form-control" placeholder="Min" 
                               v-model="searchParams.priceMin" @input="emitSearch">
                        <input type="number" class="form-control" placeholder="Max"
                               v-model="searchParams.priceMax" @input="emitSearch">
                      </div>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Sort By</label>
                      <select class="form-select" v-model="searchParams.sortBy" @change="emitSearch">
                        <option value="">Default</option>
                        <option value="price_asc">Price: Low to High</option>
                        <option value="price_desc">Price: High to Low</option>
                        <option value="rating">Rating</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch } from 'vue';
import { serviceAPI } from '@/services/api';

export default {
  name: 'ServiceSearchPanel',
  props: {
    initialParams: {
      type: Object,
      default: () => ({})
    },
    categories: {
      type: Array,
      default: () => []
    }
  },
  emits: ['search'],
  setup(props, { emit }) {
    const searchParams = reactive({
      name: props.initialParams.name || '',
      pinCode: props.initialParams.pinCode || '',
      category: props.initialParams.category || '',
      priceMin: props.initialParams.priceMin || '',
      priceMax: props.initialParams.priceMax || '',
      sortBy: props.initialParams.sortBy || ''
    });

    const emitSearch = () => {
      emit('search', { ...searchParams });
    };

    // Watch for prop changes
    watch(() => props.initialParams, (newParams) => {
      Object.keys(newParams).forEach(key => {
        if (searchParams[key] !== undefined) {
          searchParams[key] = newParams[key];
        }
      });
    }, { deep: true });

    return {
      searchParams,
      emitSearch
    };
  }
};
</script>

<style scoped>
.accordion-button:not(.collapsed)::after {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%230d6efd'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
}

.accordion-button.collapsed::after {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%230d6efd'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
}
</style>

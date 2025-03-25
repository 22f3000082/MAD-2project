<template>
  <div class="service-category-selector">
    <label :for="id" class="form-label">{{ label }}</label>
    <div class="input-group">
      <select 
        :id="id" 
        v-model="selectedCategory" 
        class="form-select" 
        :required="required"
        :disabled="loading || disabled"
        @change="onChange"
      >
        <option value="" disabled selected>{{ placeholder }}</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <button 
        v-if="showRefreshButton" 
        class="btn btn-outline-secondary" 
        type="button" 
        @click="fetchCategories" 
        :disabled="loading"
      >
        <i class="fas fa-sync" :class="{'fa-spin': loading}"></i>
      </button>
    </div>
    <div v-if="loading" class="text-muted small mt-1">
      Loading categories...
    </div>
    <div v-if="error" class="text-danger small mt-1">
      {{ error }}
    </div>
    <div v-if="debug && categories.length > 0" class="text-muted small mt-1">
      {{ categories.length }} categories available
    </div>
  </div>
</template>

<script>
import { serviceAPI } from '@/services/api';

export default {
  name: 'ServiceCategorySelector',
  props: {
    value: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      default: 'service-category'
    },
    label: {
      type: String,
      default: 'Service Category'
    },
    placeholder: {
      type: String,
      default: 'Select service category'
    },
    required: {
      type: Boolean,
      default: true
    },
    disabled: {
      type: Boolean,
      default: false
    },
    showRefreshButton: {
      type: Boolean,
      default: false
    },
    debug: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selectedCategory: this.value,
      categories: [],
      loading: false,
      error: null,
      // Default categories as fallback
      defaultCategories: [
        'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
        'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
      ]
    };
  },
  watch: {
    value(newValue) {
      this.selectedCategory = newValue;
    },
    selectedCategory(newValue) {
      this.$emit('input', newValue);
      this.$emit('change', newValue);
    }
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Fetching service categories...');
        const categories = await serviceAPI.getServiceTypes();
        console.log('Received categories:', categories);
        
        if (Array.isArray(categories) && categories.length > 0) {
          this.categories = categories;
        } else {
          console.warn('Empty or invalid categories received, using defaults');
          this.categories = [...this.defaultCategories];
          this.error = 'Could not load categories from server, using defaults';
        }
      } catch (error) {
        console.error('Error fetching service categories:', error);
        this.error = 'Failed to load categories';
        // Fall back to default categories
        this.categories = [...this.defaultCategories];
      } finally {
        this.loading = false;
      }
    },
    onChange() {
      this.$emit('change', this.selectedCategory);
    }
  }
};
</script>

<style scoped>
.service-category-selector {
  margin-bottom: 1rem;
}
</style>

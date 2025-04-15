<template>
  <div class="app-update" v-if="updateAvailable">
    <div class="update-container">
      <div class="update-content">
        <div class="update-icon">
          <i class="fas fa-sync-alt"></i>
        </div>
        <div class="update-info">
          <h4>Update Available</h4>
          <p>A new version of the app is available.</p>
        </div>
        <button class="btn btn-primary update-btn" @click="refreshApp">
          Update Now
        </button>
        <button class="btn btn-link dismiss-btn" @click="dismissUpdate">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppUpdate',
  data() {
    return {
      updateAvailable: false,
      registration: null
    }
  },
  created() {
    document.addEventListener('swUpdated', this.showUpdateUI, { once: true });
    
    // When the component is created, check for existing update event that might
    // have been fired before this component was created
    navigator.serviceWorker.getRegistration().then((registration) => {
      if (registration && registration.waiting) {
        // There's an update waiting
        this.updateAvailable = true;
        this.registration = registration;
      }
    });
  },
  methods: {
    showUpdateUI(event) {
      this.registration = event.detail;
      this.updateAvailable = true;
    },
    
    dismissUpdate() {
      this.updateAvailable = false;
    },
    
    refreshApp() {
      if (!this.registration || !this.registration.waiting) {
        window.location.reload();
        return;
      }
      
      // Send a message to the waiting service worker
      this.registration.waiting.postMessage({ type: 'SKIP_WAITING' });
      
      // The app will refresh when the next 'controllerchange' event occurs
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
      });
    }
  }
}
</script>

<style scoped>
.app-update {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.update-container {
  padding: 15px;
  max-width: 600px;
  margin: 0 auto;
}

.update-content {
  display: flex;
  align-items: center;
  position: relative;
}

.update-icon {
  flex: 0 0 40px;
  margin-right: 15px;
  font-size: 24px;
  color: #4A90E2;
}

.update-info {
  flex: 1;
}

.update-info h4 {
  margin: 0 0 5px;
  font-size: 16px;
  font-weight: 600;
}

.update-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.update-btn {
  padding: 8px 15px;
  margin-left: 10px;
  white-space: nowrap;
}

.dismiss-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: none;
  border: none;
  font-size: 16px;
  color: #999;
  cursor: pointer;
}

@media (max-width: 576px) {
  .update-content {
    flex-wrap: wrap;
  }
  
  .update-info {
    flex: 1 0 calc(100% - 60px);
    margin-bottom: 10px;
  }
  
  .update-btn {
    width: 100%;
    margin-left: 0;
    margin-top: 10px;
  }
}
</style> 
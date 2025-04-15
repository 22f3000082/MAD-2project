<template>
  <div class="add-to-home" v-if="isVisible">
    <div class="add-to-home-container">
      <div class="add-to-home-content">
        <div class="app-icon">
          <img src="/img/icons/android-chrome-192x192.png" alt="App Icon">
        </div>
        <div class="app-info">
          <h4>Install A-Z Services</h4>
          <p>Add to your home screen for easy access</p>
        </div>
        <button class="btn btn-primary install-btn" @click="installApp">
          Add to Home Screen
        </button>
        <button class="btn btn-link dismiss-btn" @click="dismiss">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddToHomeScreen',
  data() {
    return {
      deferredPrompt: null,
      isVisible: false,
      dismissed: false
    }
  },
  mounted() {
    // Check if user has previously dismissed or installed
    const installState = localStorage.getItem('a2hsState');
    if (installState === 'dismissed' || installState === 'installed') {
      this.dismissed = true;
      return;
    }

    // Listen for the beforeinstallprompt event
    window.addEventListener('beforeinstallprompt', this.capturePrompt);
    
    // Check if the app is already installed
    window.addEventListener('appinstalled', this.appInstalled);
  },
  beforeDestroy() {
    window.removeEventListener('beforeinstallprompt', this.capturePrompt);
    window.removeEventListener('appinstalled', this.appInstalled);
  },
  methods: {
    capturePrompt(e) {
      // Prevent Chrome 67 and earlier from automatically showing the prompt
      e.preventDefault();
      
      // Store the event for later use
      this.deferredPrompt = e;
      
      // Show our custom UI
      setTimeout(() => {
        if (!this.dismissed) {
          this.isVisible = true;
        }
      }, 3000); // Show after 3 seconds
    },
    
    installApp() {
      if (!this.deferredPrompt) return;
      
      // Hide our custom UI
      this.isVisible = false;
      
      // Show the browser install prompt
      this.deferredPrompt.prompt();
      
      // Wait for the user to respond
      this.deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the A2HS prompt');
          localStorage.setItem('a2hsState', 'installed');
        } else {
          console.log('User dismissed the A2HS prompt');
          localStorage.setItem('a2hsState', 'dismissed');
        }
        
        // Reset the deferred prompt
        this.deferredPrompt = null;
      });
    },
    
    dismiss() {
      this.isVisible = false;
      this.dismissed = true;
      localStorage.setItem('a2hsState', 'dismissed');
    },
    
    appInstalled(e) {
      console.log('App was installed', e);
      localStorage.setItem('a2hsState', 'installed');
      this.isVisible = false;
    }
  }
}
</script>

<style scoped>
.add-to-home {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: transform 0.3s ease;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.add-to-home-container {
  padding: 15px;
  max-width: 600px;
  margin: 0 auto;
}

.add-to-home-content {
  display: flex;
  align-items: center;
  position: relative;
}

.app-icon {
  flex: 0 0 50px;
  margin-right: 15px;
}

.app-icon img {
  width: 50px;
  height: 50px;
  border-radius: 10px;
}

.app-info {
  flex: 1;
}

.app-info h4 {
  margin: 0 0 5px;
  font-size: 16px;
  font-weight: 600;
}

.app-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.install-btn {
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

/* Responsive styles */
@media (max-width: 576px) {
  .add-to-home-content {
    flex-wrap: wrap;
  }
  
  .app-info {
    flex: 1 0 calc(100% - 70px);
    margin-bottom: 10px;
  }
  
  .install-btn {
    width: 100%;
    margin-left: 0;
    margin-top: 10px;
  }
}
</style> 
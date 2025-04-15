import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import './assets/global.css'
import './registerServiceWorker'
// import { setBackgroundImage } from './utils/setBackground';

const token = localStorage.getItem('token'); // Ensure this is not null

// Configure axios defaults
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8080'
axios.defaults.headers.common['Content-Type'] = 'application/json'
// In your frontend API calls:
// axios.defaults.headers.common['Authentication-Token'] = `Bearer ${token}`;
axios.defaults.headers.common['Authentication-Token'] = token;
// Add axios to Vue prototype
axios.defaults.withCredentials = true
Vue.prototype.$axios = axios

// Configure Vue
Vue.config.productionTip = false

// Create Vue instance
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

// Add to home screen functionality
let deferredPrompt;
const addBtn = document.createElement('button');
addBtn.style.display = 'none';
addBtn.className = 'add-to-home-btn';
addBtn.textContent = 'Add to Home Screen';

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent Chrome 67 and earlier from automatically showing the prompt
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  // Update UI to notify the user they can add to home screen
  addBtn.style.display = 'block';

  addBtn.addEventListener('click', () => {
    // Hide our user interface that shows our A2HS button
    addBtn.style.display = 'none';
    // Show the prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the A2HS prompt');
      } else {
        console.log('User dismissed the A2HS prompt');
      }
      deferredPrompt = null;
    });
  });
  
  // Add the button to the DOM
  document.body.appendChild(addBtn);
});

// setBackgroundImage('.home-container', './assets/images/bg.jpg');
// setBackgroundImage('.login-container', './assets/images/bg.jpg');
// setBackgroundImage('.register-container', './assets/images/bg.jpg');

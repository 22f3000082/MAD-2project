import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

// Configure axios defaults
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8080'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Add axios to Vue prototype
Vue.prototype.$axios = axios

// Configure Vue
Vue.config.productionTip = false

// Create Vue instance
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

"use strict";(self["webpackChunkhousehold_services"]=self["webpackChunkhousehold_services"]||[]).push([[102],{102:(e,t,r)=>{r.r(t),r.d(t,{default:()=>m});var s=function(){var e=this,t=e._self._c;return t("div",{staticClass:"home"},[t("section",{staticClass:"hero bg-primary text-white py-5"},[t("div",{staticClass:"container"},[t("div",{staticClass:"row justify-content-center text-center"},[t("div",{staticClass:"col-md-8"},[t("h1",{staticClass:"display-4 mb-4"},[e._v("Welcome to A-Z Household Services")]),t("p",{staticClass:"lead mb-4"},[e._v("Find and book professional services for your home with ease")]),t("div",{staticClass:"d-flex justify-content-center gap-3"},[e.isLoggedIn?t("router-link",{staticClass:"btn btn-light btn-lg",attrs:{to:e.dashboardRoute}},[e._v("Go to Dashboard")]):t("router-link",{staticClass:"btn btn-light btn-lg",attrs:{to:"/register"}},[e._v("Get Started")])],1)])])])]),t("section",{staticClass:"services py-5"},[t("div",{staticClass:"container"},[t("h2",{staticClass:"text-center mb-5"},[e._v("Our Services")]),t("div",{staticClass:"row g-4"},e._l(e.services,(function(r){return t("div",{key:r.id,staticClass:"col-md-4"},[t("service-card",{attrs:{service:r},on:{click:function(t){return e.handleServiceClick(r)}}})],1)})),0)])]),e._m(0)])},a=[function(){var e=this,t=e._self._c;return t("section",{staticClass:"features bg-light py-5"},[t("div",{staticClass:"container"},[t("h2",{staticClass:"text-center mb-5"},[e._v("Why Choose Us")]),t("div",{staticClass:"row g-4"},[t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"text-center"},[t("i",{staticClass:"fas fa-check-circle fa-3x text-primary mb-3"}),t("h4",[e._v("Verified Professionals")]),t("p",[e._v("All our service providers are thoroughly vetted and verified")])])]),t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"text-center"},[t("i",{staticClass:"fas fa-clock fa-3x text-primary mb-3"}),t("h4",[e._v("Quick Service")]),t("p",[e._v("Get your service requests handled promptly")])])]),t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"text-center"},[t("i",{staticClass:"fas fa-star fa-3x text-primary mb-3"}),t("h4",[e._v("Quality Assured")]),t("p",[e._v("Rated and reviewed by our community")])])])])])])}],o=function(){var e=this,t=e._self._c;return t("div",{staticClass:"card h-100 shadow-sm",on:{click:function(t){return e.$emit("click")}}},[t("div",{staticClass:"card-body text-center"},[t("div",{staticClass:"service-icon mb-3"},[t("i",{class:["fas",e.serviceIcon,"fa-3x","text-primary"]})]),t("h3",{staticClass:"card-title"},[e._v(e._s(e.service.name))]),t("p",{staticClass:"card-text text-muted"},[e._v(e._s(e.service.description))]),t("div",{staticClass:"d-flex justify-content-between align-items-center mt-3"},[t("span",{staticClass:"text-primary fw-bold"},[e._v("₹"+e._s(e.service.base_price))]),t("span",{staticClass:"badge bg-light text-dark"},[e._v(e._s(e.service.time_required))])])])])},c=[];const i={name:"ServiceCard",props:{service:{type:Object,required:!0,validator:e=>e.name&&void 0!==e.base_price}},computed:{serviceIcon(){const e={cleaning:"fa-broom",plumbing:"fa-wrench",electrical:"fa-bolt",carpentry:"fa-hammer",painting:"fa-paint-roller",gardening:"fa-leaf",default:"fa-tools"};return e[this.service.type?this.service.type.toLowerCase():"default"]}}},n=i;var l=r(656),d=(0,l.A)(n,o,c,!1,null,"252f26ec",null);const u=d.exports;var v=r(844);const h={name:"Home",components:{ServiceCard:u},data(){return{services:[],isLoading:!1,error:null}},computed:{isLoggedIn(){return!!localStorage.getItem("token")},dashboardRoute(){const e=JSON.parse(localStorage.getItem("user")||"{}");return`/${e.role}/dashboard`}},methods:{async fetchServices(){try{this.isLoading=!0,this.services=await(0,v.getServices)()}catch(e){this.error="Failed to load services",console.error("Error fetching services:",e)}finally{this.isLoading=!1}},handleServiceClick(e){this.isLoggedIn?this.$router.push({name:"ServiceRequest",params:{serviceId:e.id}}):this.$router.push("/login")}},created(){this.fetchServices()}},p=h;var g=(0,l.A)(p,s,a,!1,null,"e332ee6a",null);const m=g.exports},844:(e,t,r)=>{r.d(t,{Er:()=>l,YR:()=>i,xZ:()=>n,y1:()=>c});var s=r(194),a=r(997);const o=s.A.create({baseURL:"http://localhost:8080",headers:{"Content-Type":"application/json",Accept:"application/json"},withCredentials:!0});o.interceptors.request.use((e=>{const t=localStorage.getItem("token");return t&&(e.headers["Authorization"]=`Bearer ${t}`),e}),(e=>(console.error("Request error:",e),Promise.reject(e)))),o.interceptors.response.use((e=>e),(e=>{if(console.error("Response error:",e.response?.data||e.message),e.response){switch(e.response.status){case 401:localStorage.removeItem("token"),localStorage.removeItem("user"),a.A.push("/login");break;case 403:a.A.push("/");break;case 500:console.error("Server error:",e.response.data);break}if(e.response.data&&e.response.data.message)return Promise.reject(new Error(e.response.data.message))}return Promise.reject(e)}));const c={async register(e){try{if("professional"===e.role&&!e.service_type)throw new Error("Professionals must select a service type.");console.log("Sending registration data:",e);const t=await o.post("/auth/register",e);return console.log("Registration response:",t.data),t.data}catch(t){throw console.error("Registration error:",t.response?.data||t.message),t.response?.data||{message:"Registration failed. Please try again."}}},async login(e){try{console.log("Attempting login:",e);const t=await o.post("/auth/login",e);if(console.log("Login response:",t.data),t.data.token){localStorage.setItem("token",t.data.token),localStorage.setItem("user",JSON.stringify(t.data.user));const e=t.data.user;a.A.push(`/${e.role}/dashboard`)}return t.data}catch(t){throw console.error("Login error:",t.response?.data||t.message),t}},async logout(){try{await o.post("/auth/logout"),localStorage.removeItem("token"),localStorage.removeItem("user"),a.A.push("/login")}catch(e){console.error("Logout error:",e.response?.data||e.message),localStorage.removeItem("token"),localStorage.removeItem("user"),a.A.push("/login")}},getCurrentUser(){const e=localStorage.getItem("user");return e?JSON.parse(e):null}},i={async getServices(e={}){try{const t=await o.get("/api/services",{params:e});return t.data}catch(t){throw console.error("Error fetching services:",t),t}},async mounted(){try{this.services=await this.searchServices(),console.log("Services loaded:",this.services)}catch(e){console.error("Failed to load services:",e)}},async getServiceById(e){try{const t=await o.get(`/api/services/${e}`);return t.data}catch(t){throw console.error("Error fetching service:",t),t}}},n={async getRequests(){try{const e=await o.get("/api/customer/requests");return e.data}catch(e){throw console.error("Error fetching requests:",e),e}},async createRequest(e){try{const t=await o.post("/api/customer/requests",e);return t.data}catch(t){throw console.error("Error creating request:",t),t}},async updateRequest(e,t){try{const r=await o.put(`/api/customer/requests/${e}`,t);return r.data}catch(r){throw console.error("Error updating request:",r),r}},async closeRequest(e){try{const t=await o.put(`/api/customer/requests/${e}/close`);return t.data}catch(t){throw console.error("Error closing request:",t),t}},async addReview(e,t){try{const r=await o.post(`/api/customer/requests/${e}/review`,t);return r.data}catch(r){throw console.error("Error adding review:",r),r}}},l={async getUsers(e=null){try{const t=e?{role:e}:{},r=await o.get("/api/admin/users",{params:t});return r.data}catch(t){throw console.error("Error fetching users:",t),t}},async approveUser(e){try{const t=await o.post(`/api/admin/users/${e}/approve`);return t.data}catch(t){throw console.error("Error approving user:",t),t}},async blockUser(e){try{const t=await o.post(`/api/admin/users/${e}/block`);return t.data}catch(t){throw console.error("Error blocking user:",t),t}},async getServices(){try{const e=await o.get("/api/admin/services");return e.data}catch(e){throw console.error("Error fetching services:",e),e}},async createService(e){try{const t=await o.post("/api/admin/services",e);return t.data}catch(t){throw console.error("Error creating service:",t),t}},async updateService(e,t){try{const r=await o.put(`/api/admin/services/${e}`,t);return r.data}catch(r){throw console.error("Error updating service:",r),r}},async deleteService(e){try{const t=await o.delete(`/api/admin/services/${e}`);return t.data}catch(t){throw console.error("Error deleting service:",t),t}}}}}]);
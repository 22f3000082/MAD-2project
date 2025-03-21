"use strict";(self["webpackChunkhousehold_services"]=self["webpackChunkhousehold_services"]||[]).push([[41],{20:(e,t,r)=>{r.d(t,{Er:()=>d,Uo:()=>l,YR:()=>i,xZ:()=>n,y1:()=>c});var s=r(713),o=r(221);const a=s.A.create({baseURL:"http://localhost:8080",headers:{"Content-Type":"application/json",Accept:"application/json"},withCredentials:!0});a.interceptors.request.use((e=>{const t=localStorage.getItem("token");if(t){const r=t.startsWith("Bearer ")?t:`Bearer ${t}`;e.headers["Authorization"]=r,console.log(`Request to ${e.url} with token: ${r.substring(0,20)}...`)}else console.warn(`No token found for request to: ${e.url}`);return e}),(e=>(console.error("Request error:",e),Promise.reject(e)))),a.interceptors.response.use((e=>e),(e=>{if(console.error("Response error:",e.response?.data||e.message),e.response){switch(e.response.status){case 401:localStorage.removeItem("token"),localStorage.removeItem("user"),o.A.push("/login");break;case 403:o.A.push("/");break;case 500:console.error("Server error:",e.response.data);break}if(e.response.data&&e.response.data.message)return Promise.reject(new Error(e.response.data.message))}return Promise.reject(e)}));const c={async register(e){try{if("professional"===e.role&&!e.service_type)throw new Error("Professionals must select a service type.");console.log("Sending registration data:",e);const t=await a.post("/auth/register",e);return console.log("Registration response:",t.data),t.data}catch(t){throw console.error("Registration error:",t.response?.data||t.message),t.response?.data||{message:"Registration failed. Please try again."}}},async login(e){try{console.log("Attempting login:",e);const t=await a.post("/auth/login",e);if(console.log("Login response:",t.data),t.data.token){const e=t.data.token;localStorage.setItem("token",e),localStorage.setItem("user",JSON.stringify(t.data.user));const r=localStorage.getItem("token");console.log("Token saved successfully: "+(r?"Yes":"No")),console.log(`Saved token (first 15 chars): ${r?r.substring(0,15):"None"}`),console.log("localStorage.token:",localStorage.getItem("token")),console.log("localStorage.user:",localStorage.getItem("user")),setTimeout((()=>{o.A.push(`/${t.data.user.role}/dashboard`)}),500)}return t.data}catch(t){throw console.error("Login error:",t.response?.data||t.message),t}},async logout(){try{await a.post("/auth/logout"),localStorage.removeItem("token"),localStorage.removeItem("user"),o.A.push("/login")}catch(e){console.error("Logout error:",e.response?.data||e.message),localStorage.removeItem("token"),localStorage.removeItem("user"),o.A.push("/login")}},getCurrentUser(){const e=localStorage.getItem("user");return e?JSON.parse(e):null}},i={async getServices(e={}){try{const t=await a.get("/api/admin/services",{params:e});return t.data}catch(t){throw console.error("Error fetching services:",t),t}},async mounted(){try{this.services=await this.searchServices(),console.log("Services loaded:",this.services)}catch(e){console.error("Failed to load services:",e)}},async getServiceById(e){try{const t=await a.get(`/api/services/${e}`);return t.data}catch(t){throw console.error("Error fetching service:",t),t}}},n={async getRequests(){try{const e=await a.get("/api/customer/requests");return e.data}catch(e){throw console.error("Error fetching requests:",e),e}},async createRequest(e){try{const t=await a.post("/api/customer/requests",e);return t.data}catch(t){throw console.error("Error creating request:",t),t}},async updateRequest(e,t){try{const r=await a.put(`/api/customer/requests/${e}`,t);return r.data}catch(r){throw console.error("Error updating request:",r),r}},async closeRequest(e){try{const t=await a.put(`/api/customer/requests/${e}/close`);return t.data}catch(t){throw console.error("Error closing request:",t),t}},async addReview(e,t){try{const r=await a.post(`/api/customer/requests/${e}/review`,t);return r.data}catch(r){throw console.error("Error adding review:",r),r}}},l={async getAssignments(e=null){try{console.log("Fetching professional assignments",e?`with status: ${e}`:"");const t=e?{status:e}:{},r=await a.get("/api/professional/assignments",{params:t});return console.log("Received assignments:",r.data.length),r.data}catch(t){throw console.error("Error fetching assignments:",t),t}},async updateStatus(e,t){try{console.log(`Updating request ${e} status to ${t}`);const r=await a.put(`/api/professional/requests/${e}`,{status:t});return console.log("Status update response:",r.data),r.data}catch(r){throw console.error("Error updating status:",r),r}},async getProfile(){try{console.log("Fetching professional profile");const e=await a.get("/api/professional/profile");return console.log("Retrieved profile data"),e.data}catch(e){throw console.error("Error fetching profile:",e),e}},async updateProfile(e){try{console.log("Updating professional profile with data:",e);const t=await a.put("/api/professional/profile",e);return console.log("Profile update response:",t.data),t.data}catch(t){throw console.error("Error updating profile:",t),t}}},d={async getUsers(e=null){try{const t=localStorage.getItem("token");console.log("Fetching users with token: "+(t?t.substring(0,15)+"...":"No token!"));const r=e?{role:e}:{};await new Promise((e=>setTimeout(e,300)));const s=await a.get("/api/admin/users",{params:r,headers:{Authorization:`Bearer ${t}`}});return console.log("Users response:",s.data),s.data}catch(t){throw console.error("Error fetching users:",t.response?.data||t.message),t}},async approveUser(e){try{console.log(`Approving professional with ID: ${e}`);const t=await a.post(`/api/admin/professionals/${e}/approve`);return console.log("Professional approved:",t.data),t.data}catch(t){throw console.error("Error approving user:",t),t}},async blockUser(e,t="Violation of terms of service"){try{console.log(`Blocking user with ID: ${e}, reason: ${t}`);const r=await a.post(`/api/admin/users/${e}/block`,{reason:t});return console.log("User blocked:",r.data),r.data}catch(r){throw console.error("Error blocking user:",r),r}},async unblockUser(e){try{console.log(`Unblocking user with ID: ${e}`);const t=await a.post(`/api/admin/users/${e}/unblock`);return console.log("User unblocked:",t.data),t.data}catch(t){throw console.error("Error unblocking user:",t),t}},async getServices(){try{const e=localStorage.getItem("token");console.log("Fetching services with token: "+(e?e.substring(0,15)+"...":"No token!")),await new Promise((e=>setTimeout(e,300)));const t=await a.get("/api/admin/services",{headers:{Authorization:`Bearer ${e}`}});return console.log("Services response:",t.data),t.data}catch(e){throw console.error("Error fetching services:",e.response?.data||e.message),e}},async createService(e){try{console.log("Creating service with data:",e);const t=await a.post("/api/admin/services",e);return console.log("Service created:",t.data),t.data}catch(t){throw console.error("Error creating service:",t.response?.data||t),t}},async updateService(e,t){try{const r=await a.put(`/api/admin/services/${e}`,t);return r.data}catch(r){throw console.error("Error updating service:",r),r}},async deleteService(e){try{const t=await a.delete(`/api/admin/services/${e}`);return t.data}catch(t){throw console.error("Error deleting service:",t),t}}}},41:(e,t,r)=>{r.r(t),r.d(t,{default:()=>m});var s=function(){var e=this,t=e._self._c;return t("div",{staticClass:"home"},[t("section",{staticClass:"hero bg-primary text-white py-5"},[t("div",{staticClass:"container"},[t("div",{staticClass:"row justify-content-center text-center"},[t("div",{staticClass:"col-md-8"},[t("h1",{staticClass:"display-4 mb-4"},[e._v("Welcome to A-Z Household Services")]),t("p",{staticClass:"lead mb-4"},[e._v("Find and book professional services for your home with ease")]),t("div",{staticClass:"d-flex justify-content-center gap-3"},[e.isLoggedIn?t("router-link",{staticClass:"btn btn-light btn-lg",attrs:{to:e.dashboardRoute}},[e._v("Go to Dashboard")]):t("router-link",{staticClass:"btn btn-light btn-lg",attrs:{to:"/register"}},[e._v("Get Started")])],1)])])])]),t("section",{staticClass:"services py-5"},[t("div",{staticClass:"container"},[t("h2",{staticClass:"text-center mb-5"},[e._v("Our Services")]),t("div",{staticClass:"row g-4"},e._l(e.services,(function(r){return t("div",{key:r.id,staticClass:"col-md-4"},[t("service-card",{attrs:{service:r},on:{click:function(t){return e.handleServiceClick(r)}}})],1)})),0)])]),e._m(0)])},o=[function(){var e=this,t=e._self._c;return t("section",{staticClass:"features bg-light py-5"},[t("div",{staticClass:"container"},[t("h2",{staticClass:"text-center mb-5"},[e._v("Why Choose Us")]),t("div",{staticClass:"row g-4"},[t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"text-center"},[t("i",{staticClass:"fas fa-check-circle fa-3x text-primary mb-3"}),t("h4",[e._v("Verified Professionals")]),t("p",[e._v("All our service providers are thoroughly vetted and verified")])])]),t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"text-center"},[t("i",{staticClass:"fas fa-clock fa-3x text-primary mb-3"}),t("h4",[e._v("Quick Service")]),t("p",[e._v("Get your service requests handled promptly")])])]),t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"text-center"},[t("i",{staticClass:"fas fa-star fa-3x text-primary mb-3"}),t("h4",[e._v("Quality Assured")]),t("p",[e._v("Rated and reviewed by our community")])])])])])])}],a=function(){var e=this,t=e._self._c;return t("div",{staticClass:"card h-100 shadow-sm",on:{click:function(t){return e.$emit("click")}}},[t("div",{staticClass:"card-body text-center"},[t("div",{staticClass:"service-icon mb-3"},[t("i",{class:["fas",e.serviceIcon,"fa-3x","text-primary"]})]),t("h3",{staticClass:"card-title"},[e._v(e._s(e.service.name))]),t("p",{staticClass:"card-text text-muted"},[e._v(e._s(e.service.description))]),t("div",{staticClass:"d-flex justify-content-between align-items-center mt-3"},[t("span",{staticClass:"text-primary fw-bold"},[e._v("₹"+e._s(e.service.base_price))]),t("span",{staticClass:"badge bg-light text-dark"},[e._v(e._s(e.service.time_required))])])])])},c=[];const i={name:"ServiceCard",props:{service:{type:Object,required:!0,validator:e=>e.name&&void 0!==e.base_price}},computed:{serviceIcon(){const e={cleaning:"fa-broom",plumbing:"fa-wrench",electrical:"fa-bolt",carpentry:"fa-hammer",painting:"fa-paint-roller",gardening:"fa-leaf",default:"fa-tools"};return e[this.service.type?this.service.type.toLowerCase():"default"]}}},n=i;var l=r(656),d=(0,l.A)(n,a,c,!1,null,"252f26ec",null);const u=d.exports;var g=r(20);const p={name:"Home",components:{ServiceCard:u},data(){return{services:[],isLoading:!1,error:null}},computed:{isLoggedIn(){return!!localStorage.getItem("token")},dashboardRoute(){const e=JSON.parse(localStorage.getItem("user")||"{}");return`/${e.role}/dashboard`}},methods:{async fetchServices(){try{this.isLoading=!0,this.services=await(0,g.getServices)()}catch(e){this.error="Failed to load services",console.error("Error fetching services:",e)}finally{this.isLoading=!1}},handleServiceClick(e){this.isLoggedIn?this.$router.push({name:"ServiceRequest",params:{serviceId:e.id}}):this.$router.push("/login")}},created(){this.fetchServices()}},h=p;var v=(0,l.A)(h,s,o,!1,null,"e332ee6a",null);const m=v.exports}}]);
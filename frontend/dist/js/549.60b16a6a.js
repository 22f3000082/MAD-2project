"use strict";(self["webpackChunkhousehold_services"]=self["webpackChunkhousehold_services"]||[]).push([[549],{549:(r,e,s)=>{s.r(e),s.d(e,{default:()=>d});var a=function(){var r=this,e=r._self._c;return e("div",{staticClass:"login-container"},[e("div",{staticClass:"container py-5"},[e("div",{staticClass:"row justify-content-center"},[e("div",{staticClass:"col-md-6 col-lg-5"},[e("div",{staticClass:"card shadow"},[e("div",{staticClass:"card-body p-4"},[e("h2",{staticClass:"text-center mb-4"},[r._v("Login")]),e("form",{staticClass:"needs-validation",attrs:{novalidate:""},on:{submit:function(e){return e.preventDefault(),r.handleSubmit.apply(null,arguments)}}},[e("div",{staticClass:"mb-3"},[e("label",{staticClass:"form-label"},[r._v("Email")]),e("div",{staticClass:"input-group"},[r._m(0),e("input",{directives:[{name:"model",rawName:"v-model",value:r.formData.email,expression:"formData.email"}],staticClass:"form-control",class:{"is-invalid":r.errors.email},attrs:{type:"email",required:"",placeholder:"Enter your email",autocomplete:"email"},domProps:{value:r.formData.email},on:{input:function(e){e.target.composing||r.$set(r.formData,"email",e.target.value)}}}),e("div",{staticClass:"invalid-feedback"},[r._v(r._s(r.errors.email))])])]),e("div",{staticClass:"mb-4"},[e("label",{staticClass:"form-label"},[r._v("Password")]),e("div",{staticClass:"input-group"},[r._m(1),"checkbox"===(r.showPassword?"text":"password")?e("input",{directives:[{name:"model",rawName:"v-model",value:r.formData.password,expression:"formData.password"}],staticClass:"form-control",class:{"is-invalid":r.errors.password},attrs:{required:"",placeholder:"Enter your password",autocomplete:"current-password",type:"checkbox"},domProps:{checked:Array.isArray(r.formData.password)?r._i(r.formData.password,null)>-1:r.formData.password},on:{change:function(e){var s=r.formData.password,a=e.target,t=!!a.checked;if(Array.isArray(s)){var o=null,i=r._i(s,o);a.checked?i<0&&r.$set(r.formData,"password",s.concat([o])):i>-1&&r.$set(r.formData,"password",s.slice(0,i).concat(s.slice(i+1)))}else r.$set(r.formData,"password",t)}}}):"radio"===(r.showPassword?"text":"password")?e("input",{directives:[{name:"model",rawName:"v-model",value:r.formData.password,expression:"formData.password"}],staticClass:"form-control",class:{"is-invalid":r.errors.password},attrs:{required:"",placeholder:"Enter your password",autocomplete:"current-password",type:"radio"},domProps:{checked:r._q(r.formData.password,null)},on:{change:function(e){return r.$set(r.formData,"password",null)}}}):e("input",{directives:[{name:"model",rawName:"v-model",value:r.formData.password,expression:"formData.password"}],staticClass:"form-control",class:{"is-invalid":r.errors.password},attrs:{required:"",placeholder:"Enter your password",autocomplete:"current-password",type:r.showPassword?"text":"password"},domProps:{value:r.formData.password},on:{input:function(e){e.target.composing||r.$set(r.formData,"password",e.target.value)}}}),e("button",{staticClass:"btn btn-outline-secondary",attrs:{type:"button"},on:{click:r.togglePassword}},[e("i",{class:r.showPassword?"fas fa-eye-slash":"fas fa-eye"})]),e("div",{staticClass:"invalid-feedback"},[r._v(r._s(r.errors.password))])])]),r.loginError?e("div",{staticClass:"alert alert-danger",attrs:{role:"alert"}},[e("i",{staticClass:"fas fa-exclamation-circle me-2"}),r._v(" "+r._s(r.loginError)+" ")]):r._e(),e("div",{staticClass:"d-grid gap-2"},[e("button",{staticClass:"btn btn-primary",attrs:{type:"submit",disabled:r.isLoading}},[r.isLoading?e("span",{staticClass:"spinner-border spinner-border-sm me-2"}):r._e(),r._v(" "+r._s(r.isLoading?"Logging in...":"Login")+" ")])]),e("p",{staticClass:"text-center mt-3"},[r._v(" Don't have an account? "),e("router-link",{attrs:{to:"/register"}},[r._v("Register here")])],1)])])]),r._m(2)])])])])},t=[function(){var r=this,e=r._self._c;return e("span",{staticClass:"input-group-text"},[e("i",{staticClass:"fas fa-envelope"})])},function(){var r=this,e=r._self._c;return e("span",{staticClass:"input-group-text"},[e("i",{staticClass:"fas fa-lock"})])},function(){var r=this,e=r._self._c;return e("div",{staticClass:"row mt-4 g-3"},[e("div",{staticClass:"col-md-4"},[e("div",{staticClass:"card h-100 border-0 shadow-sm"},[e("div",{staticClass:"card-body text-center"},[e("i",{staticClass:"fas fa-user-shield fa-2x text-primary mb-2"}),e("h5",{staticClass:"card-title"},[r._v("Admin")]),e("p",{staticClass:"card-text small"},[r._v("Manage services and users")])])])]),e("div",{staticClass:"col-md-4"},[e("div",{staticClass:"card h-100 border-0 shadow-sm"},[e("div",{staticClass:"card-body text-center"},[e("i",{staticClass:"fas fa-user fa-2x text-success mb-2"}),e("h5",{staticClass:"card-title"},[r._v("Customer")]),e("p",{staticClass:"card-text small"},[r._v("Book and manage services")])])])]),e("div",{staticClass:"col-md-4"},[e("div",{staticClass:"card h-100 border-0 shadow-sm"},[e("div",{staticClass:"card-body text-center"},[e("i",{staticClass:"fas fa-user-tie fa-2x text-info mb-2"}),e("h5",{staticClass:"card-title"},[r._v("Professional")]),e("p",{staticClass:"card-text small"},[r._v("Provide services")])])])])])}],o=s(844);const i={name:"LoginView",data(){return{formData:{email:"",password:""},errors:{},loginError:"",isLoading:!1,showPassword:!1}},methods:{togglePassword(){this.showPassword=!this.showPassword},validateForm(){this.errors={};let r=!0;return this.formData.email?/\S+@\S+\.\S+/.test(this.formData.email)||(this.errors.email="Please enter a valid email address",r=!1):(this.errors.email="Email is required",r=!1),this.formData.password||(this.errors.password="Password is required",r=!1),r},async handleSubmit(){if(this.loginError="",this.validateForm()){this.isLoading=!0;try{const r=await o.y1.login(this.formData);switch(r.user.role){case"admin":await this.$router.push("/admin/dashboard");break;case"customer":await this.$router.push("/customer/dashboard");break;case"professional":if(!r.user.is_approved)return this.loginError="Your account is pending approval. Please wait for admin verification.",localStorage.removeItem("token"),void localStorage.removeItem("user");await this.$router.push("/professional/dashboard");break;default:await this.$router.push("/")}}catch(r){console.error("Login error:",r),401===r.response?.status?this.loginError="Invalid email or password":r.message?this.loginError=r.message:this.loginError="Network error. Please check your connection and try again."}finally{this.isLoading=!1}}}},created(){localStorage.removeItem("token"),localStorage.removeItem("user")}},c=i;var n=s(656),l=(0,n.A)(c,a,t,!1,null,"23f8a132",null);const d=l.exports},844:(r,e,s)=>{s.d(e,{Er:()=>l,YR:()=>c,xZ:()=>n,y1:()=>i});var a=s(194),t=s(997);const o=a.A.create({baseURL:"http://localhost:8080",headers:{"Content-Type":"application/json",Accept:"application/json"},withCredentials:!0});o.interceptors.request.use((r=>{const e=localStorage.getItem("token");return e&&(r.headers["Authorization"]=`Bearer ${e}`),r}),(r=>(console.error("Request error:",r),Promise.reject(r)))),o.interceptors.response.use((r=>r),(r=>{if(console.error("Response error:",r.response?.data||r.message),r.response){switch(r.response.status){case 401:localStorage.removeItem("token"),localStorage.removeItem("user"),t.A.push("/login");break;case 403:t.A.push("/");break;case 500:console.error("Server error:",r.response.data);break}if(r.response.data&&r.response.data.message)return Promise.reject(new Error(r.response.data.message))}return Promise.reject(r)}));const i={async register(r){try{if("professional"===r.role&&!r.service_type)throw new Error("Professionals must select a service type.");console.log("Sending registration data:",r);const e=await o.post("/auth/register",r);return console.log("Registration response:",e.data),e.data}catch(e){throw console.error("Registration error:",e.response?.data||e.message),e.response?.data||{message:"Registration failed. Please try again."}}},async login(r){try{console.log("Attempting login:",r);const e=await o.post("/auth/login",r);if(console.log("Login response:",e.data),e.data.token){localStorage.setItem("token",e.data.token),localStorage.setItem("user",JSON.stringify(e.data.user));const r=e.data.user;t.A.push(`/${r.role}/dashboard`)}return e.data}catch(e){throw console.error("Login error:",e.response?.data||e.message),e}},async logout(){try{await o.post("/auth/logout"),localStorage.removeItem("token"),localStorage.removeItem("user"),t.A.push("/login")}catch(r){console.error("Logout error:",r.response?.data||r.message),localStorage.removeItem("token"),localStorage.removeItem("user"),t.A.push("/login")}},getCurrentUser(){const r=localStorage.getItem("user");return r?JSON.parse(r):null}},c={async getServices(r={}){try{const e=await o.get("/api/services",{params:r});return e.data}catch(e){throw console.error("Error fetching services:",e),e}},async mounted(){try{this.services=await this.searchServices(),console.log("Services loaded:",this.services)}catch(r){console.error("Failed to load services:",r)}},async getServiceById(r){try{const e=await o.get(`/api/services/${r}`);return e.data}catch(e){throw console.error("Error fetching service:",e),e}}},n={async getRequests(){try{const r=await o.get("/api/customer/requests");return r.data}catch(r){throw console.error("Error fetching requests:",r),r}},async createRequest(r){try{const e=await o.post("/api/customer/requests",r);return e.data}catch(e){throw console.error("Error creating request:",e),e}},async updateRequest(r,e){try{const s=await o.put(`/api/customer/requests/${r}`,e);return s.data}catch(s){throw console.error("Error updating request:",s),s}},async closeRequest(r){try{const e=await o.put(`/api/customer/requests/${r}/close`);return e.data}catch(e){throw console.error("Error closing request:",e),e}},async addReview(r,e){try{const s=await o.post(`/api/customer/requests/${r}/review`,e);return s.data}catch(s){throw console.error("Error adding review:",s),s}}},l={async getUsers(r=null){try{const e=r?{role:r}:{},s=await o.get("/api/admin/users",{params:e});return s.data}catch(e){throw console.error("Error fetching users:",e),e}},async approveUser(r){try{const e=await o.post(`/api/admin/users/${r}/approve`);return e.data}catch(e){throw console.error("Error approving user:",e),e}},async blockUser(r){try{const e=await o.post(`/api/admin/users/${r}/block`);return e.data}catch(e){throw console.error("Error blocking user:",e),e}},async getServices(){try{const r=await o.get("/api/admin/services");return r.data}catch(r){throw console.error("Error fetching services:",r),r}},async createService(r){try{const e=await o.post("/api/admin/services",r);return e.data}catch(e){throw console.error("Error creating service:",e),e}},async updateService(r,e){try{const s=await o.put(`/api/admin/services/${r}`,e);return s.data}catch(s){throw console.error("Error updating service:",s),s}},async deleteService(r){try{const e=await o.delete(`/api/admin/services/${r}`);return e.data}catch(e){throw console.error("Error deleting service:",e),e}}}}}]);
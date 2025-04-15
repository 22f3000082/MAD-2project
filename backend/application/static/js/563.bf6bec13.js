"use strict";(self["webpackChunkhousehold_services"]=self["webpackChunkhousehold_services"]||[]).push([[563],{535:(e,a,t)=>{t.d(a,{A:()=>c});var s=function(){var e=this,a=e._self._c;return a("div",{staticClass:"service-list"},[e.loading||e.services&&0!==e.services.length?e.loading?a("div",{staticClass:"text-center py-5"},[e._m(1),a("p",{staticClass:"mt-2"},[e._v("Finding services for you...")])]):a("div",{staticClass:"row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4"},e._l(e.services,(function(t){return a("div",{key:t.id,staticClass:"col"},[a("div",{staticClass:"card h-100 service-card"},[a("div",{staticClass:"card-category-badge",style:{backgroundColor:e.getCategoryColor(t.category)}},[e._v(" "+e._s(t.category)+" ")]),a("div",{staticClass:"card-body"},[a("div",{staticClass:"d-flex justify-content-between align-items-start"},[a("h5",{staticClass:"card-title"},[e._v(e._s(t.name))]),a("span",{staticClass:"price-badge"},[e._v("₹"+e._s(t.base_price))])]),a("div",{staticClass:"service-meta my-3"},[a("span",{staticClass:"meta-item"},[a("i",{staticClass:"far fa-clock me-1"}),e._v(" "+e._s(t.time_required||60)+" mins")]),t.rating?a("span",{staticClass:"meta-item"},[a("i",{staticClass:"fas fa-star text-warning me-1"}),e._v(" "+e._s(t.rating)+" ")]):e._e()]),a("p",{staticClass:"card-text service-description"},[e._v(e._s(t.description||"No description available"))]),t.features&&t.features.length?a("div",{staticClass:"service-features mt-3"},e._l(t.features,(function(t){return a("span",{key:t,staticClass:"feature-badge"},[e._v(" "+e._s(t)+" ")])})),0):e._e()]),a("div",{staticClass:"card-footer bg-transparent border-0"},[a("div",{staticClass:"d-flex gap-2"},[a("button",{staticClass:"btn btn-outline-primary flex-grow-1",on:{click:function(a){return e.$emit("view-details",t)}}},[a("i",{staticClass:"fas fa-info-circle me-1"}),e._v(" Details ")]),a("button",{staticClass:"btn btn-primary flex-grow-1",on:{click:function(a){return e.$emit("request-service",t)}}},[a("i",{staticClass:"fas fa-plus me-1"}),e._v(" Request ")])])])])])})),0):a("div",{staticClass:"text-center py-5"},[e._m(0)]),!e.loading&&e.hasMore&&e.services.length>0?a("div",{staticClass:"text-center mt-4"},[a("button",{staticClass:"btn btn-outline-primary",on:{click:function(a){return e.$emit("load-more")}}},[a("i",{staticClass:"fas fa-spinner me-1"}),e._v(" Load More Services ")])]):e._e()])},r=[function(){var e=this,a=e._self._c;return a("div",{staticClass:"empty-state"},[a("i",{staticClass:"fas fa-search fa-3x text-muted mb-3"}),a("h5",[e._v("No services found")]),a("p",{staticClass:"text-muted"},[e._v("Try adjusting your search filters")])])},function(){var e=this,a=e._self._c;return a("div",{staticClass:"spinner-border text-primary",attrs:{role:"status"}},[a("span",{staticClass:"visually-hidden"},[e._v("Loading...")])])}];const i={name:"ServiceList",props:{services:{type:Array,default:()=>[]},loading:{type:Boolean,default:!1},hasMore:{type:Boolean,default:!1}},emits:["view-details","request-service","load-more"],setup(){const e={"AC Repair":"#4CAF50",Plumbing:"#2196F3",Electrical:"#FFC107",Carpentry:"#795548",Painting:"#9C27B0",Cleaning:"#03A9F4","Pest Control":"#F44336","Appliance Repair":"#FF9800","Moving Services":"#607D8B",Gardening:"#8BC34A"},a=a=>e[a]||"#9E9E9E";return{getCategoryColor:a}}},o=i;var l=t(656),n=(0,l.A)(o,s,r,!1,null,"4d4a653b",null);const c=n.exports},563:(e,a,t)=>{t.r(a),t.d(a,{default:()=>u});var s=function(){var e=this,a=e._self._c;return a("div",{staticClass:"register-container"},[a("div",{staticClass:"container py-5"},[a("div",{staticClass:"row justify-content-center"},[a("div",{staticClass:"col-md-8 col-lg-6"},[a("div",{staticClass:"card shadow"},[a("div",{staticClass:"card-body p-4"},[a("h2",{staticClass:"text-center mb-4"},[e._v("Register")]),e.error?a("div",{staticClass:"alert alert-danger"},[e._v(e._s(e.error))]):e._e(),a("form",{staticClass:"needs-validation",attrs:{novalidate:""},on:{submit:function(a){return a.preventDefault(),e.handleSubmit.apply(null,arguments)}}},[a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label",attrs:{for:"fullName"}},[e._v("Full Name")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.name,expression:"formData.name"}],staticClass:"form-control",class:{"is-invalid":e.errors.name},attrs:{type:"text",id:"fullName",name:"fullName",required:""},domProps:{value:e.formData.name},on:{input:function(a){a.target.composing||e.$set(e.formData,"name",a.target.value)}}}),a("div",{staticClass:"invalid-feedback"},[e._v(e._s(e.errors.name))])]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label",attrs:{for:"username"}},[e._v("Username")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.username,expression:"formData.username"}],staticClass:"form-control",class:{"is-invalid":e.errors.username},attrs:{type:"text",id:"username",name:"username",required:""},domProps:{value:e.formData.username},on:{input:function(a){a.target.composing||e.$set(e.formData,"username",a.target.value)}}}),a("div",{staticClass:"invalid-feedback"},[e._v(e._s(e.errors.username))])]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label",attrs:{for:"email"}},[e._v("Email")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.email,expression:"formData.email"}],staticClass:"form-control",class:{"is-invalid":e.errors.email},attrs:{type:"email",id:"email",name:"email",required:""},domProps:{value:e.formData.email},on:{input:function(a){a.target.composing||e.$set(e.formData,"email",a.target.value)}}}),a("div",{staticClass:"invalid-feedback"},[e._v(e._s(e.errors.email))])]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label",attrs:{for:"password"}},[e._v("Password")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.password,expression:"formData.password"}],staticClass:"form-control",class:{"is-invalid":e.errors.password},attrs:{type:"password",id:"password",name:"password",required:""},domProps:{value:e.formData.password},on:{input:function(a){a.target.composing||e.$set(e.formData,"password",a.target.value)}}}),a("div",{staticClass:"invalid-feedback"},[e._v(e._s(e.errors.password))])]),a("div",{staticClass:"mb-4"},[a("label",{staticClass:"form-label"},[e._v("Register as:")]),a("div",{staticClass:"d-flex gap-4"},[a("div",{staticClass:"form-check"},[a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.role,expression:"formData.role"}],staticClass:"form-check-input",attrs:{type:"radio",value:"customer",id:"roleCustomer"},domProps:{checked:e._q(e.formData.role,"customer")},on:{change:function(a){return e.$set(e.formData,"role","customer")}}}),a("label",{staticClass:"form-check-label",attrs:{for:"roleCustomer"}},[e._v("Customer")])]),a("div",{staticClass:"form-check"},[a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.role,expression:"formData.role"}],staticClass:"form-check-input",attrs:{type:"radio",value:"professional",id:"roleProfessional"},domProps:{checked:e._q(e.formData.role,"professional")},on:{change:function(a){return e.$set(e.formData,"role","professional")}}}),a("label",{staticClass:"form-check-label",attrs:{for:"roleProfessional"}},[e._v("Service Professional")])])])]),"professional"===e.formData.role?a("div",[a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("Service Type")]),a("select",{directives:[{name:"model",rawName:"v-model",value:e.formData.service_type,expression:"formData.service_type"}],staticClass:"form-select",attrs:{required:""},on:{change:function(a){var t=Array.prototype.filter.call(a.target.options,(function(e){return e.selected})).map((function(e){var a="_value"in e?e._value:e.value;return a}));e.$set(e.formData,"service_type",a.target.multiple?t:t[0])}}},[a("option",{attrs:{value:""}},[e._v("Select a service type")]),e._l(e.service_types,(function(t){return a("option",{key:t,domProps:{value:t}},[e._v(e._s(t))])}))],2)]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("Experience (years)")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.experience,expression:"formData.experience"}],staticClass:"form-control",attrs:{type:"number",min:"0",required:""},domProps:{value:e.formData.experience},on:{input:function(a){a.target.composing||e.$set(e.formData,"experience",a.target.value)}}})]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("Description")]),a("textarea",{directives:[{name:"model",rawName:"v-model",value:e.formData.description,expression:"formData.description"}],staticClass:"form-control",attrs:{rows:"3"},domProps:{value:e.formData.description},on:{input:function(a){a.target.composing||e.$set(e.formData,"description",a.target.value)}}})]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("Upload Documents")]),a("input",{staticClass:"form-control",attrs:{type:"file",multiple:""},on:{change:e.handleFileUpload}})])]):e._e(),"customer"===e.formData.role?a("div",[a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("Phone")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.phone,expression:"formData.phone"}],staticClass:"form-control",attrs:{type:"tel",required:""},domProps:{value:e.formData.phone},on:{input:function(a){a.target.composing||e.$set(e.formData,"phone",a.target.value)}}})]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("Address")]),a("textarea",{directives:[{name:"model",rawName:"v-model",value:e.formData.address,expression:"formData.address"}],staticClass:"form-control",attrs:{required:""},domProps:{value:e.formData.address},on:{input:function(a){a.target.composing||e.$set(e.formData,"address",a.target.value)}}})]),a("div",{staticClass:"mb-3"},[a("label",{staticClass:"form-label"},[e._v("PIN Code")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.formData.pin_code,expression:"formData.pin_code"}],staticClass:"form-control",attrs:{type:"text",required:"",pattern:"[0-9]{6}"},domProps:{value:e.formData.pin_code},on:{input:function(a){a.target.composing||e.$set(e.formData,"pin_code",a.target.value)}}})])]):e._e(),a("div",{staticClass:"d-grid gap-2"},[a("button",{staticClass:"btn btn-primary",attrs:{type:"submit",disabled:e.loading}},[e._v(e._s(e.loading?"Registering...":"Register"))])]),a("p",{staticClass:"text-center mt-3"},[e._v(" Already have an account? "),a("router-link",{attrs:{to:"/login"}},[e._v("Login here")])],1)])])])])])])])},r=[],i=t(648),o=t(194),l=t(997);t(535);const n={name:"RegisterView",data(){return{service_types:["AC Repair","Plumbing","Electrical","Carpentry","Painting","Cleaning","Pest Control","Appliance Repair","Moving Services","Gardening"]}},setup(){const e=(0,i.KR)(!1),a=(0,i.KR)(""),t=(0,i.KR)([]),s=(0,i.Kh)({name:"",username:"",email:"",password:"",role:"",service_type:"",experience:"",description:"",phone:"",address:"",pin_code:"",documents:[]}),r=(0,i.Kh)({}),n=async()=>{},c=e=>{s.documents=Array.from(e.target.files)},m=async()=>{try{if(e.value=!0,a.value="",Object.keys(r).forEach((e=>r[e]="")),s.name||(r.name="Name is required"),s.username||(r.username="Username is required"),s.email||(r.email="Email is required"),s.password||(r.password="Password is required"),s.role||(r.role="Role is required"),"professional"===s.role?(s.service_type||(r.service_type="Service type is required"),s.experience||(r.experience="Experience is required")):"customer"===s.role&&(s.phone||(r.phone="Phone is required"),s.address||(r.address="Address is required"),s.pin_code||(r.pin_code="PIN code is required")),Object.values(r).some((e=>e)))return;const t=new FormData;Object.keys(s).forEach((e=>{"documents"===e?s.documents.forEach((e=>{t.append("documents",e)})):t.append(e,s[e])}));const i=await o.A.post("http://localhost:8080/auth/register",t,{headers:{"Content-Type":"multipart/form-data",Accept:"application/json"},withCredentials:!0});console.log("Registration successful:",i.data),a.value="",alert("Registration successful! Please login to continue."),l.A.push("/login")}catch(t){console.error("Registration error:",t),a.value=t.response?.data?.message||t.response?.data?.error||"Registration failed. Please try again."}finally{e.value=!1}};return(0,i.sV)(n),{formData:s,errors:r,loading:e,error:a,services:t,handleSubmit:m,handleFileUpload:c,fetchServiceTypes:n}}},c=n;var m=t(656),d=(0,m.A)(c,s,r,!1,null,"3f0c0192",null);const u=d.exports}}]);
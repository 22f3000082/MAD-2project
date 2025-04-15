"use strict";(self["webpackChunkhousehold_services"]=self["webpackChunkhousehold_services"]||[]).push([[454],{454:(e,t,s)=>{s.r(t),s.d(t,{default:()=>u});var a=function(){var e=this,t=e._self._c;return t("div",{staticClass:"professional-requests"},[t("div",{staticClass:"d-flex justify-content-between align-items-center mb-4"},[t("h2",[e._v(e._s(e.pageTitle))]),t("div",{staticClass:"d-flex"},[t("div",{staticClass:"input-group"},[t("input",{directives:[{name:"model",rawName:"v-model",value:e.searchQuery,expression:"searchQuery"}],staticClass:"form-control",attrs:{type:"text",placeholder:"Search requests..."},domProps:{value:e.searchQuery},on:{input:[function(t){t.target.composing||(e.searchQuery=t.target.value)},e.filterRequests]}}),e._m(0)])])]),t("ul",{staticClass:"nav nav-tabs mb-4"},[t("li",{staticClass:"nav-item"},[t("router-link",{staticClass:"nav-link",class:{active:"ProfessionalNewRequests"===e.$route.name},attrs:{to:"/professional/requests/new"}},[t("i",{staticClass:"fas fa-bell me-2"}),e._v(" New Requests "),e.newRequestsCount>0?t("span",{staticClass:"badge bg-primary ms-2"},[e._v(e._s(e.newRequestsCount))]):e._e()])],1),t("li",{staticClass:"nav-item"},[t("router-link",{staticClass:"nav-link",class:{active:"ProfessionalOngoingRequests"===e.$route.name},attrs:{to:"/professional/requests/ongoing"}},[t("i",{staticClass:"fas fa-spinner me-2"}),e._v(" Ongoing ")])],1),t("li",{staticClass:"nav-item"},[t("router-link",{staticClass:"nav-link",class:{active:"ProfessionalCompletedRequests"===e.$route.name},attrs:{to:"/professional/requests/completed"}},[t("i",{staticClass:"fas fa-check-circle me-2"}),e._v(" Completed ")])],1)]),t("div",{staticClass:"card shadow-sm"},[t("div",{staticClass:"card-body p-0"},[t("div",{staticClass:"table-responsive"},[e.filteredRequests.length>0?t("table",{staticClass:"table table-hover mb-0"},[e._m(1),t("tbody",e._l(e.filteredRequests,(function(s){return t("tr",{key:s.id},[t("td",[t("strong",[e._v("#"+e._s(s.id))])]),t("td",[e._v(e._s(s.service_name))]),t("td",[e._v(e._s(s.customer_name))]),t("td",[e._v(e._s(e.formatDate(s.scheduled_date)))]),t("td",[e._v(e._s(s.location))]),t("td",[e._v("₹"+e._s(s.price))]),t("td",[t("span",{staticClass:"badge",class:e.getStatusBadgeClass(s.status)},[e._v(" "+e._s(s.status)+" ")])]),t("td",[t("div",{staticClass:"btn-group"},[t("button",{staticClass:"btn btn-sm btn-primary",attrs:{title:"View Details"},on:{click:function(t){return e.viewRequestDetails(s)}}},[t("i",{staticClass:"fas fa-eye"})]),"pending"===s.status?[t("button",{staticClass:"btn btn-sm btn-success",attrs:{title:"Accept Request"},on:{click:function(t){return e.acceptRequest(s)}}},[t("i",{staticClass:"fas fa-check"})]),t("button",{staticClass:"btn btn-sm btn-danger",attrs:{title:"Reject Request"},on:{click:function(t){return e.rejectRequest(s)}}},[t("i",{staticClass:"fas fa-times"})])]:e._e(),"accepted"===s.status?[t("button",{staticClass:"btn btn-sm btn-success",attrs:{title:"Start Service"},on:{click:function(t){return e.startService(s)}}},[t("i",{staticClass:"fas fa-play"})])]:e._e(),"in_progress"===s.status?[t("button",{staticClass:"btn btn-sm btn-success",attrs:{title:"Complete Service"},on:{click:function(t){return e.completeService(s)}}},[t("i",{staticClass:"fas fa-check-double"})])]:e._e()],2)])])})),0)]):t("div",{staticClass:"text-center py-5"},[t("i",{staticClass:"fas fa-clipboard-list fa-3x text-muted mb-3"}),t("h4",[e._v("No requests found")]),t("p",{staticClass:"text-muted"},[e._v("There are no "+e._s(e.statusText)+" service requests at the moment.")])])])])]),t("div",{ref:"detailsModal",staticClass:"modal fade",attrs:{id:"requestDetailsModal",tabindex:"-1","aria-hidden":"true"}},[t("div",{staticClass:"modal-dialog modal-lg"},[e.selectedRequest?t("div",{staticClass:"modal-content"},[t("div",{staticClass:"modal-header"},[t("h5",{staticClass:"modal-title"},[e._v("Request #"+e._s(e.selectedRequest.id)+" Details")]),t("button",{staticClass:"btn-close",attrs:{type:"button","data-bs-dismiss":"modal","aria-label":"Close"}})]),t("div",{staticClass:"modal-body"},[t("div",{staticClass:"row"},[t("div",{staticClass:"col-md-6"},[t("h6",[e._v("Service Information")]),t("table",{staticClass:"table table-borderless"},[t("tbody",[t("tr",[t("th",{attrs:{width:"40%"}},[e._v("Service:")]),t("td",[e._v(e._s(e.selectedRequest.service_name))])]),t("tr",[t("th",[e._v("Date:")]),t("td",[e._v(e._s(e.formatDate(e.selectedRequest.scheduled_date)))])]),t("tr",[t("th",[e._v("Time:")]),t("td",[e._v(e._s(e.selectedRequest.scheduled_time))])]),t("tr",[t("th",[e._v("Price:")]),t("td",[e._v("₹"+e._s(e.selectedRequest.price))])]),t("tr",[t("th",[e._v("Status:")]),t("td",[t("span",{staticClass:"badge",class:e.getStatusBadgeClass(e.selectedRequest.status)},[e._v(" "+e._s(e.selectedRequest.status)+" ")])])])])])]),t("div",{staticClass:"col-md-6"},[t("h6",[e._v("Customer Information")]),t("table",{staticClass:"table table-borderless"},[t("tbody",[t("tr",[t("th",{attrs:{width:"40%"}},[e._v("Name:")]),t("td",[e._v(e._s(e.selectedRequest.customer_name))])]),t("tr",[t("th",[e._v("Phone:")]),t("td",[e._v(e._s(e.selectedRequest.customer_phone))])]),t("tr",[t("th",[e._v("Address:")]),t("td",[e._v(e._s(e.selectedRequest.location))])]),t("tr",[t("th",[e._v("PIN Code:")]),t("td",[e._v(e._s(e.selectedRequest.pin_code))])])])])])]),t("hr"),t("h6",[e._v("Additional Notes")]),t("p",{staticClass:"mb-0"},[e._v(e._s(e.selectedRequest.notes||"No additional notes provided."))])]),t("div",{staticClass:"modal-footer"},["pending"===e.selectedRequest.status?[t("button",{staticClass:"btn btn-danger",on:{click:function(t){return e.rejectRequest(e.selectedRequest)}}},[t("i",{staticClass:"fas fa-times me-1"}),e._v(" Reject ")]),t("button",{staticClass:"btn btn-success",on:{click:function(t){return e.acceptRequest(e.selectedRequest)}}},[t("i",{staticClass:"fas fa-check me-1"}),e._v(" Accept ")])]:e._e(),"accepted"===e.selectedRequest.status?[t("button",{staticClass:"btn btn-success",on:{click:function(t){return e.startService(e.selectedRequest)}}},[t("i",{staticClass:"fas fa-play me-1"}),e._v(" Start Service ")])]:e._e(),"in_progress"===e.selectedRequest.status?[t("button",{staticClass:"btn btn-success",on:{click:function(t){return e.completeService(e.selectedRequest)}}},[t("i",{staticClass:"fas fa-check-double me-1"}),e._v(" Complete Service ")])]:e._e(),e._m(2)],2)]):e._e()])])])},i=[function(){var e=this,t=e._self._c;return t("button",{staticClass:"btn btn-primary"},[t("i",{staticClass:"fas fa-search"})])},function(){var e=this,t=e._self._c;return t("thead",[t("tr",[t("th",[e._v("ID")]),t("th",[e._v("Service")]),t("th",[e._v("Customer")]),t("th",[e._v("Date")]),t("th",[e._v("Location")]),t("th",[e._v("Price")]),t("th",[e._v("Status")]),t("th",[e._v("Actions")])])])},function(){var e=this,t=e._self._c;return t("button",{staticClass:"btn btn-secondary",attrs:{type:"button","data-bs-dismiss":"modal"}},[t("i",{staticClass:"fas fa-times me-1"}),e._v(" Close ")])}],n=s(844);const c={name:"ProfessionalRequests",props:{status:{type:String,default:"new",validator:e=>["new","ongoing","completed"].includes(e)}},data(){return{allRequests:[],filteredRequests:[],selectedRequest:null,searchQuery:"",isLoading:!1,error:null,modalInstance:null}},computed:{statusFilter(){const e={new:["pending"],ongoing:["accepted","in_progress"],completed:["completed","cancelled","rejected"]};return e[this.status]||["pending"]},newRequestsCount(){return this.allRequests.filter((e=>"pending"===e.status)).length},pageTitle(){const e={new:"New Service Requests",ongoing:"Ongoing Services",completed:"Completed Services"};return e[this.status]||"Service Requests"},statusText(){const e={new:"new",ongoing:"ongoing",completed:"completed"};return e[this.status]||""}},watch:{status:{handler(){this.filterRequests()},immediate:!0}},methods:{async fetchRequests(){try{this.isLoading=!0,this.error=null;const e=await n.YR.getProfessionalRequests();e&&e.length>0?this.allRequests=e:this.allRequests=this.getMockRequests(),this.filterRequests()}catch(e){console.error("Error fetching requests:",e),this.error="Failed to load service requests",this.allRequests=this.getMockRequests(),this.filterRequests()}finally{this.isLoading=!1}},getMockRequests(){return[{id:1001,service_name:"Plumbing Service",customer_name:"John Doe",customer_phone:"9876543210",scheduled_date:"2023-05-15",scheduled_time:"10:00 AM",location:"123 Main St, Apartment 4B",pin_code:"600001",price:550,status:"pending",notes:"Water leakage in kitchen sink"},{id:1002,service_name:"Electrical Repair",customer_name:"Jane Smith",customer_phone:"8765432109",scheduled_date:"2023-05-16",scheduled_time:"2:00 PM",location:"456 Park Ave, House 7",pin_code:"600002",price:650,status:"accepted",notes:"Faulty wiring in the living room"},{id:1003,service_name:"House Cleaning",customer_name:"Mike Johnson",customer_phone:"7654321098",scheduled_date:"2023-05-14",scheduled_time:"9:00 AM",location:"789 Oak Street, Villa 12",pin_code:"600003",price:450,status:"in_progress",notes:"Deep cleaning of 2BHK apartment"},{id:1004,service_name:"AC Repair",customer_name:"Sarah Williams",customer_phone:"6543210987",scheduled_date:"2023-05-10",scheduled_time:"11:00 AM",location:"101 Pine Road, Block C",pin_code:"600004",price:750,status:"completed",notes:"AC not cooling properly"},{id:1005,service_name:"Plumbing Service",customer_name:"Robert Brown",customer_phone:"5432109876",scheduled_date:"2023-05-08",scheduled_time:"3:00 PM",location:"202 Maple Drive, Floor 3",pin_code:"600005",price:600,status:"cancelled",notes:"Bathroom faucet replacement"}]},filterRequests(){let e=[...this.allRequests];if(e=e.filter((e=>this.statusFilter.includes(e.status))),this.searchQuery.trim()){const t=this.searchQuery.toLowerCase();e=e.filter((e=>e.service_name.toLowerCase().includes(t)||e.customer_name.toLowerCase().includes(t)||e.location.toLowerCase().includes(t)||e.id.toString().includes(t)))}this.filteredRequests=e},formatDate(e){if(!e)return"";const t={year:"numeric",month:"short",day:"numeric"};return new Date(e).toLocaleDateString(void 0,t)},getStatusBadgeClass(e){const t={pending:"bg-warning",accepted:"bg-info",in_progress:"bg-primary",completed:"bg-success",cancelled:"bg-secondary",rejected:"bg-danger"};return t[e]||"bg-secondary"},viewRequestDetails(e){this.selectedRequest={...e},this.$nextTick((()=>{this.$refs.detailsModal&&(this.initModal?(this.modalInstance=this.initModal(),this.modalInstance&&this.modalInstance.show()):Promise.resolve().then(s.bind(s,292)).then((e=>{this.modalInstance=new e.Modal(this.$refs.detailsModal),this.modalInstance.show()})).catch((e=>{console.error("Error loading bootstrap:",e)})))}))},async updateRequestStatus(e,t){try{this.modalInstance&&this.modalInstance.hide();const s=await n.YR.updateRequestStatus(e,t);if(s){const s=this.allRequests.findIndex((t=>t.id===e));-1!==s&&(this.allRequests[s].status=t,this.filterRequests()),alert(`Request ${e} has been ${t}`)}else{const s=this.allRequests.findIndex((t=>t.id===e));-1!==s&&(this.allRequests[s].status=t,this.filterRequests())}}catch(s){console.error("Error updating request status:",s),alert("Failed to update request status. Please try again.");const a=this.allRequests.findIndex((t=>t.id===e));-1!==a&&(this.allRequests[a].status=t,this.filterRequests())}},acceptRequest(e){this.updateRequestStatus(e.id,"accepted")},rejectRequest(e){this.updateRequestStatus(e.id,"rejected")},startService(e){this.updateRequestStatus(e.id,"in_progress")},completeService(e){this.updateRequestStatus(e.id,"completed")}},created(){this.fetchRequests()},mounted(){this.$nextTick((()=>{this.$refs.detailsModal&&Promise.resolve().then(s.bind(s,292)).then((e=>{const t=e.Modal;this.initModal=()=>this.$refs.detailsModal?new t(this.$refs.detailsModal):null})).catch((e=>{console.error("Error loading bootstrap:",e)}))}))}},l=c;var r=s(656),o=(0,r.A)(l,a,i,!1,null,null,null);const u=o.exports}}]);
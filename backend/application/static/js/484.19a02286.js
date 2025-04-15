"use strict";(self["webpackChunkhousehold_services"]=self["webpackChunkhousehold_services"]||[]).push([[484],{484:(e,t,s)=>{s.r(t),s.d(t,{default:()=>q});var a=function(){var e=this,t=e._self._c;return t("div",{staticClass:"customer-dashboard"},[t("div",{staticClass:"container py-4"},[t("div",{staticClass:"row mb-4"},[t("div",{staticClass:"col-md-8"},[t("h2",[e._v("Welcome, "+e._s(e.userName)+"!")]),t("p",{staticClass:"text-muted"},[e._v("Find services and manage your requests")])]),t("div",{staticClass:"col-md-4 text-md-end"},[t("router-link",{staticClass:"btn btn-outline-primary me-2",attrs:{to:"/customer/profile"}},[t("i",{staticClass:"fas fa-user-circle me-1"}),e._v(" My Profile ")]),t("button",{staticClass:"btn btn-primary",on:{click:function(t){e.showNewRequestModal=!0}}},[t("i",{staticClass:"fas fa-plus me-2"}),e._v("New Service Request ")])],1)]),t("ul",{staticClass:"nav nav-pills mb-4"},[t("li",{staticClass:"nav-item"},[t("a",{staticClass:"nav-link",class:{active:"browse"===e.activeSection},attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.activeSection="browse"}}},[t("i",{staticClass:"fas fa-search me-1"}),e._v(" Browse Services ")])]),t("li",{staticClass:"nav-item"},[t("a",{staticClass:"nav-link",class:{active:"requests"===e.activeSection},attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.activeSection="requests"}}},[t("i",{staticClass:"fas fa-list-alt me-1"}),e._v(" My Requests ")])])]),"browse"===e.activeSection?t("div",[t("div",{staticClass:"browse-services-container"},[t("div",{staticClass:"services-header mb-4"},[t("div",{staticClass:"row align-items-center"},[t("div",{staticClass:"col-md-6"},[t("h4",[e._v("Browse Available Services")]),t("p",{staticClass:"text-muted mb-md-0"},[e.loading?t("span",[e._v("Finding the best services for you...")]):t("span",[e._v(e._s(e.filteredServices.length)+" services available")])])]),t("div",{staticClass:"col-md-6 text-md-end"},[t("div",{staticClass:"btn-group"},[t("button",{staticClass:"btn btn-outline-primary",on:{click:e.refreshServices}},[t("i",{staticClass:"fas fa-sync-alt me-1"}),e._v(" Refresh ")]),t("button",{attrs:{claFss:"btn btn-outline-secondary"},on:{click:e.toggleAdvancedSearch}},[t("i",{staticClass:"fas fa-sliders-h me-1"}),e._v(" Filters ")])])])])]),t("ServiceSearchPanel",{class:{"mb-4":!0,collapsed:!e.showAdvancedSearch},attrs:{initialParams:e.searchQuery,categories:e.categories},on:{search:e.handleSearch}}),t("div",{staticClass:"category-chips mb-4"},[e._l(e.popularCategories,(function(s){return t("button",{key:s,staticClass:"category-chip",class:{active:e.searchQuery.category===s},on:{click:function(t){return e.quickFilterByCategory(s)}}},[t("span",[e._v(e._s(s))])])})),t("button",{staticClass:"category-chip",on:{click:e.clearCategoryFilter}},[t("i",{staticClass:"fas fa-times me-1"}),e._v(" Clear ")])],2),e.error?t("div",{staticClass:"alert alert-danger mb-4",attrs:{role:"alert"}},[t("i",{staticClass:"fas fa-exclamation-triangle me-2"}),e._v(" "+e._s(e.error)+" "),t("button",{staticClass:"btn-close float-end",attrs:{type:"button"},on:{click:function(t){e.error=null}}})]):e._e(),t("ServiceList",{attrs:{services:e.filteredServices,loading:e.loading,hasMore:e.hasMoreServices},on:{"view-details":e.selectService,"request-service":e.directRequestService,"load-more":e.loadMoreServices}})],1)]):e._e(),"requests"===e.activeSection?t("div",[t("ul",{staticClass:"nav nav-tabs mb-4"},[t("li",{staticClass:"nav-item"},[t("a",{staticClass:"nav-link",class:{active:"active"===e.activeTab},attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.activeTab="active"}}},[t("i",{staticClass:"fas fa-spinner me-1"}),e._v(" Active Requests "),e.getActiveCount()>0?t("span",{staticClass:"badge rounded-pill bg-primary ms-1"},[e._v(" "+e._s(e.getActiveCount())+" ")]):e._e()])]),t("li",{staticClass:"nav-item"},[t("a",{staticClass:"nav-link",class:{active:"completed"===e.activeTab},attrs:{href:"#"},on:{click:function(t){t.preventDefault(),e.activeTab="completed"}}},[t("i",{staticClass:"fas fa-check-circle me-1"}),e._v(" Service History "),e.getCompletedCount()>0?t("span",{staticClass:"badge rounded-pill bg-success ms-1"},[e._v(" "+e._s(e.getCompletedCount())+" ")]):e._e()])])]),e.loading?t("div",{staticClass:"text-center py-5"},[e._m(0),t("p",{staticClass:"mt-2"},[e._v("Loading your requests...")])]):0===e.filteredRequests.length?t("div",{staticClass:"text-center py-5"},[t("i",{staticClass:"fas fa-inbox fa-3x text-muted mb-3"}),t("h5",[e._v("No service requests found")]),t("p",{staticClass:"text-muted"},[e._v(" "+e._s("active"===e.activeTab?"Create a new request to get started!":"No completed requests yet.")+" ")]),"active"===e.activeTab?t("button",{staticClass:"btn btn-primary mt-2",on:{click:function(t){e.showNewRequestModal=!0}}},[t("i",{staticClass:"fas fa-plus me-2"}),e._v("Create Service Request ")]):e._e()]):t("div",{staticClass:"row g-4"},e._l(e.filteredRequests,(function(s){return t("div",{key:s.id,staticClass:"col-md-6"},[t("div",{staticClass:"card h-100 shadow-sm",class:{"border-warning":"pending"===s.status,"border-primary":"in_progress"===s.status,"border-success":"completed"===s.status}},[t("div",{staticClass:"card-header bg-transparent d-flex justify-content-between align-items-center"},[t("span",{class:e.getStatusBadgeClass(s.status)},[e._v(" "+e._s(s.status)+" ")]),t("small",{staticClass:"text-muted"},[t("i",{staticClass:"fas fa-calendar me-1"}),e._v(" "+e._s(e.formatDate(s.created_at,!0))+" ")])]),t("div",{staticClass:"card-body"},[t("h5",{staticClass:"card-title mb-3"},[e._v(e._s(s.service.name))]),t("div",{staticClass:"d-flex mb-3"},[t("div",{staticClass:"me-3"},[t("i",{staticClass:"fas fa-map-marker-alt text-muted me-1"}),e._v(" "+e._s(s.pin_code)+" ")]),s.final_amount?t("div",[t("i",{staticClass:"fas fa-money-bill-wave text-success me-1"}),e._v(" ₹"+e._s(s.final_amount)+" ")]):e._e()]),s.professional?t("div",{staticClass:"mb-3 p-2 bg-light rounded"},[t("div",{staticClass:"d-flex align-items-center"},[t("i",{staticClass:"fas fa-user-tie text-primary me-2 fa-lg"}),t("div",[t("strong",[e._v(e._s(s.professional.professional_name))]),t("p",{staticClass:"text-muted mb-0 small"},[e._v(e._s(s.professional.service_type))])])])]):e._e(),s.special_instructions?t("p",{staticClass:"card-text text-truncate mb-3",attrs:{title:s.special_instructions}},[e._v(" "+e._s(s.special_instructions)+" ")]):e._e(),t("div",{staticClass:"mb-3 service-progress"},[t("div",{staticClass:"status-track d-flex justify-content-between"},[t("div",{staticClass:"status-point",class:{active:!0}},[t("i",{staticClass:"fas fa-plus-circle"}),t("span",[e._v("Created")])]),t("div",{staticClass:"status-point",class:{active:["in_progress","completed","closed"].includes(s.status)}},[t("i",{staticClass:"fas fa-tools"}),t("span",[e._v("In Progress")])]),t("div",{staticClass:"status-point",class:{active:["completed","closed"].includes(s.status)}},[t("i",{staticClass:"fas fa-check-circle"}),t("span",[e._v("Completed")])])])]),t("div",{staticClass:"d-flex justify-content-end gap-2 mt-3"},["pending"===s.status||"assigned"===s.status?t("button",{staticClass:"btn btn-outline-danger btn-sm",on:{click:function(t){return e.closeRequest(s)}}},[t("i",{staticClass:"fas fa-times me-1"}),e._v(" Close ")]):e._e(),"pending"===s.status?t("button",{staticClass:"btn btn-outline-primary btn-sm",on:{click:function(t){return e.editRequest(s)}}},[t("i",{staticClass:"fas fa-edit me-1"}),e._v(" Edit ")]):e._e(),"completed"!==s.status||s.has_review?e._e():t("button",{staticClass:"btn btn-outline-success btn-sm",on:{click:function(t){return e.addReview(s)}}},[t("i",{staticClass:"fas fa-star me-1"}),e._v(" Review ")]),t("button",{staticClass:"btn btn-outline-secondary btn-sm",on:{click:function(t){return e.viewRequestDetails(s)}}},[t("i",{staticClass:"fas fa-eye me-1"}),e._v(" Details ")])])])])])})),0)]):e._e()]),e.showServiceModal?t("div",{staticClass:"modal fade",class:{show:e.showServiceModal}},[t("div",{staticClass:"modal-dialog"},[t("div",{staticClass:"modal-content"},[t("div",{staticClass:"modal-header"},[t("h5",{staticClass:"modal-title"},[e._v("Service Details")]),t("button",{staticClass:"btn-close",attrs:{type:"button"},on:{click:function(t){e.showServiceModal=!1}}})]),e.selectedService?t("div",{staticClass:"modal-body"},[t("div",{staticClass:"service-details"},[t("h4",[e._v(e._s(e.selectedService.name))]),t("div",{staticClass:"d-flex justify-content-between mb-3"},[t("span",{staticClass:"badge bg-primary fs-5"},[e._v("₹"+e._s(e.selectedService.base_price))]),t("span",{staticClass:"text-muted"},[t("i",{staticClass:"far fa-clock me-2"}),e._v(e._s(e.selectedService.time_required)+" minutes")])]),t("p",[e._v(e._s(e.selectedService.description))]),t("div",{staticClass:"mb-3"},[t("strong",[e._v("Category:")]),e._v(" "+e._s(e.selectedService.category)+" ")])])]):e._e(),t("div",{staticClass:"modal-footer"},[t("button",{staticClass:"btn btn-secondary",attrs:{type:"button"},on:{click:function(t){e.showServiceModal=!1}}},[e._v("Close")]),t("button",{staticClass:"btn btn-primary",attrs:{type:"button"},on:{click:e.requestSelectedService}},[t("i",{staticClass:"fas fa-plus me-1"}),e._v(" Request Service ")])])])])]):e._e(),e.showNewRequestModal?t("div",{staticClass:"modal fade",class:{show:e.showNewRequestModal}},[t("div",{staticClass:"modal-dialog"},[t("div",{staticClass:"modal-content"},[t("div",{staticClass:"modal-header"},[t("h5",{staticClass:"modal-title"},[e._v("New Service Request")]),t("button",{staticClass:"btn-close",attrs:{type:"button"},on:{click:function(t){e.showNewRequestModal=!1}}})]),t("div",{staticClass:"modal-body"},[t("form",{on:{submit:function(t){return t.preventDefault(),e.createRequest.apply(null,arguments)}}},[t("div",{staticClass:"mb-3"},[t("label",{staticClass:"form-label",attrs:{for:"serviceCategory"}},[e._v("Service Category")]),t("select",{directives:[{name:"model",rawName:"v-model",value:e.newRequest.category,expression:"newRequest.category"}],staticClass:"form-select",attrs:{id:"serviceCategory",name:"serviceCategory"},on:{change:function(t){var s=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){var t="_value"in e?e._value:e.value;return t}));e.$set(e.newRequest,"category",t.target.multiple?s:s[0])}}},[t("option",{attrs:{value:""}},[e._v("Select Category")]),e._l(e.categories,(function(s){return t("option",{key:s,domProps:{value:s}},[e._v(" "+e._s(s)+" ")])}))],2)]),t("div",{staticClass:"mb-3"},[t("label",{staticClass:"form-label",attrs:{for:"pinCode"}},[e._v("PIN Code")]),t("input",{directives:[{name:"model",rawName:"v-model",value:e.newRequest.pin_code,expression:"newRequest.pin_code"}],staticClass:"form-control",attrs:{id:"pinCode",name:"pinCode",type:"text",required:"",pattern:"[0-9]{6}",placeholder:"Enter 6-digit PIN code"},domProps:{value:e.newRequest.pin_code},on:{input:function(t){t.target.composing||e.$set(e.newRequest,"pin_code",t.target.value)}}})]),t("div",{staticClass:"mb-3"},[t("label",{staticClass:"form-label",attrs:{for:"specialInstructions"}},[e._v("Special Instructions")]),t("textarea",{directives:[{name:"model",rawName:"v-model",value:e.newRequest.special_instructions,expression:"newRequest.special_instructions"}],staticClass:"form-control",attrs:{id:"specialInstructions",name:"specialInstructions",rows:"3",placeholder:"Any specific requirements or details..."},domProps:{value:e.newRequest.special_instructions},on:{input:function(t){t.target.composing||e.$set(e.newRequest,"special_instructions",t.target.value)}}})]),t("div",{staticClass:"text-end"},[t("button",{staticClass:"btn btn-secondary me-2",attrs:{type:"button"},on:{click:function(t){e.showNewRequestModal=!1}}},[e._v(" Cancel ")]),t("button",{staticClass:"btn btn-primary",attrs:{type:"submit",disabled:e.isLoading}},[e.isLoading?t("span",{staticClass:"spinner-border spinner-border-sm me-2"}):e._e(),e._v(" Create Request ")])])])])])])]):e._e(),e.showReviewModal?t("div",{staticClass:"modal fade",class:{show:e.showReviewModal}},[t("div",{staticClass:"modal-dialog"},[t("div",{staticClass:"modal-content"},[t("ServiceReviewForm",{attrs:{requestId:e.selectedRequest?.id,serviceName:e.selectedRequest?.service?.name,serviceDate:e.selectedRequest?.completed_at,professionalName:e.selectedRequest?.professional?.professional_name},on:{close:function(t){e.showReviewModal=!1},submitted:e.handleReviewSubmitted}})],1)])]):e._e(),e.showRequestDetailsModal?t("div",{staticClass:"modal fade",class:{show:e.showRequestDetailsModal}},[t("div",{staticClass:"modal-dialog modal-lg"},[t("div",{staticClass:"modal-content"},[t("div",{staticClass:"modal-header"},[t("h5",{staticClass:"modal-title"},[e._v("Request Details")]),t("button",{staticClass:"btn-close",attrs:{type:"button"},on:{click:function(t){e.showRequestDetailsModal=!1}}})]),e.selectedRequest?t("div",{staticClass:"modal-body"},[t("div",{staticClass:"row mb-4"},[t("div",{staticClass:"col-md-6"},[t("h5",[e._v(e._s(e.selectedRequest.service?.name))]),t("div",{staticClass:"mb-2 badge-lg",class:e.getStatusBadgeClass(e.selectedRequest.status)},[e._v(" "+e._s(e.selectedRequest.status)+" ")]),t("p",{staticClass:"text-muted"},[t("i",{staticClass:"fas fa-map-marker-alt me-2"}),e._v(" PIN Code: "+e._s(e.selectedRequest.pin_code)+" ")]),e.selectedRequest.final_amount?t("p",{staticClass:"badge bg-success"},[e._v(" Final Amount: ₹"+e._s(e.selectedRequest.final_amount)+" ")]):e._e()]),t("div",{staticClass:"col-md-6 text-md-end"},[t("p",{staticClass:"mb-1"},[t("strong",[e._v("Requested:")]),e._v(" "+e._s(e.formatDate(e.selectedRequest.created_at)))]),e.selectedRequest.accepted_at?t("p",{staticClass:"mb-1"},[t("strong",[e._v("Accepted:")]),e._v(" "+e._s(e.formatDate(e.selectedRequest.accepted_at))+" ")]):e._e(),e.selectedRequest.completed_at?t("p",{staticClass:"mb-1"},[t("strong",[e._v("Completed:")]),e._v(" "+e._s(e.formatDate(e.selectedRequest.completed_at))+" ")]):e._e(),e.selectedRequest.closed_at?t("p",{staticClass:"mb-1"},[t("strong",[e._v("Closed:")]),e._v(" "+e._s(e.formatDate(e.selectedRequest.closed_at))+" ")]):e._e()])]),t("div",{staticClass:"service-timeline mb-4"},[t("h6",[e._v("Service Timeline")]),t("div",{staticClass:"timeline"},[t("div",{staticClass:"timeline-item"},[t("div",{staticClass:"timeline-marker bg-success"}),t("div",{staticClass:"timeline-content"},[e._m(1),t("p",{staticClass:"text-muted small mb-0"},[e._v(e._s(e.formatDate(e.selectedRequest.created_at)))])])]),e.selectedRequest.accepted_at?t("div",{staticClass:"timeline-item"},[t("div",{staticClass:"timeline-marker bg-primary"}),t("div",{staticClass:"timeline-content"},[e._m(2),t("p",{staticClass:"text-muted small mb-0"},[e._v(e._s(e.formatDate(e.selectedRequest.accepted_at)))]),e.selectedRequest.professional?t("p",{staticClass:"small mb-0"},[e._v(" "+e._s(e.selectedRequest.professional.professional_name)+" was assigned to your request ")]):e._e()])]):e._e(),e.selectedRequest.completed_at?t("div",{staticClass:"timeline-item"},[t("div",{staticClass:"timeline-marker bg-info"}),t("div",{staticClass:"timeline-content"},[e._m(3),t("p",{staticClass:"text-muted small mb-0"},[e._v(e._s(e.formatDate(e.selectedRequest.completed_at)))]),e.selectedRequest.final_amount?t("p",{staticClass:"small mb-0"},[e._v(" Service completed with final amount: ₹"+e._s(e.selectedRequest.final_amount)+" ")]):e._e()])]):e._e(),e.selectedRequest.closed_at?t("div",{staticClass:"timeline-item"},[t("div",{staticClass:"timeline-marker bg-secondary"}),t("div",{staticClass:"timeline-content"},[e._m(4),t("p",{staticClass:"text-muted small mb-0"},[e._v(e._s(e.formatDate(e.selectedRequest.closed_at)))])])]):e._e(),e.selectedRequest.has_review?t("div",{staticClass:"timeline-item"},[t("div",{staticClass:"timeline-marker bg-warning"}),t("div",{staticClass:"timeline-content"},[e._m(5),e.selectedRequest.review?t("div",{staticClass:"mt-1"},[t("div",{staticClass:"star-rating small"},e._l(5,(function(s){return t("i",{key:s,staticClass:"fas fa-star",class:s<=e.selectedRequest.review.rating?"text-warning":"text-muted"})})),0),t("p",{staticClass:"small mt-1 mb-0"},[e._v(e._s(e.selectedRequest.review.remarks))])]):e._e()])]):e._e()])]),t("div",{staticClass:"mb-4"},[t("h6",[e._v("Special Instructions")]),t("p",{staticClass:"p-3 bg-light rounded"},[e._v(e._s(e.selectedRequest.special_instructions||"No special instructions provided."))])]),e.selectedRequest.professional?t("div",{staticClass:"mb-4"},[t("h6",[e._v("Professional Details")]),t("div",{staticClass:"card"},[t("div",{staticClass:"card-body"},[t("h5",{staticClass:"card-title"},[e._v(e._s(e.selectedRequest.professional.professional_name))]),t("p",{staticClass:"text-muted mb-1"},[t("strong",[e._v("Service Type:")]),e._v(" "+e._s(e.selectedRequest.professional.service_type)+" ")]),t("p",{staticClass:"text-muted mb-0"},[t("strong",[e._v("Experience:")]),e._v(" "+e._s(e.selectedRequest.professional.experience)+" years ")])])])]):e._e(),t("div",{staticClass:"d-flex justify-content-end gap-2 mt-4"},["pending"===e.selectedRequest.status||"assigned"===e.selectedRequest.status?t("button",{staticClass:"btn btn-danger",on:{click:function(t){return e.closeRequest(e.selectedRequest,!0)}}},[t("i",{staticClass:"fas fa-times me-1"}),e._v(" Cancel Request ")]):e._e(),"completed"!==e.selectedRequest.status||e.selectedRequest.has_review?e._e():t("button",{staticClass:"btn btn-warning",on:{click:function(t){return e.addReview(e.selectedRequest)}}},[t("i",{staticClass:"fas fa-star me-1"}),e._v(" Review Service ")]),t("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.showRequestDetailsModal=!1}}},[e._v(" Close ")])])]):e._e()])])]):e._e()])},i=[function(){var e=this,t=e._self._c;return t("div",{staticClass:"spinner-border text-primary",attrs:{role:"status"}},[t("span",{staticClass:"visually-hidden"},[e._v("Loading...")])])},function(){var e=this,t=e._self._c;return t("p",{staticClass:"mb-0"},[t("strong",[e._v("Request Created")])])},function(){var e=this,t=e._self._c;return t("p",{staticClass:"mb-0"},[t("strong",[e._v("Professional Assigned")])])},function(){var e=this,t=e._self._c;return t("p",{staticClass:"mb-0"},[t("strong",[e._v("Service Completed")])])},function(){var e=this,t=e._self._c;return t("p",{staticClass:"mb-0"},[t("strong",[e._v("Request Closed")])])},function(){var e=this,t=e._self._c;return t("p",{staticClass:"mb-0"},[t("strong",[e._v("Review Submitted")])])}],r=s(844),c=function(){var e=this,t=e._self._c;return t("div",{staticClass:"service-search-panel"},[t("div",{staticClass:"card shadow-sm mb-4"},[t("div",{staticClass:"card-body"},[t("h5",{staticClass:"card-title mb-3"},[e._v("Find Services")]),t("div",{staticClass:"row g-3"},[t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"input-group"},[e._m(0),t("input",{directives:[{name:"model",rawName:"v-model",value:e.searchParams.name,expression:"searchParams.name"}],staticClass:"form-control",attrs:{type:"text",placeholder:"Service name..."},domProps:{value:e.searchParams.name},on:{input:[function(t){t.target.composing||e.$set(e.searchParams,"name",t.target.value)},e.emitSearch]}})])]),t("div",{staticClass:"col-md-4"},[t("div",{staticClass:"input-group"},[e._m(1),t("input",{directives:[{name:"model",rawName:"v-model",value:e.searchParams.pinCode,expression:"searchParams.pinCode"}],staticClass:"form-control",attrs:{type:"text",placeholder:"PIN code..."},domProps:{value:e.searchParams.pinCode},on:{input:[function(t){t.target.composing||e.$set(e.searchParams,"pinCode",t.target.value)},e.emitSearch]}})])]),t("div",{staticClass:"col-md-4"},[t("select",{directives:[{name:"model",rawName:"v-model",value:e.searchParams.category,expression:"searchParams.category"}],staticClass:"form-select",on:{change:[function(t){var s=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){var t="_value"in e?e._value:e.value;return t}));e.$set(e.searchParams,"category",t.target.multiple?s:s[0])},e.emitSearch]}},[t("option",{attrs:{value:""}},[e._v("All Categories")]),e._l(e.categories,(function(s){return t("option",{key:s,domProps:{value:s}},[e._v(" "+e._s(s)+" ")])}))],2)])]),t("div",{staticClass:"mt-3"},[t("div",{staticClass:"accordion",attrs:{id:"accordionFilters"}},[t("div",{staticClass:"accordion-item border-0"},[e._m(2),t("div",{staticClass:"accordion-collapse collapse",attrs:{id:"collapseAdvanced","aria-labelledby":"headingAdvanced","data-bs-parent":"#accordionFilters"}},[t("div",{staticClass:"accordion-body px-0 pt-3"},[t("div",{staticClass:"row g-3"},[t("div",{staticClass:"col-md-6"},[t("label",{staticClass:"form-label"},[e._v("Price Range")]),t("div",{staticClass:"d-flex gap-2"},[t("input",{directives:[{name:"model",rawName:"v-model",value:e.searchParams.priceMin,expression:"searchParams.priceMin"}],staticClass:"form-control",attrs:{type:"number",placeholder:"Min"},domProps:{value:e.searchParams.priceMin},on:{input:[function(t){t.target.composing||e.$set(e.searchParams,"priceMin",t.target.value)},e.emitSearch]}}),t("input",{directives:[{name:"model",rawName:"v-model",value:e.searchParams.priceMax,expression:"searchParams.priceMax"}],staticClass:"form-control",attrs:{type:"number",placeholder:"Max"},domProps:{value:e.searchParams.priceMax},on:{input:[function(t){t.target.composing||e.$set(e.searchParams,"priceMax",t.target.value)},e.emitSearch]}})])]),t("div",{staticClass:"col-md-6"},[t("label",{staticClass:"form-label"},[e._v("Sort By")]),t("select",{directives:[{name:"model",rawName:"v-model",value:e.searchParams.sortBy,expression:"searchParams.sortBy"}],staticClass:"form-select",on:{change:[function(t){var s=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){var t="_value"in e?e._value:e.value;return t}));e.$set(e.searchParams,"sortBy",t.target.multiple?s:s[0])},e.emitSearch]}},[t("option",{attrs:{value:""}},[e._v("Default")]),t("option",{attrs:{value:"price_asc"}},[e._v("Price: Low to High")]),t("option",{attrs:{value:"price_desc"}},[e._v("Price: High to Low")]),t("option",{attrs:{value:"rating"}},[e._v("Rating")])])])])])])])])])])])])},l=[function(){var e=this,t=e._self._c;return t("span",{staticClass:"input-group-text"},[t("i",{staticClass:"fas fa-search"})])},function(){var e=this,t=e._self._c;return t("span",{staticClass:"input-group-text"},[t("i",{staticClass:"fas fa-map-marker-alt"})])},function(){var e=this,t=e._self._c;return t("h2",{staticClass:"accordion-header",attrs:{id:"headingAdvanced"}},[t("button",{staticClass:"accordion-button collapsed p-0 bg-transparent shadow-none",attrs:{type:"button","data-bs-toggle":"collapse","data-bs-target":"#collapseAdvanced","aria-expanded":"false","aria-controls":"collapseAdvanced"}},[t("small",[e._v("Advanced Filters")])])])}],n=s(648);const o={name:"ServiceSearchPanel",props:{initialParams:{type:Object,default:()=>({})},categories:{type:Array,default:()=>[]}},emits:["search"],setup(e,{emit:t}){const s=(0,n.Kh)({name:e.initialParams.name||"",pinCode:e.initialParams.pinCode||"",category:e.initialParams.category||"",priceMin:e.initialParams.priceMin||"",priceMax:e.initialParams.priceMax||"",sortBy:e.initialParams.sortBy||""}),a=()=>{t("search",{...s})};return(0,n.wB)((()=>e.initialParams),(e=>{Object.keys(e).forEach((t=>{void 0!==s[t]&&(s[t]=e[t])}))}),{deep:!0}),{searchParams:s,emitSearch:a}}},d=o;var u=s(656),v=(0,u.A)(d,c,l,!1,null,null,null);const m=v.exports;var p=s(535),h=function(){var e=this,t=e._self._c;return t("div",[t("div",{staticClass:"modal-header"},[t("h5",{staticClass:"modal-title"},[e._v("Rate Your Service")]),t("button",{staticClass:"btn-close",attrs:{type:"button"},on:{click:function(t){return e.$emit("close")}}})]),t("div",{staticClass:"modal-body"},[t("div",{staticClass:"service-review-form"},[t("div",{staticClass:"text-center mb-4"},[t("h5",[e._v(e._s(e.serviceName))]),t("p",{staticClass:"text-muted small"},[e._v(" Completed on "+e._s(e.formatDate(e.serviceDate))+" by "+e._s(e.professionalName)+" ")])]),t("form",{on:{submit:function(t){return t.preventDefault(),e.submitReview.apply(null,arguments)}}},[t("div",{staticClass:"mb-4 text-center"},[t("label",{staticClass:"form-label d-block"},[e._v("Your Rating")]),t("div",{staticClass:"star-rating"},e._l(5,(function(s){return t("span",{key:s,staticClass:"star-rating-item",class:{selected:s<=e.rating},on:{click:function(t){return e.setRating(s)},mouseover:function(t){e.hoverRating=s},mouseleave:function(t){e.hoverRating=0}}},[t("span",{staticClass:"star-icon",class:{"text-warning":s<=(e.hoverRating||e.rating),"text-muted":s>(e.hoverRating||e.rating)}},[e._v("★")])])})),0),t("div",{staticClass:"rating-text mt-2"},[e._v(" "+e._s(e.getRatingText())+" ")]),e.validationErrors.rating?t("div",{staticClass:"text-danger"},[e._v(" "+e._s(e.validationErrors.rating)+" ")]):e._e()]),t("div",{staticClass:"mb-4"},[t("label",{staticClass:"form-label",attrs:{for:"reviewRemarks"}},[e._v("Your Comments")]),t("textarea",{directives:[{name:"model",rawName:"v-model",value:e.remarks,expression:"remarks"}],staticClass:"form-control",attrs:{id:"reviewRemarks",rows:"4",placeholder:"Share your experience with this service professional..."},domProps:{value:e.remarks},on:{input:function(t){t.target.composing||(e.remarks=t.target.value)}}}),e.validationErrors.remarks?t("div",{staticClass:"text-danger"},[e._v(" "+e._s(e.validationErrors.remarks)+" ")]):e._e()]),t("div",{staticClass:"d-flex justify-content-end"},[t("button",{staticClass:"btn btn-secondary me-2",attrs:{type:"button"},on:{click:function(t){return e.$emit("close")}}},[e._v("Cancel")]),t("button",{staticClass:"btn btn-primary",attrs:{type:"submit",disabled:e.isSubmitting}},[e.isSubmitting?t("span",{staticClass:"spinner-border spinner-border-sm me-1"}):e._e(),e._v(" Submit Review ")])])])])])])},g=[];const C={name:"ServiceReviewForm",props:{requestId:{type:Number,required:!0},serviceName:{type:String,default:"Service"},serviceDate:{type:String,default:null},professionalName:{type:String,default:"Professional"}},data(){return{rating:0,hoverRating:0,remarks:"",isSubmitting:!1,validationErrors:{rating:"",remarks:""}}},methods:{setRating(e){this.rating=e,this.validationErrors.rating=""},getRatingText(){const e=["Select a rating","Poor","Fair","Good","Very Good","Excellent"];return e[this.rating]||e[0]},validateForm(){let e=!0;return this.validationErrors={rating:"",remarks:""},(!this.rating||this.rating<1)&&(this.validationErrors.rating="Please select a rating",e=!1),this.remarks.trim()?this.remarks.length<5&&(this.validationErrors.remarks="Comments must be at least 5 characters",e=!1):(this.validationErrors.remarks="Please provide some comments about your experience",e=!1),e},async submitReview(){try{if(!this.validateForm())return;this.isSubmitting=!0;const e={rating:this.rating,remarks:this.remarks};await r.xZ.addReview(this.requestId,e),this.rating=0,this.remarks="",this.$emit("submitted")}catch(e){console.error("Error submitting review:",e),alert("Failed to submit review: "+(e.message||"Unknown error"))}finally{this.isSubmitting=!1}},formatDate(e){if(!e)return"N/A";const t=new Date(e);return t.toLocaleDateString("en-US",{year:"numeric",month:"short",day:"numeric"})}}},f=C;var _=(0,u.A)(f,h,g,!1,null,"40435700",null);const b=_.exports,y={name:"CustomerDashboard",components:{ServiceSearchPanel:m,ServiceList:p.A,ServiceReviewForm:b},data(){const e=JSON.parse(localStorage.getItem("user"))||{};return{userName:e.name||e.username||"Customer",activeSection:"browse",activeTab:"active",showServiceModal:!1,showNewRequestModal:!1,showReviewModal:!1,showRequestDetailsModal:!1,selectedService:null,selectedRequest:null,searchQuery:{name:"",category:"",pinCode:""},services:[],categories:["AC Repair","Plumbing","Electrical","Carpentry","Painting","Cleaning","Pest Control","Appliance Repair","Moving Services","Gardening"],serviceRequests:[],loading:!1,error:null,newRequest:{service_id:"",pin_code:"",special_instructions:"",category:""},isLoading:!1,page:1,hasMoreServices:!0,showAdvancedSearch:!1}},computed:{filteredRequests(){return this.serviceRequests.filter((e=>"active"===this.activeTab?["pending","assigned","in_progress"].includes(e.status):["completed","closed"].includes(e.status)))},filteredServices(){return this.services.length?this.services.filter((e=>!(this.searchQuery.name&&!e.name.toLowerCase().includes(this.searchQuery.name.toLowerCase()))&&((!this.searchQuery.category||e.category===this.searchQuery.category)&&!(this.searchQuery.pinCode&&e.available_pin_codes&&!e.available_pin_codes.includes(this.searchQuery.pinCode))))):[]}},methods:{async fetchServices(){try{this.loading=!0,this.error=null;const e=await r.YR.getPublicServices();this.services=e||[]}catch(e){console.error("Error fetching services:",e),this.error="Failed to load services. Please try again."}finally{this.loading=!1}},async fetchServiceTypes(){try{this.loading=!0,console.log("Fetching service categories from database...");const e=await r.YR.getServiceTypes();e&&Array.isArray(e)&&e.length>0?(this.categories=e,console.log(`Received ${this.categories.length} service categories`)):(console.warn("No service categories returned from API, using defaults"),this.categories=["AC Repair","Plumbing","Electrical","Carpentry","Painting","Cleaning","Pest Control","Appliance Repair","Moving Services","Gardening"]),this.loading=!1}catch(e){console.error("Error fetching service categories:",e),this.categories=["AC Repair","Plumbing","Electrical","Carpentry","Painting","Cleaning","Pest Control","Appliance Repair","Moving Services","Gardening"],this.loading=!1}},async fetchRequests(){try{this.loading=!0,console.log("Fetching customer requests...");const e=await r.xZ.getRequests();e&&Array.isArray(e)?(console.log(`Retrieved ${e.length} requests for customer`),this.serviceRequests=e):(console.warn("Invalid response format for customer requests:",e),this.serviceRequests=[])}catch(e){console.error("Error fetching requests:",e),this.error="Failed to load service requests. Please try again.",this.serviceRequests=[]}finally{this.loading=!1}},async refreshServices(){try{this.loading=!0,this.error=null,await this.fetchServices();const e=this.searchQuery.category;this.searchQuery={name:"",category:e,pinCode:""}}catch(e){console.error("Error refreshing services:",e),this.error="Failed to refresh services. Please try again."}finally{this.loading=!1}},toggleAdvancedSearch(){this.showAdvancedSearch=!this.showAdvancedSearch},quickFilterByCategory(e){this.searchQuery.category===e?this.searchQuery.category="":this.searchQuery.category=e,this.handleSearch(this.searchQuery)},clearCategoryFilter(){this.searchQuery.category="",this.handleSearch(this.searchQuery)},async loadMoreServices(){if(!this.loading&&this.hasMoreServices)try{this.loading=!0,this.page+=1;const e=await r.YR.getServices({page:this.page,...this.searchQuery});e&&e.length?(this.services=[...this.services,...e],this.hasMoreServices=e.length>=10):this.hasMoreServices=!1}catch(e){console.error("Error loading more services:",e),this.error="Failed to load more services."}finally{this.loading=!1}},async createRequest(){this.isLoading=!0;try{if(!this.newRequest.service_id&&!this.newRequest.category)throw new Error("Please select a service category");if(!this.newRequest.pin_code||!/^\d{6}$/.test(this.newRequest.pin_code))throw new Error("Please enter a valid 6-digit PIN code");console.log("Submitting request with data:",this.newRequest);try{await r.xZ.createRequest(this.newRequest);this.showNewRequestModal=!1,this.newRequest={service_id:"",pin_code:"",special_instructions:"",category:""},this.activeSection="requests",await this.fetchRequests(),alert("Service request created successfully!")}catch(e){throw e.message.includes("No service found in category")?new Error(`We currently don't have service professionals for ${this.newRequest.category}. Please try a different category.`):e}}catch(t){console.error("Error creating request:",t),alert("Failed to create service request: "+(t.message||"Unknown error"))}finally{this.isLoading=!1}},async closeRequest(e,t=!1){if(confirm("Are you sure you want to cancel this request?"))try{this.isLoading=!0,await r.xZ.closeRequest(e.id),await this.fetchRequests(),t&&(this.showRequestDetailsModal=!1),alert("Request cancelled successfully.")}catch(s){console.error("Error closing request:",s),alert("Failed to cancel request: "+(s.message||"Unknown error"))}finally{this.isLoading=!1}},editRequest(e){this.newRequest={service_id:e.service_id,pin_code:e.pin_code,special_instructions:e.special_instructions||"",category:e.category||""},this.showNewRequestModal=!0},addReview(e){this.selectedRequest=e,this.review={rating:0,remarks:""},this.showReviewModal=!0},async submitReview(){try{this.isLoading=!0,await r.xZ.addReview(this.selectedRequest.id,this.review),this.showReviewModal=!1,this.review={rating:0,remarks:""},await this.fetchRequests(),alert("Review submitted successfully.")}catch(e){console.error("Error submitting review:",e),alert("Failed to submit review: "+(e.message||"Unknown error"))}finally{this.isLoading=!1}},selectService(e){this.selectedService=e,this.showServiceModal=!0},requestSelectedService(){this.newRequest.service_id=this.selectedService.id,this.showServiceModal=!1,this.showNewRequestModal=!0},viewRequestDetails(e){this.selectedRequest=e,this.showRequestDetailsModal=!0},formatDate(e,t=!1){if(!e)return"N/A";const s=new Date(e);return t?s.toLocaleDateString("en-US",{month:"short",day:"numeric"}):s.toLocaleString("en-US",{year:"numeric",month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"})},getStatusBadgeClass(e){const t={pending:"badge bg-warning",assigned:"badge bg-info",in_progress:"badge bg-primary",completed:"badge bg-success",closed:"badge bg-secondary",cancelled:"badge bg-danger"};return t[e]||"badge bg-secondary"},handleSearch(e){this.searchQuery={...e},this.page=1,this.fetchServices()},directRequestService(e){this.selectedService=e,this.showNewRequestModal=!0,this.newRequest.service_id=e.id},handleReviewSubmitted(){this.showReviewModal=!1,alert("Thank you for your review!"),this.fetchRequests()},getActiveCount(){return this.serviceRequests.filter((e=>["pending","assigned","in_progress"].includes(e.status))).length},getCompletedCount(){return this.serviceRequests.filter((e=>["completed","closed"].includes(e.status))).length},async createServiceRequest(e){try{if(!this.newRequest.pin_code||!/^\d{6}$/.test(this.newRequest.pin_code))throw new Error("Please enter a valid 6-digit PIN code");this.isLoading=!0,await r.xZ.createRequest({service_id:e,pin_code:this.newRequest.pin_code,special_instructions:this.newRequest.special_instructions}),this.showNewRequestModal=!1,this.fetchRequests(),this.$toast.success("Service request created successfully")}catch(t){console.error("Error creating request:",t),this.$toast.error(t.message||"Failed to create request")}finally{this.isLoading=!1}}},async created(){try{console.log("CustomerDashboard created, loading data..."),await Promise.all([this.fetchServices(),this.fetchServiceTypes(),this.fetchRequests()])}catch(e){console.error("Error initializing dashboard:",e),this.error="Failed to load dashboard data. Please refresh the page."}}},w=y;var R=(0,u.A)(w,a,i,!1,null,"5c2c2238",null);const q=R.exports},535:(e,t,s)=>{s.d(t,{A:()=>o});var a=function(){var e=this,t=e._self._c;return t("div",{staticClass:"service-list"},[e.loading||e.services&&0!==e.services.length?e.loading?t("div",{staticClass:"text-center py-5"},[e._m(1),t("p",{staticClass:"mt-2"},[e._v("Finding services for you...")])]):t("div",{staticClass:"row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4"},e._l(e.services,(function(s){return t("div",{key:s.id,staticClass:"col"},[t("div",{staticClass:"card h-100 service-card"},[t("div",{staticClass:"card-category-badge",style:{backgroundColor:e.getCategoryColor(s.category)}},[e._v(" "+e._s(s.category)+" ")]),t("div",{staticClass:"card-body"},[t("div",{staticClass:"d-flex justify-content-between align-items-start"},[t("h5",{staticClass:"card-title"},[e._v(e._s(s.name))]),t("span",{staticClass:"price-badge"},[e._v("₹"+e._s(s.base_price))])]),t("div",{staticClass:"service-meta my-3"},[t("span",{staticClass:"meta-item"},[t("i",{staticClass:"far fa-clock me-1"}),e._v(" "+e._s(s.time_required||60)+" mins")]),s.rating?t("span",{staticClass:"meta-item"},[t("i",{staticClass:"fas fa-star text-warning me-1"}),e._v(" "+e._s(s.rating)+" ")]):e._e()]),t("p",{staticClass:"card-text service-description"},[e._v(e._s(s.description||"No description available"))]),s.features&&s.features.length?t("div",{staticClass:"service-features mt-3"},e._l(s.features,(function(s){return t("span",{key:s,staticClass:"feature-badge"},[e._v(" "+e._s(s)+" ")])})),0):e._e()]),t("div",{staticClass:"card-footer bg-transparent border-0"},[t("div",{staticClass:"d-flex gap-2"},[t("button",{staticClass:"btn btn-outline-primary flex-grow-1",on:{click:function(t){return e.$emit("view-details",s)}}},[t("i",{staticClass:"fas fa-info-circle me-1"}),e._v(" Details ")]),t("button",{staticClass:"btn btn-primary flex-grow-1",on:{click:function(t){return e.$emit("request-service",s)}}},[t("i",{staticClass:"fas fa-plus me-1"}),e._v(" Request ")])])])])])})),0):t("div",{staticClass:"text-center py-5"},[e._m(0)]),!e.loading&&e.hasMore&&e.services.length>0?t("div",{staticClass:"text-center mt-4"},[t("button",{staticClass:"btn btn-outline-primary",on:{click:function(t){return e.$emit("load-more")}}},[t("i",{staticClass:"fas fa-spinner me-1"}),e._v(" Load More Services ")])]):e._e()])},i=[function(){var e=this,t=e._self._c;return t("div",{staticClass:"empty-state"},[t("i",{staticClass:"fas fa-search fa-3x text-muted mb-3"}),t("h5",[e._v("No services found")]),t("p",{staticClass:"text-muted"},[e._v("Try adjusting your search filters")])])},function(){var e=this,t=e._self._c;return t("div",{staticClass:"spinner-border text-primary",attrs:{role:"status"}},[t("span",{staticClass:"visually-hidden"},[e._v("Loading...")])])}];const r={name:"ServiceList",props:{services:{type:Array,default:()=>[]},loading:{type:Boolean,default:!1},hasMore:{type:Boolean,default:!1}},emits:["view-details","request-service","load-more"],setup(){const e={"AC Repair":"#4CAF50",Plumbing:"#2196F3",Electrical:"#FFC107",Carpentry:"#795548",Painting:"#9C27B0",Cleaning:"#03A9F4","Pest Control":"#F44336","Appliance Repair":"#FF9800","Moving Services":"#607D8B",Gardening:"#8BC34A"},t=t=>e[t]||"#9E9E9E";return{getCategoryColor:t}}},c=r;var l=s(656),n=(0,l.A)(c,a,i,!1,null,"4d4a653b",null);const o=n.exports}}]);
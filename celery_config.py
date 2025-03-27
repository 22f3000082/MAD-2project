
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
timezone = "Asia/Kolkata"  # Changed from 'Timezone' to 'timezone'
broker_connection_retry_on_startup = True
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
worker_hijack_root_logger = False  # Don't hijack the root logger
worker_redirect_stdouts = False    # Don't redirect stdout/stderr
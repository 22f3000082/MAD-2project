broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
timezone = "Asia/Kolkata"  # Changed from 'Timezone' to 'timezone'
broker_connection_retry_on_startup = True
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
worker_hijack_root_logger = False  # Don't hijack the root logger
worker_redirect_stdouts = False    # Don't redirect stdout/stderr

worker_cancel_long_running_tasks_on_connection_loss = True  # Cancel tasks on connection loss
broker_transport_options = {
    'max_retries': 5,  # Retry up to 5 times before giving up
    'interval_start': 0,  # Initial retry delay
    'interval_step': 2,  # Step size for retry delay
    'interval_max': 10,  # Maximum retry delay
}

imports = [
    'backend.application.task'  # Import the task module
]


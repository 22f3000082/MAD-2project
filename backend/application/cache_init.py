from flask_caching import Cache

# Create global cache instance
cache = Cache()

def cache_init_app(app):
    """Initialize the cache extension with the given app."""
    # Configure caching from app config
    cache_config = {
        'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple'),
        'CACHE_DEFAULT_TIMEOUT': app.config.get('CACHE_DEFAULT_TIMEOUT', 300)
    }
    
    # If Redis is configured
    if app.config.get('CACHE_TYPE') == 'redis':
        cache_config['CACHE_REDIS_URL'] = app.config.get('CACHE_REDIS_URL', 'redis://localhost:6379/0')
    
    # Initialize with app
    cache.init_app(app, config=cache_config)
    return cache 
from jinja2 import Template
import requests
import functools
import hashlib
import json
from backend.application.cache_init import cache

def format_report(html_template, data):
    with open(html_template) as file:
        template = Template(file.read())
        # Allow both dictionary with 'data' key and direct parameter passing
        if isinstance(data, dict) and 'data' not in data:
            return template.render(**data)
        return template.render(data=data)

def fetch_user_data():
    url = "http://localhost:8025/api/v2/users/jim"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Failed with status code {response.status_code}: {response.text}")

# Cache helper functions

def cached(timeout=300, key_prefix='view'):
    """Simple wrapper for cached routes using Flask-Caching.
    
    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for the cache key
        
    Example:
        @cached(timeout=60, key_prefix='my_view')
        def my_view():
            return expensive_operation()
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            return cache.cached(timeout=timeout, key_prefix=key_prefix)(f)(*args, **kwargs)
        return decorated_function
    return decorator

def cached_with_args(timeout=300):
    """Cache a function based on its arguments.
    
    Args:
        timeout: Cache timeout in seconds
        
    Example:
        @cached_with_args(timeout=60)
        def get_user(user_id):
            return db.query.get(user_id)
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Create a cache key based on function name and arguments
            cache_key = f.__module__ + f.__name__ + str(args) + str(sorted(kwargs.items()))
            cache_key = hashlib.md5(cache_key.encode('utf-8')).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # If not in cache, call the function
            result = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, timeout=timeout)
            return result
        return decorated_function
    return decorator

def invalidate_cache_key(key):
    """Manually invalidate a specific cache key."""
    cache.delete(key)
    
def invalidate_cache_prefix(prefix):
    """Invalidate all cache keys with a given prefix."""
    cache.delete_many(prefix)

def memoize(func):
    """Cache the result of a function for the duration of a request.
    
    This is useful for functions that are called multiple times 
    within a single request but with the same arguments.
    
    Example:
        @memoize
        def expensive_calculation(x, y):
            # This will only be executed once per request
            # for the same x and y values
            return x * y
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from the function name and arguments
        key = func.__name__ + str(args) + str(sorted(kwargs.items()))
        key = hashlib.md5(key.encode('utf-8')).hexdigest()
        
        # Check if we have a request context
        from flask import g, has_request_context
        if not has_request_context():
            # If not in a request context, just call the function
            return func(*args, **kwargs)
        
        # Initialize cache dict in g if not present
        if not hasattr(g, 'memoize_cache'):
            g.memoize_cache = {}
            
        # Check if result is in cache
        if key in g.memoize_cache:
            return g.memoize_cache[key]
            
        # Call the function and cache the result
        result = func(*args, **kwargs)
        g.memoize_cache[key] = result
        return result
        
    return wrapper
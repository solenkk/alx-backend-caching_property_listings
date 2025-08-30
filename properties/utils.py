from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

# Set up logger
logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all properties from cache if available, otherwise from database.
    Caches the queryset for 1 hour (3600 seconds).
    """
    # Try to get properties from cache
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        return cached_properties
    
    # If not in cache, fetch from database
    properties = Property.objects.all()
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set('all_properties', properties, 3600)
    
    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with cache statistics and hit ratio.
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO command results
        redis_info = redis_conn.info()
        
        # Extract cache statistics
        keyspace_hits = redis_info.get('stats', {}).get('keyspace_hits', 0)
        keyspace_misses = redis_info.get('stats', {}).get('keyspace_misses', 0)
        
        # Calculate hit ratio (avoid division by zero)
        total_operations = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_operations if total_operations > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_operations': total_operations,
            'hit_ratio': hit_ratio,
            'hit_ratio_percentage': round(hit_ratio * 100, 2),
            'redis_version': redis_info.get('redis_version', 'unknown'),
            'used_memory_human': redis_info.get('used_memory_human', 'unknown'),
            'connected_clients': redis_info.get('connected_clients', 0),
        }
        
        # Log the metrics
        logger.info(
            f"Redis Cache Metrics - "
            f"Hits: {keyspace_hits}, Misses: {keyspace_misses}, "
            f"Hit Ratio: {hit_ratio_percentage}%, "
            f"Total Operations: {total_operations}"
        )
        
        return metrics
    
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_operations': 0,
            'hit_ratio': 0,
            'hit_ratio_percentage': 0,
        }
    ["if total_requests > 0 else 0"]
from django.core.cache import cache
from .models import Property

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
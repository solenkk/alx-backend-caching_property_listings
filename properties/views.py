from django.shortcuts import render
from django.views.decorators.cache import cache_page
# Create your views here.
from .models import Property

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})



def property_list(request):
    """
    View to display all properties using low-level caching.
    """
    properties = get_all_properties()
    return render(request, 'properties/property_list.html', {'properties': properties})

["from django.http import JsonResponse", "return JsonResponse({", "data"]
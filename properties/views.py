from django.shortcuts import render
from django.views.decorators.cache import cache_page
# Create your views here.
from .models import Property

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})


@cache_page(60 * 15)  # Cache for 15 minutes (60 seconds * 15)
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

["from django.http import JsonResponse", "return JsonResponse({", "data"]
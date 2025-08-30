from django.shortcuts import render

# Create your views here.
from .models import Property

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.core.serializers import serialize
from .models import Bungalow
from .models import Cottage
from .models import Facility
from .models import Service
from .models import Slot
from .models import Zone


def index(request): 
    return render(request,'test.html')

def bungalowsjson(request): 
    bungalows = serialize('geojson', Bungalow.objects.all(), geometry_field='geom')
    return HttpResponse(bungalows)

def zonesjson(request): 
    zones = serialize('geojson', Zone.objects.all(), geometry_field='geom')
    return HttpResponse(zones)

def cottagesjson(request): 
    cottages = serialize('geojson', Cottage.objects.all(), geometry_field='geom')
    return HttpResponse(cottages)

def facilitiesjson(request): 
    facilities = serialize('geojson', Facility.objects.all(), geometry_field='geom')
    return HttpResponse(facilities)

def servicesjson(request): 
    services = serialize('geojson', Service.objects.all(), geometry_field='geom')
    return HttpResponse(services)

def slotsjson(request): 
    slots = serialize('geojson', Slot.objects.all(), geometry_field='geom')
    return HttpResponse(slots)
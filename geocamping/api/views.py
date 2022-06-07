from geocamping.models import Bungalow
from geocamping.models import Cottage
from geocamping.models import Facility
from geocamping.models import Service
from geocamping.models import Slot
from geocamping.models import Zone
from .serializers import ZoneSerializer, ServiceSerializer, FacilitySerializer,BungalowSerializer,CottageSerializer, SlotSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Sum
from django.contrib.gis.db.models.functions import Area
from django.contrib.gis.geos import MultiPolygon
from rest_framework.response import Response


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer    


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    @action(detail=False, methods=["get"])
    def total_slot_capacity(self, request):
        total_capacity = Slot.objects.aggregate(total_capacity=Sum("capacity"))
        return Response(total_capacity)


class BungalowViewSet(viewsets.ModelViewSet):
    queryset = Bungalow.objects.all()
    serializer_class = BungalowSerializer

    @action(detail=False, methods=["get"])
    def total_slot_capacity(self, request):
        total_capacity = Bungalow.objects.aggregate(total_capacity=Sum("capacity"))
        return Response(total_capacity)



class CottageViewSet(viewsets.ModelViewSet):
    queryset = Cottage.objects.all()
    serializer_class = CottageSerializer


    @action(detail=False, methods=["get"])
    def total_slot_capacity(self, request):
        total_capacity = Cottage.objects.aggregate(total_capacity=Sum("capacity"))
        return Response(total_capacity)

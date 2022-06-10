from .models import Bungalow
from .models import Cottage
from .models import Facility
from .models import Service
from .models import Slot
from .models import Zone
from .serializers import ZoneSerializer, ServiceSerializer, FacilitySerializer,BungalowSerializer,CottageSerializer, SlotSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Sum , Count, OuterRef, Subquery
from django.contrib.gis.db.models.functions import Transform, Area
from django.contrib.gis.geos import GEOSGeometry
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

    def get_queryset(self):
        zone_query = Zone.objects.filter(geom__intersects = OuterRef("geom"))
        #get area
        queryset = Slot.objects.annotate(area = Area(Transform("geom", 27700)), price= Subquery(zone_query.values("price")))
        return queryset

    @action(detail=False, methods=["get"])
    def total_capacity(self, request):
        total_capacity = Slot.objects.aggregate(total_capacity=Sum("capacity"))
        return Response(total_capacity)
    
    @action(detail=False, methods=["get"])
    def total_count(self, request):
        total_count= Slot.objects.aggregate(total_count=Count("id"))
        return Response(total_count)



class BungalowViewSet(viewsets.ModelViewSet):
    queryset = Bungalow.objects.all()
    serializer_class = BungalowSerializer

    def get_queryset(self):
        zone_query = Zone.objects.filter(geom__intersects = OuterRef("geom"))
        #get area
        queryset = Bungalow.objects.annotate(area = Area(Transform("geom", 27700)), price= Subquery(zone_query.values("price")))
        return queryset

    @action(detail=False, methods=["get"])
    def total_capacity(self, request):
        total_capacity = Bungalow.objects.aggregate(total_capacity=Sum("capacity"))
        return Response(total_capacity)
    
    @action(detail=False, methods=["get"])
    def total_count(self, request):
        total_count= Bungalow.objects.aggregate(total_count=Count("id"))
        return Response(total_count)



class CottageViewSet(viewsets.ModelViewSet):
    queryset = Cottage.objects.all()
    serializer_class = CottageSerializer

    def get_queryset(self):
        zone_query = Zone.objects.filter(geom__intersects = OuterRef("geom"))
        #get area
        queryset = Cottage.objects.annotate(area = Area(Transform("geom", 27700)), price= Subquery(zone_query.values("price")))
        return queryset


    @action(detail=False, methods=["get"])
    def total_capacity(self, request):
        total_capacity = Cottage.objects.aggregate(total_capacity=Sum("capacity"))
        return Response(total_capacity)

    @action(detail=False, methods=["get"])
    def total_count(self, request):
        total_count= Cottage.objects.aggregate(total_count=Count("id"))
        return Response(total_count)

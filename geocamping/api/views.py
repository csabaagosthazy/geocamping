from .models import Bungalow
from .models import Cottage
from .models import Facility
from .models import Service
from .models import Slot
from .models import Zone
from .serializers import ZoneSerializer, ServiceSerializer, FacilitySerializer,BungalowSerializer,CottageSerializer, SlotSerializer
from rest_framework import viewsets, status, views
from rest_framework.decorators import action, api_view
from django.db.models import Sum , Count, OuterRef, Subquery
from django.contrib.gis.db.models.functions import Transform, Area, Distance, Centroid, GeometryDistance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from django.contrib.gis.db.models.aggregates import Union


@api_view()
def camp_details(request):
    
    #get details of the camp
    #area
    total_area_sq_m = Zone.objects.all().aggregate(sum_area = Area(Union(Transform("geom", 27700))))['sum_area']
    #lease details
    #cottages
    total_cottage_capacity = Cottage.objects.aggregate(total_capacity=Sum("capacity"))
    total_cottage_count = Cottage.objects.aggregate(total_count=Count("id"))
    total_cottage_area = Cottage.objects.aggregate(sum_area=Area(Union(Transform("geom", 27700))))['sum_area']    

    #bungalows
    total_bungalow_capacity = Bungalow.objects.aggregate(total_capacity=Sum("capacity"))
    total_bungalow_count = Bungalow.objects.aggregate(total_count=Count("id"))
    total_bungalow_area = Bungalow.objects.aggregate(sum_area=Area(Union(Transform("geom", 27700))))['sum_area']

    #slots
    total_slot_capacity = Slot.objects.aggregate(total_capacity=Sum("capacity"))
    total_slot_count = Slot.objects.aggregate(total_count=Count("id"))
    total_slot_area = Slot.objects.aggregate(sum_area=Area(Union(Transform("geom", 27700))))['sum_area']

    #Facilities
    facilities = Facility.objects.all().order_by('type').values('type'
                            ).annotate(count=Count('type'))
    fac_dict = {}
    for f in facilities:
        if(f.get("count") > 1):
            fac_dict[f.get("type")] = str(f.get("count")) + " pcs"
        else:
             fac_dict[f.get("type")] = str(f.get("count")) + " pc"

    #get main entrance
    main_entrance = Facility.objects.filter(name = "Main entrance").values("geom").first()["geom"]

    #Services
    #Nearest shop
    nearest_shop = Service.objects.filter(type = "Shop").annotate(
            distance = Distance(Centroid("geom"), Centroid(main_entrance))
        ).order_by("distance").values("distance").first()["distance"]
    
    #Nearest shop
    nearest_petrol_station = Service.objects.filter(type = "Petrol station").annotate(
            distance = Distance(Centroid("geom"), Centroid(main_entrance))
        ).order_by("distance").values("distance").first()["distance"]
    #nearest bus station
    nearest_bus_station = Service.objects.filter(subtype = "Bus").annotate(
            distance = Distance(Centroid("geom"), Centroid(main_entrance))
        ).order_by("distance").values("distance").first()["distance"]

    #get distance other services
    services_dist = Service.objects.filter(name__in = ["Tesco", "Main bus station", "Train station", "Harbor"]).annotate(
        distance = Distance(Centroid("geom"), Centroid(main_entrance))
        ).values("name", "distance")

    dict = {}

    for fdist in services_dist:
        dict[fdist.get('name').lower().replace(" ", "_")] = {'dist_to': fdist.get('name'),
                                                                'distance': round(fdist.get('distance').m,1),
                                                                'measure': 'm'}
    print(dict)
    return_obj = {
        'total_area':{
            'area': round(total_area_sq_m.sq_km,3),
            'measure': 'sq_km'
        },
        'lease_details':{
            'cottages':{
                **total_cottage_capacity,
                **total_cottage_count,
                'total_area': {
                    "area": round(total_cottage_area.sq_m,1),
                    "measure": 'sq_m'
                    }
            },
            'bungalows':{
                **total_bungalow_capacity,
                **total_bungalow_count,
                'total_area': {
                    "area": round(total_bungalow_area.sq_m,1),
                    "measure": 'sq_m'
                    }
            },
            'slots':{
                **total_slot_capacity,
                **total_slot_count,
                'total_area': {
                    "area": round(total_slot_area.sq_m,1),
                    "measure": 'sq_m'
                    }
            }
        },
        "services": {
            "shop":{
                'dist_to': "Shop",
                'distance': round(nearest_shop.m,1),
                'measure': 'm'
            },
            "petrol_station":{
                'dist_to': "Petrol station",
                'distance': round(nearest_petrol_station.m,1),
                'measure': 'm'
            },
            "bus_station":{
                'dist_to': "Bus station",
                'distance': round(nearest_bus_station.m,1),
                'measure': 'm'
            },
            **dict
        }

        
    }


    return Response(return_obj)


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        print(instance.id)
        serialized = self.get_serializer(instance).data
        return Response(serialized)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        print(instance.id)
        serialized = self.get_serializer(instance).data
        return Response(serialized)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer    

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        print(instance.id)
        serialized = self.get_serializer(instance).data
        return Response(serialized)

class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer



    def get_queryset(self):

        #sub query for price
        zone_query = Zone.objects.filter(geom__intersects = OuterRef("geom"))
        #get area
        queryset = Slot.objects.annotate(area = Area(Transform("geom", 27700)), 
                                         price = Subquery(zone_query.values("price")))
        return queryset

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        print(instance.id)
        serialized = self.get_serializer(instance).data

        #get closest parking place
        parking_dist = Zone.objects.filter(type = "Parking").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).order_by("distance").values("distance").first()["distance"]

        #get distance to beach
        beach_dist = Zone.objects.filter(type = "Beach").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).values("distance").first()["distance"]

        #get closest shower
        shower_dist = Facility.objects.filter(name = "Toilettes and shower").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).order_by("distance").values("distance").first()["distance"]



        #get distance to facilities
        facilites_dist = Facility.objects.exclude(name = "Toilettes and shower").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).values("name", "distance")

        dict = {}

        for fdist in facilites_dist:
            dict[fdist.get('name').lower().replace(" ", "_")] = {'dist_to': fdist.get('name'),
                                                                'distance': round(fdist.get('distance').m,1),
                                                                'measure': 'm'}
        #generate custom data
        custom_data = {
            'instance': serialized,
            'parking_distance': { 
                'dist_to': "Parking place",
                'distance': round(parking_dist.m,1),
                'measure': 'm'
            },
            'beach_distance':{
                'dist_to': "Beach",
                'distance': round(beach_dist.m,1),
                'measure': 'm'
            },
            'facilites_dist':{
                'shower': {
                    'dist_to': "Shower",
                    'distance': round(shower_dist.m,1),
                    'measure': 'm'
                },
                **dict
            }
        }
        return Response(custom_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["get"])
    def available_capacity(self, request):
        available_capacity = Slot.objects.filter(is_available = True).aggregate(available_capacity=Sum("capacity"))
        return Response(available_capacity)
    
    @action(detail=False, methods=["get"])
    def available_count(self, request):
        available_count= Slot.objects.filter(is_available = True).aggregate(available_count=Count("id"))
        return Response(available_count)



class BungalowViewSet(viewsets.ModelViewSet):
    queryset = Bungalow.objects.all()
    serializer_class = BungalowSerializer

    def get_queryset(self):
        zone_query = Zone.objects.filter(geom__intersects = OuterRef("geom"))
        #get area
        queryset = Bungalow.objects.annotate(area = Area(Transform("geom", 27700)), price= Subquery(zone_query.values("price")))
        return queryset

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        print(instance.id)
        serialized = self.get_serializer(instance).data

        #get closest parking place
        parking_dist = Zone.objects.filter(type = "Parking").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).order_by("distance").values("distance").first()["distance"]

        #get distance to beach
        beach_dist = Zone.objects.filter(type = "Beach").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).values("distance").first()["distance"]

        #get closest shower
        shower_dist = Facility.objects.filter(name = "Toilettes and shower").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).order_by("distance").values("distance").first()["distance"]



        #get distance to facilities
        facilites_dist = Facility.objects.exclude(name = "Toilettes and shower").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).values("name", "distance")

        dict = {}

        for fdist in facilites_dist:
            dict[fdist.get('name').lower().replace(" ", "_")] = {'dist_to': fdist.get('name'),
                                                                'distance': round(fdist.get('distance').m,1),
                                                                'measure': 'm'}
        #generate custom data
        custom_data = {
            'instance': serialized,
            'parking_distance': { 
                'dist_to': "Parking place",
                'distance': round(parking_dist.m,1),
                'measure': 'm'
            },
            'beach_distance':{
                'dist_to': "Beach",
                'distance': round(beach_dist.m,1),
                'measure': 'm'
            },
            'facilites_dist':{
                'shower': {
                    'dist_to': "Shower",
                    'distance': round(shower_dist.m,1),
                    'measure': 'm'
                },
                **dict
            }
        }
        return Response(custom_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def available_capacity(self, request):
        available_capacity = Bungalow.objects.filter(is_available = True).aggregate(available_capacity=Sum("capacity"))
        return Response(available_capacity)
    
    @action(detail=False, methods=["get"])
    def available_count(self, request):
        available_count= Bungalow.objects.filter(is_available = True).aggregate(available_count=Count("id"))
        return Response(available_count)



class CottageViewSet(viewsets.ModelViewSet):
    queryset = Cottage.objects.all()
    serializer_class = CottageSerializer

    def get_queryset(self):
        zone_query = Zone.objects.filter(geom__intersects = OuterRef("geom"))
        #get area
        queryset = Cottage.objects.annotate(area = Area(Transform("geom", 27700)), price= Subquery(zone_query.values("price")))
        return queryset

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        print(instance.id)
        serialized = self.get_serializer(instance).data

        #get closest parking place
        parking_dist = Zone.objects.filter(type = "Parking").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).order_by("distance").values("distance").first()["distance"]

        #get distance to beach
        beach_dist = Zone.objects.filter(type = "Beach").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).values("distance").first()["distance"]

        #get closest shower
        shower_dist = Facility.objects.filter(name = "Toilettes and shower").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).order_by("distance").values("distance").first()["distance"]



        #get distance to facilities
        facilites_dist = Facility.objects.exclude(name = "Toilettes and shower").annotate(
            distance = Distance(Centroid("geom"), Centroid(instance.geom))
        ).values("name", "distance")

        dict = {}

        for fdist in facilites_dist:
            dict[fdist.get('name').lower().replace(" ", "_")] = {'dist_to': fdist.get('name'),
                                                                'distance': round(fdist.get('distance').m,1),
                                                                'measure': 'm'}
        #generate custom data
        custom_data = {
            'instance': serialized,
            'parking_distance': { 
                'dist_to': "Parking place",
                'distance': round(parking_dist.m,1),
                'measure': 'm'
            },
            'beach_distance':{
                'dist_to': "Beach",
                'distance': round(beach_dist.m,1),
                'measure': 'm'
            },
            'facilites_dist':{
                'shower': {
                    'dist_to': "Shower",
                    'distance': round(shower_dist.m,1),
                    'measure': 'm'
                },
                **dict
            }
        }
        return Response(custom_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["get"])
    def available_capacity(self, request):
        available_capacity = Cottage.objects.filter(is_available = True).aggregate(available_capacity=Sum("capacity"))
        return Response(available_capacity)

    @action(detail=False, methods=["get"])
    def available_count(self, request):
        available_count= Cottage.objects.filter(is_available = True).aggregate(available_count=Count("id"))
        return Response(available_count)

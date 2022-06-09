from cmath import nan
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework import serializers
from .models import Zone,Service,Facility,Bungalow, Cottage, Slot 

from django.contrib.gis.geos import MultiPolygon


class ZoneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model= Zone
        geo_field="geom"
        fields = "__all__"

class ServiceSerializer(GeoFeatureModelSerializer):
        class Meta:
            model= Service
            geo_field="geom"
            fields = "__all__"


class FacilitySerializer(GeoFeatureModelSerializer):
     class Meta:
            model= Facility
            geo_field="geom"
            fields = "__all__"

class BungalowSerializer(GeoFeatureModelSerializer):
    area = serializers.SerializerMethodField()

    def get_area(self, obj):
        obj.geom.transform(27700, clone=False)
        return obj.geom.area

    class Meta:
        model = Bungalow
        geo_field="geom"
        fields = "__all__"

class CottageSerializer(GeoFeatureModelSerializer):
    area = serializers.SerializerMethodField()

    def get_area(self, obj):
        obj.geom.transform(27700, clone=False)
        return obj.geom.area

    class Meta:
        model = Cottage
        geo_field="geom"
        fields = "__all__"


class SlotSerializer(GeoFeatureModelSerializer):

    area = serializers.SerializerMethodField()

    def get_area(self, obj):
        obj.geom.transform(27700, clone=False)
        return obj.geom.area

    class Meta:
        model = Slot
        geo_field="geom"
        fields = "__all__"

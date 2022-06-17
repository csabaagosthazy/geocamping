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
    price = serializers.SerializerMethodField()
    feature_type = serializers.SerializerMethodField()
    feature_id = serializers.SerializerMethodField()

    def get_area(self, obj):
        return round(obj.area.sq_m,1)

    def get_price(self, obj):
        return obj.price

    def get_feature_type(self, obj):
        return "bungalow"

    def get_feature_id(self, obj):
        return obj.id

    class Meta:
        model = Bungalow
        geo_field="geom"
        fields = "__all__"

class CottageSerializer(GeoFeatureModelSerializer):
    area = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    feature_type = serializers.SerializerMethodField()
    feature_id = serializers.SerializerMethodField()

    def get_area(self, obj):
        return round(obj.area.sq_m,1)
    
    def get_price(self, obj):
        return obj.price

    def get_feature_type(self, obj):
        return "cottage"

    def get_feature_id(self, obj):
        return obj.id

    class Meta:
        model = Cottage
        geo_field="geom"
        fields = "__all__"


class SlotSerializer(GeoFeatureModelSerializer):

    area = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    feature_type = serializers.SerializerMethodField()
    feature_id = serializers.SerializerMethodField()

    def get_area(self, obj):
        return round(obj.area.sq_m,1)

    def get_price(self, obj):
        return obj.price

    def get_feature_type(self, obj):
        return "slot"

    def get_feature_id(self, obj):
        return obj.id

    class Meta:
        model = Slot
        geo_field="geom"
        fields = "__all__"

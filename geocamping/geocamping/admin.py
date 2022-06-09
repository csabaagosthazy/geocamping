from django.contrib.gis import admin
from api.models import Bungalow
from api.models import Cottage
from api.models import Facility
from api.models import Service
from api.models import Slot
from api.models import Zone

admin.site.register(Bungalow, admin.OSMGeoAdmin)
admin.site.register(Cottage, admin.OSMGeoAdmin)
admin.site.register(Facility, admin.OSMGeoAdmin)
admin.site.register(Service, admin.OSMGeoAdmin)
admin.site.register(Slot, admin.OSMGeoAdmin)
admin.site.register(Zone, admin.OSMGeoAdmin)
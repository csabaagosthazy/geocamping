from django.contrib.gis import admin
from .models import Bungalow
from .models import Cottage
from .models import Facility
from .models import Service
from .models import Slot
from .models import Zone

admin.site.register(Bungalow, admin.OSMGeoAdmin)
admin.site.register(Cottage, admin.OSMGeoAdmin)
admin.site.register(Facility, admin.OSMGeoAdmin)
admin.site.register(Service, admin.OSMGeoAdmin)
admin.site.register(Slot, admin.OSMGeoAdmin)
admin.site.register(Zone, admin.OSMGeoAdmin)
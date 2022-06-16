
from . import views
from django.urls import path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(prefix=r"zones", viewset=views.ZoneViewSet, basename="zone")
router.register(prefix=r"services", viewset=views.ServiceViewSet, basename="service")
router.register(prefix=r"facilities", viewset=views.FacilityViewSet, basename="facility")
router.register(prefix=r"bungalows", viewset=views.BungalowViewSet, basename="bungalow")
router.register(prefix=r"cottages", viewset=views.CottageViewSet, basename="cottage")
router.register(prefix=r"slots", viewset=views.SlotViewSet, basename="slot")

urlpatterns = [
    path('camp_details', views.camp_details, name='camp-details'),
]


urlpatterns += router.urls


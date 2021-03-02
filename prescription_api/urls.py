from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('drugs', views.DrugViewSet)
router.register('doctors', views.DoctorViewSet)
router.register('users', views.UserViewSet)
router.register('pharmacies', views.PharmacyViewSet)
router.register('bookings', views.BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

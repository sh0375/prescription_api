from rest_framework import viewsets

from . import serializers
from .models import Doctor, Drug, Pharmacy, Booking, User

# Create your views here.


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all().order_by('name')
    serializer_class = serializers.DrugSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by("first_name", "last_name")
    serializer_class = serializers.DoctorSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("first_name", "last_name")
    serializer_class = serializers.UserSerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all().order_by("name")
    serializer_class = serializers.PharmacySerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = serializers.BookingSerializer

from rest_framework import viewsets

from . import serializers
from .models import Doctor, Drug, Pharmacy, Booking, User

# Create your views here.


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all().order_by('name')
    serializer_class = serializers.DrugSerializer
    search_fields = ['name']


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by("first_name", "last_name")
    serializer_class = serializers.DoctorSerializer
    search_fields = ['reg_number', 'first_name', 'last_name', 'email']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("first_name", "last_name")
    serializer_class = serializers.UserSerializer
    search_fields = ['first_name', 'last_name', 'email']


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all().order_by("name")
    serializer_class = serializers.PharmacySerializer
    search_fields = ['name', 'address']


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = serializers.BookingSerializer
    filterset_fields = ['doctor_id', 'user_id', 'drug_id', 'pharmacy_id']

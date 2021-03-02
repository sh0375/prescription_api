from rest_framework import serializers

from .models import Doctor, Drug, Pharmacy, Booking, User


class DrugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drug
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class PharmacySerializer(serializers.ModelSerializer):

    class Meta:
        model = Pharmacy
        fields = '__all__'


class BookingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'

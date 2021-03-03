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
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.IntegerField()

    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField()

    drug = DrugSerializer(read_only=True)
    drug_id = serializers.IntegerField()

    pharmacy = PharmacySerializer(read_only=True)
    pharmacy_id = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = '__all__'

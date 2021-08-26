from rest_framework import serializers
from .. import models


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = '__all__'


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomType
        fields = '__all__'


class RoomFeatureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomFeatureType
        fields = '__all__'


class BedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BedType
        fields = '__all__'


class RoomTypePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomTypePicture
        fields = '__all__'


class RoomPricePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomPricePeriod
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invoice
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'


class SearchAvailabilitySerializer(serializers.Serializer):
    room_type = serializers.IntegerField()
    number_of_guests = serializers.IntegerField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


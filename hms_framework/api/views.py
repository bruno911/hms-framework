from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, mixins, status

from hms_framework.api import permissions as custom_permissions, paginations
from . import serializers
from .. import models
from ..factory import BookingFactory


class HotelViewSet(viewsets.ModelViewSet):
    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['name']


class AddressViewSet(viewsets.ModelViewSet):
    queryset = models.Hotel.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = []


class CountryViewSet(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['name', 'phone_prefix']

    
class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    pagination_class = paginations.SmallPagination
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['name']


class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['hotel']


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = models.RoomType.objects.all()
    serializer_class = serializers.RoomTypeSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['name']


class RoomFeatureTypeViewSet(viewsets.ModelViewSet):
    queryset = models.RoomFeatureType.objects.all()
    serializer_class = serializers.RoomFeatureTypeSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['name', 'is_active', 'is_everywhere']


class BedTypeViewSet(viewsets.ModelViewSet):
    queryset = models.BedType.objects.all()
    serializer_class = serializers.BedTypeSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['name', 'people_capacity']


class RoomTypePictureViewSet(viewsets.ModelViewSet):
    queryset = models.RoomTypePicture.objects.all()
    serializer_class = serializers.RoomTypePictureSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = []


class RoomPricePeriodViewSet(viewsets.ModelViewSet):
    queryset = models.RoomPricePeriod.objects.all()
    serializer_class = serializers.RoomPricePeriodSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['room', 'valid_date_from', 'valid_date_to']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['first_name', 'last_name', 'telephone', 'email', 'has_debts',
                        'last_has_debts_notified_datetime']


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['customer', 'due_date', 'is_deleted']


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceItemSerializer
    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['invoice']


class BookingViewSet(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    pagination_class = paginations.SmallPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['date_from']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        make_booking_service = BookingFactory().make_booking_service()
        booking = make_booking_service.execute(
            room_id=request.data.room.id,
            customer_id=request.data.customer.id,
            date_from=request.data['date_from'],
            date_to=request.data['date_to'],
            created_by_user_id=request.user
        )

        return Response(booking.__dict__, status=status.HTTP_201_CREATED)


class SearchAvailabilityViewSet(mixins.CreateModelMixin, viewsets.ViewSetMixin, GenericAPIView):

    permission_classes = [custom_permissions.IsSuperUserOrManagementReadOnly]
    serializer_class = serializers.SearchAvailabilitySerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        make_booking_service = BookingFactory().make_booking_service()
        booking = make_booking_service.execute(
            room_id=request.data.room.id,
            customer_id=request.data['customer_id'],
            date_from=request.data['date_from'],
            date_to=request.data['date_to'],
            created_by_user_id=request.user
        )

        return Response(data=booking.__dict__, status=status.HTTP_200_OK)

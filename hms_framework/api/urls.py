from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('hotel', views.HotelViewSet)
router.register('address', views.AddressViewSet)
router.register('country', views.CountryViewSet)
router.register('city', views.CityViewSet)
router.register('room', views.RoomViewSet)
router.register('room-type', views.RoomTypeViewSet)
router.register('room-feature-type', views.RoomFeatureTypeViewSet)
router.register('bed-type', views.BedTypeViewSet)
router.register('room-type-picture', views.RoomTypePictureViewSet)
router.register('room-price-period', views.RoomPricePeriodViewSet)
router.register('customer', views.CustomerViewSet)
router.register('invoice', views.CustomerViewSet)
router.register('booking', views.BookingViewSet)
router.register('search-availability-service', views.SearchAvailabilityViewSet, basename='search-availability-service')


urlpatterns = [
    path("", include(router.urls))
]

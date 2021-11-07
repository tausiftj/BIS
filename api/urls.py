from django.urls import include, path
from api.models import CarBrand

from api.views import (
    BookingViewSet,
    CarBrandViewSet,
    CarCityViewSet,
    CarModelViewSet,
    CarRegistrationNumberViewSet,
    CityViewSet,
    UserCreateView,
    GetBookingHistory,
    LoginAPIView,
)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register(r'sign-up', UserCreateView, basename='sign-up')
router.register(r'car-brand', CarBrandViewSet, basename='car-brand')
router.register(r'car-model', CarModelViewSet, basename='car-model')
router.register(r'car-rc', CarRegistrationNumberViewSet, basename='car-rc')
router.register(r'city', CityViewSet, basename='city')
router.register(r'car-city', CarCityViewSet, basename='car-city')
router.register(r'booking', BookingViewSet, basename='booking')


urlpatterns = [
    path('sign-in/', LoginAPIView.as_view(), name='sign-in' ),
    path('booking-history', GetBookingHistory, name='booking-history'),
    path('', include(router.urls)),
]
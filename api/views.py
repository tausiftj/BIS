from django.db.models import query
from django.shortcuts import render
from api import querysets, serializers
from api.models import (
    Booking,
    CarBrand,
    CarModel,
    CarRegistrationNumber,
    City
)
from rest_framework.authtoken.models import Token
from api.serializers import (
    BookingSerializer,
    CarBrandSerializer,
    CarModelSerializer,
    CarRegistrationNumberSerializer,
    CitySerializer,
    UserSerializer,
    LoginSerializer
)
from api.signal import (
    cancelled_booking,
    save_booking,
    update_booking,
)
from rest_framework.decorators import action, api_view,  permission_classes
from api.filters import CarCityFilter
from django.contrib.auth import get_user_model
from api.permission_helper import GenericObjectPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import (
    CreateModelMixin,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet,
)
from rest_framework import status
from zoom.settings import AUTH_PASSWORD_VALIDATORS

User = get_user_model()


class UserCreateView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class CarBrandViewSet(ModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    permission_classes = (GenericObjectPermissions, )
    pagination_class = None

    perms_map = {
        'POST': ('panel.add_carbrand',),
        'PATCH': ('panel.change_carbrand',),
        'PUT': ('panel.change_carbrand',),
        'DELETE': ('panel.delete_carbrand',),
    }



class CarModelViewSet(ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = (GenericObjectPermissions, )
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('type', 'brand', )
    perms_map = {
        'POST': ('panel.add_carmodel',),
        'PATCH': ('panel.change_carmodel',),
        'PUT': ('panel.change_carmodel',),
        'DELETE': ('panel.delete_carmodel',),
    }


class CarRegistrationNumberViewSet(ModelViewSet):
    queryset = CarRegistrationNumber.objects.all()
    serializer_class = CarRegistrationNumberSerializer
    permission_classes = (GenericObjectPermissions, )
    perms_map = {
        'POST': ('panel.add_carregistrationnumber',),
        'PATCH': ('panel.change_carregistrationnumber',),
        'PUT': ('panel.change_carregistrationnumber',),
        'DELETE': ('panel.delete_carregistrationnumber',),
    }

    def paginate_queryset(self, queryset):
        if self.request.query_params.get('no_page'):
            return None
        return super().paginate_queryset(queryset)


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (GenericObjectPermissions, )
    perms_map = {
        'POST': ('panel.add_city',),
        'PATCH': ('panel.change_city',),
        'PUT': ('panel.change_city',),
        'DELETE': ('panel.delete_city',),
    }

    def paginate_queryset(self, queryset):
        if self.request.query_params.get('no_page'):
            return None
        return super().paginate_queryset(queryset)


class CarCityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (GenericObjectPermissions, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = CarCityFilter
    perms_map = {
        'POST': ('panel.add_carcity',),
        'PATCH': ('panel.change_carcity',),
        'PUT': ('panel.change_carcity',),
        'DELETE': ('panel.delete_carcity',),
    }


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (GenericObjectPermissions, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('available', 'since', 'upto', 'car')
    perms_map = {
        'GET': ('panel.view_booking'),
        'POST': ('panel.add_booking',),
        'PATCH': ('panel.change_booking',),
        'PUT': ('panel.change_booking',),
        'DELETE': ('panel.delete_booking',),
    }

    def get_queryset(self):
        queryset = self.queryset
        args = self.request.query_params
        since = args.get('since')
        upto = args.get('upto')
        car = args.get('car')
        if car:
            queryset = queryset.filter(car=car)
        if self.action == "list":
            queryset = queryset.exclude(available=False,since__gte=since, upto__lte=upto)
        return queryset

    def create(self, request, *args, **kwargs):
        save_booking.delay(self, request, *args, **kwargs)
        return Response({'flag': True, 'msg': "Booking Created Successfully!"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        update_booking.delay(self, request, *args, **kwargs)
        return Response({'flag':True, 'msg': 'Booking Updated Successfully'})

    def destroy(self, request, *args, **kwargs):
        cancelled_booking.delay(self, request)
        return Response({'flag':True, 'msg': 'Booking cancelled Successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def GetBookingHistory(request):
    user = request.user
    return Response(BookingSerializer(Booking.objects.filter(created_by=user.id)).data, status=200)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_data = serializer.validated_data
        login_key = req_data.get('login_key')
        password = req_data.get('password')
        user = get_user_model().objects.get(username=login_key)
        error = {}

        if not user.check_password(password):
            error.update({'password': 'Invalid Password'})

        if error:
            raise serializers.ValidationError(error)
        return Response(status=200)
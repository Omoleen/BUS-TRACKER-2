from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.generics import *


class PassengerSignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        reg_serializer = PassengerSignUpSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_passenger = reg_serializer.save()
            if new_passenger:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update and view profile
class PassengerProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        profiles = PassengerProfile.objects.get(user_id=pk)
        prof_serializer = PassengerProfileSerializer(instance=profiles)
        return Response(prof_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(PassengerProfile.objects.all(), user_id=pk)
        # profile = PassengerProfile.objects.get(user_id=pk)
        data = request.data
        profile.payment_method = data.get('payment_method', profile.payment_method)
        # profile.in_ride = data.get('in_ride', profile.in_ride)
        # profile.wallet = data.get('wallet', profile.wallet)
        profile.save()
        prof_serializer = PassengerProfileSerializer(instance=profile)
        # if prof_serializer.is_valid():
        return Response(prof_serializer.data, status=status.HTTP_200_OK)
        # return Response(prof_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# function to book a a ride
class PassengerRideView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        profile = PassengerRides.objects.filter(user_id=pk)
        serializer = PassengerRideSerializer(instance=profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # book a ride - should already have the drivers id
    def post(self, request, pk, *args, **kwargs):
        data = request.data
        new_ride = PassengerRides.objects.create(user_id=pk, start_location=data['start_location'],
                                                 destination=data['destination'],
                                                 driver=data['driver'])
        serializer = PassengerRideSerializer(instance=new_ride)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, *args, **kwargs):
        profile_ride = get_object_or_404(PassengerRides.objects.all(), user_id=pk, id=request.data.id)
        # profile = PassengerProfile.objects.get(user_id=pk)
        data = request.data
        #  add condition for payment
        profile = get_object_or_404(PassengerProfile.objects.all(), user_id=pk)
        if profile_ride.status == 'PROGRESS':
            profile.in_ride = True
        elif profile_ride.status == 'COMPLETED' or profile_ride.status == 'CANCELLED':
            profile.in_ride = False
        profile.save()
        profile_ride.price = data.get('price', profile_ride.price)
        profile_ride.status = data.get('status', profile_ride.status)
        profile_ride.save()
        prof_serializer = PassengerRideSerializer(instance=profile_ride)
        return Response(prof_serializer.data, status=status.HTTP_200_OK)
        # return Response(prof_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# pointfield in model - scan for the nearest drivers
class ProfileScan(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        long, lat = data['long'], data['lat']
        available = DriverProfile.objects.filter(in_trip=False)
        # function to find drivers around the user
        serializer = ProfileScanSerializer(instance=available, many=True)
        # positions = []
        # for driver in serializer.data:

        return Response(serializer.data, status=status.HTTP_200_OK)

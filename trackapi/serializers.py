from rest_framework.serializers import ModelSerializer
from .models import *


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(f'validated_data: {validated_data}')
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            if validated_data.get('role') == 'ADMIN':
                instance.is_staff = True
        instance.save()
        return instance


class PassengerProfileSerializer(ModelSerializer):

    class Meta:
        model = PassengerProfile
        fields = ['id', 'user_id', 'payment_method', 'in_ride', 'wallet']
        read_only_fields = ['id']


class PassengerRideSerializer(ModelSerializer):
    # user_id = PassengerProfileSerializer()

    class Meta:
        model = PassengerRides
        fields = ['id', 'user_id', 'start_time', 'end_time', 'start_location', 'destination', 'price', 'status', 'driver']
        read_only_fields = ['id']
        # depth = 1


class ProfileScanSerializer(ModelSerializer):

    class Meta:
        model = DriverProfile
        fields = ['id', 'user_id', 'available', 'current_location', 'destination', 'in_trip']
        read_only_fields = ['id']


class RouteSerializer(ModelSerializer):

    class Meta:
        model = Route
        fields = ['id', 'start_location', 'destination_location', 'price']
        read_only_fields = ['id']


class DriverProfileSerializer(ModelSerializer):
    journey = RouteSerializer(many=True)

    class Meta:
        model = DriverProfile
        fields = ['id', 'available', 'in_trip', 'verified', 'current_location',
                  'destination', 'in_trip', 'wallet', 'vehicle', 'journey', 'passengers']
        read_only_fields = ['id', 'passengers']


class VehicleSerializer(ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['id', 'tracking_id', 'plate_number', 'is_active']
        read_only_fields = ['id']


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'role']
        read_only_fields = ['id', 'role']
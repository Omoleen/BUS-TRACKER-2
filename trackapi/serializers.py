from rest_framework.serializers import ModelSerializer
from .models import *


class PassengerSignUpSerializer(ModelSerializer):

    class Meta:
        model = Passenger
        fields = ['id', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PassengerProfileSerializer(ModelSerializer):

    class Meta:
        model = PassengerProfile
        fields = ['id', 'user_id', 'payment_method', 'in_ride', 'wallet']
        read_only_fields = ['id']


class PassengerRideSerializer(ModelSerializer):

    class Meta:
        model = PassengerRides
        fields = ['id', 'user_id', 'start_time', 'end_time', 'start_location', 'destination', 'price', 'status', 'driver']
        read_only_fields = ['id']


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
        read_only_fields = ['id']
        # fields = '__all__'

# user = models.OneToOneField(Driver, on_delete=models.CASCADE)
# available = models.BooleanField(default=True)
# verifyID = models.BinaryField(null=True, blank=True)
# verified = models.BooleanField(default=False)
# current_location = models.TextField(blank=True)
# destination = models.TextField(blank=True)
# in_trip = models.BooleanField(default=False)
# wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
# vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True, related_name='vehicle')
# # journey = models.ManyToManyField(Route, related_name='route', null=True, blank=True)
# journey = SortedManyToManyField(Route, blank=True, related_name='journey')
# passengers = models.IntegerField(default=0,)

# class TransactionSerializer(serializers.ModelSerializer):
#     SplitInfo = SplitInfoSerializer(many=True)
#
#     class Meta:
#         model = Transaction
#         fields = ['ID', "Amount", "Currency", "CustomerEmail", "Balance", 'SplitInfo']
#
#     def create(self, validated_data):
#         splitinfo = validated_data.pop('SplitInfo')
#         transaction = Transaction.objects.create(**validated_data)
#         splits = [SplitInfo.objects.create(Transaction=transaction, **split) for split in splitinfo]
#         # for split in splitinfo:
#         #     SplitInfo.objects.create(Transaction=transaction, **split)
#         return transaction
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         custom = {
#             "ID": instance.ID,
#             "Balance": instance.Balance,
#             "SplitBreakdown": representation.get('SplitInfo')
#         }
#         return custom
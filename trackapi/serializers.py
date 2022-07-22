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
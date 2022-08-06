from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.generics import *
from django.db.models import Q
from rest_framework.schemas import ManualSchema
import coreschema
import coreapi


class SignUpView(APIView):
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "role",
            required=False,
            location="form",
            schema=coreschema.String(description="default: PASSENGER, PASSENGER or ADMIN"),
        ),
    ],
    )

    def post(self, request, *args, **kwargs):
        request.data['role'] = request.data.get('role', 'PASSENGER')
        reg_serializer = SignUpSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update and view profile - passenger
class PassengerProfileView(APIView):
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[
        coreapi.Field(
            "id",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "payment_method",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
    ]
    )

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
    schema = ManualSchema(fields=[
        coreapi.Field(
            "id",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "pickup",
            required=False,
            location="form",
            schema=coreschema.String(description='location should be valid in routes')
        ),
        coreapi.Field(
            "destination",
            required=False,
            location="form",
            schema=coreschema.String(description='location should be valid in routes')
        ),
        coreapi.Field(
            "driver",
            required=False,
            location="form",
            schema=coreschema.String(description='driver id')
        ),
        coreapi.Field(
            "price",
            required=False,
            location="form",
            schema=coreschema.String(description='automatically calculated by the backend')
        ),
        coreapi.Field(
            "status",
            required=False,
            location="form",
            schema=coreschema.String(description='default status: REQUESTED, choices are COMPLETED, PROGRESS, CANCELLED')
        ),
    ])

    # get all rides taken in the past
    def get(self, request, pk, *args, **kwargs):
        profile = PassengerRides.objects.filter(user_id=pk)
        serializer = PassengerRideSerializer(instance=profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # book a ride - should already have the drivers id
    def post(self, request, pk, *args, **kwargs):
        data = request.data
        new_ride = PassengerRides.objects.create(user_id=pk, start_location=data['pickup'],
                                                 destination=data['destination'],
                                                 driver=data['driver'])
        serializer = PassengerRideSerializer(instance=new_ride)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # update a ride
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
        return Response(prof_serializer.data, status=status.HTTP_202_ACCEPTED)


class RouteScanView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        routes = Route.objects.all()
        serializer = RouteSerializer(instance=routes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# scan for destination in routes
class DriverScan(APIView):
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[
        coreapi.Field(
            "pickup",
            required=True,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "destination",
            required=True,
            location="query",
            schema=coreschema.String()
        ),
    ],
    )

    def get(self, request, *args, **kwargs):
        data = request.query_params

        routes = Route.objects.filter(Q(destination_location__contains=data.get('destination').lower()) | Q(start_location__contains=data.get('pickup').lower()))  # check if destination is in routes
        # print(routes)
        drivers = DriverProfile.objects.filter(in_trip=False, available=True, journey__in=routes, passengers__lt=18).distinct()  # check of route is in any driver's journey
        print(drivers)
        final = []
        start, dest = None, None
        for driver in drivers:
            journey = driver.journey.values()
            i=0
            for trip in journey:
                if trip.get('start_location') == data.get('pickup').lower():
                    start = i
                if trip.get('destination_location') == data.get('destination').lower():
                    dest = i
                i+=1
            print(start, dest)
            if start and dest:
                final.append(driver)
                total = sum(driver.journey.values()[i].get('price') for i in range(start, dest+1))
                print(total)
                # for i in range(start, dest+1):
                #     driver.journey.values().get('price')


        #     price_sum =
        # driv = DriverProfile.objects.get(user=11)
        # print(driv.journey.values())
        serializer = DriverProfileSerializer(instance=final, many=True)

        # {'message': 'successful'}

        return Response(serializer.data, status=status.HTTP_200_OK)


# update and view profile - Driver
class DriverProfileView(APIView):
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[
        coreapi.Field(
            "id",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "available",
            required=False,
            location="form",
            schema=coreschema.String(description='Boolean')
        ),
        coreapi.Field(
            "wallet",
            required=False,
            location="form",
            schema=coreschema.String(description='e.g wallet value')
        ),
        coreapi.Field(
            "destination",
            required=False,
            location="form",
            schema=coreschema.String(description='location should be valid in routes')
        ),
        coreapi.Field(
            "current_location",
            required=False,
            location="form",
            schema=coreschema.String(description='location should be valid in routes')
        ),
        coreapi.Field(
            "vehicle",
            required=False,
            location="form",
            schema=coreschema.String(description='"null" to initialize driver to no vehicle')
        ),
        coreapi.Field(
            "journey",
            required=False,
            location="form",
            schema=coreschema.String(description='A list of routes')
        ),
    ]
    )

    def get(self, request, pk, *args, **kwargs):
        # profiles = DriverProfile.objects.get(user_id=pk)
        profile = get_object_or_404(DriverProfile.objects.all(), user_id=pk)
        serializer = DriverProfileSerializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(DriverProfile.objects.all(), user_id=pk)
        data = request.data
        print(data)
        profile.available = data.get('available', profile.available)
        # profile.in_trip = data.get('in_trip', profile.in_trip)
        profile.wallet = data.get('wallet', profile.wallet)
        profile.destination = data.get('destination', profile.destination)
        profile.current_location = data.get('current_location', profile.current_location)
        if 'vehicle' in data.keys():
            # profile.vehicle = get_object_or_404(Vehicle.objects.all(), id=data.get('vehicle', profile.vehicle))
            if data.get('vehicle') is None:
                profile.vehicle = None
            elif data.get('vehicle'):
                profile.vehicle = get_object_or_404(Vehicle.objects.all(), id=data.get('vehicle', profile.vehicle))
        if 'journey' in data.keys():
            if data.get('journey') is None:
                profile.journey.clear()
            elif data.get('journey'):
                profile.journey.add(get_object_or_404(Route.objects.all(), id__in=data.get('journey')))
                # for i in data.get('journey'):
                #     profile.journey.add(get_object_or_404(Route.objects.all(), id=i))
        profile.save()
        serializer = DriverProfileSerializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DriverScanPassengers(APIView):
    permission_classes = [AllowAny]
    # for drivers to see passengers in their present routes
    def get(self, request, pk, *args, **kwargs):
        # profiles = DriverProfile.objects.get(user_id=pk)
        print(request.data)
        print(pk)
        profile = get_object_or_404(Driver.objects.all(), id=pk)
        print(profile)
        passengers = PassengerRides.objects.filter(status='REQUESTED', driver=profile)
        print(passengers)
        serializer = PassengerRideSerializer(instance=passengers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, pk, *args, **kwargs):


class RouteView(APIView):
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[
        coreapi.Field(
            "id",
            required=False,
            location="query",
            schema=coreschema.String(description='to query trip details')
        ),
        coreapi.Field(
            "start_location",
            required=False,
            location="form",
            schema=coreschema.String(description='location should be valid in routes')
        ),
        coreapi.Field(
            "destination_location",
            required=False,
            location="form",
            schema=coreschema.String(description='location should be valid in routes')
        ),
        coreapi.Field(
            "price",
            required=False,
            location="form",
            schema=coreschema.String(description='cost of route')
        ),
    ]
    )

    def get_queryset(self):
        routes = Route.objects.all()
        return routes

    def get(self, request, *args, **kwargs):

        try:
            id = request.query_params["id"]
            if id != None:
                route = Route.objects.get(id=id)
                serializer = RouteSerializer(route)
        except:
            routes = self.get_queryset()
            serializer = RouteSerializer(routes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        new_route = Route.objects.create(start_location=data["start_location"], destination_location=data[
            "destination_location"], price=data["price"])

        new_route.save()

        serializer = RouteSerializer(new_route)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        id = request.query_params["id"]
        route_object = Route.objects.get(id=id)

        data = request.data

        route_object.start_location = data["start_location"]
        route_object.destination_location = data["destination_location"]
        route_object.price = data["price"]

        route_object.save()

        serializer = RouteSerializer(route_object)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def patch(self, request, *args, **kwargs):
        id = request.query_params["id"]
        route_object = Route.objects.get(id=id)
        data = request.data

        route_object.start_location = data.get("start_location", route_object.start_location)
        route_object.destination_location = data.get("destination_location", route_object.destination_location)
        route_object.price = data.get("price", route_object.price)

        route_object.save()
        serializer = RouteSerializer(route_object)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):

        try:
            id = request.query_params["id"]
            if id != None:
                Route.objects.get(id=id).delete()
                return Response({'message': 'Route deleted'}, status=status.HTTP_200_OK)
        except:
            Route.objects.all().delete()
            routes = self.get_queryset()
            serializer = RouteSerializer(routes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VehicleView(APIView):
    permission_classes = [AllowAny]
    schema = ManualSchema(fields=[
        coreapi.Field(
            "id",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "tracking_id",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "plate_number",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "is_active",
            required=False,
            location="form",
            schema=coreschema.String(description='Boolean')
        ),
    ]
    )

    def get_queryset(self):
        vehicles = Vehicle.objects.all()
        return vehicles

    def get(self, request, *args, **kwargs):

        try:
            id = request.query_params["id"]
            if id != None:
                vehicle = Vehicle.objects.get(id=id)
                serializer = VehicleSerializer(vehicle)
        except:
            vehicles = self.get_queryset()
            serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        new_vehicle = Vehicle.objects.create(tracking_id=data.get('tracking_id'), plate_number=data[
            "plate_number"], is_active=data.get('is_active'))

        new_vehicle.save()

        serializer = VehicleSerializer(new_vehicle)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        id = request.query_params["id"]
        vehicle_object = Route.objects.get(id=id)

        data = request.data

        vehicle_object.tracking_id = data["tracking_id"]
        vehicle_object.plate_number = data["plate_number"]
        vehicle_object.is_active = data["is_active"]

        vehicle_object.save()

        serializer = VehicleSerializer(vehicle_object)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def patch(self, request, *args, **kwargs):
        id = request.query_params["id"]
        vehicle_object = Route.objects.get(id=id)
        data = request.data

        vehicle_object.tracking_id = data.get("tracking_id", vehicle_object.tracking_id)
        vehicle_object.plate_number = data.get("plate_number", vehicle_object.plate_number)
        vehicle_object.is_active = data.get("is_active", vehicle_object.is_active)

        vehicle_object.save()
        serializer = VehicleSerializer(vehicle_object)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):

        try:
            id = request.query_params["id"]
            if id != None:
                Vehicle.objects.get(id=id).delete()
                return Response({'message': 'Vehicle deleted'}, status=status.HTTP_200_OK)
        except:
            Vehicle.objects.all().delete()
            routes = self.get_queryset()
            serializer = VehicleSerializer(routes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
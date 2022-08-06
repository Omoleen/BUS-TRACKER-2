from django.contrib.auth.models import User
from trackapi.serializers import *
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from trackapi.models import *
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from rest_framework import status
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)


class RouteWebsocketView(AsyncAPIConsumer):
    permission_classes = [AllowAny]
    # queryset = Route.objects.all()
    # serializer_class = RouteSerializer

    @action()
    async def an_async_action(self, some=None, **kwargs):
        # do something async
        return {'response_with': 'some message'}, 200

    async def get_queryset(self):
        routes = Route.objects.all()
        return routes

    @action()
    def get(self, *args, **kwargs):

        # try:
        #     id = request.query_params["id"]
        #     if id != None:
        #         route = Route.objects.get(id=id)
        #         serializer = RouteSerializer(route)
        # except:
        routes = self.get_queryset()
        serializer = RouteSerializer(routes, many=True)

        return serializer.data, 200

    @action()
    async def post(self, request, *args, **kwargs):
        data = request.data

        new_route = Route.objects.create(start_location=data["start_location"], destination_location=data[
            "destination_location"], price=data["price"])

        new_route.save()

        serializer = RouteSerializer(new_route)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action()
    async def put(self, request, *args, **kwargs):
        id = request.query_params["id"]
        route_object = Route.objects.get(id=id)

        data = request.data

        route_object.start_location = data["start_location"]
        route_object.destination_location = data["destination_location"]
        route_object.price = data["price"]

        route_object.save()

        serializer = RouteSerializer(route_object)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action()
    async def patch(self, request, *args, **kwargs):
        route_object = Route.objects.get()
        data = request.data

        route_object.start_location = data.get("start_location", route_object.start_location)
        route_object.destination_location = data.get("destination_location", route_object.destination_location)
        route_object.price = data.get("price", route_object.price)

        route_object.save()
        serializer = RouteSerializer(route_object)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action()
    async def delete(self, request, *args, **kwargs):

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

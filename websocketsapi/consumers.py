from django.contrib.auth.models import User
from trackapi.serializers import *
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.permissions import AllowAny
from trackapi.models import *
import json
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from channels.db import database_sync_to_async


class RouteWebsocketView(AsyncAPIConsumer):
    permission_classes = [AllowAny]

    @action()
    async def an_async_action(self, some=None, **kwargs):
        # do something async
        return {'response_with': 'some message'}, 200

    async def get_queryset(self):
        routes = Route.objects.all()
        return routes


class BookARide(GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    # book a ride - should already have the drivers id

    @model_observer(PassengerRides)
    async def driver_watch(self,
                           message,
                           observer=None,
                           subscribing_request_ids=[],
                           **kwargs):
        await self.send_json(message)

    @driver_watch.serializer
    def driver_watch(self, instance: PassengerRides, action, **kwargs):
        return {
            "action": action.value,
            "data": PassengerRideSerializer(instance).data
        }

    @driver_watch.groups_for_signal
    def driver_watch(self, instance: PassengerRides, **kwargs):
        yield f'-Ride__{instance.pk}'
        yield f'-Driver__{instance.driver.id}'

    @driver_watch.groups_for_consumer
    def driver_watch(self, id=None, driver=None, **kwargs):
        if id is not None:
            yield f'-Ride__{id}'
        if driver is not None:
            yield f'-Driver__{driver.id}'

    @database_sync_to_async
    def get_driver(self, id):
        return Driver.objects.get(id=id)

    @database_sync_to_async
    def get_ride(self, id):
        return PassengerRides.objects.get(id=id)

    # @database_sync_to_async
    # def driver_get_rides(self, id):
    #     return PassengerRides.objects.filter(driver=id)

    @action()
    async def book_a_ride(self, request_id, driver_id, **kwargs):
        ride = await database_sync_to_async(PassengerRides.objects.create)(user_id=kwargs.get('user_id'), start_location=kwargs.get('pickup'),
                                                                    destination=kwargs.get('destination'),
                                                                    driver=await self.get_driver(kwargs.get('driver_id')))
        # await self.driver_watch.subscribe(driver=await self.get_driver(driver_id), request_id=request_id)
        await self.driver_watch.subscribe(id=ride.id, request_id=request_id)
        return PassengerRideSerializer(ride).data, 201

    @action()
    async def unsubscribe_from_ride(self, request_id, ride_id, **kwargs):
        await self.driver_watch.unsubscribe(id=ride_id, request_id=request_id)
        return {"message": f"Ride unsubscribed", "data": PassengerRideSerializer(await self.get_ride(ride_id)).data}, 204

    @action()
    async def subscribe_as_a_driver(self, request_id, **kwargs):
        driv = await self.get_driver(kwargs.get('driver_id'))
        await self.driver_watch.subscribe(driver=driv, request_id=request_id)
        return {
                   "message": f"Driver {driv.email} subscribed"
               }, 201

    @action()
    async def unsubscribe_as_a_driver(self, request_id, **kwargs):
        driv = await self.get_driver(kwargs.get('driver_id'))
        await self.driver_watch.unsubscribe(driver=driv, request_id=request_id)
        return {
                   "message": f"Driver {driv.email} subscribed"
               }, 204

    # @action()
    # async def list_request_for_driver(self, request_id, **kwargs):
    #     requested_rides = await database_sync_to_async(PassengerRides.objects.filter)\
    #         (driver=await self.get_driver(kwargs.get('driver_id')), status='REQUESTED')
    #     # print(requested_rides)
    #     return await PassengerRideSerializer(instance=requested_rides, many=True).data, 201


# class BookARide(GenericAsyncAPIConsumer):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializer
#     permission_classes = [AllowAny]
#     # book a ride - should already have the drivers id
#
#     @model_observer(PassengerRides)
#     async def driver_watch(self,
#                            message,
#                            observer=None,
#                            subscribing_request_ids=[],
#                            **kwargs):
#         await self.send_json(message)
#
#     @driver_watch.serializer
#     def driver_watch(self, instance: PassengerRides, action, **kwargs):
#         return PassengerRideSerializer(instance).data
#
#     @driver_watch.groups_for_signal
#     def driver_watch(self, instance: PassengerRides, **kwargs):
#         yield f'-Driver__{instance.driver.pk}'
#
#     @driver_watch.groups_for_consumer
#     def driver_watch(self, driver=None, **kwargs):
#         if driver is not None:
#             yield f'-Driver__{driver.pk}'
#
#     @database_sync_to_async
#     def get_driver(self, id):
#         return Driver.objects.get(id=id)
#     #
#     # @database_sync_to_async
#     # def get_ride(self, id):
#     #     return PassengerRides.objects.get(id=id)
#
#     @action()
#     async def book_a_ride(self, request_id, driver_id, **kwargs):
#         ride = await database_sync_to_async(PassengerRides.objects.create)(user_id=kwargs['user_id'], start_location=kwargs['pickup'],
#                                                                            destination=kwargs['destination'],
#                                                                            driver=await self.get_driver(driver_id))
#         # await self.driver_watch.subscribe(driver=await self.get_driver(driver_id), request_id=request_id)
#         await self.driver_watch.subscribe(id=ride.id, request_id=request_id)
#         return {"message": f"Ride subscribed"}, 201
#
#     @action()
#     async def unsubscribe_from_ride(self, request_id, driver_id, **kwargs):
#         # ride = await database_sync_to_async(PassengerRides.objects.create)(user_id=user_id, start_location=kwargs['pickup'],
#         #                                                             destination=kwargs['destination'],
#         #                                                             driver=await self.get_driver(driver_id))
#         await self.driver_watch.unsubscribe(driver=await self.get_driver(driver_id), request_id=request_id)
#         return {"message": f"Ride subscribed"}, 204
#

from django.urls import re_path, path
from .consumers import *

websockets_urlpatterns = [
    re_path(r"^ws/routes/$", RouteWebsocketView.as_asgi()),
    # re_path(r"^ws/connect/$", ConnConsumer.as_asgi()),
    # path('routes/', view_as_consumer(views.RouteView.as_view())),
    # re_path(r"^ws/routes/$", view_as_consumer(RouteView.as_asgi())),
]

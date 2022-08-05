"""
ASGI config for Bustracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
from channels.auth import AuthMiddlewareStack, SessionMiddleware, CookieMiddleware
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import websocketsapi.routing
from django.urls import re_path, path
from djangochannelsrestframework.consumers import view_as_consumer
from websocketsapi.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bustracker.settings')
django.setup()
# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocketsapi.routing.websockets_urlpatterns
            )
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})


# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocketsapi.routing.websockets_urlpatterns
#         )
#     ),
# })

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": CookieMiddleware(
#         SessionMiddleware(
#             URLRouter(
#                 websocketsapi.routing.websockets_urlpatterns
#             )
#         )
#     ),
#     # Just HTTP for now. (We can add other protocols later.)
# })

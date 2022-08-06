from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view as yasg_schema
from drf_yasg import openapi
from rest_framework import permissions

schema_view = yasg_schema(
    openapi.Info(
        title='BusTracker API',
        default_version='v1',
        description='API Documentation',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes={},
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('swag/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
    ), name='swagger-ui'),
    path('api/', include('trackapi.urls'), name='trackapi'),
    # path('api/', include('websocketsapi.routing'), name='websocketsapi'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', include_docs_urls(title='BusTrackerAPI')),
    path('schema/', get_schema_view(
        title='Bus Tracker',
        description='API documentation',
        version='1.0.0',
    ), name='api_schema'),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView

urlpatterns = [
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

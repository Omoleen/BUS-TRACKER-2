from django.urls import path
from .views import *

urlpatterns = [
    path('route/scan/', RouteScanView.as_view()),
    path('passenger/signup/', PassengerSignUpView.as_view()),
    path('passenger/profile/<int:pk>/', PassengerProfileView.as_view()),
    path('passenger/profile/<int:pk>/ride/', PassengerRideView.as_view()),
    path('passenger/profile/scan/', DriverScan.as_view()),
    path('driver/<int:pk>/profile/', DriverProfileView.as_view()),
    path('driver/<int:pk>/scan/passengers/', DriverScanPassengers.as_view()),
]

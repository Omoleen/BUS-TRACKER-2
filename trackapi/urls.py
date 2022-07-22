from django.urls import path
from .views import *

urlpatterns = [
    path('passenger/signup/', PassengerSignUpView.as_view()),
    path('passenger/profile/<int:pk>/', PassengerProfileView.as_view()),
    path('passenger/profile/<int:pk>/ride/', PassengerRideView.as_view()),
    path('passenger/profile/scan/', ProfileScan.as_view()),
]

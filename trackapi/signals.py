from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Passenger)
def create_passenger_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PASSENGER":
        PassengerProfile.objects.create(user=instance)


@receiver(post_save, sender=Driver)
def create_passenger_profile(sender, instance, created, **kwargs):
    if created and instance.role == "DRIVER":
        DriverProfile.objects.create(user=instance)


@receiver(post_save, sender=CoDriver)
def create_passenger_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CODRIVER":
        CoDriverProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PASSENGER":
        PassengerProfile.objects.create(user=instance)
    elif created and instance.role == "DRIVER":
        DriverProfile.objects.create(user=instance)
    elif created and instance.role == "CODRIVER":
        CoDriverProfile.objects.create(user=instance)

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from sortedm2m.fields import SortedManyToManyField
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.set_password(make_password(password))
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        PASSENGER = "PASSENGER", 'Passenger'
        DRIVER = "DRIVER", 'Driver'
        CODRIVER = "CODRIVER", 'CoDriver'

    base_role = Role.PASSENGER

    role = models.CharField(max_length=25, choices=Role.choices)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            # self.password = self.set_password(kwargs.get('password'))
            return super().save(*args, **kwargs)


class PassengerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PASSENGER)


class Passenger(User):
    objects = PassengerManager()
    base_role = User.Role.PASSENGER

    class Meta:
        proxy = True


class DriverManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DRIVER)


class Driver(User):
    base_role = User.Role.DRIVER
    objects = DriverManager()

    class Meta:
        proxy = True


class CoDriverManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CODRIVER)


class CoDriver(User):
    objects = CoDriverManager()
    base_role = User.Role.CODRIVER

    class Meta:
        proxy = True


class Vehicle(models.Model):
    # driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_id = models.CharField(max_length=128)
    plate_number = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)


class Route(models.Model):
    # name = models.CharField(max_length=128, blank=True)
    start_location = models.CharField(max_length=128)
    destination_location = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Route {self.id}'


class PassengerProfile(models.Model):

    class Payment(models.TextChoices):
        CARD = "CARD", 'Card'
        TRANSFER = "TRANSFER", 'Transfer'
        WALLET = "WALLET", 'Wallet'

    user = models.OneToOneField(Passenger, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=128, choices=Payment.choices, blank=True)
    in_ride = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class DriverProfile(models.Model):
    user = models.OneToOneField(Driver, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    verifyID = models.BinaryField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    current_location = models.TextField(blank=True)
    destination = models.TextField(blank=True)
    in_trip = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True, related_name='vehicle')
    # journey = models.ManyToManyField(Route, related_name='route', null=True, blank=True)
    journey = SortedManyToManyField(Route, blank=True, related_name='journey')
    passengers = models.IntegerField(default=0,)


class CoDriverProfile(models.Model):
    user = models.OneToOneField(CoDriver, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)
    verifyID = models.BinaryField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    current_location = models.TextField(blank=True)
    destination = models.TextField(blank=True)
    in_trip = models.BooleanField(default=False)


class PassengerRides(models.Model):
    class Status(models.TextChoices):
        CANCELLED = "CANCELLED", 'Cancelled'
        PROGRESS = "PROGRESS", 'Progress'
        COMPLETED = "COMPLETED", 'Completed'
        REQUESTED = "REQUESTED", 'Requested'

    class Payment(models.TextChoices):
        CARD = "CARD", 'Card'
        TRANSFER = "TRANSFER", 'Transfer'
        WALLET = "WALLET", 'Wallet'
    user = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    start_location = models.TextField()
    destination = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=128, choices=Status.choices, default=Status.REQUESTED)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True, related_name='passenger_driver')
    payment_method = models.CharField(max_length=128, choices=Payment.choices, blank=True)

    def save(self, *args, **kwargs):
        self.payment_method = PassengerProfile.objects.get(user=self.user).payment_method
        return super().save(*args, **kwargs)


class DriverRides(models.Model):
    user = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    start_location = models.TextField()
    destination = models.TextField()
    co_driver = models.ForeignKey(CoDriver, on_delete=models.SET_NULL, blank=True, null=True, related_name='co_driver')


class CoDriverRides(models.Model):
    user = models.ForeignKey(CoDriver, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    start_location = models.TextField()
    destination = models.TextField()
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True, related_name='driver')




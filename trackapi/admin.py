from django.contrib import admin
# from .models import User, DriverRides, DriverProfile, PassengerRides, PassengerProfile, Passenger, Driver
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'is_staff', 'is_active', 'role')
    list_filter = ('email', 'is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Driver)
class CustomUserAdmin(UserAdmin):
    model = Driver
    list_display = ('email', 'is_active',)
    list_filter = ('email', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Passenger)
class CustomUserAdmin(UserAdmin):
    model = Passenger
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(DriverRides)
class DriverRidesAdmin(admin.ModelAdmin):
    # model = DriverRides
    list_display = ('user', 'start_time', 'end_time', 'start_location', 'destination')


@admin.register(PassengerRides)
class PassengerRidesAdmin(admin.ModelAdmin):
    # model = Passenger
    list_display = ('user', 'start_time', 'end_time', 'start_location', 'destination', 'price')


@admin.register(PassengerProfile)
class PassengerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_method', 'in_ride')


@admin.register(DriverProfile)
class PassengerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'available', 'verified', 'current_location', 'in_trip')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'plate_number', 'is_active')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_location', 'destination_location', 'price')
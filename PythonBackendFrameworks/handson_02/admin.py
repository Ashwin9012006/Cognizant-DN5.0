from django.contrib import admin
from .models import Customer, Vehicle, ServiceRecord


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_name",
        "registration_number",
        "model_year"
    )

    search_fields = (
        "vehicle_name",
        "registration_number"
    )


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle",
        "service_type",
        "service_status",
        "service_date"
    )

    list_filter = (
        "service_status",
        "service_date"
    )
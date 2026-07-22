from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    vehicle_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=25, unique=True)
    model_year = models.IntegerField()

    def __str__(self):
        return f"{self.vehicle_name} - {self.registration_number}"


class ServiceRecord(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="service_history"
    )

    service_date = models.DateField()
    service_type = models.CharField(max_length=100)
    service_status = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.vehicle.vehicle_name} - {self.service_type}"
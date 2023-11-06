from django.db import models
from django.contrib.auth.models import User
import uuid


class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    token = models.CharField(max_length=40, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.description or str(self.id)


class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    voltage = models.DecimalField(max_digits=5, decimal_places=2)
    current = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Data for Sensor {self.sensor.id} at {self.timestamp}"

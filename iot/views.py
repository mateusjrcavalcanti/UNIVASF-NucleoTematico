# iot/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from SolarEnergyAnalysis import settings
from iot.models import Sensor


def index(request):
    return render(request, "sensor/index.html")


def info(request):
    data = {
        'host': settings.TCP_HOST,
        'port': settings.TCP_PORT
    }
    return JsonResponse(data)


def sensors(request, sensor_id=None):
    sensors = Sensor.objects.all()
    sensor = None

    if sensor_id is not None:
        sensor = Sensor.objects.get(id=sensor_id)

    context = {'sensors': sensors, 'sensor': sensor}
    template = 'sensor/sensors.html'

    return render(request, template, context)

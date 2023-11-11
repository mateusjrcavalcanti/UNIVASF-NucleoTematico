# iot/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers

from SolarEnergyAnalysis import settings
from iot.models import Sensor, SensorData


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
    sensor_data_json = None

    if sensor_id is not None:
        sensor = Sensor.objects.get(id=sensor_id)
        sensor_data = SensorData.objects.filter(sensor=sensor)
        sensor_data_json = serializers.serialize('json', sensor_data)

    context = {'sensors': sensors, 'sensor': sensor,
               'sensor_data': sensor_data_json}
    template = 'sensor/sensors.html'

    return render(request, template, context)

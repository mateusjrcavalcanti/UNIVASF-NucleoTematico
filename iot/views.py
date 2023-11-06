import json
import time
from django.http import HttpResponse
from django.shortcuts import render
import socket

from UNIVASFNucleoTematico import settings
from iot.models import Sensor


def index(request):
    return render(request, "sensor/index.html")


def sensors(request):
    sensors = Sensor.objects.all()
    context = {'sensors': sensors}
    return render(request, "sensor/sensors.html", context)


def sensor(request, sensor_id):
    sensors = Sensor.objects.all()
    sensor = Sensor.objects.get(id=sensor_id)
    context = {'sensors': sensors, "sensor": sensor}
    return render(request, "sensor/sensors.html", context)


def room(request, room_name):
    return render(request, "sensor/room.html", {"room_name": room_name})


def tcpSend(request):
    print(
        f"Enviando mensagem para o servidor TCP na porta {settings.TCP_PORT}...")

    data = json.dumps({
        "temperature": 25.5,
        "voltage": 12.3,
        "current": 2.1
    })

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((settings.TCP_HOST, settings.TCP_PORT))
        client_socket.send("Teste antes...".encode())
        time.sleep(1)
        client_socket.send(
            "token|24f37ccb-73a1-4b31-a949-ccaaf48c95be".encode())
        time.sleep(1)
        client_socket.send(data.encode())
        # response = client_socket.recv(1024).decode()
        response = "Mensagem enviada com sucesso!"

    return HttpResponse(f"Response from TCP Server: {response}")

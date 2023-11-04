import time
from django.http import HttpResponse
from django.shortcuts import render
import socket

from UNIVASFNucleoTematico import settings


def send_tcp_message(message):
    print(
        f"Enviando mensagem para o servidor TCP na porta {settings.TCP_PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((settings.TCP_HOST, settings.TCP_PORT))
        client_socket.send("Teste antes...".encode())
        time.sleep(1)
        client_socket.send(
            "token|24f37ccb-73a1-4b31-a949-ccaaf48c95be".encode())
        time.sleep(1)
        client_socket.send("Hello, World!".encode())
        time.sleep(1)
        client_socket.send("Após o hello...".encode())
        # response = client_socket.recv(1024).decode()
        response = "Mensagem enviada com sucesso!"

    return response


def index(request):
    return render(request, "sensor/index.html")


def room(request, room_name):
    return render(request, "sensor/room.html", {"room_name": room_name})


def tcpSend(request):
    response_from_tcp_server = send_tcp_message(
        "Hello, TCP Server!")

    return HttpResponse(f"Response from TCP Server: {response_from_tcp_server}")

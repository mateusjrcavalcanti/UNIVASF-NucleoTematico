import os
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Seed database'

    def handle(self, *args, **options):
        import json
        import socket
        import time
        import requests
        from django.conf import settings
        from iot.models import Sensor
        from termcolor import colored

        first_sensor = Sensor.objects.order_by('timestamp').first()

        response = requests.get('http://127.0.0.1:8000/info/')
        if response.status_code == 200:
            data = response.json()
            host = data['host']
            port = int(data['port'])
        else:
            self.stdout.write(f'Failed to fetch info: {response.status_code}')
            return

        print(colored("Enviando mensagem para o servidor TCP", 'blue'))
        print("[PORTA] \t=> " + colored(port, 'green'))
        print("[ID] \t\t=> " + colored(first_sensor.id, 'green'))
        print("[SENSOR] \t=> " + colored(first_sensor.description, 'green'))
        print("[USER] \t\t=> " + colored(first_sensor.user.username, 'green'))

        data = json.dumps({
            "temperature": 25.5,
            "voltage": 12.3,
            "current": 2.1
        })

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Usando os valores de host e port obtidos da rota /info
            client_socket.connect((host, port))
            client_socket.send(
                f"token|{first_sensor.token}".encode())
            time.sleep(1)
            client_socket.send(data.encode())

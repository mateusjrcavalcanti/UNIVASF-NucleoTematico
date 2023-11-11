# iot/apps.py
import json
import threading
from django.apps import AppConfig
from SolarEnergyAnalysis import settings
import socket
import sys
from termcolor import colored
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
import pytz


class IotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iot'
    active_clients = {}

    def forward_message_to_websocket(self, sensor_id, message):
        from iot.models import Sensor, SensorData
        channel_layer = get_channel_layer()
        group_name = f"sensor_{sensor_id}"

        try:
            data = json.loads(message)
            if Sensor.objects.filter(id=sensor_id).exists():
                newData = SensorData(
                    sensor_id=sensor_id,
                    temperature=data.get("temperature"),
                    voltage=data.get("voltage"),
                    current=data.get("current")
                )
                if "timestamp" in data:
                    # Defina o timestamp em UTC
                    timestamp = datetime.fromisoformat(data["timestamp"])
                    utc_timestamp = timestamp.replace(tzinfo=pytz.UTC)
                    newData.timestamp = utc_timestamp
                newData.save()

                newData.save()  # Salvar o objeto no banco de dados

                # Crie um dicionário com os dados de newData
                data_dict = {
                    "temperature": newData.temperature,
                    "voltage": newData.voltage,
                    "current": newData.current,
                    "timestamp": newData.timestamp.isoformat()
                }

                # Converta o dicionário em uma string JSON
                message_json = json.dumps(data_dict)

                # Envie a string JSON no campo 'message'
                async_to_sync(channel_layer.group_send)(group_name, {
                    'type': 'chat.message',
                    'message': message_json,
                })

        except json.JSONDecodeError as e:
            print(colored(f"Erro ao analisar o JSON: {e}", 'red'))
        except Exception as e:
            print(
                colored(f"Erro ao inserir os dados no banco de dados: {e}", 'red'))

    def handle_client(self, client_socket, client_address):
        from iot.models import Sensor
        self.active_clients[client_address] = None

        try:
            while True:
                data = client_socket.recv(1024)  # Tamanho do buffer
                if not data:
                    break
                message = data.decode()
                if not self.active_clients[client_address]:
                    if message.startswith("token|"):
                        token = message.split("|")[1]
                        if Sensor.objects.filter(token=token).exists():
                            sensor = Sensor.objects.get(token=token)
                            self.active_clients[client_address] = sensor.id
                            print(colored(
                                f"Sensor com ID ", 'green') + colored(self.active_clients[client_address], 'yellow') + colored(f" autenticado.", 'green'))

                        else:
                            print(colored("Token inválido", 'red'))
                    else:
                        print(colored("Token não fornecido", 'red'))
                else:
                    self.forward_message_to_websocket(
                        self.active_clients[client_address], message)
        except:
            # Lida com erros de conexão, por exemplo, cliente desconectado inesperadamente
            pass
        finally:
            client_socket.close()

    def start_tcp_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((settings.TCP_HOST, settings.TCP_PORT))
        except OSError as e:
            if e.errno == 98:  # Erro de porta em uso
                print(colored(
                    f"A porta {settings.TCP_PORT} está em uso. ", 'red') + colored(
                    f"Escolhendo uma porta dinâmica...", 'yellow'))
                server_socket.bind((settings.TCP_HOST, 0))  # Porta dinâmica
                _, settings.TCP_PORT = server_socket.getsockname()
                print(colored(
                    f"Porta dinâmica escolhida: {settings.TCP_PORT}", 'blue'))
            else:
                raise

        server_socket.listen()

        print(colored(
            f"Servidor TCP iniciado em {settings.TCP_HOST}:{settings.TCP_PORT}", 'blue'))

        while True:
            client_socket, addr = server_socket.accept()
            client_handler = threading.Thread(
                target=self.handle_client, args=(client_socket, addr))
            client_handler.start()

    def ready(self):
        if 'runserver' in sys.argv:
            server_thread = threading.Thread(
                target=self.start_tcp_server, args=())
            # Permite que o programa seja interrompido quando o programa principal terminar
            server_thread.daemon = True
            server_thread.start()
            print(colored("Servidor TCP iniciado em uma thread separada.", 'blue'))

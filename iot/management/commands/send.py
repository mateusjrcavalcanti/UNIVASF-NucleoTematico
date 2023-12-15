from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
from iot.fake import obter_coordenadas, obter_horarios_sol, simular_geracao_energia, obter_fuso_horario
import pytz
import time

from termcolor import colored
import json
import socket
import requests


class Command(BaseCommand):
    help = 'Simula envio em tempo real de valores de tensão e corrente da placa solar'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataDaUltimaExecucao = None

    def add_arguments(self, parser):
        parser.add_argument('cidade', nargs='?', type=str,
                            help='Nome da cidade')
        parser.add_argument('token', nargs='?', type=str,
                            help='Token do sensor')
        parser.add_argument('voltageMax', nargs='?',
                            type=float, help='Tensão máxima (Volts)')
        parser.add_argument('currentMax', nargs='?',
                            type=float, help='Corrente máxima (Amperes)')
        parser.add_argument('intervalSeconds', nargs='?',
                            type=int, help='Intervalo de atualização (segundos)')

    def handle(self, *args, **kwargs):
        from iot.models import Sensor

        cidade = kwargs['cidade']
        voltageMax = kwargs['voltageMax']
        currentMax = kwargs['currentMax']
        intervalSeconds = kwargs['intervalSeconds']
        token = kwargs['token']

        if not cidade:
            cidade = input('Digite o nome da cidade: ')

        if voltageMax is None:
            voltageMax = float(input('Digite a tensão máxima (Volts): '))

        if currentMax is None:
            currentMax = float(input('Digite a corrente máxima (Amperes): '))

        if intervalSeconds is None:
            intervalSeconds = int(
                input('Digite o intervalo de atualização (segundos): '))

        if not token:
            token = input('Digite o token do sensor:')

        sensor = Sensor.objects.filter(token=token).first()
        if sensor is None:
            sensor = Sensor.objects.order_by('timestamp').first()

        response = requests.get('http://127.0.0.1:8000/info/')
        if response.status_code == 200:
            data = response.json()
            host = data['host']
            port = int(data['port'])
        else:
            self.stdout.write(f'Failed to fetch info: {response.status_code}')
            return

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Conectar ao servidor TCP
            client_socket.connect((host, port))
            # Enviar o token
            client_socket.send(f"token|{sensor.token}".encode())

            # Aguardar um curto período antes de enviar dados
            time.sleep(1)
        except ConnectionRefusedError:
            self.stdout.write("Erro ao conectar ao servidor TCP.")
            exit(1)
        try:
            while True:
                # Verificar a data atual
                data_atual = date.today()

                # Se a data atual for diferente da data da última execução, chame simular_geracao_energia novamente
                if data_atual != self.dataDaUltimaExecucao:
                    # Obter coordenadas da cidade
                    latitude, longitude = obter_coordenadas(cidade)

                    if latitude is not None and longitude is not None:

                        # Chamar a função para simular geração de energia
                        resultados = simular_geracao_energia(
                            voltage_max=voltageMax, current_max=currentMax, interval_seconds=intervalSeconds, latitude=latitude, longitude=longitude)

                        if resultados is not None:
                            nascer_do_sol, meio_dia, por_do_sol, valores_tensao_corrente = resultados

                            # Defina o fuso horário local, UTC e da cidade
                            fuso_horario_local = pytz.timezone(
                                'America/Recife')
                            fuso_horario_utc = pytz.utc
                            fuso_horario_cidade = obter_fuso_horario(
                                latitude, longitude)

                            # Imprima os horários em UTC, horário local e no fuso horário da cidade
                            self.stdout.write(
                                "--------------------------------------------------")
                            self.stdout.write(
                                f"Horário local - O sol nasce às {nascer_do_sol.astimezone(fuso_horario_local)}")
                            self.stdout.write(
                                f"Horário local - Meio-dia ocorre às {meio_dia.astimezone(fuso_horario_local)}")
                            self.stdout.write(
                                f"Horário local - O sol se põe às {por_do_sol.astimezone(fuso_horario_local)}")
                            self.stdout.write(
                                "--------------------------------------------------")

                            self.stdout.write(
                                f"UTC - O sol nasce às {nascer_do_sol.astimezone(fuso_horario_utc)}")
                            self.stdout.write(
                                f"UTC - Meio-dia ocorre às {meio_dia.astimezone(fuso_horario_utc)}")
                            self.stdout.write(
                                f"UTC - O sol se põe às {por_do_sol.astimezone(fuso_horario_utc)}")
                            self.stdout.write(
                                "--------------------------------------------------")

                            self.stdout.write(
                                f"Fuso horário da cidade - O sol nasce às {nascer_do_sol.astimezone(fuso_horario_cidade)}")
                            self.stdout.write(
                                f"Fuso horário da cidade - Meio-dia ocorre às {meio_dia.astimezone(fuso_horario_cidade)}")
                            self.stdout.write(
                                f"Fuso horário da cidade - O sol se põe às {por_do_sol.astimezone(fuso_horario_cidade)}")
                            self.stdout.write(
                                "--------------------------------------------------")

                            while True:
                                for i, (tensao, corrente) in enumerate(valores_tensao_corrente):
                                    tempo = nascer_do_sol + \
                                        timedelta(seconds=i * intervalSeconds)
                                    tempo_agora = datetime.now(
                                        pytz.utc).astimezone(fuso_horario_local)

                                    if tempo_agora < nascer_do_sol:
                                        tempo_restante = nascer_do_sol - tempo_agora
                                        self.stdout.write(
                                            f"Falta {tempo_restante} para o nascer do sol.")
                                    elif tempo_agora > por_do_sol:
                                        proximo_nascer_do_sol = nascer_do_sol + \
                                            timedelta(days=1)
                                        tempo_restante = proximo_nascer_do_sol - tempo_agora
                                        self.stdout.write(
                                            f"Falta {tempo_restante} para o próximo nascer do sol.")

                                    if tempo_agora >= tempo:
                                        # self.stdout.write(
                                        #     f"Instante: {tempo}, Tensão: {tensao} Volts, Corrente: {corrente} Amperes")
                                        data = json.dumps({
                                            "temperature": None,
                                            "voltage": tensao,
                                            "current": corrente,
                                            'timestamp': f'{tempo}'
                                        })
                                        client_socket.send(data.encode())
                                        time.sleep(0.5)
                                    else:
                                        while tempo_agora < tempo:
                                            tempo_agora = datetime.now(
                                                pytz.utc).astimezone(fuso_horario_local)

                                self.dataDaUltimaExecucao = data_atual

                                time.sleep(60)
                        else:
                            self.stderr.write(
                                "Não foi possível obter os horários do nascer do sol e do pôr do sol.")
                    else:
                        self.stderr.write(
                            "Não foi possível obter as coordenadas da cidade. Certifique-se de que o nome da cidade seja válido.")
        except KeyboardInterrupt:
            # Lidar com a interrupção de teclado (Ctrl+C) para desconectar o socket
            self.stdout.write("Interrompendo o programa.")
        finally:
            # Fechar a conexão com o servidor
            client_socket.close()

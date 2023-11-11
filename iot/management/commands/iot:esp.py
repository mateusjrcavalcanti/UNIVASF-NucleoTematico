import json
import os
from django.core.management.base import BaseCommand
import serial
import serial.tools.list_ports


class Command(BaseCommand):
    help = 'ESP ESP8266'

    def run(self, command):
        self.ser.write(command.encode('utf-8'))
        response = self.ser.readline()
        print(response.decode('utf-8'))

    def handle(self, *args, **options):
        # Listar as portas disponíveis
        available_ports = list(serial.tools.list_ports.comports())

        if not available_ports:
            self.stdout.write(self.style.ERROR(
                'Nenhuma porta COM disponível. Verifique a conexão do ESP.'))
            return

        # Solicitar que o usuário escolha uma porta
        self.stdout.write('Portas COM disponíveis:')
        for idx, port in enumerate(available_ports):
            self.stdout.write(f"{idx + 1}: {port.device}")

        selected_index = int(
            input('Selecione o número da porta que deseja usar: ')) - 1

        if selected_index < 0 or selected_index >= len(available_ports):
            self.stdout.write(self.style.ERROR('Seleção inválida. Saindo.'))
            return

        selected_port = available_ports[selected_index].device

        # Conectar à porta selecionada
        self.ser = serial.Serial(selected_port, 115200)

        try:
            self.ser.timeout = 5

            self.run('AT+RST\r\n')  # Reinicia o ESP
            self.run('AT+CWMODE=1\r\n')  # Configura o ESP como cliente Wi-Fi

            ssid = input('Digite o nome da sua rede Wi-Fi: ')
            password = input('Digite a senha da sua rede Wi-Fi: ')
            command = f'AT+CWJAP="{ssid}","{password}"\r\n'
            self.run(command)  # Conecta o ESP à rede Wi-Fi

            # Conexão TCP
            self.run('AT+CIPMUX=0\r\n')  # Define modo de conexão única
            # Conectar ao servidor TCP
            self.run('AT+CIPSTART="TCP","<IP_DO_SERVIDOR>",<PORTA_DO_SERVIDOR>\r\n')

            # JSON para envio
            data_to_send = {
                'campo1': 'valor1',
                'campo2': 'valor2'
            }

            # Converter o dicionário em uma string JSON
            json_data = json.dumps(data_to_send)

            # Define o tamanho dos dados a serem enviados
            self.run(f'AT+CIPSEND={len(json_data)}\r\n')
            self.run(json_data)  # Enviar o JSON

        except serial.SerialException as e:
            self.stdout.write(self.style.ERROR(
                f'Erro ao se conectar à porta {selected_port}: {str(e)}'))

        finally:
            self.ser.close()

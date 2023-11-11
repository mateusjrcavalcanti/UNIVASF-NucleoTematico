# iot/fake.py
from datetime import datetime, timedelta
from decouple import config
import pytz
import requests
from timezonefinder import TimezoneFinder


def obter_fuso_horario(latitude, longitude):
    try:
        lat = float(latitude)
        lng = float(longitude)
        tz_finder = TimezoneFinder()
        tz_abreviacao = tz_finder.timezone_at(lng=lng, lat=lat)

        if tz_abreviacao:
            return pytz.timezone(tz_abreviacao)
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter o fuso horário: {str(e)}")
        return None


def obter_coordenadas(cidade):
    username = config('GEONAMES_USERNAME', default='sua_chave_de_api')

    # URL da API Geonames para obter as coordenadas
    url_geonames = f'http://api.geonames.org/searchJSON?q={cidade}&maxRows=1&username={username}'

    response_geonames = requests.get(url_geonames)

    if response_geonames.status_code == 200:
        data = response_geonames.json()
        if data['geonames']:
            coordenadas = data['geonames'][0]
            latitude = coordenadas['lat']
            longitude = coordenadas['lng']
            return latitude, longitude
        else:
            return None
    else:
        return None


def obter_horarios_sol(latitude, longitude):
    # URL da API Sunrise-Sunset
    url_sunrise_sunset = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0'

    response_sunrise_sunset = requests.get(url_sunrise_sunset)

    if response_sunrise_sunset.status_code == 200:
        data = response_sunrise_sunset.json()
        nascer_do_sol = datetime.strptime(
            data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S%z')
        por_do_sol = datetime.strptime(
            data['results']['sunset'], '%Y-%m-%dT%H:%M:%S%z')
        meio_dia = datetime.strptime(
            data['results']['solar_noon'], '%Y-%m-%dT%H:%M:%S%z')

        return nascer_do_sol, por_do_sol, meio_dia
    else:
        return None


def simular_geracao_energia(voltage_max, current_max, interval_seconds, latitude, longitude):
    # Obter horários do nascer do sol, pôr do sol e meio-dia
    horarios_sol = obter_horarios_sol(latitude, longitude)
    if horarios_sol is None:
        return None

    nascer_do_sol, por_do_sol, meio_dia = horarios_sol

    # Calcular o tempo de geração de energia (do nascer do sol até o pôr do sol)
    tempo_geracao = por_do_sol - nascer_do_sol

    # Calcular o tempo de geração de energia após o meio-dia
    tempo_geracao_apos_meio_dia = por_do_sol - meio_dia

    # Calcular a taxa de variação da corrente e tensão
    taxa_corrente_crescente = current_max / \
        tempo_geracao_apos_meio_dia.total_seconds()
    taxa_tensao_crescente = voltage_max / tempo_geracao_apos_meio_dia.total_seconds()

    # Inicializar o tempo atual como o nascer do sol
    tempo_atual = nascer_do_sol

    valores_tensao_corrente = []

    while tempo_atual < por_do_sol:
        if tempo_atual < meio_dia:
            # Durante a manhã, a corrente e tensão crescem até atingir seus máximos ao meio-dia
            tempo_desde_nascer = tempo_atual - nascer_do_sol
            corrente_atual = min(
                current_max, tempo_desde_nascer.total_seconds() * taxa_corrente_crescente)
            tensao_atual = min(
                voltage_max, tempo_desde_nascer.total_seconds() * taxa_tensao_crescente)
        else:
            # Após o meio-dia, a corrente e tensão decrescem até o pôr do sol
            tempo_desde_meio_dia = tempo_atual - meio_dia
            corrente_atual = max(
                0, current_max - tempo_desde_meio_dia.total_seconds() * taxa_corrente_crescente)
            tensao_atual = max(
                0, voltage_max - tempo_desde_meio_dia.total_seconds() * taxa_tensao_crescente)

        valores_tensao_corrente.append((tensao_atual, corrente_atual))

        tempo_atual += timedelta(seconds=interval_seconds)

    return nascer_do_sol, meio_dia, por_do_sol, valores_tensao_corrente

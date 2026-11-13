# API
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

#Importação das Funções
import funcoes as fc
import os
os.system('clear')

#Dicionário para guardar as informações das culturas no código
informacoes_cultura = {}
informacoes_cidade = {}

#Guarda o nome da cidade que está sendo analisada
nome_cidade = 'Nenhuma'

#Contador para limpar o terminal depois de uma certa quantidade de loops
contador = 0
print("Bem vindo ao sistema de monitoramento de culturas da Bioclimática!")
while True:
    contador += 1
    if contador == 3:
        os.system('cls')
        contador = 0
    print(f"Cidade sendo Analisada: {nome_cidade}")
    print("\nSelecione uma opção:")
    print("1 - Selecionar cultura")
    print("2 - Selecionar Cidade Analisada")
    print("3 - Fazer Análise dessa semana")
    print("4 - Verificar Análises Feitas")
    print("5 - Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
    match opcao:
        #Selecionar cultura que o usuário está cultivando e salvar as informações sobre ela no dicionário 'informacoes_cultura'
        case "1":
            informacoes_cultura = fc.selecionar_cultura()
            print(f"Valores de análise ajustados para a seguinte cultura: {informacoes_cultura['nome']}")
            input("Pressione Enter para continuar...")
            contador = 0
            os.system('cls')
        case "2":
            informacoes_cidade = fc.selecionar_localidade()
            nome_cidade = informacoes_cidade['nome']
            print(f"Cidade Selecionada: {nome_cidade}")
            input("Pressione Enter para continuar...")
            contador = 0
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": informacoes_cidade['latitude'],
                "longitude": informacoes_cidade['longitude'],
                "hourly": ["temperature_2m", "rain"],
                "timezone": "America/Sao_Paulo",
            }
            os.system('cls')
        case '3':
            responses = openmeteo.weather_api(url, params = params)
            # Process first location. Add a for-loop for multiple locations or weather models
            response = responses[0]

            # Process hourly data. The order of variables needs to be the same as requested.
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_rain = hourly.Variables(1).ValuesAsNumpy()

            hourly_data = {
                "date": pd.date_range(
                    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                    end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                    freq = pd.Timedelta(seconds = hourly.Interval()),
                    inclusive = "left"
                ).tz_convert(response.Timezone().decode())
            }

            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["rain"] = hourly_rain

            hourly_dataframe = pd.DataFrame(data = hourly_data)
            print("\nHourly data\n", hourly_dataframe)
        #Finalizar Programa
        case "5":
            print("Programa Finalizado")
            break
        #Opção Inválida
        case _:
            print("Opção Inválida, tente novamente!")
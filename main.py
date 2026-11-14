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
os.system('cls')

#Dicionário para guardar as informações das culturas no código
informacoes_cultura = {}
informacoes_cidade = {}

#Guarda o nome da cidade que está sendo analisada
nome_cidade = 'Nenhuma'
cultura_cultivada = 'Nenhuma'

#Contador para limpar o terminal depois de uma certa quantidade de loops
contador = 0
print("Bem vindo ao sistema de monitoramento de culturas da Bioclimática!")
while True:
    contador += 1
    if contador == 3:
        os.system('cls')
        contador = 0
    print(f"Cidade sendo Analisada: {nome_cidade}")
    print(f"Cultura sendo Cultivada: {cultura_cultivada}")
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
            try:
                informacoes_cultura = fc.selecionar_cultura()
                print(f"Valores de análise ajustados para a seguinte cultura: {informacoes_cultura['nome']}")
                input("Pressione Enter para continuar...")
                contador = 0
                cultura_cultivada = informacoes_cultura['nome']
                os.system('cls')
            except Exception as e:
                print(f"Erro: {e}")

        case "2":
            try:
                informacoes_cidade = fc.selecionar_localidade()
                nome_cidade = informacoes_cidade['nome']
                print(f"Cidade Selecionada: {nome_cidade}")
                input("Pressione Enter para continuar...")
                contador = 0
                url = "https://api.open-meteo.com/v1/forecast"
                parametros = {
                    "latitude": informacoes_cidade['latitude'],
                    "longitude": informacoes_cidade['longitude'],
                    "hourly": ["temperature_2m", "rain"],
                    "timezone": "America/Sao_Paulo",
                }
                os.system('cls')
            except Exception as e:
                print(f"Erro: {e}")
        case '3':
            if nome_cidade == 'Nenhuma':
                print("Nenhuma Cidade foi selecionada para análise ainda!")
                input("Pressione Enter para continuar...")
                os.system('cls')
            elif cultura_cultivada == 'Nenhuma':
                print("Você ainda não selecionou a cultura que está cultivando!")
                input("Pressione Enter para continuar...")
                os.system('cls')
            else:
                print("Realizando Análise")
                resposta = openmeteo.weather_api(url, params = parametros)
                resposta = resposta[0]

                dados_hora = resposta.Hourly()
                temperatura = dados_hora.Variables(0).ValuesAsNumpy()
                chuva = dados_hora.Variables(1).ValuesAsNumpy()

                dados_diarios = {
                    "date": pd.date_range(
                        start = pd.to_datetime(dados_hora.Time(), unit = "s", utc = True),
                        end =  pd.to_datetime(dados_hora.TimeEnd(), unit = "s", utc = True),
                        freq = pd.Timedelta(seconds = dados_hora.Interval()),
                        inclusive = "left"
                    ).tz_convert(resposta.Timezone().decode())
                }

                dados_diarios["temperature_2m"] = temperatura
                dados_diarios["rain"] = chuva

                dataframe = pd.DataFrame(data = dados_diarios)
                
        #Finalizar Programa
        case "5":
            print("Programa Finalizado")
            break
        #Opção Inválida
        case _:
            print("Opção Inválida, tente novamente!")
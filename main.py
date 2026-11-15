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
                    "hourly": "rain",
                    "daily" : ["temperature_2m_max", "temperature_2m_min"],
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
                try:
                    print("Realizando Análise")
                    resposta = openmeteo.weather_api(url, params = parametros)
                    resposta = resposta[0]

                    dados_hora = resposta.Hourly()
                    dados_diarios = resposta.Daily()

                    chuva = dados_hora.Variables(0).ValuesAsNumpy()

                    temperatura_maxima = dados_diarios.Variables(0).ValuesAsNumpy()
                    temperatura_minima = dados_diarios.Variables(1).ValuesAsNumpy()

                    dados_chuva = {
                        "date": pd.date_range(
                            start = pd.to_datetime(dados_hora.Time(), unit = "s", utc = True),
                            end =  pd.to_datetime(dados_hora.TimeEnd(), unit = "s", utc = True),
                            freq = pd.Timedelta(seconds = dados_hora.Interval()),
                            inclusive = "left"
                        ).tz_convert(resposta.Timezone().decode())
                    }

                    dados_temperatura = {
                        "date": pd.date_range(
                            start = pd.to_datetime(dados_diarios.Time(), unit = "s", utc = True),
                            end =  pd.to_datetime(dados_diarios.TimeEnd(), unit = "s", utc = True),
                            freq = pd.Timedelta(seconds = dados_diarios.Interval()),
                            inclusive = "left"
                        ).tz_convert(resposta.Timezone().decode())
                    }

                    dados_chuva["rain"] = chuva

                    dados_temperatura["temperature_2m_max"] = temperatura_maxima
                    dados_temperatura["temperature_2m_min"] = temperatura_minima

                    dataframe_chuva = pd.DataFrame(data = dados_chuva)
                    dataframe_temperatura = pd.DataFrame(data = dados_temperatura)

                    analises = {
                        "data" : str(dataframe_temperatura["date"][0])[0:10],
                        "analises" : fc.recolhimento_de_dados(dataframe_chuva, dataframe_temperatura, informacoes_cultura["temperatura_ideal"][0], informacoes_cultura["temperatura_ideal"][1])
                        }
                    fc.add_json("teste.json", analises)
                    print("Análises realizadas com sucesso!")
                    print("Confira os resultados na aba 'Verificar Análises Feitas'")
                    input("Pressione Enter para continuar...")
                    contador = 0
                    os.system('cls')
                except Exception as e:
                    print(f"Erro: {e}")
        #Finalizar Programa
        case "5":
            print("Programa Finalizado")
            break
        #Opção Inválida
        case _:
            print("Opção Inválida, tente novamente!")
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
import json
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

# Loop que limpa o terminal sempre a cada 3 erros
while True:
    contador += 1
    if contador == 3:
        os.system('cls')
        contador = 0

# Menu de Opções
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
        #Selecionar cultura que o usuário está cultivando
        case "1":
            try:
                #Salva as informações da cultura selecionada no dicionário 'informacoes_cultura'
                informacoes_cultura = fc.selecionar_cultura()
                print(f"Valores de análise ajustados para a seguinte cultura: {informacoes_cultura['nome']}")
                input("Pressione Enter para continuar...")

                # Reseta o contador
                contador = 0

                # Muda o nome da cultura cultivada no menu principal
                cultura_cultivada = informacoes_cultura['nome']

                # Limpa o terminal
                os.system('cls')
            except Exception as e:
                print(f"Erro: {e}")

        #Selecionar a cidade em que a o usuário está
        case "2":
            try:
                # Guarda as informações da cidade dentro do dicionário 'informacoes_cidade'
                informacoes_cidade = fc.selecionar_localidade()

                # Muda o nome da cidade no menu principal
                nome_cidade = informacoes_cidade['nome']
                print(f"Cidade Selecionada: {nome_cidade}")
                input("Pressione Enter para continuar...")

                #Reseta o contador
                contador = 0

                # Recolhe o endereço da API
                url = "https://api.open-meteo.com/v1/forecast"

                # Guarda as informações que serão requisitadas da api dentro de um dicionario
                parametros = {
                    "latitude": informacoes_cidade['latitude'], # Latitude da Localidade
                    "longitude": informacoes_cidade['longitude'], # Longitude da Localidade
                    "hourly": "rain", # Informações recolhidas por hora (Nível de Chuva)
                    "daily" : ["temperature_2m_max", "temperature_2m_min"], # Informações recolhidas por dia (Temperatura máxima e mínima)
                    "timezone": "America/Sao_Paulo", # Fuzo Horário da Cidade
                }

                # Limpa o terminal
                os.system('cls')
            except Exception as e:
                print(f"Erro: {e}")

        # Realizar Análise
        case '3':
            # Verifica se o json com as informações das análises já existe
            if fc.arquivo_existe_json("analise.json"): 
                analise_realizada = False

                # Importa 'date' da bibliotéca 'datetime'
                from datetime import date

                # Abre o arquivo das análies
                with open("analise.json", "r", encoding="utf-8") as ar:
                    import json
                    arquivo = json.load(ar)

                    # Verifica se uma análise já foi feita na data atual
                    for c in arquivo:
                        if c["data"] == fc.formatar_data(str(date.today())):
                            analise_realizada = True
                            ar.close()
                        # Se uma análise já foi feita hoje, o aplicativo avisa ao usuário que ele não pode realizar outra análise e retorna ele para o menu principal
                        if analise_realizada:
                            print("Você já realizou uma imagem hoje, verifique ela na opção 'Verificar Análises Feitas' no menu principal!")
                            input("Pressione Enter para continuar...")

                            # Limpa o terminal
                            os.system('cls')

                            # Reseta o contador
                            contador = 0
                            continue

            # Se o usuário não selecionou uma cidade ou uma cultura, cancela a análise e retorna o usuário para o menu principal
            elif nome_cidade == 'Nenhuma' or cultura_cultivada == 'Nenhuma':
                print("Selecione uma cultura e uma cidade antes de realizar uma análise!")
                input("Pressione Enter para continuar...")

                # Reseta o contador
                contador = 0

                # Limpa o terminal
                os.system('cls')
            else:
                try:
                    print("Realizando Análise...")

                    # Processa os dados fornecidos pela API
                    resposta = openmeteo.weather_api(url, params = parametros)
                    resposta = resposta[0]

                    # Recolhe os dados que se atualizam de hora em hora (chuva) vindos da resposta
                    dados_hora = resposta.Hourly()
                    chuva = dados_hora.Variables(0).ValuesAsNumpy()

                    dados_chuva = {
                        "date": pd.date_range(
                        start = pd.to_datetime(dados_hora.Time(), unit = "s", utc = True),
                        end =  pd.to_datetime(dados_hora.TimeEnd(), unit = "s", utc = True),
                        freq = pd.Timedelta(seconds = dados_hora.Interval()),
                        inclusive = "left"
                        ).tz_convert(resposta.Timezone().decode())
                    }

                    dados_chuva["rain"] = chuva

                    # Recolhe os daddos que se atualizam de dia em dia (temperatura máxima e temperatura mínima) vindos da resposta
                    dados_diarios = resposta.Daily()

                    temperatura_maxima = dados_diarios.Variables(0).ValuesAsNumpy()
                    temperatura_minima = dados_diarios.Variables(1).ValuesAsNumpy()

                    dados_temperatura = {
                        "date": pd.date_range(
                            start = pd.to_datetime(dados_diarios.Time(), unit = "s", utc = True),
                            end =  pd.to_datetime(dados_diarios.TimeEnd(), unit = "s", utc = True),
                            freq = pd.Timedelta(seconds = dados_diarios.Interval()),
                            inclusive = "left"
                        ).tz_convert(resposta.Timezone().decode())
                    }

                    dados_temperatura["temperature_2m_max"] = temperatura_maxima
                    dados_temperatura["temperature_2m_min"] = temperatura_minima

                    # Transforma os dados recolhidos em dataframes
                    dataframe_chuva = pd.DataFrame(data = dados_chuva)
                    dataframe_temperatura = pd.DataFrame(data = dados_temperatura)

                    # Guarda a data em que a análise foi realizada e todos os dados da análise em um dicionário
                    analises = {
                        "data" : fc.formatar_data(str(dataframe_temperatura["date"][0])[0:10]),
                        "analises" : fc.recolhimento_de_dados(dataframe_chuva, dataframe_temperatura, informacoes_cultura["temperatura_ideal"][0], informacoes_cultura["temperatura_ideal"][1])
                        }

                    # Guarda a análise realizada em um arquivo .json
                    fc.add_json("analise.json", analises)
                    print("Análises realizadas com sucesso!")
                    print("Confira os resultados na aba 'Verificar Análises Feitas'")
                    input("Pressione Enter para continuar...")

                    # Reseta o contador
                    contador = 0

                    # Limpa o terminal
                    os.system('cls')
                # Retorna uma mensagem de erro para a tela do usuário caso um erro aconteça
                except Exception as e:
                    print(f"Erro Inesperado: {e}")

        # Verificar dados das análises realizadas
        case "4":
            # Se o usuário não selecionou uma cultura, cancela a visualização 
            if cultura_cultivada == 'Nenhuma':
                print("Cultura ainda não selecionada, por favor faça sua seleção no menu principal")
                input("Pressione Enter para continuar...")

                # Reseta o contador
                contador = 0

                # Limpa o terminal
                os.system('cls')

            # Se o usuário não tiver requisitado nenhuma análise 
            elif not fc.arquivo_existe_json("analise.json"):
                print("Nenhuma Análise foi realizada ainda, requisite uma análise da semana na opção 'Fazer Análise dessa semana' no menu principal")
                input("Pressione Enter para continuar...")

                # Reseta o contador
                contador = 0

                # Limpa o terminal
                os.system('cls')
            else:
                print("Selecione a série de análises que você quer verificar a partir da data de sua requisição")

                # Coloca todas as análises requisitadas em uma lista de opções e recolhe a data selecionada pelo usuário
                data = fc.criar_escolhas("analise", "data")

                # Se o usuário digitar '0', cancela o comando e retorna para o menu
                if data == "Cancelado":
                    input("Pressione Enter para continuar...")

                    # Limpa o terminal
                    os.system('cls')

                    # Reseta o contador
                    contador = 0

                else:
                    print(f"Você selecionou as análises do dia {data}")

                    # Recolhe todos os dias dentro da análise e coloca eles dentro de uma lista
                    lista = fc.recolhe_keys("analise", data)
                    with open(f"analise.json", "r", encoding="utf-8") as arquivo:
                        ar = json.load(arquivo)
                        while True:
                            try:
                                print("Selecione o dia cujo as informações você deseja verificar:")
                                # Transforma todas as datas da lista em uma lista de opções
                                for c, i in enumerate(lista):
                                    print(f"{c+1} - {i}")
                                print("0 - Sair")
                                escolha = int(input("Escolha: "))

                                # Retorna um erro se o usuário digitar um número que não está associado a uma data
                                if escolha > len(lista) or escolha <0:
                                    print("Escolha Inválida, tente novamente!")

                                # Se o usuário digitar '0', retorna o usuário para o menu principal
                                elif escolha == 0:
                                    arquivo.close()
                                    print("Retornando ao menu principal")
                                    input("Pressione Enter para continuar...")

                                    # Limpa o terminal
                                    os.system('cls')

                                    # Reseta o contador
                                    contador = 0
                                    break
                                else:
                                    # Retorna para o usuário todos os dados da análise com base 
                                    print(f"=== Análise do Dia {ar[0]["analises"][lista[escolha-1]]['data']} ===") # Dia sendo analisado
                                    print(f"Temperatura Máxima: {ar[0]["analises"][lista[escolha-1]]['temp_maxima']}ºC") # Temperatura Máxima
                                    print(f"Temperatura Mínima: {ar[0]["analises"][lista[escolha-1]]['temp_minima']}ºC") # Temperatura Minima
                                    print(f"{ar[0]["analises"][lista[escolha-1]]['situacao_temperatura']}") # Se a temperatura do dia causa problemas para a cultura escolhida
                                    print(f"Nível de Chuva: {ar[0]["analises"][lista[escolha-1]]['chuva']:.2} ({fc.nivel_chuva(ar[0]["analises"][lista[escolha-1]]['chuva'])})") # Indice Pluviométrico
                                    # Retorna o horário em que a chuva atinge o seu pico somente se achuva tiver um indice pluviométrico superior a 0.3mm
                                    if fc.nivel_chuva(ar[0]["analises"][lista[escolha-1]]['chuva']) != "Sem chuva/chuva insignificante":
                                        print(f"Horário de Pico da Chuva: {ar[0]["analises"][lista[escolha-1]]['hora']}")

                                    # Verifica se a chuva coloca a plantação em risco e avisa o usuário
                                    if ar[0]["analises"][lista[escolha-1]]['chuva'] > informacoes_cultura['chuva_ideal']:
                                        print(f"A intensidade da chuva coloca a plantação em risco")
                                    else:
                                        print(f"A chuva não oferece riscos a plantação")
                                    continuar = input()
                            except ValueError:
                                print("Erro! A seleção não aceita nada além de números!")
                                continue
                            except Exception as e:
                                print(f"Erro: {e}")
        #Finalizar Programa
        case "5":
            print("Programa Finalizado")
            break
        #Opção Inválida
        case _:
            print("Opção Inválida, tente novamente!")

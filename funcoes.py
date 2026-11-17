import os
os.system('clear')

# Funções de Seleção

# Seletor de culturas
def selecionar_cultura() -> dict:
    # Limpa o terminal a cada 3 tentativas falhas
    cont = 0
    while True:
        if cont == 3:
            os.system('cls')
            cont = 0
        cont += 1

        # Menu de Opções
        print("Selecione a cultura que está cultivando: ")
        print("1 - Alface")
        print("2 - Tomate Cereja")
        print("3 - Cebolinha")
        escolha = input("Digite o número correspondente à cultura: ")

        # Quando o usuário toma uma escolha, retorna um dicionário com todas as informações da cultura cultivada
        match escolha:
            case "1":
                print("Você selecionou Alface.")
                return {
                    "nome": "Alface", # Nome da planta: Como ela é chamada
                    "temperatura_ideal": (15, 20), # Faixa de temperatura: A temperatura mínima ideal (0) e a máxima idel (1) para o bem estar da planta
                    "chuva_ideal": 5 # Índice Pluviométrico: A intensidade máxima de chuva que a planta pode aguentar antes de sofrer danos
                }
            case "2":
                print("Você selecionou Tomate Cereja.")
                return {
                    "nome": "Tomate Cereja",
                    "temperatura_ideal": (18, 25),
                    "chuva_ideal": 10
                }
            case "3":
                print("Você selecionou Cebolinha.")
                return {
                    "nome": "Cebolinha",
                    "temperatura_ideal": (15, 25),
                    "chuva_ideal": 5
                }
            
            # Retorna uma mensagem de erro caso o usuário digite uma opção inválida
            case _:
                print("Opção inválida!")

# Seletor de localidades
# Essa função tem funcionalidade praticamente identicas às da função 'selecionar_culturas', com a única mudança sendo os valores retornados pela escolha do usuário
def selecionar_localidade() -> dict:
    cont = 0
    while True:
        if cont == 3:
            os.system('cls')
            cont = 0
        cont += 1
        print("Selecione qual localidade você quer colocar")
        print("1 - Osasco")
        print("2 - São Paulo")
        print("3 - Guarulhos")
        escolha = input("Digite o número correspondente à cultura: ")
        match escolha:
            case '1':
                return {
                    'nome' : 'Osasco', # Nome da Cidade: O nome da cidade selecionada
                    'latitude' : -23.5325, # Latitude: A latitude da localidade
                    'longitude' : -46.7917 # Longitude: A longitude da localidade (ambas latitude e longitude são usadas para que a API possa localizar o local onde a análise será feita)
                }
            case '2':
                return {
                    'nome' : 'São Paulo',
                    'latitude' : -23.5475,
                    'longitude' : -46.6361
                }
            case '3':
                return {
                    'nome' : 'Guarulhos',
                    'latitude' : -23.4628,
                    'longitude' : -46.5333
                }
            case _:
                print("Opção Inválida!")

# =======================================================================================
# Manipulação de Arquivos JSON

# Verifica se um arquivo Json com um certo nome já existe no sistema
def arquivo_existe_json(nome: str) -> bool:
    # Importa a bibliotéca Json
    import json

    # Tenta abrir o arquivo com o nome providenciado pelo usuário e, se conseguir com sucesso, retorna um valor 'True'
    try:
        with open(nome, 'r', encoding='utf-8') as arquivo:
            json.load(arquivo)
            arquivo.close()
        return True

    # Caso não consiga encontrar um arquivo com o nome selecionado, retorna um valor 'False'
    except FileNotFoundError:
        return False

# Adiciona as informações de um dicionário a um arquivo Json
def add_json(arquivo: str, dados: dict) -> None:
    # Importa a biblioteca Json
    import json

    # Usa a função 'arquivo_existe_json' para verificar se o arquivo existe
    if not arquivo_existe_json(arquivo):
        # Caso o arquivo não exista, inicia uma lista e guarda as informações do dicionario dentro da lista
        info = []
        info.append(dados)

        # Em seguida, cria um novo arquivo com o nome providenciado, salva as informações dentro do arquivo e fecha o arquivo depois
        with open(arquivo, "w", encoding='utf-8') as ar:
            json.dump(info, ar, indent=4)
            ar.close()
    
    else:
        # Caso o arquivo já exista, abre a lista do arquivo, armazena ela dentro da variável 'info' e fecha o arquivo
        with open(arquivo, 'r', encoding='utf-8') as ar:
            info = json.load(ar)
            ar.close()
            # Em seguida, armazena os dados fornecidos como um novo elemento dentro da lista
            info.append(dados)

            # Com as atualizações feitas, abre o arquivo novamente, substitui a lista anterior com a nova e fecha o arquivo novamente
            with open(arquivo, "w", encoding='utf-8') as ar:
                json.dump(info, ar, indent=4)
                ar.close()

# =======================================================================================
# Funções de Classificação

# Recebe o índice pluviométrico em mm e, com base nesse índice, retorna uma str que diz a intensidade da chuva
def nivel_chuva(chuva: float) -> str:
    if 0 <= chuva <= 0.3:
        return "Sem chuva/chuva insignificante"
    elif 0.3 < chuva <= 2.5:
        return "Chuvisco"
    elif 2.5 < chuva <= 10:
        return "Chuva Fraca"
    elif 10 < chuva <= 25:
        return "Chuva Moderada"
    elif 25 < chuva <= 50:
        return "Chuva Forte"
    else:
        return "Chuva Extrema"

# Recebe a faixa de temperatura de uma planta (temp_minima e temp_maxima) junto com o nome do dataframe onde estão as informações das temperaturas máxiams e mínimas dos dias da semana, e retorna caso essas temperaturas apresentam riscos para a planta em questão
# Essa função também recebe um contador, pois foi feita especificamente para operar dentro de um loop da função 'recolhimento de dados'
def analisar_temperatura(temp_minima: float, temp_maxima: float, dataframe: str, contador: int) -> list:
    # A função sempre retornará as temperaturas recolhidas do dataframe (mínima e máxima) junto com uma mensagem dizendo se a temperatura está fora do ideal ou não

    if float(str(dataframe["temperature_2m_max"][contador])) > temp_maxima: # Temperatura acima do ideal
        return [float(str(dataframe["temperature_2m_min"][contador])), float(str(dataframe["temperature_2m_max"][contador])), "A temperatura Maxima está acima do ideal"]
    
    if float(str(dataframe["temperature_2m_min"][contador])) < temp_minima: # Temperatura abaixo do ideal
        return [float(str(dataframe["temperature_2m_min"][contador])), float(str(dataframe["temperature_2m_max"][contador])), "A temperatura Minima está abaixo do ideal"]
    
    if float(str(dataframe["temperature_2m_min"][contador])) > temp_minima and float(str(dataframe["temperature_2m_max"][contador])) < temp_maxima: # Temperatura Ideal
        return [float(str(dataframe["temperature_2m_min"][contador])), float(str(dataframe["temperature_2m_max"][contador])), "A temperatura está ideal"]

# Muda o formato de uma data para o padrão brasileiro
# Como a API que utilizamos não é brasileira, as datas recolhidas dela vem no formato YYYY-MM-DD, então criamos uma função para mudar a formatação das datas para o padrão brasileiro
def formatar_data(data: str) -> str:
    # Cria uma lista dos valores da data separados a partir do caracter '-'
    separacao = data.split("-")

    # Rearranja os valores da lista em uma string na ordem correta e retorna essa string
    data_formatada = f"{separacao[2]}-{separacao[1]}-{separacao[0]}"
    return data_formatada


def recolhimento_de_dados(dataframe_hora: str, dataframe_dia: str, temp_minima:float, temp_maxima:float) -> dict:
    dicionario_return = {}
    lista_datas = []
    lista_datas_add = []
    lista_temperaturas = []
    numero = []
    data = ''
    contador = 0
    for c, i in enumerate(dataframe_hora['date']):
        if c == 0:
            data = str(i)[0:10]
        if str(i)[0:10] != data:
            data = str(i)[0:10]
        if data not in lista_datas:
            lista_datas.append(data)
        if lista_datas[contador] in str(i) and c != len(dataframe_hora['date'])-1:
            if len(lista_datas_add) == 0:
                lista_datas_add.append(str(i)[11:19]) 
                lista_datas_add.append(float(str(dataframe_hora['rain'][c])))
            else:
                if float(str(dataframe_hora['rain'][c])) > lista_datas_add[1]:
                    lista_datas_add[0] = str(i)[11:19]
                    lista_datas_add[1] = float(str(dataframe_hora['rain'][c]))            
        else:
            numero.append(list(lista_datas_add))
            lista_datas_add.clear()
            contador += 1
            lista_datas_add.append(str(dataframe_hora['date'][c])[11:19]) 
            lista_datas_add.append(float(str(dataframe_hora['rain'][c])))
    for c, i in enumerate(dataframe_dia['date']):
        lista_temperaturas.append(analisar_temperatura(temp_minima, temp_maxima, dataframe_dia, c))

    for c in range(0,7):
        dicionario_add = {
            "data" : formatar_data(lista_datas[c]),
            "hora" : numero[c][0],
            "chuva" : numero[c][1],
            "temp_maxima" : lista_temperaturas[c][1],
            "temp_minima" : lista_temperaturas[c][0],
            "situacao_temperatura" : lista_temperaturas[c][2]
        }
        dicionario_return[f"{lista_datas[c]}"] = dicionario_add

    return dicionario_return

def criar_escolhas(nome_arquivo: str, nome_campo: str) -> str:
    lista_numeros = []
    lista_nomes = []
    import json
    with open(f"{nome_arquivo}.json", "r", encoding="utf-8") as arquivo:
        ar = json.load(arquivo)
        print("0 - Sair")
        for c, i in enumerate(ar):
            print(f"{c+1} - {i[nome_campo]}")
            lista_nomes.append(i[nome_campo])
            lista_numeros.append(c+1)
            arquivo.close()
            while True:
                try:
                    escolha = int(input("Escolha: "))
                    if escolha == 0:
                        return "Cancelado"
                    elif escolha not in lista_numeros:
                        print("Escolha Inválida, tente novamente")
                    else:
                        return lista_nomes[escolha-1]
                except ValueError:
                    print("Erro, o valor não pode ser uma palavra!")
                    continue

# Recolhe as keys de um dicionário dentro de um arquivo json que estão associadas a uma certa data
# Fizemos essa função para recolher as datas dentro de uma análise, datas essas que estão associadas à data em que a análise foi requisitada e à key 'analises'
def recolhe_keys(nome_arquivo: str, data: str) -> list:
    # Importa a biblioteca JSON
    import json

    # Abre o arquivo json e recolhe as informações dentro dele
    with open(f"{nome_arquivo}.json", "r", encoding="utf-8") as arquivo:
            ar = json.load(arquivo)

            # Percorre todo o arquivo e, se encontrar uma data correspondente à informada, retorna todas as keys associadas à key 'analises'
            for c, i in enumerate(ar):
                if i["data"] == data:
                    return list(i["analises"].keys())
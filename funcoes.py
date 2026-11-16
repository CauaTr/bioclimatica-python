import os
os.system('clear')

def selecionar_cultura() -> dict:
    cont = 0
    while True:
        if cont == 3:
            os.system('cls')
            cont = 0
        cont += 1
        print("Selecione a cultura que está cultivando: ")
        print("1 - Alface")
        print("2 - Tomate Cereja")
        print("3 - Cebolinha")
        escolha = input("Digite o número correspondente à cultura: ")
        match escolha:
            case "1":
                print("Você selecionou Alface.")
                return {
                    "nome": "Alface",
                    "temperatura_ideal": (15, 20),
                    "chuva_ideal": 5
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
            case _:
                print("Opção inválida!")

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
                    'nome' : 'Osasco',
                    'latitude' : -23.5325,
                    'longitude' : -46.7917
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

def arquivo_existe_json(nome: str) -> bool:
    import json
    try:
        with open(nome, 'r', encoding='utf-8') as arquivo:
            json.load(arquivo)
            arquivo.close()
        return True
    except FileNotFoundError:
        return False

def add_json(arquivo: str, dados: dict) -> None:
    import json
    if not arquivo_existe_json(arquivo):
        alunos = []
        alunos.append(dados)
        with open(arquivo, "w", encoding='utf-8') as ar:
            json.dump(alunos, ar, indent=4)
            ar.close()
    else:
        with open(arquivo, 'r', encoding='utf-8') as ar:
            alunos = json.load(ar)
            ar.close()
            alunos.append(dados)
            with open(arquivo, "w", encoding='utf-8') as ar:
                json.dump(alunos, ar, indent=4)
                ar.close()

def analisar_temperatura(temp_minima: float, temp_maxima: float, dataframe: str, contador: int) -> str:
    if float(str(dataframe["temperature_2m_max"][contador])) > temp_maxima:
        return [float(str(dataframe["temperature_2m_min"][contador])), float(str(dataframe["temperature_2m_max"][contador])), "A temperatura Maxima está acima do ideal"]
    if float(str(dataframe["temperature_2m_min"][contador])) < temp_minima:
        return [float(str(dataframe["temperature_2m_min"][contador])), float(str(dataframe["temperature_2m_max"][contador])), "A temperatura Minima está abaixo do ideal"]
    if float(str(dataframe["temperature_2m_min"][contador])) > temp_minima and float(str(dataframe["temperature_2m_max"][contador])) < temp_maxima:
        return [float(str(dataframe["temperature_2m_min"][contador])), float(str(dataframe["temperature_2m_max"][contador])), "A temperatura está ideal"]

def formatar_data(data: str) -> str:
    separacao = data.split("-")
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

def recolhe_keys(nome_arquivo: str, chave: str) -> list:
    import json
    with open(f"{nome_arquivo}.json", "r", encoding="utf-8") as arquivo:
            ar = json.load(arquivo)
            for c, i in enumerate(ar):
                if i["data"] == chave:
                    return list(i["analises"].keys())
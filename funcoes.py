import os
os.system('clear')

def selecionar_cultura() -> dict:
    cont = 0
    while True:
        if cont == 3:
            os.system('clear')
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
                    "umidade_ideal": (60, 70),
                    "chuva_ideal": (0, 5)
                }
            case "2":
                print("Você selecionou Tomate Cereja.")
                return {
                    "nome": "Tomate Cereja",
                    "temperatura_ideal": (18, 25),
                    "umidade_ideal": (60, 80),
                    "chuva_ideal": (0, 10)
                }
            case "3":
                print("Você selecionou Cebolinha.")
                return {
                    "nome": "Cebolinha",
                    "temperatura_ideal": (15, 25),
                    "umidade_ideal": (50, 70),
                    "chuva_ideal": (0, 5)
                }
            case _:
                print("Opção inválida. Por favor, selecione uma cultura válida.")
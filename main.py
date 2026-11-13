import funcoes as fc
import os
os.system('clear')

informacoes_cultura = {}
contador = 0
print("Bem vindo ao sistema de monitoramento de culturas da Bioclimática!")
while True:
    contador += 1
    if contador == 3:
        os.system('cls')
        contador = 0
    print("\nSelecione uma opção:")
    print("1 - Selecionar cultura")
    print("2 - Fazer Análise do Clima")
    print("3 - Verificar Análises Recentes")
    print("4 - Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
    match opcao:
        case "1":
            informacoes_cultura = fc.selecionar_cultura()
        case "4":
            print("Programa Finalizado")
            break
        case _:
            print("Opção Inválida, tente novamente!")
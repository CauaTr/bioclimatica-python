import funcoes as fc

informacoes_cultura = {}

print("Bem vindo ao sistema de monitoramento de culturas da Bioclimática!")
while True:
    print("\nSelecione uma opção:")
    print("1 - Selecionar cultura")
    print("2 - Fazer Análise do Clima")
    print("3 - Verificar Análises Recentes")
    print("4 - Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
    match opcao:
        case "1":
            informacoes_cultura = fc.selecionar_cultura()
        case _:
            print("Opção Inválida, tente novamente!")
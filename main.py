from base_conhecimento import BaseConhecimento
from assistente import Assistente


def mostrar_menu():
    print("\n" + "=" * 42)
    print("CITIZEN ASSIST AI - PRIMEIRO EMPREGO")
    print("=" * 42)
    print("1 - Fazer uma pergunta")
    print("2 - Navegar por categorias")
    print("3 - Ver indicadores")
    print("4 - Exportar atendimentos para CSV")
    print("0 - Sair")


def main():
    base = BaseConhecimento("data/base_conhecimento.json")

    if not base.carregar():
        print("O programa será encerrado porque a base não pôde ser carregada.")
        return

    assistente = Assistente(
        "Citizen Assist AI - Primeiro Emprego",
        base
    )

    print("Assistente carregado com sucesso.")
    print("Não informe CPF, telefone, e-mail ou outros dados pessoais.")

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()

        elif opcao == "2":
            assistente.navegar()

        elif opcao == "3":
            assistente.indicadores()

        elif opcao == "4":
            assistente.exportar_csv()

        elif opcao == "0":
            assistente.avaliar_facilidade()
            assistente.exportar_csv()
            print("Atendimento encerrado.")
            break

        else:
            print("Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    main()

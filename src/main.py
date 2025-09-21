import os
import sys
import time
from src import converter
from src import quack
from src import splitter
from src import utils

def main_menu():
    while True:
        utils.clear()
        print("=" * 32)
        print("--------------MENU--------------")
        print("=" * 32)
        print("0 - 🔌 Finalizar o Programa")
        print("1 - 🔄 Converter Arquivo")
        print("2 - 📊 Relatório de Arquivo")
        print("3 - 🦆 Rodar Query SQL (DuckDB)")
        print("4 - ⚔️ Splitter de arquivos")
        print("=" * 32)

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Saindo... 👋")
            time.sleep(1)
            os.system("cls")
            break
        elif opcao == "1":
            os.system("cls")
            converter.convert_menu()
        elif opcao == "2":
            print("\n>> [Relatório de Arquivo ainda não implementado]")
            time.sleep(1)
            os.system("cls")
        elif opcao == "3":
            quack.pato_menu()
            #print("\n>> [Rodar Query SQL ainda não implementado]")
            time.sleep(1)
            os.system("cls")
        elif opcao == "4":
            splitter.split_menu()
            #print("\n>> [Módulo Splitter ainda não implementado]")
            time.sleep(1)
        else:
            print("⚠️ Opção inválida, tente novamente!")
            time.sleep(1)
            os.system("cls")

if __name__ == "__main__":
    main_menu()

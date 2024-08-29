import timeit
import tracemalloc
from tab import BTree

def medir_tempo(func):
    """Decorator para medir o tempo de execução de uma função em milissegundos."""
    def wrapper(*args, **kwargs):
        tempo_execucao = timeit.timeit(lambda: func(*args, **kwargs), number=1) * 1000  # Convertendo para milissegundos
        print(f"Tempo de execução da função '{func.__name__}': {tempo_execucao:.6f} ms")
        return tempo_execucao
    return wrapper

@medir_tempo
def inserir_registro(btree, id, nome, idade):
    btree.insert(id, nome, idade)

@medir_tempo
def buscar_registro(btree, id):
    return btree.search(id)

@medir_tempo
def atualizar_registro(btree, id, nome, idade):
    return btree.update(id, nome, idade)

@medir_tempo
def remover_registro(btree, id):
    return btree.remove(id)

def main():
    ordem = 2
    btree = BTree(ordem)
    btree.load_from_file()  # Carrega os dados do arquivo ao iniciar o programa

    # Dicionário para armazenar os tempos de execução das operações
    tempos_execucao = {
        "inserir": [],
        "buscar": [],
        "atualizar": [],
        "remover": []
    }

    tracemalloc.start()  # Inicia a medição do consumo de memória

    while True:
        print("\nMenu de Operações:")
        opcoes = [
            "1. Inserir registro",
            "2. Buscar registro",
            "3. Atualizar registro",
            "4. Remover registro",
            "5. Exibir tabela",
            "6. Sair"
        ]

        for opcao in opcoes:
            print(opcao)
        
        escolha = input("Escolha uma operação (1-6): ")

        if escolha == '1':
            while True:
                id = int(input("Digite o ID: "))
                nome = input("Digite o nome: ")
                idade = int(input("Digite a idade: "))
                tempo_execucao = inserir_registro(btree, id, nome, idade)
                tempos_execucao["inserir"].append(tempo_execucao)
                print(f"Registro {id} inserido com sucesso. Tempo de execução: {tempo_execucao:.6f} ms")
                continuar = input("Deseja inserir outro registro? (s/n): ")
                if continuar.lower() != 's':
                    break

        elif escolha == '2':
            while True:
                id = int(input("Digite o ID a ser buscado: "))
                tempo_execucao = buscar_registro(btree, id)
                tempos_execucao["buscar"].append(tempo_execucao)
                if tempo_execucao:
                    print(f"Registro com ID {id} encontrado. Tempo de execução: {tempo_execucao:.6f} ms")
                else:
                    print(f"Registro com ID {id} não encontrado. Tempo de execução: {tempo_execucao:.6f} ms")
                continuar = input("Deseja buscar outro registro? (s/n): ")
                if continuar.lower() != 's':
                    break

        elif escolha == '3':
            while True:
                id = int(input("Digite o ID do registro a ser atualizado: "))
                nome = input("Digite o novo nome: ")
                idade = int(input("Digite a nova idade: "))
                tempo_execucao = atualizar_registro(btree, id, nome, idade)
                tempos_execucao["atualizar"].append(tempo_execucao)
                print(f"Registro {id} atualizado com sucesso. Tempo de execução: {tempo_execucao:.6f} ms")
                continuar = input("Deseja atualizar outro registro? (s/n): ")
                if continuar.lower() != 's':
                    break

        elif escolha == '4':
            while True:
                id = int(input("Digite o ID do registro a ser removido: "))
                tempo_execucao = remover_registro(btree, id)
                tempos_execucao["remover"].append(tempo_execucao)
                print(f"Registro {id} removido com sucesso. Tempo de execução: {tempo_execucao:.6f} ms")
                continuar = input("Deseja remover outro registro? (s/n): ")
                if continuar.lower() != 's':
                    break

        elif escolha == '5':
            print("Tabela atual:")
            btree.print_table()

        elif escolha == '6':
            print("Encerrando o programa.")
            btree.save_to_file()  # Salva os dados no arquivo ao encerrar o programa

            # Exibe o relatório de desempenho
            print("\nRelatório de Desempenho:")
            for operacao, tempos in tempos_execucao.items():
                if tempos:
                    media_tempo = sum(tempos) / len(tempos)  # Calcula o tempo médio de execução para cada operação
                    print(f"Tempo médio para {operacao}: {media_tempo:.6f} ms")
                else:
                    print(f"Nenhuma operação de {operacao} foi realizada.")

            # Consumo de memória
            memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"Memória atual usada: {memoria_atual / 1024:.2f} KB")
            print(f"Pico de memória usada: {memoria_pico / 1024:.2f} KB")

            break

        else:
            print("Escolha inválida! Por favor, selecione uma opção válida.")

if __name__ == "__main__":
    main()
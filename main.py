from tab import BTree

def menu():
    print("\nMenu:")
    print("1. Inserir")
    print("2. Buscar")
    print("3. Atualizar")
    print("4. Remover")
    print("5. Imprimir Árvore")
    print("6. Sair")
    return input("Escolha uma opção: ")

def main():
    grau = int(input("Informe o grau mínimo da Árvore B: "))
    arvore = BTree(grau)
    arvore.load_tree()
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            chave = int(input("Informe a chave a ser inserida: "))
            arvore.insert(chave)
            print(f"Chave {chave} inserida.")
            
        elif opcao == "2":
            chave = int(input("Informe a chave a ser buscada: "))
            if arvore.find(chave):
                print(f"Chave {chave} encontrada.")
            else:
                print(f"Chave {chave} não encontrada.")
        
        elif opcao == "3":
            chave_antiga = int(input("Informe a chave a ser atualizada: "))
            chave_nova = int(input("Informe a nova chave: "))
            arvore.update(chave_antiga, chave_nova)
        
        elif opcao == "4":
            chave = int(input("Informe a chave a ser removida: "))
            if arvore.delete(chave):
                print(f"Chave {chave} removida.")
            else:
                print(f"Chave {chave} não encontrada.")
        
        elif opcao == "5":
            arvore.print_tree()
        
        elif opcao == "6":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()

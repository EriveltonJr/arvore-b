import json

class Registro:
    """
    Representa um registro individual na árvore B.
    """
    def __init__(self, id, nome, idade):
        self.id = id  # Identificador único do registro
        self.nome = nome  # Nome do registro
        self.idade = idade  # Idade do registro

    def __lt__(self, other):
        return self.id < other.id  # Compara registros pelo ID

    def __eq__(self, other):
        return self.id == other.id  # Verifica igualdade pelo ID

    def __str__(self):
        return f"{self.id:<10} {self.nome:<20} {self.idade:<5}"  # Formata o registro como string

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "idade": self.idade}  # Converte para dicionário

    @staticmethod
    def from_dict(data):
        return Registro(data['id'], data['nome'], data['idade'])  # Cria registro a partir de dicionário

class BTreeNode:
    """
    Representa um nó em uma árvore B.
    """
    def __init__(self, t):
        self.t = t  # Grau mínimo da árvore
        self.registros = []  # Lista de registros no nó
        self.children = []  # Lista de filhos do nó
        self.leaf = True  # Indica se é folha

    def insert_non_full(self, registro):
        """
        Insere registro em nó não cheio.
        """
        i = len(self.registros) - 1

        if self.leaf:
            # Adiciona um espaço para o novo registro e desloca os existentes
            self.registros.append(None)
            while i >= 0 and registro < self.registros[i]:
                self.registros[i + 1] = self.registros[i]
                i -= 1
            self.registros[i + 1] = registro
        else:
            # Encontra o filho apropriado para descer
            while i >= 0 and registro.id < self.registros[i].id:
                i -= 1
            i += 1

            # Certifique-se de que estamos dentro dos limites dos filhos
            if i >= len(self.children):
                i = len(self.children) - 1  # Ajusta o índice para o último filho disponível

            if len(self.children[i].registros) == 2 * self.t - 1:
                self.split_child(i)
                if registro.id > self.registros[i].id:
                    i += 1
                if i >= len(self.children):
                    i = len(self.children) - 1  # Reajusta o índice novamente após a divisão

            self.children[i].insert_non_full(registro)

    def split_child(self, i):
        """
        Divide um filho cheio em dois.
        """
        y = self.children[i]
        z = BTreeNode(y.t)
        z.leaf = y.leaf
        z.registros = y.registros[y.t:]  # Move a metade superior dos registros para z
        y.registros = y.registros[:y.t-1]  # Mantém a metade inferior dos registros em y

        if not y.leaf:
            z.children = y.children[y.t:]  # Move os filhos correspondentes para z
            y.children = y.children[:y.t]  # Mantém os filhos correspondentes em y

        self.children.insert(i + 1, z)  # Insere z como filho do nó atual
        self.registros.insert(i, y.registros.pop())  # Move o registro do meio para o nó pai

    def search(self, id):
        """
        Busca um registro pelo ID.
        """
        i = 0
        while i < len(self.registros) and id > self.registros[i].id:
            i += 1

        if i < len(self.registros) and id == self.registros[i].id:
            return self.registros[i]  # Retorna registro encontrado
        elif self.leaf:
            return None  # Retorna None se não encontrado
        else:
            # Garante que o índice `i` não ultrapasse o número de filhos
            if i >= len(self.children):
                return None
            return self.children[i].search(id)  # Continua busca no filho

    def update(self, id, nome, idade):
        """
        Atualiza um registro existente pelo ID.
        """
        i = 0
        while i < len(self.registros) and id > self.registros[i].id:
            i += 1
        
        if i < len(self.registros) and id == self.registros[i].id:
            self.registros[i].nome = nome  # Atualiza nome do registro
            self.registros[i].idade = idade  # Atualiza idade do registro
            return True
        
        if self.leaf:
            return False  # Retorna False se não encontrado
        else:
            return self.children[i].update(id, nome, idade)  # Continua atualização no filho

    def remove(self, id, t):
        """
        Remove um registro da árvore B.
        """
        i = 0
        while i < len(self.registros) and id > self.registros[i].id:
            i += 1
        
        if i < len(self.registros) and id == self.registros[i].id:
            if self.leaf:
                self.registros.pop(i)  # Remove registro de uma folha
            else:
                self._remove_internal_node(i, t)  # Remove registro de nó interno
        elif self.leaf:
            print(f"Erro: Registro com ID {id} não existe.")  # Mensagem de erro se não encontrado
            return  # Não faz nada se não encontrado
        else:
            if len(self.children[i].registros) < t:
                self._fill(i, t)  # Garante que filho tenha registros suficientes
            if i > len(self.registros):
                self.children[i - 1].remove(id, t)  # Continua remoção no filho à esquerda
            else:
                self.children[i].remove(id, t)  # Continua remoção no filho à direita
                
    def _remove_internal_node(self, i, t):
        """
        Remove um registro de um nó interno.
        """
        registro = self.registros[i]

        # Se o filho anterior (à esquerda) tem pelo menos t registros, encontre o predecessor.
        if len(self.children[i].registros) >= t:
            pred = self._get_predecessor(i)
            self.registros[i] = pred
            self.children[i].remove(pred.id, t)
        
        # Se o filho seguinte (à direita) tem pelo menos t registros, encontre o sucessor.
        elif i + 1 < len(self.children) and len(self.children[i + 1].registros) >= t:
            succ = self._get_sucessor(i)
            self.registros[i] = succ
            self.children[i + 1].remove(succ.id, t)
        
        # Se ambos os filhos têm menos de t registros, fundir os filhos e remover o registro.
        else:
            if i < len(self.children) - 1:
                self._merge(i)
                self.children[i].remove(registro.id, t)
            else:
                self._merge(i - 1)
                self.children[i - 1].remove(registro.id, t)

    def _get_predecessor(self, i):
        """
        Obtém o predecessor de um registro no índice i.
        """
        current = self.children[i]
        while not current.leaf:
            current = current.children[-1]
        return current.registros[-1]

    def _get_sucessor(self, i):
        """
        Obtém o sucessor de um registro no índice i.
        """
        current = self.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.registros[0]

    def _merge(self, i):
        """
        Funde dois filhos e um registro do nó pai.
        """
        child = self.children[i]
        sibling = self.children[i + 1]

        # Puxar o registro do meio do pai para o filho
        child.registros.append(self.registros[i])

        # Adicionar os registros do irmão ao filho
        child.registros.extend(sibling.registros)

        # Adicionar os filhos do irmão ao filho (se houver)
        if not child.leaf:
            child.children.extend(sibling.children)

        # Remover o registro do meio do pai e o ponteiro do irmão
        self.registros.pop(i)
        self.children.pop(i + 1)

    def print_table(self, level=0, indent=""):
        """
        Exibe a tabela de registros.
        """
        if level == 0:
            print(f"{'ID':<10} {'Nome':<20} {'Idade':<5}")
            print("=" * 35)
        for registro in self.registros:
            print(str(registro))  # Exibe cada registro
        for i, child in enumerate(self.children):
            child.print_table(level + 1, indent + "    ")  # Exibe registros dos filhos

    def to_dict(self):
        """
        Converte o nó para um dicionário.
        """
        return {
            "registros": [registro.to_dict() for registro in self.registros],
            "children": [child.to_dict() for child in self.children] if not self.leaf else [],
            "leaf": self.leaf  # Indica se o nó é folha
        }

    @staticmethod
    def from_dict(data, t):
        """
        Cria um nó a partir de um dicionário.
        """
        node = BTreeNode(t)
        node.registros = [Registro.from_dict(registro) for registro in data["registros"]]
        node.leaf = data["leaf"]  # Define se é folha
        if not node.leaf:
            node.children = [BTreeNode.from_dict(child, t) for child in data["children"]]
        return node

class BTree:
    """
    Representa a árvore B em si.
    """
    def __init__(self, t):
        self.root = BTreeNode(t)  # Cria a raiz da árvore
        self.t = t  # Grau mínimo da árvore

    def insert(self, id, nome, idade):
        """
        Insere um novo registro na árvore.
        """
        if self.search(id) is not None:
            print(f"Erro: Já existe um registro com o ID {id}.")
            return

        registro = Registro(id, nome, idade)
        root = self.root
        if len(root.registros) == 2 * self.t - 1:  # Verifica se a raiz está cheia
            temp = BTreeNode(self.t)
            temp.children.insert(0, root)
            temp.leaf = False
            temp.split_child(0)  # Divide a raiz
            i = 0
            if temp.registros[0] < registro:
                i += 1
            temp.children[i].insert_non_full(registro)  # Insere no filho apropriado
            self.root = temp
        else:
            root.insert_non_full(registro)  # Insere diretamente na raiz

        self.save_to_file()  # Salva a árvore após a inserção

    def search(self, id):
        """
        Busca um registro na árvore.
        """
        return self.root.search(id)  # Busca a partir da raiz

    def update(self, id, nome, idade):
        """
        Atualiza um registro na árvore.
        """
        if self.root.update(id, nome, idade):  # Atualiza a partir da raiz
            self.save_to_file()  # Salva a árvore após a atualização
        else:
            print(f"Erro: Registro com ID {id} não encontrado.")

    def remove(self, id):
        """
        Remove um registro da árvore.
        """
        if self.root:
            original_size = len(self.root.registros)
            self.root.remove(id, self.t)
            if len(self.root.registros) < original_size:
                self.save_to_file()  # Salva a árvore após a remoção
            else:
                print(f"Erro: Registro com ID {id} não encontrado.")
            
            if len(self.root.registros) == 0:  # Verifica se a raiz está vazia
                if not self.root.leaf:
                    self.root = self.root.children[0]  # A raiz se torna o filho
                else:
                    self.root = None  # A árvore fica vazia
        else:
            print(f"Erro: Registro com ID {id} não encontrado.")

    def print_table(self):
        """
        Exibe todos os registros da árvore.
        """
        if self.root:
            self.root.print_table()  # Exibe registros a partir da raiz
        else:
            print("A tabela está vazia.")

    def save_to_file(self, filename="btree_data.json"):
        """
        Salva a árvore em um arquivo JSON.
        """
        with open(filename, 'w') as file:
            json.dump(self.root.to_dict(), file, indent=4)  # Serializa a árvore

    def load_from_file(self, filename="btree_data.json"):
        """
        Carrega a árvore de um arquivo JSON.
        """
        try:
            with open(filename, 'r') as file:
                data = json.load(file)  # Desserializa a árvore
                self.root = BTreeNode.from_dict(data, self.t)
        except FileNotFoundError:
            print("Arquivo de dados não encontrado.")  # Mensagem se o arquivo não existir
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo de dados. Iniciando com uma árvore vazia.")
            self.root = BTreeNode(self.t)  # Inicializa com uma árvore vazia
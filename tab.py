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
            self.registros.append(None)  # Cria espaço para novo registro
            while i >= 0 and registro < self.registros[i]:
                self.registros[i + 1] = self.registros[i]  # Desloca registros para inserir novo
                i -= 1
            self.registros[i + 1] = registro  # Insere novo registro na posição correta
        else:
            while i >= 0 and registro.id < self.registros[i].id:
                i -= 1
            i += 1
            if len(self.children[i].registros) == 1:  # Verifica se filho está cheio
                self.split_child(i)
                if registro.id > self.registros[i].id:
                    i += 1
            self.children[i].insert_non_full(registro)  # Insere no filho adequado

    def split_child(self, i):
        """
        Divide um filho cheio em dois.
        """
        y = self.children[i]
        z = BTreeNode(y.t)
        z.leaf = y.leaf
        self.children.insert(i + 1, z)  # Adiciona novo nó filho
        self.registros.insert(i, y.registros[0])  # Move registro do meio para o nó pai
        if not y.leaf:
            z.children = y.children[1:]  # Atribui filhos ao novo nó
            y.children = y.children[:1]  # Mantém um filho no nó original
        y.registros = [y.registros[0]]  # Mantém um registro no nó original

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
            return  # Não faz nada se não encontrado
        else:
            if len(self.children[i].registros) < t:
                self._fill(i, t)  # Garante que filho tenha registros suficientes
            if i > len(self.registros):
                self.children[i - 1].remove(id, t)  # Continua remoção no filho à esquerda
            else:
                self.children[i].remove(id, t)  # Continua remoção no filho à direita

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
        registro = Registro(id, nome, idade)
        root = self.root
        if len(root.registros) == 1:  # Verifica se a raiz está cheia
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

    def search(self, id):
        """
        Busca um registro na árvore.
        """
        return self.root.search(id)  # Busca a partir da raiz

    def update(self, id, nome, idade):
        """
        Atualiza um registro na árvore.
        """
        return self.root.update(id, nome, idade)  # Atualiza a partir da raiz

    def remove(self, id):
        """
        Remove um registro da árvore.
        """
        self.root.remove(id, self.t)
        if len(self.root.registros) == 0:  # Verifica se a raiz está vazia
            if not self.root.leaf:
                self.root = self.root.children[0]  # A raiz se torna o filho
            else:
                self.root = None  # A árvore fica vazia

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
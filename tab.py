import json

class Registro:
    def __init__(self, id, nome, idade):
        self.id = id
        self.nome = nome
        self.idade = idade

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.id:<10} {self.nome:<20} {self.idade:<5}"

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "idade": self.idade}

    @staticmethod
    def from_dict(data):
        return Registro(data['id'], data['nome'], data['idade'])

class BTreeNode:
    def __init__(self, t):
        self.t = t  # Grau mínimo da árvore B (t)
        self.registros = []  # Lista de registros
        self.children = []  # Lista de filhos
        self.leaf = True  # Verifica se é folha (nó folha)

    def insert_non_full(self, registro):
        i = len(self.registros) - 1
        
        if self.leaf:
            self.registros.append(None)  # Adiciona espaço para o novo registro
            while i >= 0 and registro < self.registros[i]:
                self.registros[i + 1] = self.registros[i]
                i -= 1
            self.registros[i + 1] = registro
        else:
            while i >= 0 and registro.id < self.registros[i].id:
                i -= 1
            i += 1
            if len(self.children[i].registros) == 1:  # Verifica se o nó filho está cheio
                self.split_child(i)
                if registro.id > self.registros[i].id:
                    i += 1
            self.children[i].insert_non_full(registro)

    def split_child(self, i):
        y = self.children[i]
        z = BTreeNode(y.t)
        z.leaf = y.leaf
        self.children.insert(i + 1, z)
        self.registros.insert(i, y.registros[0])  # Move o registro do meio para o nó pai
        if not y.leaf:
            z.children = y.children[1:]
            y.children = y.children[:1]
        y.registros = [y.registros[0]]

    def search(self, id):
        i = 0
        while i < len(self.registros) and id > self.registros[i].id:
            i += 1
        if i < len(self.registros) and id == self.registros[i].id:
            return self.registros[i]
        elif self.leaf:
            return None
        else:
            return self.children[i].search(id)

    def update(self, id, nome, idade):
        i = 0
        while i < len(self.registros) and id > self.registros[i].id:
            i += 1
        
        if i < len(self.registros) and id == self.registros[i].id:
            self.registros[i].nome = nome
            self.registros[i].idade = idade
            return True
        
        if self.leaf:
            return False
        else:
            return self.children[i].update(id, nome, idade)

    def remove(self, id, t):
        i = 0
        while i < len(self.registros) and id > self.registros[i].id:
            i += 1
        
        if i < len(self.registros) and id == self.registros[i].id:
            if self.leaf:
                self.registros.pop(i)
            else:
                self._remove_internal_node(i, t)
        elif self.leaf:
            return
        else:
            if len(self.children[i].registros) < t:
                self._fill(i, t)
            if i > len(self.registros):
                self.children[i - 1].remove(id, t)
            else:
                self.children[i].remove(id, t)

    def print_table(self, level=0, indent=""):
        if level == 0:
            print(f"{'ID':<10} {'Nome':<20} {'Idade':<5}")
            print("=" * 35)
        for registro in self.registros:
            print(str(registro))
        for i, child in enumerate(self.children):
            child.print_table(level + 1, indent + "    ")

    def to_dict(self):
        return {
            "registros": [registro.to_dict() for registro in self.registros],
            "children": [child.to_dict() for child in self.children] if not self.leaf else [],
            "leaf": self.leaf
        }

    @staticmethod
    def from_dict(data, t):
        node = BTreeNode(t)
        node.registros = [Registro.from_dict(registro) for registro in data["registros"]]
        node.leaf = data["leaf"]
        if not node.leaf:
            node.children = [BTreeNode.from_dict(child, t) for child in data["children"]]
        return node

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t)
        self.t = t

    def insert(self, id, nome, idade):
        registro = Registro(id, nome, idade)
        root = self.root
        if len(root.registros) == 1:  # Modificado para manter um valor por nó
            temp = BTreeNode(self.t)
            temp.children.insert(0, root)
            temp.leaf = False
            temp.split_child(0)
            i = 0
            if temp.registros[0] < registro:
                i += 1
            temp.children[i].insert_non_full(registro)
            self.root = temp
        else:
            root.insert_non_full(registro)

    def search(self, id):
        return self.root.search(id)

    def update(self, id, nome, idade):
        return self.root.update(id, nome, idade)

    def remove(self, id):
        self.root.remove(id, self.t)
        if len(self.root.registros) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = None

    def print_table(self):
        if self.root:
            self.root.print_table()
        else:
            print("A tabela está vazia.")

    def save_to_file(self, filename="btree_data.json"):
        with open(filename, 'w') as file:
            json.dump(self.root.to_dict(), file, indent=4)

    def load_from_file(self, filename="btree_data.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.root = BTreeNode.from_dict(data, self.t)
        except FileNotFoundError:
            print("Arquivo de dados não encontrado. Iniciando com uma árvore vazia.")
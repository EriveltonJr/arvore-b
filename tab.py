class BTreeNode:
    def __init__(self, t):
        self.t = t  # Mínimo grau (defines the range for number of keys)
        self.keys = []
        self.children = []
        self.leaf = True

    def split_child(self, i, y):
        t = self.t
        z = BTreeNode(y.t)
        z.leaf = y.leaf
        z.keys = y.keys[t:]
        y.keys = y.keys[:t]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys.pop(-1))

    def insert_non_full(self, k):
        if self.leaf:
            self.keys.append(k)
            self.keys.sort()
        else:
            if k in self.keys:
                return
            i = len(self.keys) - 1
            while i >= 0 and k < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i, self.children[i])
                if k > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(k)

    def delete(self, k):
        if k in self.keys:
            self.keys.remove(k)
            return True
        if self.leaf:
            return False
        i = 0
        while i < len(self.keys) and k > self.keys[i]:
            i += 1
        if i < len(self.children):
            return self.children[i].delete(k)
        return False

    def find(self, k):
        if k in self.keys:
            return True
        if self.leaf:
            return False
        i = 0
        while i < len(self.keys) and k > self.keys[i]:
            i += 1
        return self.children[i].find(k)

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t)
        self.t = t

    def insert(self, k):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t)
            s.children.append(root)
            s.leaf = False
            s.split_child(0, root)
            self.root = s
            s.insert_non_full(k)
        else:
            root.insert_non_full(k)

    def delete(self, k):
        if self.root:
            return self.root.delete(k)
        return False

    def find(self, k):
        if self.root:
            return self.root.find(k)
        return False

    def update(self, old_k, new_k):
        if self.delete(old_k):
            self.insert(new_k)
            print(f"Chave {old_k} atualizada para {new_k}.")
        else:
            print(f"Chave {old_k} não encontrada para atualização.")

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("Level", level, " ", len(node.keys), ":", node.keys)
        level += 1
        if len(node.children) > 0:
            for child in node.children:
                self.print_tree(child, level)

class ItemSetTree:
    def __init__(self, list):
        self.itemset_list = list
        self.root = ItemSetNode(None, 0)
        if len(list) > 0:
            self.height = len(list[0])
            self.build()

    def build(self):
        for itemset in self.itemset_list:
            parent = self.root
            level = 1
            for item in itemset:
                if item not in parent.children:
                    isn = ItemSetNode(item, level)
                    parent.children[item] = isn
                level += 1

                parent = parent.children[item]

    def find(self, hash):
        found = []
        self.find_itemsets(self.root, hash, [], found)
        return found

    def find_itemsets(self, node, hash, l, found):
        for child in node.children:
            if child in hash:
                l.append(child)
                self.find_itemsets(node.children[child], hash, l, found)
                l.pop()
        # this is a leaf
        if not bool(node.children):
            found.append(l[:])

    def print_tree(self, node='root', level=0):
        if node == 'root':
            node = self.root
        print("{}{}".format("\t"*level,node.item))
        if len(node.children) > 0:
            for child in node.children:
                self.print_tree(node.children[child], level+1)

class ItemSetNode:
    def __init__(self, item, level):
        self.item = item
        self.children = {}
        self.level = level
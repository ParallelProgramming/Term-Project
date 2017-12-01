"""
--------------------------------------------------------------------------------
utils/itemset.py
Defines the ItemSet, ItemSetTree and ItemSetNode classes
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

class ItemSet:
    """Represents an itemset candidate

        Attributes:
            key         string representation of the itemset. e.g ['a','b']
            list        the itemset in list representation
            count       number of occurrences of the candidates
            support     count divided by number of transaction in dataset

        """
    def __init__(self, list, count=1):
        self.key = str(list)
        self.list = list
        self.count = count
        self.support = None

class ItemSetTree:
    """Represents a collection of ItemSet in a tree form

        Attributes:
        root        root node of the tree (ItemSetNode)
        step        the iteration step the tree corresponds to
    """

    def __init__(self, list):
        '''Build the tree from an itemset list'''
        self.itemset_list = list
        self.root = ItemSetNode(None, 0)
        self.step = 0
        if len(list) > 0:
            self.step = len(list[0])
            self.__build()

    def __build(self):
        '''Constructes the tree'''

        # for every item set
        for itemset in self.itemset_list:
            # start from the root
            parent = self.root
            level = 1
            # insert each item in the itemset into the tree as a ItemSetNode child node of it's predecessor
            # e.g. ['a', 'b'] will be inserted as root->a->b
            for item in itemset:
                # if a node for the item doesn't exists - create a new one
                if item not in parent.children:
                    isn = ItemSetNode(item, level)
                    parent.children[item] = isn
                level += 1

                parent = parent.children[item]

    def find(self, transaction):
        """
        ----------------------------------------------------------------------------
        Retrieves all itemsets which exists a given transaction
        ---------------------------------------------------------------------------
        Preconditions:
            transaction - a single transaction in a dict form
        Postconditions:
            returns a list of itemset keys which occur in the transaction
        ----------------------------------------------------------------------------
        """
        found = []
        self.__find_itemsets(self.root, transaction, [], found)
        return found

    def __find_itemsets(self, node, transaction, l, found):
        """Collects all itemsets in a transaction recursively and stores them in 'found' argument"""

        # for all the current nodes children
        for child in node.children:
            # if the child is in the transaction - explore it's children
            if child in transaction:
                # collect the itemsets element in 'l'
                l.append(child)
                self.__find_itemsets(node.children[child], transaction, l, found)
                l.pop()

        # append the itemset when we reach a leaf
        if not bool(node.children):
            found.append(l[:])

    def print_tree(self, node='root', level=0):
        '''prints the tree for debug purposes'''
        if node == 'root':
            node = self.root
        print("{}{}".format("\t"*level,node.item))
        if len(node.children) > 0:
            for child in node.children:
                self.print_tree(node.children[child], level+1)

class ItemSetNode:
    """Represents a node of ItemSetTree

     Attributes:
        item        the element the node represents (string)
        children    a dict of child nodes
        level       the nodes level in the tree
    """

    def __init__(self, item, level):
        self.item = item
        self.children = {}
        self.level = level


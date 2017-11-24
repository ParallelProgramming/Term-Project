from itertools import combinations

class AssociationRule:
    def __init__(self, union, x, y, n):
        self.x = x
        self.y = y
        self.union = union
        self.support = union.support/n
        self.confidence = union.support/x.support
        self.lift = (union.support*n)/(x.support*y.support)
        self.key = "{}->{}".format(x.key, y.key)
        
    def __str__(self):
        output = "{0},support={1:.2f},confidence={2:.2f},lift={3:.2f}".format(self.key ,self.support,
                                                                    self.confidence,self.lift)
        return output

class RuleGenerator:
    def __init__(self, level_itemsets, n):
        self.level_itemsets = level_itemsets
        self.n = n

    def generate_rules(self, min_confidence):
        rules = {}
        for k in range(1, len(self.level_itemsets)):
            for iset in self.level_itemsets[k].values():
                union = set(iset.list)
                for i in range(len(union) - 1):
                    subsets = combinations(union, i + 1)
                    for x in subsets:
                        y = union - set(x)
                        x = sorted(list(x))
                        y = sorted(list(y))
                        ar = AssociationRule(iset, self.level_itemsets[i][str(x)],
                                              self.level_itemsets[k - i - 1][str(y)], self.n)
                        if ar.confidence > min_confidence and ar.key not in rules:
                            rules[ar.key] = ar

        for ar in rules.values():
            print(ar)
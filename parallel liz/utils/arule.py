"""
--------------------------------------------------------------------------------
utils/arule.py
Defines the AssociationRule and RuleGenerator classes
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import logging
from itertools import combinations

class AssociationRule:
    """Represents an association rule where lhs -> rhs

    Attributes:
        lhs         Left hand side itemset
        rhs         Right hand side itemset
        union       (lhs U rhs) itemset
        support     support value of the union - count(union)/number of transactions
        confidence  confidence value of the rule - count(union)/count(lhs)
        lift        lift value of the rule - support(union)/support(lhs)*support(rhs)
        key         string representation of the rule - lhs -> rhs
    """
    def __init__(self, union, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.union = union
        self.support = union.support
        self.confidence = union.count/lhs.count
        self.lift = union.support/(lhs.support*rhs.support)
        self.key = "{}->{}".format(lhs.key, rhs.key)
        
    def __str__(self):
        output = "{0},support={1:.3f},confidence={2:.3f},lift={3:.3f}".format(
            self.key, self.support, self.confidence, self.lift)
        return output

class RuleGenerator:
    """Rule generator class"""
    def __init__(self, level_itemsets):
        self.level_itemsets = level_itemsets

    def generate_rules(self, min_confidence):
        """
        ----------------------------------------------------------------------------
        Generates the association rules based on frequent itemsets and prints them
        ---------------------------------------------------------------------------
        Preconditions:
            min_confidence - min confidence value required to accept a rule
        ----------------------------------------------------------------------------
        """
        rules = {}
        # for each level of itemsets
        for k in range(1, len(self.level_itemsets)):
            # for all frequent itemsets in the level
            for iset in self.level_itemsets[k].values():
                union = set(iset.list)
                # create subsets of all size smaller than the itemset length
                for i in range(len(union) - 1):
                    subsets = combinations(union, i + 1)
                    # for each subset - find the "complementary" itemset and create an association rule
                    for x in subsets:
                        y = union - set(x)
                        x = sorted(list(x))
                        y = sorted(list(y))
                        ar = AssociationRule(iset,
                                             self.level_itemsets[i][str(x)],
                                             self.level_itemsets[k - i - 1][str(y)])
                        # if the rule's confidence is higher than the minimum and we haven't collected it yet
                        if ar.confidence > min_confidence and ar.key not in rules:
                            # store the rule
                            rules[ar.key] = ar

        # print out all the rules found
        logging.info("Found {} rules.".format(len(rules)))
        for ar in rules.values():
            logging.info(ar)
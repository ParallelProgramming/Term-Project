"""
--------------------------------------------------------------------------------
utils/candidates.py
Provides helper methods to handle itemset candidates
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import logging
from itertools import combinations
from utils.itemset import ItemSet

def generate_next_level_candidates(candidates, step):
    """
    ----------------------------------------------------------------------------
    calculates next level candidates from the current level frequent itemsets
    ---------------------------------------------------------------------------
    Preconditions:
        candidates - dict of candidate keys to itemsets objects
        step - current step (int)
    Postconditions:
        returns a list of set objects representing the next level candidates
    ----------------------------------------------------------------------------
    """
    next_level_candidates = []

    # extract all distinct items from the current level candidates
    items = set()
    for c in candidates:
        items |= set(candidates[c].list)

    # generate all combinations of items of size=step + 1
    combos = combinations(sorted(list(items)), step + 1)

    # for the step 1 accept combinations
    if step == 1:
        for combo in combos:
            next_level_candidates.append(combo)
    # for any other step
    else:
        # accept a combination only if all of its subsets of size=step are supported candidates
        for combo in combos:
            relevent = True
            for i in range(step + 1):
                subset = list(combo[0:i]) + list(combo[i + 1:step + 1])
                if str(subset) not in candidates:
                    relevent = False
                    break
            if relevent:
                next_level_candidates.append(combo)

    logging.debug("Created {} potential candidates for step {}".format(len(next_level_candidates), step + 1))
    return next_level_candidates

def filter_candidates(candidates, min_support, n):
    """
    ----------------------------------------------------------------------------
    Filters candidates with support lower than the min support
    ---------------------------------------------------------------------------
    Preconditions:
        min_support - percentage of all transactions
        n - total number of transactions
    Postconditions:
        return a dictionary of candidates to itemset objects containing the count
    ----------------------------------------------------------------------------
    """
    filtered = {}
    min_support_count = min_support * n
    for c in candidates:
        # filter out candidates with lower count than the minimun
        if candidates[c].count >= min_support_count:
            filtered[c] = candidates[c]
            # calculate the support value of the itemset
            candidates[c].support = candidates[c].count/n

    return filtered

def initialize_candidates(transactions):
    """
    ----------------------------------------------------------------------------
    Creates the first step candidates - counts all distinct items in a transactions list
    ---------------------------------------------------------------------------
    Preconditions:
        transactions - a list of transactions (in the form of dicts)
    Postconditions:
        return a dictionary of itemset objects containing the count
    ----------------------------------------------------------------------------
    """
    candidates = {}
    for t in transactions:
        for i in t:
            # create a new itemset object if we encounter a new item, otherwise increase the count
            key = str([i])
            if key not in candidates:
                candidates[key] = ItemSet([i])
            else:
                candidates[key].count += 1
    return candidates

def count_candidates(transactions, candidates_tree):
    """
    ----------------------------------------------------------------------------
    Counts the appearance of the candidates in the given transactions,
    removes irrelevant transaction records
    ---------------------------------------------------------------------------
    Preconditions:
        transactions - a list of transactions (in the form of dicts)
        candidates_tree - an ItemsetTree object, expected to be None for step 1
    Postconditions:
        return a dictionary of itemset objects containing the count
    ----------------------------------------------------------------------------
    """
    step = candidates_tree.step if candidates_tree else 1
    candidates = {}
    obsolete = []
    # in first iteration all items are considered candidates
    if step == 1:
        candidates = initialize_candidates(transactions)
    else:
        for i in range(len(transactions)):
            t = transactions[i]

            # using the candidate tree to find candidates in the transaction
            found = candidates_tree.find(t)

            # update the count
            for c in found:
                if str(c) not in candidates:
                    candidates[str(c)] = ItemSet(c)
                else:
                    candidates[str(c)].count += 1

            # candidates of size k+1 have k+1 candidates of size k, transactions with less than k+1 candidates -
            # will not contribute in future steps, therefore can be removed
            if len(found) <= step:
                obsolete.append(i)

    # delete transactions from bottom to top to keep the indexes correct
    obsolete.reverse()
    for i in obsolete:
        del transactions[i]

    return candidates

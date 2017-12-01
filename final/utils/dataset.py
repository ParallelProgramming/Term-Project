"""
--------------------------------------------------------------------------------
utils/dataset.py
Provides helper methods to work with the dataset
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import os

def load_dataset(dataset):
    """
    ----------------------------------------------------------------------------
    Loads transaction from a dataset file
    ---------------------------------------------------------------------------
    Preconditions:
        dataset - relative path to the dataset file
    Postconditions:
        returns a list of transactions represented by dicts
    ----------------------------------------------------------------------------
    """
    transactions = []
    with open(dataset) as f:
        line = f.readline()

        # read all dataset file
        while line:
            t = {}

            # for all items in each transactions
            for item in line.split():
                # store in dict with value true
                t[item] = True

            transactions.append(t)
            line = f.readline()
    return transactions

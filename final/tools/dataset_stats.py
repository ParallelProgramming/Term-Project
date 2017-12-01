"""
--------------------------------------------------------------------------------
tools/dataset_stats.py
Reports the number of transactions, number of unique items and density ratio of
a given dataset
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import sys
def stats(dataset):
    transactions_count = 0
    items_count = 0
    unique_items = set()
    with open(dataset) as f:
        line = f.readline()
        # read all dataset file
        while line:
            t = {}
            transactions_count += 1
            # for all items in each transactions
            for item in line.split():
                items_count += 1
                unique_items.add(item)


            line = f.readline()
    print("Number of transactions: ", transactions_count)
    print("Number of unique items: ", len(unique_items))
    print("Number of all items: ", items_count)
    print("Density: {:.4f}%".format(100*items_count/(transactions_count*len(unique_items)) ))

if __name__ == "__main__":
    stats(sys.argv[1])

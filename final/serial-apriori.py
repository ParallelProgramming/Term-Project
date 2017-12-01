"""
--------------------------------------------------------------------------------
serial-apriori.py
A parallel apriori algorithm implementation in python for CP431/CP631 term project
The program finds and prints out the association rules in a given dataset. It takes the min support
and min confidence values as parameters
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""


import os
import argparse
import datetime
import logging

from utils.itemset import ItemSet, ItemSetTree
from utils.dataset import load_dataset
from utils.arule import RuleGenerator
from utils.candidates import *

def main():
    parser = argparse.ArgumentParser(description='Find association rules in a dataset')
    parser.add_argument('-d', '--dataset', help='dataset file', default='ds1.txt')
    parser.add_argument('-s', '--support', type=float, help='minimum support for frequent item sets', default='0.01')
    parser.add_argument('-c', '--confidence', type=float, help='minimum confidence for association rules', default='0.6')
    parser.add_argument('-v', '--verbose', action='store_true', help='include verbose output', default=False)
    args = parser.parse_args()

    # set logging level
    FORMAT = '%(asctime)-15s: %(message)s'
    if args.verbose:
        logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    else:
        logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

    logging.info("Running apriori with support {}% and confidence {}%".format(args.support * 100, args.confidence * 100))

    # load dataset
    transactions = load_dataset(os.path.join('datasets', args.dataset))
    dataset_size = len(transactions)

    step = 0
    level_itemsets = []
    itemset_tree = None
    next_candidates = []

    # benchmark run time
    start_t = datetime.datetime.now()

    # while next level has candidates or step 0
    while (len(next_candidates) > 0 or step == 0):
        step += 1
        logging.debug("step {}: starting".format(step))

        # count the candidate
        candidates = count_candidates(transactions, itemset_tree)
        logging.debug("step {}: counted candidates supports".format(step))

        # filter candidates
        filtered = filter_candidates(candidates, args.support, dataset_size)
        logging.debug("step {}: filtered candidates".format(step))

        # store the current levels frequent itemsets
        level_itemsets.append(filtered)

        # generate next level candidate
        next_candidates = generate_next_level_candidates(level_itemsets[step - 1], step)
        logging.debug("step {}: generated next step candidates".format(step))

        # build the candidate tree
        itemset_tree = ItemSetTree(next_candidates)
        logging.debug("step {}: created tree".format(step))

    logging.debug("Found {} levels.".format(len(level_itemsets)))
    for i in range(len(level_itemsets)):
        logging.debug("Level {}  - {} frequent itemsets".format(i+1, len(level_itemsets[i])))
    for i in range(len(level_itemsets)):
        logging.debug("Level {}: {}".format(i+1, " ".join(x for x in level_itemsets[i])))

    # Generate and print rules
    RuleGenerator(level_itemsets).generate_rules(args.confidence)

    end_t = datetime.datetime.now()
    logging.info("Serial apriori took {}".format(end_t - start_t))

if __name__ == "__main__":
    main()
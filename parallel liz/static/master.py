"""
--------------------------------------------------------------------------------
static/master.py
Defines the Master class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import os
import math
import logging
from itertools import combinations

from static.node import Node
from utils.itemset import ItemSetTree
from utils.candidates import *

from mpi4py import MPI

class Master(Node):
    '''Extends Node to provide a Slave node behaviour'''
    def __init__(self, comm, dataset, min_support):
        Node.__init__(self, comm, dataset)
        self.min_support = min_support
        self.next_transactions = []
        self.candidates_tree = ItemSetTree([])
        self.level_itemsets =[]

    def execute(self):
        finished = 0

        # while not all processes have finished counting
        while finished < self.p_size - 1:
            # wait for count results from any process
            candidate_counts = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
            # add the received results to the masters candidates
            self.__add_counts(candidate_counts)
            finished += 1

        # filter candidates
        filtered = filter_candidates(self.candidates, self.min_support, self.dataset_size)

        # store the current levels frequent itemsets
        self.level_itemsets.append(filtered)

        # generate next level candidate
        next_level_candidates = generate_next_level_candidates(filtered, self.step)
        next = len(next_level_candidates) > 0

        # if the are candidates for the next level
        if next:
            logging.debug("next level candidates: ({})".format(len(next_level_candidates)))
            logging.debug(','.join(str(c) for c in next_level_candidates))

            # build the candidate tree
            self.canidates_tree = ItemSetTree(next_level_candidates)

            logging.debug("broadcasting item set tree")
            self.comm.bcast(self.canidates_tree, root=0)
        # else broadcase None - as an END signal
        else:
            logging.debug("broadcasting END")
            self.comm.bcast(None, root=0)
        return next

    def __add_counts(self, supports):
        '''add the received counts'''
        for c in supports:
            if c in self.candidates:
                self.candidates[c].count += supports[c].count
            else:
                self.candidates[c] = supports[c]

    def print_supports(self):
        '''prints out the frequent itemsets in all levels with their supports and counts'''
        logging.info("Found {} levels.".format(len(self.level_itemsets)))
        for i in range(len(self.level_itemsets)):
            logging.info("Level {}  - {} frequent itemsets".format(i + 1, len(self.level_itemsets[i])))


        for i in range(len(self.level_itemsets)):
            logging.debug("level: {}".format(i + 1))
            logging.debug(', '.join("({}:{}({:.3f}))".format(c.key, c.count, c.support) for c in self.level_itemsets[i].values()))
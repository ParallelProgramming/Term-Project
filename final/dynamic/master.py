"""
--------------------------------------------------------------------------------
dynamic/master.py
Defines the Master class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import os
import math
import logging
from mpi4py import MPI

from dynamic.node import Node, Tags
from dynamic.count_task import CountTask
from utils.itemset import ItemSetTree
from utils.dataset import load_dataset
from utils.candidates import *

class Master(Node):
    '''Extends Node to provide a Slave node behaviour'''
    def __init__(self, comm, dataset, min_support):
        Node.__init__(self, comm)
        self.dataset = dataset
        self.min_support = min_support

        # load dataset
        self.transactions = load_dataset(os.path.join('datasets', self.dataset))
        self.dataset_size = len(self.transactions)
        self.level_itemsets =[]

    def execute(self):
        self.next_transactions = []
        self.candidates = {}
        logging.debug("step: {}, transacion count: {}".format(self.step, len(self.transactions)))

        # assign counting tasks to slave and collect results
        self.__partiotion_transactions()
        self.transactions = self.next_transactions

        # filter candidates
        filtered = filter_candidates(self.candidates, self.min_support, self.dataset_size)

        # store the current levels frequent itemsets
        self.level_itemsets.append(filtered)

        # generate next level candidate
        next_level_candidates = generate_next_level_candidates(filtered, self.step)
        next = len(next_level_candidates) > 0
        if next:
            logging.debug("next level candidates: ({})".format(len(next_level_candidates)))
            logging.debug(','.join(str(c) for c in next_level_candidates))

            # build the candidate tree
            canidates_tree = ItemSetTree(next_level_candidates)

            logging.debug("broadcasting item set tree")
            self.comm.bcast(canidates_tree, root=0)
        # else broadcase None - as an END signal
        else:
            logging.debug("broadcasting END")
            self.comm.bcast(None, root=0)
        return next

    def __partiotion_transactions(self):
        # calculate partition size
        t_size = len(self.transactions)
        partition_size = math.ceil(math.log(t_size, 2))
        logging.debug("step {}: partition size {}".format(self.step, partition_size))

        finished = 0
        start = 0
        curr_partition = 0
        status = MPI.Status()

        # while not all slave have finished
        while finished < self.p_size - 1:
            # wait for task request
            task = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            m_from = status.Get_source();
            m_tag = status.Get_tag();

            if m_tag == Tags.JOB_REQ.value or m_tag == Tags.JOB_RESULT.value:
                # if there are still tasks to assign
                if start < t_size:
                    curr_partition += 1
                    partition = self.transactions[start:(start + partition_size)]
                    logging.debug("step {}: assignig partition {} starting at {} (length {}) to process {}".format(
                        self.step, curr_partition, start, len(partition), m_from
                    ))

                    # send task to slave
                    req = self.comm.isend(CountTask(curr_partition, partition), dest=m_from, tag=1)
                    start += partition_size
                else:
                    # send end tag and increase finished count
                    req = self.comm.isend(None, dest=m_from, tag=Tags.END.value)
                    finished += 1

                # if received results process them
                if m_tag == Tags.JOB_RESULT.value:
                    # store the returned "filtered" transactions
                    self.next_transactions += task.transactions
                    # add counts
                    self.__add_counts(task.candidate_counts)

                # wait for sending to finish
                req.wait()

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
            logging.debug(
                ', '.join("({}:{}({}))".format(c.key, c.count, c.support) for c in self.level_itemsets[i].values()))
"""
--------------------------------------------------------------------------------
static/node.py
Defines the Node abstract class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import os
from abc import ABCMeta, abstractmethod
from utils.dataset import load_dataset
from utils.candidates import initialize_candidates, count_candidates

class Node:
    '''Node is an abstract class which exposes the main execution method of all processors'''
    __metaclass__ = ABCMeta

    def __init__(self, comm, dataset):
        '''Initializes the node with a comm object and the dataset filename'''
        self.comm = comm
        self.rank = comm.Get_rank()
        self.p_size = comm.Get_size()
        self.dataset = dataset

        # load the transaction from the dataset
        self.transactions = load_dataset(os.path.join('datasets', self.dataset))
        self.dataset_size = len(self.transactions)

        # calculate the work range and keep only the transactions in the range
        self.t_size = len(self.transactions)//self.p_size
        if self.rank < (len(self.transactions) % self.p_size):
            self.t_start = self.rank * self.t_size + self.rank
        else:
            self.t_start = self.rank * self.t_size + (len(self.transactions) % self.p_size)
        self.transactions = self.transactions[self.t_start: self.t_start + self.t_size]

        # initialize attributes
        self.step = 0
        self.canidates = []
        self.canidates_tree = None

    def execute_step(self):
        # increase the steps count
        self.step += 1
        # count the candidates in the node's transactions
        self.candidates = count_candidates(self.transactions, self.canidates_tree)
        # preform additional computations according to the "true" type (Master or Slave)
        return self.execute()

    @abstractmethod
    def execute(self): pass
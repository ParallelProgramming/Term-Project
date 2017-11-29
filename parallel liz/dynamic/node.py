"""
--------------------------------------------------------------------------------
dynamic/node.py
Defines the Node abstract class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

from abc import ABCMeta, abstractmethod
from enum import Enum

class Tags(Enum):
    JOB_REQ = 0
    JOB_ASSIGN = 1
    JOB_RESULT = 2
    END = 100

class Node:
    '''Node is an abstract class which exposes the main execution method of all processors'''
    __metaclass__ = ABCMeta

    def __init__(self, comm):
        '''Initializes the node with a comm object'''
        self.comm = comm
        self.rank = comm.Get_rank()
        self.p_size = comm.Get_size()

        # initialize attributes
        self.step = 0
        self.canidates_tree = None

    def execute_step(self):
        # increase the steps count
        self.step += 1
        # preform additional computations according to the "true" type (Master or Slave)
        return self.execute()

    @abstractmethod
    def execute(self): pass
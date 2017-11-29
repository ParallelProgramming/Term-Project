"""
--------------------------------------------------------------------------------
static/slave.py
Defines the Slave class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

from static.node import Node

from mpi4py import MPI

class Slave(Node):
    '''Extends Node to provide a Slave node behaviour'''
    def __init__(self, comm, dataset):
        Node.__init__(self, comm, dataset)

    def execute(self):
        # send the counted candidates to the master node
        self.comm.send(self.candidates, dest=0, tag=0)

        # recieve a candidate tree from master
        self.canidates_tree = self.comm.bcast(None, root=0)

        # if the tree is None - there is no next step
        next = True if self.canidates_tree is not None else False
        return next


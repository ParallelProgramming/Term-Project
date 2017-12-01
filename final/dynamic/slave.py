"""
--------------------------------------------------------------------------------
dynamic/slave.py
Defines the Slave class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import logging
from dynamic.node import Node, Tags
from utils.candidates import initialize_candidates, count_candidates

from mpi4py import MPI

class Slave(Node):
    '''Extends Node to provide a Slave node behaviour'''
    def __init__(self, comm, dataset):
        Node.__init__(self, comm)

    def execute(self):
        task = None
        jobs = True
        status = MPI.Status()

        # while didn't receive end tag
        while jobs:
            # if no previous task exists
            if task is None:
                # request the first task
                self.comm.send(None, dest=0, tag=Tags.JOB_REQ.value)
                task = self.comm.recv(None, source=0, tag=MPI.ANY_TAG, status=status)
            # else send results of previous task
            else:
                self.comm.send(task, dest=0, tag=Tags.JOB_RESULT.value)
                # expect a new task assignment
                task = self.comm.recv(None, source=0, tag=MPI.ANY_TAG, status=status)

            m_tag = status.Get_tag()

            # if got a new task
            if m_tag == Tags.JOB_ASSIGN.value:
                # count candidates in the new task's transactions
                transactions = task.transactions
                task.candidate_counts = count_candidates(task.transactions, self.canidates_tree)
            elif m_tag == Tags.END.value:
                logging.debug("{}: got end tag in step {}".format(self.rank, self.step))
                jobs = False

        # recieve a candidate tree from master
        self.canidates_tree = self.comm.bcast(None, root=0)

        # if the tree is None - there is no next step
        next = True if self.canidates_tree is not None else False
        return next
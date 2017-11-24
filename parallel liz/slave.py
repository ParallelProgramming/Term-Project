from node import Node
from count_task import CountTask
from itemset import ItemSet
from itemset_tree import ItemSetTree
from mpi4py import MPI

class Slave(Node):
    def __init__(self, comm):
        Node.__init__(self, comm)
        self.canidates = []
        self.canidates_tree = ItemSetTree([])

    def execute(self):
        task = None
        jobs = True
        status = MPI.Status()
        while jobs:
            if task is None:
                self.comm.send(None, dest=0, tag=0)
                task = self.comm.recv(None, source=0, tag=MPI.ANY_TAG, status=status)
            else:
                self.comm.send(task, dest=0, tag=2)
                task = self.comm.recv(None, source=0, tag=MPI.ANY_TAG, status=status)
            m_tag = status.Get_tag()
            if m_tag == 1:
                transactions = task.transactions
                task.candidate_counts = self.count_support(task.transactions)
            elif m_tag == 100:
                print('got end tag')
                jobs = False

        self.itemset_tree = self.comm.bcast(None, root=0)
        next = True if self.itemset_tree is not None else False
        return next

    def count_support(self, transactions):
        candidates = {}
        obsolete = []
        if self.step == 1:
            candidates = self.initialize_candidate(transactions)
        else:
            for i in range(len(transactions)):
                t = transactions[i]
                found = self.itemset_tree.find(t)

                for c in found:
                    if str(c) not in candidates:
                        candidates[str(c)] = ItemSet(c)
                    else:
                        candidates[str(c)].support += 1

                if len(found) == 0:
                    obsolete.append(i)

        obsolete.reverse()
        # delete transactions
        for i in obsolete:
            del transactions[i]

        return candidates

    def initialize_candidate(self, transactions):
        candidates = {}
        for t in transactions:
            for i in t:
                key = str([i])
                if key not in candidates:
                    candidates[key] = ItemSet([i])
                else:
                    candidates[key].support += 1
        return candidates
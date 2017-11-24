from node import Node
from count_task import CountTask
from itemset import ItemSet
from itemset_tree import ItemSetTree
from itertools import combinations
import math
from mpi4py import MPI

class Master(Node):
    def __init__(self, comm, min_support, dataset):
        Node.__init__(self, comm)
        self.dataset = dataset
        self.min_support = min_support
        self.transactions = self.load_dataset()
        self.next_transactions = []
        self.n = len(self.transactions)
        self.min_support_count = self.n*self.min_support
        self.candidates_tree = ItemSetTree([])
        self.level_itemsets =[]

    def load_dataset(self):
        transactions = []
        with open(self.dataset) as f:
            line = f.readline()
            while line:
                t = {}
                for item in line.split():
                    t[item] = True
                transactions.append(t)
                line = f.readline()
        return transactions

    def execute(self):
        print('step:', self.step, 'transacion count:', len(self.transactions))
        self.candidates = {}
        self.partiotion_transactions()
        self.transactions = self.next_transactions
        self.next_transactions = []
        filtered = self.filter_candidates()
        self.level_itemsets.append(filtered)
        next_level_candidates = self.generate_next_level_candidates(filtered)
        next = len(next_level_candidates) > 0
        if next:
            #print("next level candidates: ({})".format(len(next_level_candidates)))
            #for c in next_level_candidates:
            #    print(c)
            itemset_tree = ItemSetTree(next_level_candidates)
            #itemset_tree.print_tree()
            self.remove_transactions()
            print('broadcasting item set tree')
            self.comm.bcast(itemset_tree, root=0)
        else:
            print('broadcasting END. step: ', self.step)
            self.comm.bcast(None, root=0)
        return next

    # tags: 0 - new partition request
    #       1 - partition assignment
    #       2 - partition count results
    #       100 - END - no more partitions to assign
    def partiotion_transactions(self):
        t_size = len(self.transactions)
        partition_size = math.ceil(math.log(t_size, 2))
        start = 0
        curr_partition = 0
        print("partition size ", partition_size)
        status = MPI.Status()
        finished = 0
        while finished < self.p_size - 1:
            task = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            m_from = status.Get_source();
            m_tag = status.Get_tag();

            if m_tag == 0 or m_tag ==2:
                if start < t_size:
                    curr_partition += 1
                    partition = self.transactions[start:(start + partition_size)]
                    #print('step', self.step, ' - assignig partition {} starting at {} length - {}'.format(curr_partition,
                    #                                                                                      start, len(partition)))
                    req = self.comm.isend(CountTask(curr_partition, partition), dest=m_from, tag=1)
                    start += partition_size
                else:
                    req = self.comm.isend(None, dest=m_from, tag=100)
                    finished += 1
                if m_tag == 2:
                    self.next_transactions += task.transactions
                    self.add_supports(task.candidate_counts)
                req.wait()

    def add_supports(self, supports):
        for c in supports:
            if c in self.candidates:
                self.candidates[c].support += supports[c].support
            else:
                self.candidates[c] = supports[c]

    def filter_candidates(self):
        # filtered = []
        # for c in self.candidates:
        #     if self.candidates[c].support >= self.min_support_count:
        #         filtered.append(self.candidates[c])
        # filtered.sort(key=lambda x: x.key)
        # return filtered
        filtered = {}
        for c in self.candidates:
            if self.candidates[c].support >= self.min_support_count:
                filtered[c] = self.candidates[c]
        return filtered

    def generate_next_level_candidates(self, candidates):
        next_level_candidates = []
        items = set()
        for c in candidates:
            #items |= set(c.list)
            items |= set(candidates[c].list)
        subsets = combinations(sorted(list(items)), self.step + 1)

        if self.step == 1:
            for subset in subsets:
                next_level_candidates.append(subset)
        # if all smaller are in candidates add
        else:
            #previous_level = dict((c.key,0) for c in candidates)
            for subset in subsets:
                relevent = True
                for i in range(self.step+1):
                    temp = list(subset[0:i])+list(subset[i+1:self.step+1])
                    #if str(temp) not in previous_level:
                    if str(temp) not in candidates:
                        #print ('discarding combination', subset, " - ", temp, "is not in previous step")
                        relevent = False
                        break
                if relevent:
                    #print('adding combination ', subset)
                    next_level_candidates.append(subset)
        return next_level_candidates

    def remove_transactions(self):
        pass

    def print_supports(self):
        for i in range(len(self.level_itemsets)):
            print("level: ", i + 1)
            print(', '.join("({}:{})".format(c.key, c.support) for c in self.level_itemsets[i].values()))



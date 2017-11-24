class Node:
    def __init__(self, comm):
        self.comm = comm
        self.rank = comm.Get_rank()
        self.p_size = comm.Get_size()
        self.step = 0

    def execute_step(self):
        self.step += 1
        return self.execute()
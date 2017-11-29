import argparse
from mpi4py import MPI
from master import Master
from slave import Slave
from arule import RuleGenerator

def main():
    parser = argparse.ArgumentParser(description='Find association rules in a dataset')
    parser.add_argument('-dataset', help='dataset file', default='ds3.txt')
    parser.add_argument('-support', type=float, help='minimum support for frequent item sets', default='0.01')
    parser.add_argument('-confidence', type=float, help='minimum confidence for association rules', default='0.6')

    args = parser.parse_args()

    # initialize mpi
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        node = Master(comm, args.support, args.dataset)
    else:
        node = Slave(comm)

    comm.Barrier()
    wt = MPI.Wtime()

    next_step = True
    while next_step:
       next_step = node.execute_step()

    if rank == 0:
        node.print_supports()
        #can be parallelized maybe
        RuleGenerator(node.level_itemsets, node.n).generate_rules(args.confidence)
        print("Total time to compute: {:2f} seconds".format(MPI.Wtime() - wt))

main()
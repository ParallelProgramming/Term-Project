"""
--------------------------------------------------------------------------------
parallel-apriori.py
A parallel apriori algorithm implementation in python for CP431/CP631 term project
The program finds and prints out the association rules in a given dataset. It takes the min support
and min confidence values as parameters
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import argparse
import importlib
import logging
from mpi4py import MPI

from utils.arule import RuleGenerator

def main():
    parser = argparse.ArgumentParser(description='Find association rules in a dataset')
    parser.add_argument('-d', '--dataset', help='dataset file', default='ds1.txt')
    parser.add_argument('-s', '--support', type=float, help='minimum support for frequent item sets', default='0.01')
    parser.add_argument('-c', '--confidence', type=float, help='minimum confidence for association rules', default='0.6')
    parser.add_argument('-m', '--mode', help='load balancing mode. May be static or dynamic', default='static')
    parser.add_argument('-v', '--verbose', action='store_true', help='include verbose output', default=False)

    args = parser.parse_args()

    # load the requested parallel version (static or dynamic)
    Master = getattr(importlib.import_module(args.mode + '.master'), 'Master')
    Slave = getattr(importlib.import_module(args.mode + '.slave'), 'Slave')

    # set logging level
    FORMAT = '%(asctime)-15s: %(message)s'
    if args.verbose:
        logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    else:
        logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

    # initialize mpi
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # assign nodes
    if rank == 0:
        node = Master(comm, args.dataset, args.support)
        logging.info("Running apriori with support {}% and confidence {}%".format(args.support * 100, args.confidence * 100))
        logging.info("Executing {} parallel version on {} processors".format(args.mode, node.p_size))
    else:
        node = Slave(comm, args.dataset)

    # benchmark run time
    comm.Barrier()
    wt = MPI.Wtime()

    # while there is a next step
    next_step = True
    while next_step:
        # exexute the step
        next_step = node.execute_step()

    if rank == 0:
        logging.debug("Total time to calc supports: {:2f} seconds".format(MPI.Wtime() - wt))
        node.print_supports()

        # Generate and print rules
        wt_rules = MPI.Wtime()
        RuleGenerator(node.level_itemsets).generate_rules(args.confidence)
        logging.debug("Total time to compute rules: {:2f} seconds".format(MPI.Wtime() - wt_rules))

        logging.info("Total time to compute: {:2f} seconds".format(MPI.Wtime() - wt))

if __name__ == "__main__":
    main()
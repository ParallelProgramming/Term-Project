"""
--------------------------------------------------------------------------------
dynamic/count_task.py
Defines the CountTask class
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

class CountTask:
    """Represents an counting task assigned by the Master node to Slave nodes

        Attributes:
            partition_id         the Id of the partition assigned
            transactions         a list of transaction to perform the count on, after count is done -
                                    irrelevent transactions are removed and returned to Maser via this attribute
            candidate_counts     the results of counting the candidates
        """
    def __init__(self, partition_id, transactions):
        self.partition_id = partition_id
        self.transactions = transactions
        self.candidate_counts = {}
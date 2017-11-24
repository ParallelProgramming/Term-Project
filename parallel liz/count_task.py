class CountTask:
    def __init__(self, partition_id, transactions):
        self.partition_id = partition_id
        self.transactions = transactions
        self.candidate_counts = {}
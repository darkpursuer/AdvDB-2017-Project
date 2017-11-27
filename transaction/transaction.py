class Transaction(object):
    """
    stands for a transaction
    """

    def __init__(self, tp, name):
        self.type = tp # NORMAL or READ means read-only.
        self.name = name # e.g. T1
        self.status = "RUNNING" # RUNNING, BLOCKED, COMMITED, ABORTED
        self.buffer = [] # pending operations

class Transaction(object):
    """
    stands for a transaction
    """

    def __init__(self, tp, name):
        self.type = tp # NORMAL or READ means read-only.
        self.name = name # e.g. T1
        self.status = "RUNNING" # RUNNING, BLOCKED, COMMITED, ABORTED
        self.buffer = [] # pending operations
        self.variables = dict() # read variables

    def set_status(self, status):
        if status in ("RUNNING", "BLOCKED", "COMMITED", "ABORTED"):
            self.status = status

    def get_status(self):
        return self.status

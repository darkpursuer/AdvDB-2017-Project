class Transaction(object):
    """
    stands for a transaction
    """

    def __init__(self, tp, name):
        """
        Create a transaction object.
        Author: Yi Zhang
        Date: 11/15/2017
        - Param:
        :tp (String): The type of the transaction: NORMAL or READ
        :name (String): The name of this transaction
        """
        self.type = tp # NORMAL or READ means read-only.
        self.name = name # e.g. T1
        self.status = "RUNNING" # RUNNING, BLOCKED, COMMITED, ABORTED
        self.buffer = [] # pending operations
        self.variables = dict() # read variables

    def set_status(self, status):
        """
        Set the status of this transaction.
        Author: Yi Zhang
        Date: 11/15/2017
        - Param:
        :status (String): The status that this transaction will be set
        """
        if status in ("RUNNING", "BLOCKED", "COMMITED", "ABORTED"):
            self.status = status

    def get_status(self):
        """
        Get the status of this transaction.
        Author: Yi Zhang
        Date: 11/15/2017
        - Return:
        The status of this transaction
        """
        return self.status

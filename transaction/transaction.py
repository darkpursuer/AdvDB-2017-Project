class Transaction(object):
    """
    Each transaction has a type and a name.
    type can be NORMAL or READ means read-only.
    NORMAL
    """

    def __init__(self, tp, name):
        self.TYPE = tp
        self.NAME = name

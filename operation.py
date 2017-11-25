class Operation(object):
    """Stands for an operation"""

    def __init__(self, op):
        self.OP = op


class OPBegin(Operation):
    """begin a transaction"""

    def __init__(self, op, name):
        super().__init__(op)
        self.NAME = name


class OPBeginRO(Operation):
    """begin a read-only transaction"""

    def __init__(self, op, name):
        super().__init__(op)
        self.NAME = name


class OPRead(Operation):
    """a read operation"""

    def __init__(self, op, t, x):
        super().__init__(op)
        self.T, self.X = t, x


class OPWrite(Operation):
    """a write operation"""

    def __init__(self, op, t, x, v):
        super().__init__(op)
        self.T, self.X, self.V = t, x, v


class OPDump(Operation):
    """dump data operation"""

    def __init__(self, op, site=-1, var=""):
        super().__init__(op)
        self.SITE, self.VAR = site, var


class OPEnd(Operation):
    """end a transaction"""

    def __init__(self, op, name):
        super().__init__(op)
        self.NAME = name


class OPFail(Operation):
    """fail a site"""

    def __init__(self, op, site):
        super().__init__(op)
        self.SITE = site


class OPRecover(Operation):
    """recover a failed site"""

    def __init__(self, op, site):
        super().__init__(op)
        self.SITE = site

class DatabaseManager(object):
    """DB manager is responsible for all transactions"""

    def __init__(self):
        # initialize 10 sites
        self.SITES = [Site() for i in range(10)]

    def receive(self, operations):

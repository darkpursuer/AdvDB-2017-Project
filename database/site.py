class Site(object):
    """An object represent a site"""

    def __init__(self):
        """
        index if the index of this site.
        """
        self.ON = True # online
        # create 20 slots
        # but some variables should not be store here
        self.VARS = [0 for i in range(20)]

    def get_var(self, index):
        return self.VARS[index - 1]

    def set_var(self, index):
        self.VARS[index - 1]

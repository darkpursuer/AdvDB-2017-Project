from copy import copy

class Server(object):
    """
    An object represent a server.
    """

    def __init__(self):
        # a flag to show if the Server
        # is alive or not
        self.alive = True
        # the current version number
        self.version = 0
        # the data values of
        # the current version
        # here I create 20 slots, but not all the vars should be
        # stored here
        self.variables = [0 for i in range(20)]
        # previous versions
        # (version_number -> variables)
        self.old = dict()

    def recover(self):
        self.alive = True

    def fail(self):
        self.alive = False

    def clean(self, version):
        """clean the data for an old version"""
        # only check the version in
        # old, do not delete the current version
        if version in self.old:
            del self.old[version]

    def write(self, variable, value, backup):
        if backup:
            self.old[self.version] = copy(self.variables)
        self.variables[variable-1] = value
        self.version += 1

    def read(self, variable, version=-1):
        if version == -1 or version == self.version:
            return self.variables[variable-1]
        else:
            return self.old[version][variable-1]

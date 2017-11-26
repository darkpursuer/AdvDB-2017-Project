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
        # a flag to indicate if server need to
        # store current data into old
        # this should be set to True when
        # a new read-only transaction occurs
        # and set back to false if some updates happen
        # to this server
        self.store_old = False

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

    def write(self, variable, value):
        if self.store_old:
            self.old[self.version] = copy(self.variables)
        self.variables[variable] = value
        self.version += 1

    def read(self, variable, version=-1):
        if version == -1:
            return self.variables[variable]
        else:
            return self.old[version][variable]

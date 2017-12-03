from copy import copy

class Server(object):
    """
    An object represent a server.
    """

    def __init__(self):
        """
        Create a server object.
        Author: Taikun Guo
        Date: 11/15/2017
        """
        # a flag to show if the Server
        # is alive or not
        self.alive = True
        # the current version number
        self.version = 0
        # the data values of
        # the current version
        # here I create 20 slots, but not all the vars should be
        # stored here
        self.variables = [10 * (i+1) for i in range(20)]
        # previous versions
        # (version_number -> variables)
        self.old = dict()

    def recover(self):
        """
        Recover this server.
        Author: Taikun Guo
        Date: 11/15/2017
        """
        self.alive = True

    def fail(self):
        """
        Fail this server.
        Author: Taikun Guo
        Date: 11/15/2017
        """
        self.alive = False

    def clean(self, version):
        """
        Clean the data for an old version.
        Author: Taikun Guo
        Date: 11/15/2017
        - Param:
        :version (String): The version of the backup needed to be cleaned
        """
        # only check the version in
        # old, do not delete the current version
        if version in self.old:
            del self.old[version]

    def write(self, variable, value, backup):
        """
        Write the new value to a variable.
        Author: Taikun Guo
        Date: 11/16/2017
        - Param:
        :variable (int): The variable index to be updated
        :value (int): The value to be updated
        :backup (boolean): Whether this server needs to backup the data
        """
        if backup:
            self.old[self.version] = copy(self.variables)
        self.variables[variable-1] = value
        self.version += 1

    def read(self, variable, version=-1):
        """
        Read the value of a variable with specified version.
        Author: Taikun Guo
        Date: 11/16/2017
        - Param:
        :variable (int): The variable index to be read
        :version (int): The version of the variable, if it is -1, then return the latest version
        - Return:
        The value of this variable.
        """
        if version == -1 or version == self.version:
            return self.variables[variable-1]
        else:
            return self.old[version][variable-1]

from database.server import Server

class DatabaseManager(object):
    """DB manager is responsible for all transactions"""

    def __init__(self):
        # initialize 10 servers
        self.servers = [Server() for i in range(10)]
        # a lock map
        # indicates which variable is currently
        # locked by whom
        # int -> string if write lock
        # int -> set if read lock
        self.locks = dict()
        # a lock queue
        # indicates who is queued up to lock
        # which variables
        # int -> list()
        self.lock_queue = dict()
        # a version table
        # keeps track of which RO transaction
        # is reading which version of a server
        # T name, server -> version
        self.version_table = dict()
        # keep track of which transaction
        # accessed which servers
        # if server fails, then we need to abort
        # those transactions
        self.accessed = [set() for i in range(10)]

    def fail(self, index):

    def recover(self, index):

    def read(self, trans, var):
        """
        returns:
            >= 0 : the value
            -1 : need abort
            -2 : need wait
        """
        # check if server is online
        if var % 2 == 0: # even
            s_index = -1
            for i in range(10):
                if self.servers[i].alive:
                    s_index = i
                    break
        else: # odd
            s_index = (var + 1) % 10
            if not self.servers[s_index].alive:
                s_index = -1
        if s_index == -1:
            # server is offline, abort this transaction
            return -1 # abort
        #check if this is a read-only transaction
        if (trans, s_index+1) in self.version_table:
            v = self.version_table[trans, s_index+1]
            return self.servers[s_index].read(var, version=v)
        # check if there is a write lock on this variable
        if var in self.locks and type(self.locks[var]) is str:
            # add the waiting list
            self.lock_queue[var]
            return -2 # wait
        # now we can read and return the value
        # but before that we need to:
        # add to accessed
        # add a read lock to this item
        self.accessed[s_index].add(trans)
        if var not in self.locks:
            self.locks[var] = set()
        self.locks[var].add(trans)
        value = self.servers[s_index].read(var)
        return value

    def write(self, trans, var, val):
        """
        returns:
            0 : success
            -1 : need abort
            -2 : need wait
        """


    def dump():

    def end():

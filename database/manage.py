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
        self.lock_queue = [list() for i in range(10)]
        # a version table
        # keeps track of which RO transaction
        # is reading which version of a server
        # T name, server -> version
        self.version_table = dict()
        # buffer all the changes by transaction
        # they will be commit when such transaction
        # ends
        # trans_name -> (var -> val)
        self.changes = dict()

    def _release_locks(self, trans):
        """
        release the locks related to this trans
        then return a list of trans that can be resume
        """
        released = set()
        for var in self.locks:
            if type(self.locks[var]) is str and self.locks[var] == trans:
                del self.locks[var]
                released.add(var)
            elif trans in self.locks[var]:
                self.locks[var].remove(trans)
                if len(self.locks[var]) == 0:
                    del self.locks[var]
                    released.add(var)
        # find out pending trans that can be resume
        resume = []
        for var in released:
            resume += self.lock_queue[var]
            self.lock_queue[var] = list() # reset
        return list(set(resume))

    def fail(self, server):
        """returns a list of transaction that should be abort"""
        # set server offline
        self.servers[server-1].fail()
        # find out all the transactions that has lock on this server
        trans = set()
        # loop through 20 variables
        for i in range(20):
            add = False
            if (i+1) % 2 == 0:
                add = True
            elif (i+2) % 10 == server:
                add = True
            if add:
                if type(self.locks[i+1]) is str:
                    trans.add(self.locks[i+1])
                else:
                    trans = trans.union(self.locks[i+1])
        return trans

    def recover(self, server):
        self.servers[server-1].recover()
        # sync even variables with other servers
        for i in range(10):
            if i != server-1 and self.servers[i].alive:
                for j in range(10):
                    self.servers[server-1].write((j+1) * 2, \
                        self.servers[i].read((j+1) * 2))
                break

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
            # add to the waiting list
            self.lock_queue[var-1].append(trans)
            return -2 # wait
        # now we can read and return the value
        # but before that we need to:
        # add a read lock to this item
        if var not in self.locks:
            self.locks[var] = set()
        self.locks[var].add(trans)
        value = self.servers[s_index].read(var)
        return value

    def write(self, trans, var, val):
        """
        returns:
            0 : success
            -2 : need wait
        not checking if servers are online or not
        sine write operation commit the changes
        when ending
        """
        # check if there is a lock on this variable
        if var in self.locks:
            # add to waiting list
            self.lock_queue[var-1].append(trans)
            return -2
        else:
            # put a lock on this variable
            self.locks[var] = trans
            # store the change to the buffer
            if trans not in self.changes:
                self.changes[trans] = dict()
            self.changes[trans][var] = val
            return 0

    def register_read_only(self, trans):
        """register a read-only transaction"""
        for i in range(10):
            self.version_table[trans, i+1] = self.servers[i].version

    def dump(self, server=-1, var=-1):
        if server != -1:
            # print everything in this server
            if not self.servers[server-1].alive:
                print("Server " + str(server) " is down!")
            else:
                print("Server " + str(server) ":")
                # print even variable first
                for i in range(10):
                    print("x" + str((i+1)*2) + " -> " + str(self.servers[server-1].read((i+1)*2)))
                # print the two odd variables
                print("x" + str(server-1) + " -> " + str(self.servers[server-1].read(server-1)))
                print("x" + str(server+9) + " -> " + str(self.servers[server-1].read(server+9)))
        elif var != -1:
            # TODO
            pass
        else:
            # TODO
            pass

    def end(self, trans):
        """
        commit a transaction and then end it
        return a list of waiting transactions
        that need to conitnue immediately
        or None if this transaction need to be abort
        """
        # first check if this is a read-only
        if (trans, 1) in self.version_table:
            for i in range(10):
                v = self.version_table[trans, i+1]
                del self.version_table[trans, i+1]
                delete_version = True
                for (t, s) in self.version_table:
                    if s == i+1 and v == self.version_table[t, s]:
                        delete_version = False
                        break
                if delete_version:
                    self.servers[i].clean(v)
            return [] # empty list since read-only does not hold locks
        else:
            # a normal transaction
            # commit changes first
            # release locks
            # find out other trans that is waiting for this
            patch = self.changes[trans]
            del self.changes[trans]
            # before commit, we need to check for server offlines
            offlines = set()
            for i in range(10):
                if not self.servers[i].alive:
                    offlines.add(i+1)
            # now check all the variables that we are writing to
            need_abort = False
            for var in patch:
                if len(offlines) == 10:
                    need_abort == True
                    break
                if (var + 1) % 10 in offlines:
                    need_abort == True
                    break
            if need_abort:
                return None
            # commit changes
            for var in patch:
                if var % 2 == 0:
                    for i in range(10):
                        if self.servers[i].alive:
                            # before store
                            # we need to check if we need to
                            # backup the current version
                            need_backup = False
                            for (t, s) in self.version_table:
                                if s == i+1 and self.version_table[t, s] == self.servers[i].version:
                                    need_backup = True
                            s.write(var, patch[var], need_backup)
            # release locks
            return self._release_locks(trans)

    def abort(self, trans):
        """
        abort the transaction
        clean data related to this transaction
        then return a list of trans that should be resume
        """
        # check if it is a read-only
        if (trans, 1) in self.version_table:
            for i in range(10):
                v = self.version_table[trans, i+1]
                del self.version_table[trans, i+1]
                delete = True
                for (t, s) in self.version_table:
                    if s == i+1 and v == self.version_table[t, s]:
                        delete = False
                        break
                if delete:
                    self.servers[i].old.remove(v)
            return []
        else:
            # clean changes
            del self.changes[trans]
            # release lock
            return self._release_locks(trans)

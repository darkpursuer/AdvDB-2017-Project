from transaction.transaction import Transaction
from console.operation import *
from database.manager import DatabaseManager

class TransactionManager(object):

    def __init__(self):
        self.database = DatabaseManager()
        self.transactions = []
        self.history = []

    def _find_transaction(self, trans):
        """
        Find the transaction with its name.
        Author: Yi Zhang
        Date: 11/16/2017
        - Param:
        :trans (String): The name of the transaction
        - Return:
        The targeted transaction object, if not found, return None
        """
        for t in self.transactions:
            if t.name == trans:
                return t
        return None

    def _resume(self, transactions):
        """
        Resume the transactions, and continue processing their rest operations.
        Author: Yi Zhang
        Date: 11/17/2017
        - Param:
        :transactions (String[]): The list of name of those transactions which needed to be resumed
        """
        for t in transactions:
            trans = self._find_transaction(t)
            if trans is not None:
                # if it is none than it means this trans
                # has already been aborted
                trans.set_status("RUNNING")
                ops = trans.buffer
                trans.buffer = list()
                self.process(ops)

    def _clean_deadlocks(self):
        """
        Detect the deadlocks, and then abort the youngest transaction to keep going.
        Author: Yi Zhang
        Date: 11/18/2017
        """
        loop = self.database.check_deadlocks()
        while loop is not None:
            # find the youngest
            for t in reversed(self.transactions):
                if t.name in loop:
                    # abort this and break
                    rl = self.database.abort(t.name)
                    t.set_status("ABORTED")
                    self._resume(rl)
                    break
            loop = self.database.check_deadlocks()

    def _print_trans(self, trans):
        """
        Print the variables stored in this transaction.
        Author: Yi Zhang
        Date: 11/18/2017
        - Param:
        :trans (String): The name of transaction that needed to be print
        """
        t = self._find_transaction(trans)
        print(str(t.name))
        for var in t.variables:
            print("x" + str(var) + " -> " + str(t.variables[var]))

    def process(self, ops):
        """
        Process a list of operations.
        Author: Yi Zhang
        Date: 11/18/2017
        - Param:
        :ops (Operation[]): The list of operations needed to be processed
        """
        for op in ops:
            if op.OP == "begin":
                # initialize transaction
                t = Transaction("NORMAL", op.NAME)
                self.transactions.append(t)
            elif op.OP == "beginRO":
                # initialize RO trans
                self.database.register_read_only(op.NAME)
                t = Transaction("READ", op.NAME)
                self.transactions.append(t)
            elif op.OP == "R": # read
                # check the status of this trans
                trans = self._find_transaction(op.T)
                if trans == None:
                    print("Transaction not found: " + str(op.T))
                elif trans.get_status() == "RUNNING":
                    rs = self.database.read(op.T, int(op.X[1:]))
                    if rs == -1:
                        # abort
                        rl = self.database.abort(op.T)
                        trans.set_status("ABORTED")
                        self._resume(rl)
                    elif rs == -2:
                        # blocked
                        trans.set_status("BLOCKED")
                        trans.buffer.append(op)
                        self._clean_deadlocks()
                    else:
                        # success
                        trans.variables[int(op.X[1:])] = rs
                elif trans.get_status() == "BLOCKED":
                    trans.buffer.append(op)
            elif op.OP == "W": # write
                # check the status of this trans
                trans = self._find_transaction(op.T)
                if trans == None:
                    print("Transaction not found: " + str(op.T))
                elif trans.get_status() == "RUNNING":
                    # send to database
                    rs = self.database.write(op.T, int(op.X[1:]), op.V)
                    if rs == -2:
                        # need to wait
                        trans.set_status("BLOCKED")
                        trans.buffer.append(op)
                        self._clean_deadlocks()
                elif trans.get_status() == "BLOCKED":
                    trans.buffer.append(op)
            elif op.OP == "dump":
                if op.SITE != -1:
                    self.database.dump(server=op.SITE)
                elif op.VAR != "":
                    self.database.dump(var=int(op.VAR[1:]))
                else:
                    self.database.dump()
            elif op.OP == "end":
                # check the status of this trans
                trans = self._find_transaction(op.NAME)
                if trans == None:
                    print("Transaction not found: " + str(op.NAME))
                elif trans.get_status() == "RUNNING":
                    # send to database
                    rs = self.database.end(op.NAME)
                    if rs is None: # abort
                        rl = self.database.abort(op.NAME)
                        trans.set_status("ABORTED")
                        self._resume(rl)
                    else:
                        trans.set_status("COMMITED")
                        self._print_trans(trans.name)
                        self._resume(rs)
                elif trans.get_status() == "BLOCKED":
                    trans.buffer.append(op)
            elif op.OP == "fail":
                to_be_abort = self.database.fail(op.SITE)
                for t in to_be_abort:
                    r = self.database.abort(t)
                    trans = self._find_transaction(t)
                    trans.set_status("ABORTED")
                    self._resume(r)
            else: # recover
                self.database.recover(op.SITE)
            n_transactions = []
            for t in self.transactions:
                if t.get_status() == "COMMITED" or t.get_status() == "ABORTED":
                    self.history.append(t)
                else:
                    n_transactions.append(t)
            self.transactions = n_transactions

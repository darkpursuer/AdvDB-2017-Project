from transaction.transaction import Transaction
from console.operation import *
from database.manage import DatabaseManager

class TransactionManager(object):

    def __init__(self):
        self.database = DatabaseManager()
        self.transactions = []

    def _find_transaction(self, trans):
        for t in self.transactions:
            if t.name == trans:
                return t
        return None

    def _resume(self, transactions):
        for t in transactions:
            trans = self._find_transaction(trans)
            trans.status = "RUNNING"
            ops = trans.buffer
            trans.buffer = list()
            self.process(ops)

    def _clean_deadlocks(self):
        loop = self.database.check_deadlocks()
        while loop is not None:
            # find the youngest
            for t in reversed(self.transactions):
                if t.name in loop:
                    # abort this and break
                    rl = self.database.abort(t.name)
                    t.status = "ABORTED"
                    self._resume(rl)
                    break
            loop = self.database.check_deadlocks()

    def _print_trans(self, trans):
        """print the variables stored in this transaction"""
        t = self._find_transaction(trans)
        print(str(t.name))
        for var in t.variables:
            print("x" + str(var) + " -> " + str(t.variables[var]))

    def process(self, ops):
        """process a list of operations"""
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
                elif trans.status == "RUNNING":
                    rs = self.database.read(op.T, int(op.X[1:]))
                    if rs == -1:
                        # abort
                        rl = self.database.abort(op.T)
                        trans.status = "ABORTED"
                        self._resume(rl)
                    elif rs == -2:
                        # blocked
                        trans.status = "BLOCKED"
                        trans.buffer.append(op)
                    else:
                        # success
                        trans.variables[int(op.X[1:])] = rs
                        self._clean_deadlocks()
                elif trans.status == "BLOCKED":
                    trans.buffer.append(op)
            elif op.OP == "W": # write
                # check the status of this trans
                trans = self._find_transaction(op.T)
                if trans == None:
                    print("Transaction not found: " + str(op.T))
                elif trans.status == "RUNNING":
                    # send to database
                    rs = self.database.write(op.T, int(op.X[1:]), op.V)
                    if rs == -2:
                        # need to wait
                        trans.status = "BLOCKED"
                        trans.buffer.append(op)
                    else: # success
                        self._clean_deadlocks()
                elif trans.status == "BLOCKED":
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
                elif trans.status == "RUNNING":
                    # send to database
                    rs = self.database.end(op.NAME)
                    if rs is None: # abort
                        rl = self.database.abort(op.NAME)
                        trans.status = "ABORTED"
                        self._resume(rl)
                    else:
                        trans.status = "COMMITED"
                        self._print_trans(trans.name)
                        self._resume(rs)
                elif trans.status == "BLOCKED":
                    trans.buffer.append(op)
            elif op.OP == "fail":
                self.database.fail(op.SITE)
            else: # recover
                self.database.recover(op.SITE)

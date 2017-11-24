"""
Supported DB operations:
- begin(T1) - begin of a normal transaction
- beginRO(T3) - begin of a read-only transaction
- R(T1, x4) - T1 wants to read x4
- W(T1, x6,v) - T1 wants to write v to x6
- dump() - get all variables from all sites
- dump(i) - get all variables at site i
- dump(xj) - get variable xj at all sites
"""

import sys, re


class TransactionManager(object):
    """
    This module is the entry point of all
    the transactions, it validate and process them.
    """

    def __init__(self):
        """
        Initialize object, create regex for validating comments and operations
        """
        self.REGEX_COMMENT = re.compile(r"(\/\/|===).*")
        self.REGEX_OPERATIONS = re.compile(r"(begin\(T\d+\)|beginRO\(T\d+\)" \
            + "|R\(T\d+,x\d+\)|W\(T\d+,x\d+,\d+\)|dump\((\d+|x\d+)?\)|" \
            + "end\(T\d+\)|fail\(\d+\)|recover\(\d+\))")

    def process(self, line):
        """
        validate a line and process all the operations
        """
        operations = self._validate(line)
        if operations is None:
            print("Line contains invalid operation!")
            print(__doc__)
        else:
            self._execute_ops(operations)

    def _validate(self, line):
        """
        Check if this line contains a sequence of
        valid operations.\n
        If so, returns a list of operations\n
        If this line is a comment e.g. "//" or "===" then
        return an empty list\n
        If invalid, return None
        """
        # remove whitespaces since it will cause trouble parsing this line
        no_whitespaces = "".join(line.split())
        if self.REGEX_COMMENT.match(no_whitespaces):
            # check if this line is a comment
            return []
        elif self.REGEX_OPERATIONS.match(no_whitespaces):
            # check if this line is a list of operations
            operations = [(i.split("(")[0], i.split("(")[0]) \
                for i in no_whitespaces.split(")")]
            return operations
        else:
            # the operation is not valid, return None
            return None

    def _execute_ops(self, operations):
        pass

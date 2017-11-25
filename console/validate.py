"""
Supported DB operations:
- begin(T1) - begin of a normal transaction
- beginRO(T3) - begin of a read-only transaction
- R(T1, x4) - T1 wants to read x4
- W(T1, x6,v) - T1 wants to write v to x6
- dump() - get all variables from all sites
- dump(i) - get all variables at site i
- dump(xj) - get variable xj at all sites
- end(T1) - end a transaction T1
- fail(1) - fail site 1
- recover(1) - recover site 1
"""

import sys, re
from console.operation import *

class Validator(object):
    """
    Validate if operations are valid
    """

    def __init__(self):
        """
        Initialize object, create regex for validating comments
        """
        self.REGEX_COMMENT = re.compile(r"(\/\/|===).*")
        self.REGEX_OPERATIONS = re.compile(r"(begin\(T\d+\)|beginRO\(T\d+\)" \
            + "|R\(T\d+,x\d+\)|W\(T\d+,x\d+,\d+\)|dump\((\d+|x\d+)?\)|" \
            + "end\(T\d+\)|fail\(\d+\)|recover\(\d+\))")

    def validate(self, line):
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
            operations = [(i.split("(")[0], \
                "" if len(i.split("(")) == 1 else i.split("(")[1])
                for i in no_whitespaces.split(")")]
            return self._parse_ops(operations[:-1]) # filter out empty strings
        else:
            # the operation is not valid, return None
            return None

    def _parse_ops(self, operations):
        """
        convert a list of raw operation strings
        into objects and send them to the
        database manager.
        """
        ops = []
        for o in operations:
            if o[0] == "begin":
                ops.append(OPBegin("begin", o[1]))
            elif o[0] == "beginRO":
                ops.append(OPBeginRO("beginRO", o[1]))
            elif o[0] == "R":
                ops.append(OPRead("R", o[1].split(",")[0], o[1].split(",")[1]))
            elif o[0] == "W":
                ops.append(OPWrite("W", o[1].split(",")[0], o[1].split(",")[1], int(o[1].split(",")[2])))
            elif o[0] == "dump":
                if o[1] == "":
                    ops.append(OPDump("dump"))
                else:
                    try:
                        arg = int(o[1])
                        ops.append(OPDump("dump", site=arg))
                    except ValueError:
                        arg = o[1]
                        ops.append(OPDump("dump", var=arg))
            elif o[0] == "end":
                ops.append(OPEnd("end", o[1]))
            elif o[0] == "fail":
                ops.append(OPFail("fail", int(o[1])))
            else: # recover
                ops.append(OPRecover("recover", int(o[1])))
        return ops

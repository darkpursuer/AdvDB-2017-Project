"""
Supported commands:
- help - print all the commands
- load <filename> - load and process a file
- exit - quit the console
- a bunch of DB operations

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

import sys, re, readline
from console.validate import Validator
from transaction.manage import TransactionManager

class Console(object):
    """
    Console is the main process deals with user's input.\n
    It will deal with the following commands:\n
    - help - print all the commands\n
    - load <filename> - load and process a file\n
    - exit - quit the console\n
    - a bunch of DB operations
    """

    def __init__(self):
        """Initialize the object"""
        self.REGEX_LOAD_FILE = re.compile(r"load [^\s]+")
        self.validator = Validator()
        self.manager = TransactionManager()

    def _process_line(self, line):
        """
        Check if this line is valid and process it.
        """
        # strip the line
        stripped = line.strip()
        # check for commands
        if stripped: # ignore empty line
            if stripped == "help":
                print(__doc__)
            elif stripped == "exit":
                sys.exit(0)
            elif self.REGEX_LOAD_FILE.match(stripped):
                filepath = stripped.split(" ")[1]
                self._process_file(filepath)
            else:
                # validate this Line
                operations = self.validator.validate(stripped)
                if operations is None:
                    print("Line contains invalid operation!")
                    print(__doc__)
                else:
                    # call TM to process operations
                    self.manager.process(operations)

    def _process_file(self, filepath):
        """
        Load the file line by line and process each line\n
        - param:\n
        :filepath (String): The path of the file to be loaded
        """
        try:
            with open(filepath) as f:
                for line in f:
                    self._process_line(line)
        except FileNotFoundError as e:
            print(e)

    def start(self, infile):
        """
        Start the main loop
        """
        if infile:
            self._process_file(infile)
        # start main loop
        while True:
            try:
                line = input("~> ")
                self._process_line(line)
            except EOFError:
                continue

#!/usr/bin/python
"""
Usage:
"""

import sys, getopt
from console.main import Console

def main(argv):
    """
    Parse command line arguments\n
    Process preloaded file if there is one\n
    Start the console
    """
    # read command line arguments
    infile = ""
    try:
        opts, args = getopt.getopt(argv,"hf:",["help"])
    except getopt.GetoptError:
        print(__doc__)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif opt == "-f":
            infile = arg
        else:
            print(__doc__)
            sys.exit(2)

    #initialize console
    console = Console()
    # start console
    console.start(infile)


if __name__ == "__main__":
    # start main function
    main(sys.argv[1:])

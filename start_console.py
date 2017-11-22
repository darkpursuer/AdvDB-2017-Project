#!/usr/bin/python
"""
Usage: 
"""

import sys, getopt
from console import Console


def main(argv):
  """
  Parse command line arguments\n
  Start the main loop
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
  # process infile
  if infile:
    console.process_file(infile)
  # start console
  console.start()
    

if __name__ == "__main__":
  # start main function
  main(sys.argv[1:])
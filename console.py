"""

"""

import sys


class Console(object):

  def process_line(self, line):
    print(line)

  def process_file(self, filepath):
    pass

  def start(self):
    # start main loop
    sys.stdout.write("~> ")
    sys.stdout.flush()
    for line in sys.stdin:
      # strip the line
      stripped = line.strip()
      # process this line
      self.process_line(stripped)
      sys.stdout.write("~> ")
      sys.stdout.flush()
  
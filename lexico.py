import sys

class Lexical:
  raw_string = None
  end_of_file = None

  def __init__(self, raw_string):
    self.raw_string = raw_string
    print self.raw_string

  def scan(self):
    pass

  def isDigit(self, c):
    return c.isdigit()


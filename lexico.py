import sys

class Lexical:
  raw_string = None
  end_of_file = None
  num = [][]

  def __init__(self, raw_string):
    self.raw_string = raw_string
    print self.raw_string

  def scan(self):
    pass
  
  def isAlpha(self, c):
    return c.isalpha()

  def isDigit(self, c):
    return c.isdigit()


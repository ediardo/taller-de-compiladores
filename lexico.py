import sys
import StringIO

class Lexical:

  error_state = 128
  raw_string = None
  end_of_file = None
  states = None 

  def __init__(self, raw_string):
    self.raw_string = raw_string
    self.states = [
      # alpha, digit, dot, +, -, _, EOL
      [2, 3, self.error_state, 2, 2, 2, None]
      [2, 3, self.error_state, 3, ]
      ]
    self.analyzer()

  def analyzer(self):
    current_state = 0
    previous_state = None 
    i = 0
    while current_state != self.accept_state and current_state != self.error_state:
      for line in StringIO.StringIO(self.raw_string):
        for char in line:
          self.scanner(char)
          if char != '\n' and current_state == 0 and char != :
            if
          
  def scanner(self, char):
    if self.isDigit(char): return 1
    if self.isAlpha(char): return 2
    if self.isUnderscore(char): return 3
    if self.isDot(char): return 4
    

  def isUnderscore(self, char):
    if char == '_': 
      return True
    return False

  def isDot(self, char):
    if char == '.':
      return True
    return False

  def isBlank(self, char):
    if char == ' ' or char == '\t':
      return True
    return False

  def isAlpha(self, char):
    return char.isalpha()

  def isDigit(self, char):
    return char.isdigit()

  def isArithmeticSum(self, char):
    if char == '+':
      return True
    return False

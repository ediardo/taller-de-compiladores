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
          #self.scanner(char)
          swic
          
            case 0 
            if isdi c_sta=1
            if isalpha c_sta=2
            if + c_sta=3
            if - c_sta=4
            
            
            
            case 1 if isdi c_sta=1
            if . c_sta=10
            
            case 10
            if isdi c_sta=11
            
            case 11
            if isdi c_sta=1
            
            case 2 
            if isalpha c_sta=2
            
            case 4
            
          
          
          swich (c_state)
          
          case 1 int 
          case 11 
        
        
        
          
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

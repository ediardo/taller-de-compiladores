import sys
import StringIO

class Lexical:
  error_state = -1 
  accept_state = 128
  raw_string = None
  end_of_file = None
  states = None 

  def __init__(self, raw_string):
    self.raw_string = raw_string
    self.states = [
      # alpha, digit, dot, +, -, *,  _, EOL
      [1, 3, -1, 4, 4, 4, 4, 4, 4, 1],
      [128, 128, -1, -1, -1, -1, -1 , -1, -1, 128],
      [-1, 128, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, 128, 128, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, 128, 128, 128, 128, 128, 128, -1],
      ]
    self.generate()

  def generate(self):
    current_state = 0
    previous_state = None 
    position = 0
    symbol = None
    for line in StringIO.StringIO(self.raw_string):
      for char in line:
        if current_state != self.accept_state and current_state != self.error_state:
          position += position
          if self.is_blank(char):
            if current_state == 0:
              continue
            else:
              previous_state, current_state = current_state, self.accept_state 
          if current_state != self.accept_state:
            symbol = self.char_to_symbol(char)
        
          if symbol < 0:
            break

          if symbol >= 0 and symbol <= 9 and current_state != self.accept_state:
            previous_state, current_state = current_state, self.states[current_state][symbol]
          print previous_state, current_state


        
        
          
  def char_to_symbol(self, char):
    if self.is_alpha(char): 
      return 0
    if self.is_digit(char): 
      return 1
    if self.is_dot(char):
      return 2 
    if self.is_arithmetic_sum(char): 
      return 3
    if self.is_underscore(char): 
      return 9
    return -1

  def is_underscore(self, char):
    if char == '_': 
      return True
    return False

  def is_dot(self, char):
    if char == '.':
      return True
    return False

  def is_blank(self, char):
    if char == ' ' or char == '\t':
      return True
    return False

  def is_alpha(self, char):
    return char.isalpha()

  def is_digit(self, char):
    return char.isdigit()

  def is_arithmetic_sum(self, char):
    if char == '+':
      return True
    return False

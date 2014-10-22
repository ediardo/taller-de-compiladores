import sys
import StringIO

class Lexical:
  raw_string = None

  def __init__(self, raw_string):
    self.raw_string = raw_string
    self.generate()

  def generate(self):
    index = 0
    for line in StringIO.StringIO(self.raw_string):
      current_state = 0
      previous_state = None 
      for index, char in enumerate(line):
        if not self.is_blank(char) and char != '\n':
          print index, char, previous_state, current_state  
          
          if current_state == 0:
            if self.is_alpha(char):
              previous_state, current_state = current_state, 1
            elif self.is_digit(char):
              previous_state, current_state = current_state, 2
            elif self.is_underscore(char):
              previous_state, current_state = current_state, 1
            elif self.is_arithmetic_sum(char):
              previous_state, current_state = current_state, 4
            else:
              error_state = True
            continue 

          if current_state == 1:
            if self.is_alpha(char):
              previous_state, current_state = current_state, 1

            elif self.is_digit(char):
              previous_state, current_state = current_state, 1

            elif self.is_underscore(char):
              previous_state, current_state = current_state, 1
              accept_state = True
            else:
              error_state = True
            continue

          if current_state == 2:
            if self.is_digit(char):
              previous_state, current_state = current_state, 2

            elif self.is_dot(char):
              previous_state, current_state = current_state, 3
            continue

          if current_state == 3:
            if self.is_digit(char):
              previous_state, current_state = current_state, 3
            continue
        else:
          current_state = 0
          previous_state = None 

        
        
          
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

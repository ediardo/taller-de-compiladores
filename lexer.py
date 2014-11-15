import sys
import StringIO
import csv

class Lexer:
  symbols = []
  states = []
  line_number = 0
  position = 0
  EOF = False

  def __init__(self):
    with open("states.csv") as f:
      reader = csv.reader(f)
      for row, state in enumerate(reader):
        if row != 0:
          self.states.append(state)
        else:
          self.symbols = state

  def generate(self, line):
    total_symbols = len(self.symbols)
    total_states = len(self.states)
    lexeme = ""
    current_state = 0
    previous_state = None 
    while self.position < len(line) and current_state != '':
      symbol = None
      char = line[self.position]
      self.position += 1
      if not self.is_blank(char):
        symbol = self.char_to_symbol(char)
        if symbol >= 0 and symbol < total_symbols:
          if self.states[current_state][symbol] != '':
            previous_state, current_state = current_state, int(self.states[current_state][symbol]) 
            lexeme += char
          else:
            previous_state, current_state = current_state, 0
            self.position -= 1
        else:
          return False
      else:
        if current_state > 0:
          previous_state, current_state = current_state, 0
      if current_state == 0:
        for state in range(total_states):
          if previous_state == state:
            return dict({'name': self.states[previous_state][-1], 'lexeme': lexeme})

    return None

  def get_next_state(self, state, symbol):
    return self.states[state][symbol]

  def char_to_symbol(self, char):
    if self.is_alpha(char): 
      return 0
    if self.is_digit(char): 
      return 1
    if self.is_dot(char):
      return 2 
    if self.is_plus(char):
      return 3
    if self.is_minus(char):
      return 4
    if self.is_star(char):
      return 5
    if self.is_percentage(char):
      return 6
    if self.is_equals(char):
      return 7
    if self.is_slash(char):
      return 8
    if self.is_underscore(char):
      return 9
    if self.is_less_than(char):
      return 10
    if self.is_greater_than(char):
      return 11
    if self.is_left_parenthesis(char):
      return 12
    if self.is_right_parenthesis(char):
      return 13
    if self.is_bang(char):
      return 14
    if self.is_pipe(char):
      return 15
    if self.is_ampersand(char):
      return 16
    if self.is_left_brace(char):
      return 17
    if self.is_right_brace(char):
      return 18
    return -1


  def is_blank(self, char):
    if char == ' ' or char == '\t' or char == '\n':
      return True
    return False

  def is_alpha(self, char):
    return char.isalpha()

  def is_digit(self, char):
    return char.isdigit()

  def is_dot(self, char):
    if char == '.':
      return True
    return False

  def is_plus(self, char):
    if char == '+':
      return True
    return False

  def is_minus(self, char):
    if char == '-':
      return True
    return False

  def is_star(self, char):
    if char == '*':
      return True
    return False

  def is_percentage(self, char):
    if char == '%':
      return True
    return False

  def is_equals(self, char):
    if char == '=':
      return True

  def is_slash(self, char):
    if char == '/':
      return True
    return False

  def is_underscore(self, char):
    if char == '_': 
      return True
    return False

  def is_less_than(self, char):
    if char == '<':
      return True
    return False

  def is_greater_than(self, char):
    if char == '>':
      return True
    return False

  def is_left_parenthesis(self, char):
    if char == '(':
      return True
    return False

  def is_right_parenthesis(self, char):
    if char == ')':
      return True
    return False

  def is_bang(self, char):
    if char == '!':
      return True
    return False

  def is_pipe(self, char):
    if char == '|':
      return True
    return False
  
  def is_ampersand(self, char):
    if char == '&':
      return True
    return False

  def is_left_brace(self, char):
    if char == '{':
      return True
    return False

  def is_right_brace(self, char):
    if char == '}':
      return True
    return False



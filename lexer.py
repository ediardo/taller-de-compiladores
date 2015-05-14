import sys
import StringIO
import csv

class Lexer:
  symbols = []
  states = []
  EOF = False
  file_contents = None
  keywords = ['if', 'switch','break','default','true', 'false', 'nil', 'def', 'int', 'decimal', 'string', 'import', 'boolean', 'void', 'for', 'function', 'while', 'print', 'case', 'return']
  def __init__(self, file_contents):
    with open("states.csv") as f:
      reader = csv.reader(f)
      for row, state in enumerate(reader):
        if row != 0:
          self.states.append(state)
        else:
          self.symbols = state
    self.file_contents = file_contents

  def generate(self):
    total_symbols = len(self.symbols)
    total_states = len(self.states)
    lexeme = ""
    current_state = 0
    # loop every line
    for line_pos, line in enumerate(self.file_contents):
      col_position = 0
      previous_state = None
      # while there's a char in line and current state is not E
      while col_position < len(line):
        char = line[col_position]
        # column character position +1 for offset
        col_position += 1
        # if char is not null
        symbol = self.char_to_symbol(char)
        # if char is a valid symbol 
        if symbol in range(0, total_symbols):
          previous_state, current_state = current_state, self.get_next_state(current_state, symbol)
          if current_state == 'A':
            lexeme_name = self.states[int(previous_state)][-1]
            if lexeme in self.keywords:
              lexeme_name = lexeme
            #print "Char: ", char, ", Line: ", line_pos + 1, ", Col: ", col_position, ", Symbol: ", symbol, ", Prev State: ", previous_state, ", Current state: ", current_state
            yield dict({'name': lexeme_name, 'lexeme': lexeme, 'line': line_pos + 1})
            lexeme = ""
            col_position -= 1
            current_state = 0 
          elif current_state == 'E':
            print "error"
          else:
            if not self.is_blank(char):
              lexeme += char
        else:
          print "error2"

  def get_next_state(self, state, symbol):
    if type(self.states[int(state)][int(symbol)]) is int:
      return int(self.states[int(state)][int(symbol)])
    return self.states[int(state)][int(symbol)]

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
    if self.is_semicolon(char):
      return 19
    if self.is_comma(char):
      return 20
    if self.is_blank(char):
      return 21
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
  def is_semicolon(self, char):
    if char == ';':
      return True
    return False
  def is_comma(self, char):
    if char == ',':
      return True
    return False

  def is_keyword(self, lexeme):
    if lexeme == 'for':
      return True
    if lexeme == 'while':
      return True
    if lexeme == 'int':
      return True
    if lexeme == 'decimal':
      return True
    if lexeme == 'string':
      return True
    if lexeme == 'boolean':
      return True
    if lexeme == 'void':
      return True
    if lexeme == 'function':
      return True

if __name__ == "__main__":
  lex = Lexer('file.txt')
  lex.start()

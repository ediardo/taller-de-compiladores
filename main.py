import sys
from lexer import *
from parsing import *
file_name = sys.argv[1]
file_contents = open(file_name, 'r').readlines()
token = None
lex = Lexer(file_contents)
for token in lex.generate():
  if token == None:
    break
  print token

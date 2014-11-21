import sys
from lexer import *
from parsing import *
file_contents = None
file_name = None
file_name = sys.argv[1]
file_contents = open(file_name, 'r').readlines()
lexical_analyzer = Lexer()
print lexical_analyzer.symbols
token = None
for line in file_contents:
  for token in lexical_analyzer.generate(line):
    if token == None:
      print "Error"
    else:
      print token

import sys
from lexer import *
from parsing import *
file_contents = None
file_name = None
file_name = sys.argv[1]
file_contents = open(file_name, 'r').readlines()
lexical_analyzer = Lexer()
token = None
for line in file_contents:
  print line

  #while token != False:
   # token = lexical_analyzer.generate(line)
    #if token == False:
     # break
#    else:  
 #     print token


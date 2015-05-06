import sys
from lexer import *
#from parsing import *
file_name = sys.argv[1]
file_contents = open(file_name, 'r').readlines()
token = None
lex = Lexer(file_contents)
token = lex.generate()
#parser = Parsing(token)

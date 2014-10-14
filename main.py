import sys
from lexico import *
file_contents = None
file_name = None
try:
  file_name = sys.argv[1]
  file_contents = open(file_name, 'r').read()
except IOError:
  print "No se pudo abrir el archivo", file_name

l = Lexical(file_contents)
print l.isDigit('1')

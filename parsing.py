class Parsing:
  
  def __init__(self, token_generator):
    self.token_generator = token_generator
    self.get_token()
    self.program()

  def get_token(self):
    self.current_token = next(self.token_generator)

  def accept(self, symbol):
    if self.current_token['name'] == symbol:
      self.get_token()
      return True
    return False
  
  def expect(self, symbol):
    if self.accept(symbol):
      return True
    print "error"
    return False

  def program(self):
    if self.accept('function'): 
      self.function()
    if self.accept('identifier'):
      self.expect('assignment') 

  def function(self):
    if self.token.next()['name'] == 'identifier':
      self.token.next()
      print "soy function"

  def factor(self):
    pass
    


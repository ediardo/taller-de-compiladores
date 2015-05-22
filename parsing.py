class Parsing:

  #self.tabsim = []
    
  def __init__(self, token_generator):
    self.token_generator = token_generator
    self.get_token()
    self.program()

  def get_token(self):
    self.current_token = next(self.token_generator, None)

  def raise_error(self,type, msg):
    print type, msg
    exit()

  def accept(self, symbol):
    if self.current_token <> None:
      if self.current_token['name'] == symbol:
        print self.current_token
        self.get_token()
        return True
    return False
  
  def expect(self, symbol):
    if self.accept(symbol):
      return True
    if self.current_token <> None:
      self.raise_error(" ", "error: se esperaba " + symbol + " y se leyo " + self.current_token['lexeme'])
    else:
      self.raise_error("", "error: se esperaba " + symbol + " y se llego al final del programa")

    return False

  def program(self):
    while self.accept('import'): 
      self.importer()
    while self.accept('function'):
      self.function()
    self.statement()

  def importer(self):
    self.expect('identifier')
    self.expect('semicolon')

  def params(self):
    self.expression()
    while True:
      if not self.accept('comma'):
        break
      else:
        self.expression() 
    self.expect('right_parenthesis')

  def function(self):
    if self.accept('identifier'):
      self.expect('left_parenthesis')
      self.params()
      self.expect('left_brace')
      self.block()
      self.expect('right_brace')

  def block(self):
    self.statement() 
  
  def statement(self):
    if self.accept('identifier'):
      if self.accept('assignment'):
        self.assignment()
      elif self.accept('left_parenthesis'):
        self.call_function()
      self.expect('semicolon')
      self.statement()
    elif self.accept('if'):
      self.if_condition()
      self.statement()
    elif self.accept('while'):
      self.while_loop()
      self.statement()
    elif self.accept('for'):
      self.for_loop()
      self.statement()
    elif self.accept('print'):
      self.print_function()
      self.expect('semicolon')
      self.statement()
    elif self.accept('switch'):
      self.switch()
      self.statement()

  def expression(self):
    if self.accept('string'):
      self.string()
    else:
      if self.accept('arithmetic_addition'):
        pass  
      elif self.accept('arithmetic_subtraction'):
        pass
      self.term() 
      while True:
        if not (self.accept('arithmetic_addition') or self.accept('arithmetic_subtraction')):
          break
        self.term()

  def term(self):
    self.factor()
    while True:
      if not (self.accept('arithmetic_multiplication') or self.accept('arithmetic_division')):
        break
      self.factor()


  def factor(self):
    if self.accept('identifier'):
      pass
    elif self.accept('real_number'):
      pass
    elif self.accept('integer_number'):
      pass
    elif self.accept('left_parenthesis'):
      self.expression()
      self.expect('right_parenthesis')
    else:
      self.raise_error("", "error factor")
  
  def assignment(self):
    self.expression() 

  def string(self):
    while True:
      if not self.accept('arithmetic_addition'):
        break
      self.expression()

  def condition(self):
    self.expression()
    if self.accept('comparison_less_than'):
      pass
    elif self.accept('comparison_less_than_or_equal'):
      pass
    elif self.accept('comparison_equal'):
      pass
    elif self.accept('comparison_greater_than_or_equal'):
      pass
    elif self.accept('comparison_greater_than'):
      pass
    else:
      self.raise_error("", "error comparativo")
    self.expression()

  def if_condition(self):
    self.expect('left_parenthesis')
    self.condition()
    self.expect('left_brace')
    self.statement()
    self.expect('right_brace')
    if self.accept('else'):
      self.expect('left_brace')
      self.statement()
      self.expect('right_brace')

  def while_loop(self):
    self.condition()
    self.expect('left_brace')
    self.statement()
    self.expect('right_brace')

  def for_loop(self):
    self.expect('left_parenthesis')
    if self.accept('identifier'):
      if self.accept('assignment'):
        self.assignment()
      else:
        pass
    self.expect('semicolon')
    self.condition()
    if self.accept('comparison_less_than'):
      pass
    elif self.accept('comparison_less_than_or_equal'):
      pass
    elif self.accept('comparison_equal'):
      pass
    elif self.accept('comparison_greater_than'):
      pass
    else:
      self.raise_error("", "error comparativo")
    self.expression()
    self.expect('semicolon')
    self.expect('identifier')
    if self.accept('increment'):
      pass
    elif self.accept('decrement'):
      pass
    self.expect('right_parenthesis')
    self.expect('left_brace')
    self.statement()
    self.expect('right_brace')

  def switch(self):
    self.expect('left_parenthesis')
    self.expression()
    self.expect('right_parenthesis')
    self.expect('left_brace')
    while True:
      if not self.accept('case'):
        self.raise_error("", "error case")
        break
      else:
        self.expression()
        self.expect('colon')
      self.statement()

  
  def print_function(self):
    if self.accept('string'):
      self.string()
    else:
      self.expression() 
     
  def call_function(self):
    self.params()

  def search_tabsym(self, item):
    pass 

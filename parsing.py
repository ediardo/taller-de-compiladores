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
    return False

  def accept(self, symbol, next=True):
    if self.current_token <> None:
      if self.current_token['name'] == symbol:
        print self.current_token
        if next:
          self.get_token()
        return True
    return False
  
  def expect(self, symbol):
    if self.accept(symbol):
      return True
    if self.current_token <> None:
      return self.raise_error(" ", "error: se esperaba " + symbol + " y se leyo " + self.current_token['lexeme'])
    else:
      return self.raise_error("", "error: se esperaba " + symbol + " y se llego al final del programa")
  
  def atom(self):
    if self.accept('identifier'):
      pass
    elif self.literal():
      pass
    elif self.enclosure():
      pass
    else:
      return False
    return True

  def enclosure(self):
    if self.accept('left_parenthesis'):
      if self.expression():
        if self.expect('right_parenthesis'):
          return True
    return False

  def literal(self):
    if self.accept('string'):
      pass
    elif self.accept('integer_number'):
      pass
    elif self.accept('real_number'):
      pass
    else:
      return False
    return True

  def primary(self):
    if self.atom():
      pass
    else:
      return False
    return True
  
  def power(self):
    if self.primary():
      if self.accept('arithmetic_power'):
        if self.u_expression():
          return True
        else:
          return False
      return True
    else:
      return False

  def u_expression(self):
    if self.power():
      return True
    else:
      if self.accept('arithmetic_subtraction'):
        if self.u_expression():
          return True
        else:
          print "aqui1"
          return self.raise_error("", "Falta operador o primary")
      elif self.accept('arithmetic_addition'):
        if self.u_expression():
          return True
        else:
          print "aqui2"
          return self.raise_error("", "Falta operador o primary")
      return False

  def m_expression(self):
    if self.u_expression():
      while True:
        if self.accept('arithmetic_multiplication'):
          self.u_expression()
        elif self.accept('arithmetic_division'):
          self.u_expression()
        elif self.accept('arithmetic_modulo'):
          self.u_expression()
        else:
          break
      return True
    else:
      return False

  def a_expression(self):
    if self.m_expression():
      while True:
        if self.accept('arithmetic_addition'):
          if self.m_expression():
            return True
          else:
            return self.raise_error("", "Falta operador o primary")
        elif self.accept('arithmetic_subtraction'):
          if self.m_expression():
            return True
          else:
            return self.raise_error("", "Falta operador o primary")
        else:

          break
      return True
    else:
      return False



  def expression(self):
    while True:
      if self.a_expression():
        return True
      else:
        break
    return False

  def program(self):
    while True:
      if self.function_definition():
        pass
      elif self.statement():
        self.expect('semicolon')
      else:
        break

  def function_definition(self):
    if self.accept('function'):
      if self.function_name():
        self.expect('left_parenthesis')
        self.parameter_list()
        self.expect('right_parenthesis')
        self.expect('left_brace')
        while True:
          if self.statement():
            pass
          else:
            break
        self.expect('right_brace')
        return True
    return False
        
  def function_name(self):
    return self.expect('identifier')
    
  def parameter_list(self):
    if self.def_parameter():
      while True:
        if not self.accept('comma'):
          break
        else:
          if not self.def_parameter():
            return self.raise_error("", "Falta identificar")

  def def_parameter(self):
    if self.parameter():
      if self.accept('assignment'):
        if self.expression():
          return True
        else:
          return False
      return True
    else:
      return False

  def parameter(self):
    if self.accept('identifier'):
      return True
    else:
      return False

  def statement(self):
    if self.assignment_stmt():
      return True
    return False


  def assignment_stmt(self):
    if self.target():
      self.expect('assignment')
      if self.expression():
        return True
    return False

  def target(self):
    if self.accept('identifier'):
      return True
    return False 

  def logical_and(self):
    if self.accept('logical_and'):
      return True
    return False

  def logical_or(self):
    if self.accept('logical_or'):
      return True
    return False

  def logical_not(self):
    if self.accept('logical_not'):
      return True
    return False

  def condition_less_than(self):
    pass

  def comparison_operator(self):
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
      return False
    return True

  def logical_expression(self):
    if self.accept('left_parenthesis'):
      self.condition()
      self.expect('right_parenthesis')
    else:
      if self.logical_not():
        self.expression()
        return True
      self.expression()
      if self.accept('ampersand'):
        pass
      
      while True:
        if self.logical_and():
          self.condition()
        elif self.logical_or():
          self.condition()
        else:
          break

  def if_condition(self):
    self.expect('left_parenthesis')
    self.condition()
    self.expect('right_parenthesis')
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
    self.expression() 
     
  def call_function(self):
    self.params()

  def search_tabsym(self, item):
    pass 

class Parsing:

  symtab = []
  ctypes = {
                'I=I': '', 'R=R': '', 'R=I': '', 
                'I+I': 'I', 'I+R': 'R', 'R+I': 'R', 'R+R': 'R', 'S+S': 'S', 
                'I-I': 'I', 'I-R': 'R', 'R-I': 'R', 'R-R': 'R', 
                'I*I': 'I', 'I*R': 'R', 'R*I': 'R', 'R*R': 'R', 'S*S': 'S',
                'I/I': 'I', 'I/R': 'R', 'R/I': 'R', 'R/R': 'R', 
                'I%I': 'I', '-I': 'I', '-R': 'R', 
                'LandL': 'L', 'LorL': 'L', '!L': 'L', 
                'I>I': 'L', 'I>R': 'L', 'R>I': 'L', 'R>R': 'L', 'S>S': 'L',
                'I<I': 'L', 'I<R': 'L', 'R<I': 'L', 'R<R': 'L', 'S<S': 'L',
                'I>=I': 'L', 'I>=R': 'L', 'R>=I': 'L', 'R>=R': 'L',
                'I<=I': 'L', 'I<=R': 'L', 'R<=I': 'L', 'R<=R': 'L',
                'I!=I': 'L', 'I!=R': 'L', 'R!=I': 'L', 'R!=R': 'L',
                'I==I': 'L', 'I==R': 'L', 'R==I': 'L', 'R==R': 'L', 'S==S': 'L'
  }
  ptypes = []
  previous_token = None
  current_token = None

  def __init__(self, token_generator):
    self.token_generator = token_generator
    self.get_token()
    self.program()

  def get_token(self):
    self.previous_token = self.current_token
    self.current_token = next(self.token_generator, None)

  def raise_error(self,type, msg):
    print type, msg
    return False

  def insert_symtab(self, symbol_name, type, scope):
    self.symtab.append({'symbol_name': symbol_name, 'type': type, 'scope': scope})

  def in_symtab(self, symbol_name):
    for sym in self.symtab:
      if symbol_name in sym.values():
        return sym
    return False

  def get_ctype(self, input):
    return self.ctypes.get(input)

  def get_data_type(self):
    if self.current_token['name'] == 'real_number':
      return 'R'
    elif self.current_token['name'] == 'integer_number':
      return 'I'
    elif self.current_token['name'] == 'string':
      return 'S'
    elif self.current_token['name'] == 'boolean':
      return 'B'
    else:
      return self.raise_error('', 'error: se esperaba tipo de dato y se encontro ' + symbol)

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
    if self.accept('identifier', False):
      symtab = self.in_symtab(self.current_token['lexeme'])
      if not symtab:
        self.raise_error('', 'error: el identificador ' + self.current_token['lexeme'] + ' no ha sido identificado')
      else:
        self.ptipos.append(symtab['type'])
      self.get_token()
      return True
    elif self.literal():
      return True
    elif self.enclosure():
      return True
    return False

  def enclosure(self):
    if self.accept('left_parenthesis'):
      if self.expression():
        if self.expect('right_parenthesis'):
          return True
    return False

  def is_boolean(self):
    if self.accept('false'):
      return True
    elif self.accept('true'):
      return True
    return False

  def literal(self):
    if self.accept('string'):
      self.ptypes.append('S')
      return True
    elif self.accept('integer_number'):
      self.ptypes.append('I')
      return True
    elif self.accept('real_number'):
      self.ptypes.append('R')
      return True
    elif self.accept('boolean'):
      self.ptypes.append('B')
      return True
    return False

  def primary(self):
    if self.atom():
      return True
    return False
  
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
        operator = self.previous_token['lexeme']
        if self.u_expression():
          dtype_right = self.ptypes.pop()
          type = str(operator) + dtype_right
          if self.get_ctype(type) is not None:
            self.ptypes.append(self.get_ctype(type))
          else:
            self.raise_error('Error semantico: ', 'Conflicto en tipos en la operacion')
          return True
        else:
          return self.raise_error("", "Falta operador o primary")
      return False

  def get_dtype(self, operator):
    dtype_right = self.ptypes.pop()
    dtype_left = self.ptypes.pop()
    tp = dtype_left + str(operator) + dtype_right
    if self.get_ctype(tp) is not None:
      self.ptypes.append(self.get_ctype(tp))
    else:
      self.raise_error('Error semantico: ', 'Conflicto en tipos en la operacion')

  def m_expression(self):
    if self.u_expression():
      while True:
        if self.accept('arithmetic_multiplication'):
          operator = self.previous_token['lexeme']
          if self.u_expression():
            self.get_dtype(operator)
            continue
          else:
            return False
        elif self.accept('arithmetic_division'):
          operator = self.previous_token['lexeme']
          if self.u_expression():
            self.get_dtype(operator)
            continue
          else:
            return False
        elif self.accept('arithmetic_modulo'):
          operator = self.previous_token['lexeme']
          if self.u_expression():
            self.get_dtype(operator)
            continue
          else:
            return False
        else:
          break
      return True
    return False

  def a_expression(self):
    if self.m_expression():
      while True:
        if self.accept('arithmetic_addition'):
          operator = self.previous_token['lexeme']
          if self.m_expression():
            self.get_dtype(operator)
            continue
          else:
            return self.raise_error("", "Falta operador o primary")
        elif self.accept('arithmetic_subtraction'):
          operator = self.previous_token['lexeme']
          if self.m_expression():
            self.get_dtype(operator)
            continue
          else:
            return self.raise_error("", "Falta operador o primary")
        else:
          break
      return True
    else:
      return False

  def expression(self):
    if self.a_expression():
      return True
    return False

  def program(self):
    while True:
      if self.function_definition():
        continue
      elif self.statement():
        continue
      else:
        break
    print self.ptypes
      

  def function_definition(self):
    if self.accept('function'):
      if self.function_name():
        self.expect('left_parenthesis')
        self.parameter_list()
        self.expect('right_parenthesis')
        self.expect('left_brace')
        while True:
          if self.statement():
            continue
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
      return self.expect('semicolon')
    elif self.augmented_assignment_stmt():
      return self.expect('semicolon')
    elif self.print_stmt():
      return self.expect('semicolon')
    elif self.if_stmt():
      return True 
    elif self.while_stmt():
      return True
    elif self.for_stmt():
      return True
    else:
      return False

  def augmented_assignment_stmt(self):
    if self.augop():
      if self.expression():
        return True
    return False
    
  def assignment_stmt(self):
    if self.target():
      symbol_name = self.current_token['lexeme']
      if self.accept('assignment'):
        if self.expression():
          return True
    return False

  def target(self):
    if self.accept('identifier'):
      return True
    return False 

  def print_stmt(self):
    if self.accept('print'):
      if self.expression():
        return True
    return False

  def augop(self):
    if self.accept('assignment_and_add'):
      return True
    elif self.accept('assignment_and_subtract'):
      return True
    return False

  def comp_operator(self):
    if self.accept('comparison_less_than'):
      return True
    elif self.accept('comparison_less_than_or_equal'):
      return True
    elif self.accept('comparison_equal'):
      return True
    elif self.accept('comparison_greater_than'):
      return True
    elif self.accept('comparison_greter_than_or_equal'):
      return True
    elif self.accept('comparison_equal'):
      return True
    elif self.accept('comparison_not_equal'):
      return True
    return False 

  def comparison(self):
    if self.a_expression():
      while True:
        if self.comp_operator():
          if self.expression():
            continue
          else:
            return self.raise_error("", "Falta expr")
        else:
          break
      return True


  def not_test(self):
    if self.comparison():
      return True
    else:
      if self.accept('not'):
        if self.not_test():
          return True
        else:
          self.raise_error("", "Fallo not_test")
      return False

  def and_test(self):
    if self.not_test():
      while True:
        if self.accept('and'):
          if self.not_test():
            continue
          else:
            return self.raise_error("", "Fallo and_test") 
        else:
          break
      return True
    else:
      return False

  def or_test(self):
    if self.and_test():
      while True:
        if self.accept('or'):
          if self.and_test():
            continue
          else:
            return self.raise_error("", "Fallo or_test") 
        else:
          break
      return True
    else:
      return False

  def conditional_expression(self):
    if self.or_test():
      return True
    return False
         
  def if_stmt(self):
    if self.accept('if'):
      if self.conditional_expression():
        self.expect('left_brace')
        while True:
          if self.statement():
            continue
          else:
            break
        self.expect('right_brace')
      while True:
        if self.accept('elif'):
          if self.conditional_expression():
            self.expect('left_brace')
            while True:
              if self.statement():
                continue
              else:
                break
            self.expect('right_brace')
        else:
          break
      if self.accept('else'):
        self.expect('left_brace')
        while True:
          if self.statement():
            continue
          else:
            break
        self.expect('right_brace')
      return True
    else:
      return False

  def while_stmt(self):
    if self.accept('while'):
      if self.conditional_expression():
        self.expect('left_brace')
        while True:
          if self.statement():
            continue
          else:
            break
        self.expect('right_brace')
      if self.accept('else'):
        self.expect('left_brace')
        while True:
          if self.statement():
            continue
          else:
            break
        self.expect('right_brace')
      return True
    else:
      return False

  def for_stmt(self):
    if self.accept('for'):
      self.expect('left_parenthesis')
      if self.assignment_stmt():
        self.expect('semicolon')
        if self.conditional_expression():
          self.expect('semicolon')
          if self.accept('identifier') and  self.augmented_assignment_stmt():
            self.expect('right_parenthesis')
            self.expect('left_brace')
            while True:
              if self.statement():
                continue
              else:
                break
            self.expect('right_brace')
            return True
    return False



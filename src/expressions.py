from decimal import Decimal
import exceptions
from func import *
class Expression: pass
class Variable: pass
class MathExpression(Expression):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
  def eval(self, val):
    if type(val) != Number:
      val = Number(val) 
      return self.value.eval(val)
class Number(Expression):
  def __init__(self, value):
    if type(value) != Decimal: value = Decimal(value)
    self.value = value
  def __str__(self):
    return str(self.value)
  def __sub__(self, n):
    return Number(self.value-n)
  def __add__(self, n):
    return Number(self.value+n)
  def eval(self, val=0):
    return self.value
class Product(Expression):
  def __init__(self, a, b):
    if type(a) == int or type(a) == float or type(a) == Decimal:
      a = Number(a)
    if type(b) == int or type(b) == float or type(b) == Decimal:
      b = Number(b)
      if (a == None): self.a = Number(1)
      if (b == None): self.b = Number(1)
    self.a = a
    self.b = b
  def __str__(self): return f"{self.a}*{self.b}"
  def eval(self, val):
    if type(val) != Number: val = Number(val)
    return self.a.eval(val) * self.b.eval(val)
class Quotient(Expression):
  def __init__(self, a, b):
    if type(a) == int or type(a) == float or type(a) == Decimal:
      a = Number(a)
      if type(b) == int or type(b) == float or type(b) == Decimal:
        b = Number(b)
      self.a = a
      self.b = b
  def __str__(self): return f"{self.a}/{self.b}"
  def eval(self, val):
    if type(val) != Number:
      val = Number(val)
    return self.a.eval(val) / self.b.eval(val)
class Sum(Expression):
  def __init__(self, a, b):
    if type(a) == int or type(a) == float or type(a) == Decimal:
      a = Number(a)
    if type(b) == int or type(b) == float or type(b) == Decimal:
      b = Number(b)
    self.a = a
    self.b = b
  def __str__(self): return f"({self.a}+{self.b})"
  def eval(self, val):
    if type(val) != Number:
      val = Number(val)
    return self.a.eval(val) + self.b.eval(val)
class Exponent(Expression):
  def __init__(self, x, exp):
    if type(x) == int or type(x) == float or type(x) == Decimal:
      x = Number(x)
    if type(exp) == int or type(exp) == float or type(exp) == Decimal:
      exp = Number(exp)
    self.x = x
    self.exp = exp
  def __str__(self): return f"({self.x})^({self.exp})"
  def eval(self, val):
    if type(val) != Number:
      val = Number(val)
    return self.x.eval(val) ** self.exp.eval(val)
class DependentVariable(Variable):
  def __str__(self):
    return "y"
class DepedentVariableDerivative(Variable):
  def __init__(self, degree=1):
    self.degree = degree
  def __str__(self):
    if self.degree == 1: return f"y{'\''*self.degree}"
class IndependentVariable(Variable):
  def eval(self, val):
    if type(val) != Number:
      val = Number(val)
    return val.eval()
  def __str__(self): return "x"
class Polynomial(Expression):
  def __init__(self, coefficients):
    self.coeff = coefficients
  def eval(self, x):
    return sum([self.coeff[i]*x**(len(self.coeff-1-i)) for i in range(len(self.coeff))])
  def __str__(self):
    "+".join([f"{c}x^{len(self.coeff)-i-1}"] for i, c in enumerate(self.coeff))
class TwoVariableEqurtion:
  def __init__(self, left:Expression, right:Expression):
    self.left = left
    self.right = right
  pass
class Difference(Expression):
  def __init__(self, a, b):
    if type(a) == int or type(a) == float or type(a) == Decimal:
      a = Number(a)
    if type(b) == int or type(b) == float or type(b) == Decimal:
      b = Number(b)
    self.a = a
    self.b = b
  def __str__(self): return f"({self.a}-{self.b})"
  def eval(self, val):
    if type(val) != Number:
      val = Number(val)
    return self.a.eval(val) - self.b.eval(val)
class StdFunction(Expression):
  def __init__(self, ftype, val):
    self.ftype = ftype
    self.val = val
    if ftype == "cos":
      self.derivative = lambda argument: Product(-1, StdFunction("sin", argument, False)) 
    elif ftype == "sin":
      self.derivative = lambda argument: StdFunction("cos", argument, False)
    elif ftype == "tan":
      self.derivative = lambda argument: Quotient(1, Exponent(StdFunction("cos", argument, False), 2)) #replace with sec^2
    elif ftype == "arccos":
      self.derivative = lambda argument: Quotient(-1, Exponent(Difference(1,Exponent(argument,2)),Number(1/2)))
    elif ftype == "arcsin":
      self.derivative = lambda argument: Quotient(-1, Exponent(Difference(1, Exponent(argument,2)),Number(1/2)))
    elif ftype == "arctan":
      self.derivative = lambda argument: Quotient(1, Sum(1, Exponent(argument,2)))
    elif ftype == "ln":
      self.derivative = lambda argument: Exponent(argument, -1)
    else:
      raise(exceptions.UnknownStdFunc)
  def __str__(self):
    return f"{self.ftype}({self.val})"
  def eval(self, x):
    if self.ftype == "cos":
      return cos(x)
    elif self.ftype == "sin":
      return sin(x)
    elif self.ftype == "tan":
      return tan(x)
    elif self.ftype == "sec":
      return sec(x)
    elif self.ftype == "csc":
      return csc(x)
    elif self.ftype == "cot":
      return cot(x)
    elif self.ftype == "ln":
      return ln(x)
def simplify(exp):
  if type(exp) == Product or type(exp) == Sum or type(exp) == Difference:
    exp.a = simplify(exp.a)
    exp.b = simplify(exp.b)
  elif type(exp) == Exponent:
    exp.x = simplify(exp.x)
    exp.exp = simplify(exp.exp)
  elif type(exp) == StdFunction:
    exp.val = simplify(exp.val)
  elif type(exp) == MathExpression:
    exp.value = simplify(exp.value)
  

  if type(exp) == MathExpression: return simplify(exp.value)
  elif type(exp) == Product:
    if type(exp.a) == Number and exp.a.value == 1: return simplify(exp.b) #fix this
    elif type(exp.b) == Number and exp.b.value == 1: return simplify(exp.a)
    elif type(exp.a) == Number and exp.a.value == 0: return Number(0)
    elif type(exp.b) == Number and exp.b.value == 0: return Number(0)
  elif type(exp) == Quotient:
    if exp.b == Number(1): return simplify(exp.a)
    elif type(exp.b) == Quotient: exp = Product(exp.a, Quotient(exp.b.b, exp.b.a))
  elif type(exp) == StdFunction:
    if exp.ftype == "ln":
      if type(exp.val) == Exponent:
        return Product(simplify(exp.val.exp), simplify(StdFunction("ln", simplify(exp.val.x))))
      elif type(exp.val) == Product:
        return Sum(simplify(StdFunction("ln", simplify(exp.val.a))), simplify(StdFunction("ln", simplify(exp.val.b))))
      elif type(exp.val) == Quotient:
        return Difference(simplify(StdFunction("ln", simplify(exp.val.a))), simplify(StdFunction("ln", simplify(exp.val.b))))
  elif type(exp) == Exponent:
    if type(exp.x) == Exponent:
      return Exponent(simplify(exp.x.x), simplify(Product(exp.x.exp, exp.exp)))
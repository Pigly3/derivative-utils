from decimal import Decimal
import exceptions
from func import *

def ensureNumber(x):
  return Number(x) if not isinstance(x, Number) else x
def convertNumber(x):
  return Number(x) if isinstance(x, int) or isinstance(x, float) or isinstance(x, Decimal) else x

class Expression:
  def __add__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Sum(self, n))
  def __radd__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Sum(n, self))
  def __sub__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Difference(self, n))
  def __rsub__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Difference(n, self))
  def __mul__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Product(self, n))
  def __rmul__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Product(n, self))
  def __truediv__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Quotient(self, n))
  def __rtruediv__(self, n):
    if not isinstance(n, Expression): n = Number(n)
    return simplify(Quotient(n, self))
  def __pow__(self, n):
    return simplify(Exponent(self, n))
  def __rpow__(self, n):
    return simplify(Exponent(n, self))
class Variable(Expression): pass
class MathExpression(Expression):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
  def eval(self, val):
    if not isinstance(val, Number):
      val = Number(val) 
      return self.value.eval(val)
class Number(Expression):
  def __init__(self, value):
    if not isinstance(value, Decimal): value = Decimal(value)
    self.value = value
  def __str__(self):
    return str(self.value)
  def eval(self, val=0):
    return self.value

class Product(Expression):
  def __init__(self, a, b):
    if (a == None): self.a = Number(1)
    if (b == None): self.b = Number(1)
    a = convertNumber(a)
    b = convertNumber(b)
    self.a = a
    self.b = b
  def __str__(self): return f"{self.a}*{self.b}"
  def eval(self, val):
    if not isinstance(val, Number): val = Number(val)
    return self.a.eval(val) * self.b.eval(val)
class Quotient(Expression):
  def __init__(self, a, b):
    a = convertNumber(a)
    b = convertNumber(b)
    self.a = a
    self.b = b
  def __str__(self): return f"{self.a}/{self.b}"
  def eval(self, val):
    if type(val) != Number:
      val = Number(val)
    return self.a.eval(val) / self.b.eval(val)
class Sum(Expression):
  def __init__(self, a, b):
    a = convertNumber(a)
    b = convertNumber(b)
    self.a = a
    self.b = b
  def __str__(self): return f"({self.a}+{self.b})"
  def eval(self, val):
    val = ensureNumber(val)
    return self.a.eval(val) + self.b.eval(val)
class Exponent(Expression):
  def __init__(self, x, exp):
    x = convertNumber(x)
    exp = convertNumber(exp)
    self.x = x
    self.exp = exp
  def __str__(self): return f"({self.x})^({self.exp})"
  def eval(self, val):
    val = ensureNumber(val)
    return self.x.eval(val) ** self.exp.eval(val)
class Y(Variable):
  def __str__(self):
    return "y"
class DyDx(Variable):
  def __init__(self, degree=1):
    self.degree = degree
  def __str__(self):
    if self.degree == 1: return f"y{'\''*self.degree}"
class X(Variable):
  def eval(self, val):
    val = ensureNumber(val)
    return val.eval()
  def __str__(self): return "x"
class Polynomial(Expression):
  def __init__(self, coefficients):
    self.coeff = coefficients
  def eval(self, x):
    return sum([self.coeff[i]*x**(len(self.coeff-1-i)) for i in range(len(self.coeff))])
  def __str__(self):
    "+".join([f"{c}x^{len(self.coeff)-i-1}"] for i, c in enumerate(self.coeff))
class TwoVariableEquation:
  def __init__(self, left:Expression, right:Expression):
    self.left = left
    self.right = right
  pass
class Difference(Expression):
  def __init__(self, a, b):
    a = convertNumber(a)
    b = convertNumber(b)
    self.a = a
    self.b = b
  def __str__(self): return f"({self.a}-{self.b})"
  def eval(self, val):
    val = ensureNumber(val)
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
    elif ftype == "csc":
      self.derivative = lambda argument: -1*Product(csc(argument), cot(argument))
    elif ftype == "sec":
      self.derivative = lambda argument: Product(tan(argument), sec(argument))
    elif ftype == "cot":
      self.derivative = lambda argument: -1*Exponent(csc(argument), 2)
    else:
      raise(exceptions.UnknownStdFunc)
  def __str__(self):
    return f"{self.ftype}({self.val})"
  def eval(self, x):
    if self.ftype == "cos":
      return cosine(x)
    elif self.ftype == "sin":
      return sine(x)
    elif self.ftype == "tan":
      return tangent(x)
    elif self.ftype == "sec":
      return secant(x)
    elif self.ftype == "csc":
      return cosecant(x)
    elif self.ftype == "cot":
      return cotangent(x)
    elif self.ftype == "ln":
      return logn(x)
    elif self.ftype == "arcsin":
      return arcsine(x)
    elif self.ftype == "arccos":
      return arccosine(x)
    elif self.ftype == "arctan":
      return arctangent(x)

#standard function bindings
def ln(exp:Expression): return StdFunction("ln", exp)
def sin(exp:Expression): return StdFunction("sin", exp)
def cos(exp:Expression): return StdFunction("cos", exp)
def tan(exp:Expression): return StdFunction("tan", exp)
def arcsin(exp:Expression): return StdFunction("arcsin", exp)
def arccos(exp:Expression): return StdFunction("arccos", exp)
def arctan(exp:Expression): return StdFunction("arctan", exp)
def csc(exp:Expression): return StdFunction("csc", exp)
def sec(exp:Expression): return StdFunction("sec", exp)
def cot(exp:Expression): return StdFunction("cot", exp)

def simplify(exp):
  if isinstance(exp, Product) or isinstance(exp, Sum) or isinstance(exp, Difference) or isinstance(exp, Quotient):
    exp.a = simplify(exp.a)
    exp.b = simplify(exp.b)
  elif isinstance(exp, Exponent):
    exp.x = simplify(exp.x)
    exp.exp = simplify(exp.exp)
  elif isinstance(exp, StdFunction):
    exp.val = simplify(exp.val)
  elif isinstance(exp, MathExpression):
    exp.value = simplify(exp.value)
  

  if isinstance(exp, MathExpression): return simplify(exp.value)
  elif isinstance(exp, Product):
    if isinstance(exp.a, Number) and exp.a.value == 1: return simplify(exp.b)
    elif isinstance(exp.b, Number) and exp.b.value == 1: return simplify(exp.a)
    elif isinstance(exp.a, Number) and exp.a.value == 0: return Number(0)
    elif isinstance(exp.b, Number) and exp.b.value == 0: return Number(0)
    elif isinstance(exp.a, Number) and isinstance(exp.b, Number):
      return Number(exp.a.value*exp.b.value)
    elif isinstance(exp.a, Product):
      if isinstance(exp.b, Number):
        if isinstance(exp.a.a, Number):
          return simplify(Product(exp.b.value*exp.a.a.value, exp.a.b))
        elif isinstance(exp.a.b, Number):
          return simplify(Product(exp.b.value*exp.a.b.value, exp.a.a))
    elif isinstance(exp.b, Product):
      if isinstance(exp.a, Number):
        if isinstance(exp.b.a, Number):
          return simplify(Product(exp.a*exp.b.a, exp.b.b))
        elif isinstance(exp.b.b, Number):
          return simplify(Product(exp.a*exp.b.b, exp.b.a))
  elif isinstance(exp, Quotient):
    if exp.b == Number(1): return simplify(exp.a)
    elif isinstance(exp.b, Quotient): exp = Product(exp.a, Quotient(exp.b.b, exp.b.a))
    elif isinstance(exp.a, Number):
      if isinstance(exp.b, Exponent):
        return simplify(Product(exp.a, Exponent(exp.b.x, Product(-1, exp.b.exp))))
      else:
        return simplify(Product(exp.a, Exponent(exp.b, -1)))
  elif isinstance(exp, StdFunction):
    if exp.ftype == "ln":
      if isinstance(exp.val, Exponent):
        return Product(simplify(exp.val.exp), simplify(StdFunction("ln", simplify(exp.val.x))))
      elif isinstance(exp.val, Product):
        return Sum(simplify(StdFunction("ln", simplify(exp.val.a))), simplify(StdFunction("ln", simplify(exp.val.b))))
      elif isinstance(exp.val, Quotient):
        return Difference(simplify(StdFunction("ln", simplify(exp.val.a))), simplify(StdFunction("ln", simplify(exp.val.b))))
  elif isinstance(exp, Exponent):
    if isinstance(exp.x, Exponent):
      return simplify(Exponent(exp.x.x, Product(exp.x.exp, exp.exp)))
    elif isinstance(exp.exp, Number) and exp.exp.value == 1:
      return simplify(exp.x)
  elif isinstance(exp, Sum):
    if isinstance(exp.a, Number) and isinstance(exp.b, Number):
      return Number(exp.a.value + exp.b.value)
    elif isinstance(exp.a, Number) and exp.a.value == 0:
      return exp.b
    elif isinstance(exp.b, Number) and exp.b.value == 0:
      return exp.a
  elif isinstance(exp, Difference):
    if isinstance(exp.a, Number) and isinstance(exp.b, Number):
      return Number(exp.a.value - exp.b.value)
    elif isinstance(exp.b, Number) and exp.b == 0:
      return exp.a
  return exp
from derivative_utils.expressions import *
from derivative_utils.dat import *

def differentiate(func, order=1):
  func = simplify(func)

  if order > 1: func = differentiate(func)
  if isinstance(func, X): return Number(1)
  elif isinstance(func, Quotient):
    return simplify(Quotient(Difference(Product(differentiate(func.a), func.b),Product(differentiate(func.b), func.a)),Exponent(func.b,2)))
  elif isinstance(func, Product):
    if not isinstance(func.a, Number) and not isinstance(func.a, Number): return simplify(Sum(Product(differentiate(func.a), func.b),Product(differentiate(func.b), func.a)))
    elif not isinstance(func.a, Number): return simplify(Product(differentiate(func.a), func.b))
    elif not isinstance(func.b, Number): return simplify(Product(differentiate(func.b), func.a))
  elif isinstance(func, Sum): return simplify(Sum(differentiate(func.a), differentiate(func.b)))
  elif isinstance(func, Difference): return simplify(Difference(differentiate(func.a), differentiate(func.b)))
  elif isinstance(func, Exponent):
    if not isinstance(func.x, Number) and not isinstance(func.exp, Number):
      return simplify(differentiate(Exponent(e, Product(StdFunction("ln"), func.exp))))
    elif not isinstance(func.x, Number): return simplify(Product(differentiate(func.x), Product(func.exp, Exponent(func.x, func.exp - 1))))
    elif not isinstance(func.exp, Number): return simplify(Product(StdFunction("ln").eval(func.x), Product(differentiate(func.exp), func)))
    else: return Number(0)
  elif isinstance(func, StdFunction):
    return simplify(Product(differentiate(func.val), func.derivative(func.val)))
  elif isinstance(func, X): return Number(1)
  elif isinstance(func, Number): return Number(0)
  elif isinstance(func, Polynomial):
    coeff = func.coeff[:]
    coeff.pop()
    coeff = [c*(len(coeff)-i) for i,c in enumerate(coeff)]
    return Polynomial(coeff)
  elif isinstance(func, Y):
    return DyDx()
  elif isinstance(func, DyDx):
    return DyDx(func.degree + 1)
def partial(func:Expression, var:str, order=1):
  func = simplify(func)

  if order > 1: func = differentiate(func, var, order-1)

  if isinstance(func, Variable): return Number(1 if func.name == var else 0)
  elif isinstance(func, Quotient):
    return simplify(Quotient(Difference(Product(differentiate(func.a), func.b),Product(differentiate(func.b), func.a)),Exponent(func.b,2))) 
  elif isinstance(func, Product): #working here
    if not isinstance(func.a, Number) and not isinstance(func.a, Number) and not hasVarName(func.a, var) and not hasVarName(func.b, var): return simplify(Sum(Product(differentiate(func.a), func.b),Product(differentiate(func.b), func.a)))
    elif not isinstance(func.a, Number) and not hasVarName(func.a, var): return simplify(Product(differentiate(func.a), func.b))
    elif not isinstance(func.b, Number) and not hasVarName(func.b, var): return simplify(Product(differentiate(func.b), func.a))
  elif isinstance(func, Sum): return simplify(Sum(differentiate(func.a), differentiate(func.b)))
  elif isinstance(func, Difference): return simplify(Difference(differentiate(func.a), differentiate(func.b)))
  elif isinstance(func, Exponent):
    if not isinstance(func.x, Number) and not isinstance(func.exp, Number):
      return simplify(differentiate(Exponent(e, Product(StdFunction("ln"), func.exp))))
    elif not isinstance(func.x, Number): return simplify(Product(differentiate(func.x), Product(func.exp, Exponent(func.x, func.exp - 1))))
    elif not isinstance(func.exp, Number): return simplify(Product(StdFunction("ln").eval(func.x), Product(differentiate(func.exp), func)))
    else: return Number(0)
  elif isinstance(func, StdFunction):
    return simplify(Product(differentiate(func.val), func.derivative(func.val)))
  elif isinstance(func, Number): return Number(0)

def implicitlyDifferentiate(equation:TwoVariableEquation):
  return TwoVariableEquation(differentiate(equation.left), differentiate(equation.right))

def gradient(func, variables:tuple[str]):
  return Vector([partial(func, var) for var in variables])
from expressions import *
from dat import *
def differentiate(func):
  if type(func) == IndependentVariable: return Number(1)
  elif type(func) == Quotient:
    return Quotient(Difference(Product(differentiate(func.a), func.b),Product(differentiate(func.b), func.a)),Exponent(func.b,2))
  elif type(func) == Product:
    if type(func.a) != Number and type(func.a) != Number: return Sum(Product(differentiate(func.a), func.b),Product(differentiate(func.b), func.a))
    elif type(func.a) != Number: return Product(differentiate(func.a), func.b)
    elif type(func.b) != Number: return Product(differentiate(func.b), func.a)
  elif type(func) == Sum: return Sum(differentiate(func.a), differentiate(func.b))
  elif type(func) == Difference: return Difference(differentiate(func.a), differentiate(func.b))
  elif type(func) == Exponent:
    if type(func.x) != Number and type(func.exp) != Number:
      return differentiate(Exponent(e, Product(StdFunction("ln"), func.exp)))
    elif type(func.x) != Number: return simplify(Product(differentiate(func.x), Product(func.exp, Exponent(func.x, func.exp - 1))))
    elif type(func.exp) != Number: return simplify(Product(StdFunction("ln").eval(func.x), Product(differentiate(func.exp), func)))
    else: return Number(0)
  elif type(func) == StdFunction:
    return simplify(Product(differentiate(func.val), func.derivative(func.val)))
  elif type(func) == IndependentVariable:
    return Number(1)
  elif type(func) == Number: return Number(0)
  elif type(func) == Polynomial:
    coeff = func.coeff[:]
    coeff.pop()
    coeff = [c*(len(coeff)-i) for i,c in enumerate(coeff)]
    return Polynomial(coeff)
  elif type(func) == DependentVariable:
    return DepedentVariableDerivative()
  elif type(func) == DepedentVariableDerivative:
    return DepedentVariableDerivative(func.degree + 1)
def implicitlyDifferentiate(equation:TwoVariableEqurtion):
  return TwoVariableEqurtion(differentiate(equation.left), differentiate(equation.right))
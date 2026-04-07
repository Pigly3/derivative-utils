from util import *
from const import *
from decimal import Decimal
from expressions import *
def cos(x, terms=100, places=12):
    o = 0
    x = x % (2*pi)
    multiplier = 1
    if x > pi:
      x = x - pi
      multiplier = -1
    for i in range(terms):
        c = [1, 0, -1, 0][i % 4]
        o += Decimal(c*x**i)/Decimal(factorial(i))
    return round(multiplier*o,places)
def sin(x, terms=100, places=12):
    o = 0
    x = (x + pi/2) % (2*pi) - pi/2
    for i in range(terms):
        c = [0, 1, 0, -1][i % 4]
        o += (c*x**i)/factorial(i)
    return round(o,places)
def tan(x, terms=100):
    try: return sin(x, terms)/cos(x, terms)
    except ZeroDivisionError: pass
def sec(x, terms=100):
    v = cos(x, terms)
    if v == 0: return
    else: return 1/v
def csc(x, terms=100):
    v = sin(x, terms)
    if v == 0: return
    else: return 1/v
def cot(x, terms=100):
    try: return cos(x, terms)/sin(x, terms)
    except ZeroDivisionError: pass
def exp(x, terms=100):
  o = 0
  if type(x) == Number: x = x.eval()
  for i in range(terms):
    o += x**i/factorial(i)
  return o
def ln(x, prec=0.000001):
  guess = 0
  while abs(exp(guess) - x) > prec:
    guess -= (exp(guess) - x)/exp(guess)
  return guess

from expressions import *
from __init__ import differentiate
def newtonMethod(function:MathExpression, prec=0.01, maxTries=1000):
  guess = 0
  tries = 0
  while abs(function.eval(guess)) > prec and tries < maxTries:
    guess -= function.eval(guess)/differentiate(function).eval(guess)
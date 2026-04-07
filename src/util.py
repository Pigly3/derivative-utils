from expressions import *
from __init__ import differentiate
def factorial(n):
  o = 1
  if n == 0:
    return o
  for i in [t+1 for t in range(n)]:
    o*= i
  return o
def newtonMethod(function:MathExpression, prec=0.01, maxTries=1000):
  guess = 0
  tries = 0
  while abs(function.eval(guess)) > prec and tries < maxTries:
    guess -= function.eval(guess)/differentiate(function).eval(guess)
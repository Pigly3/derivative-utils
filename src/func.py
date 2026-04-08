from util import *
from const import *
from decimal import Decimal
from expressions import *

def cosine(x, terms=100, places=12):
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
def sine(x, terms=100, places=12):
    o = 0
    x = (x + pi/2) % (2*pi) - pi/2
    for i in range(terms):
        c = [0, 1, 0, -1][i % 4]
        o += (c*x**i)/factorial(i)
    return round(o,places)
def tangent(x, terms=100):
    try: return sine(x, terms)/cosine(x, terms)
    except ZeroDivisionError: pass
def secant(x, terms=100):
    v = cosine(x, terms)
    if v == 0: return
    else: return 1/v
def cosecant(x, terms=100):
    v = sine(x, terms)
    if v == 0: return
    else: return 1/v
def cotangent(x, terms=100):
    try: return cosine(x, terms)/sine(x, terms)
    except ZeroDivisionError: pass
def exponential(x, terms=100):
  o = 0
  if type(x) == Number: x = x.eval()
  for i in range(terms):
    o += x**i/factorial(i)
  return o
def logn(x, prec=0.000001):
  guess = 0
  while abs(exponential(guess) - x) > prec:
    guess -= (exponential(guess) - x)/exponential(guess)
  return guess
def arcsine(x, prec=0.000001):
  guess = 0
  while abs(sine(guess) - x) > prec:
    guess -= (sine(guess) - x)/sine(guess)
  return (guess + pi/2) % pi - pi/2
def arccosine(x, prec=0.000001):
  guess = 0
  while abs(cosine(guess) - x) > prec:
    guess -= (cosine(guess) - x)/cosine(guess)
  return (guess) % pi
def arctangent(x, prec=0.000001):
  guess = 0
  while abs(tangent(guess) - x) > prec:
    guess -= (tangent(guess) - x)/tangent(guess)
  return (guess + pi/2) % pi - pi/2
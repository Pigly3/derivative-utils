def factorial(n):
  o = 1
  if n == 0:
    return o
  for i in [t+1 for t in range(n)]:
    o*= i
  return o
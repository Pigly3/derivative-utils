import json
class Table:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def display(self):
    pass
  def json(self):
    return json.dumps({"x":self.x, "y": self.y})
  def obj(self):
    return {"x":self.x, "y": self.y}
def table(expression, xL:list):
  yL = []
  for x in xL:
    yL.append(expression.eval(x))
  return Table(xL, yL)
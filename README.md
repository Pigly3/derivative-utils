# derivative-utils
![PyPI - Version](https://img.shields.io/pypi/v/derivative-utils)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A simple package for working with derivatives.
This is in alpha, and may not work as intended.


### Get exact expressions for derivatives
```
from derivative-utils import differentiate
from derivative-utils.expressions import *

y = X()*StdFunction("ln", X())
dydx = differentiate(y)
print(dydx)
```
The package will return `(ln(x)+(x)^(-1)*x)`.

Expressions support addition, subtraction, multiplication, division, and exponentiation.
Expressions will be automatically simplified, although current simplifcation is not perfect.
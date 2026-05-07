from typing import Protocol

from sympy import Rational
from sympy import symbols
from sympy.core.expr import Expr

from .model import RandomModel
from .observable import Observable

n = symbols("n", integer=True)


class Statistic(Protocol):

    model: RandomModel
    observable: Observable

    def __init__(self, model: RandomModel, observable: Observable):
        self.model = model
        self.observable = observable

    def __call__(self, size: int, *parameters) -> Rational:
        obj = self.model(size, *parameters)
        return self.observable(obj)

    def expectation(self) -> Expr: ...

    def moment(self, k: int = 1) -> Expr: ...

    def cumulant(self, k: int = 1) -> Expr: ...

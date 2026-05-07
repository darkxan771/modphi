# Defines Observable, ObserbableCombination and ObservableAlgebra

from typing import Protocol

from sympy import Rational

from .object import CombinatorialObject


class Observable(Protocol):
    category: str
    label: CombinatorialObject

    def __call__(self, obj: CombinatorialObject) -> Rational: ...

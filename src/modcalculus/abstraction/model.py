# Defines a generic class RandomModel

from typing import Protocol

from .object import CombinatorialObject


class RandomModel(Protocol):

    category: str

    def __call__(self, size: int, *parameters) -> CombinatorialObject: ...

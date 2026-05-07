from typing import Any, Protocol
from collections.abc import Callable


class CombinatorialObject(Protocol):
    category: str

    def __repr__(self) -> str:
        return f"{self.category.capitalize()} with size {abs(self)}"

    def __abs__(self) -> int: ...

    def __len__(self) -> int: ...

    def __eq__(self, other) -> bool:
        return self.convert("code") == other.convert("code")

    @property
    def size(self) -> int:
        return abs(self)

    @property
    def length(self) -> int:
        return len(self)

    @property
    def convert(self) -> Callable[[str], Any]:
        from .conversions import conversions

        return lambda S: conversions[(self.category, S)](self)

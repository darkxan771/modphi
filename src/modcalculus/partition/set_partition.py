# Defines SetPartition, which is used in particular to compute cumulants from
# moments

# TODO: equitable set partition for a graph
from __future__ import annotations

from reprlib import Repr
from typing import Iterable, Sequence

import numpy as np

from ..abstraction import CombinatorialObject
from .integer_partition import IntegerPartition


class SetPartition(CombinatorialObject):
    """
    A class for the manipulation of set partitions of integer sets.

    Internally, a set partition P is saved as a dictionary {k: P[k]},
    where k runs over the set of indices of the parts, and P[k]
    is the k-th part, saved as a sorted list of integers. The parts
    are themselves sorted according to their minimal element.
    """

    def _partial_init(self, L: Sequence[Sequence[int]], ordered=False) -> list:
        if any([len(p) == 0 for p in L]):
            raise ValueError("One of the parts is empty.")
        S = [x for p in L for x in p]
        S.sort()
        if any([S[i] == S[i + 1] for i in range(len(S) - 1)]):
            raise ValueError("The parts are not disjoint.")
        M = list(list(p) for p in L)
        if not ordered:
            M.sort(key=lambda p: min(p))
        return M

    def __init__(self, L: Sequence[Sequence[int]]):
        self.category = "set partition"
        self.dictionary = {}
        M = self._partial_init(L)
        for k in range(len(L)):
            self.dictionary[k] = M[k]
            self.dictionary[k].sort()

    def __repr__(self) -> str:
        return f"Set partition {Repr(maxdict=10).repr(self.dictionary)}"

    def __call__(self, k: int) -> list[int]:
        return self.dictionary[k]

    def __abs__(self) -> int:
        return len(self.set)

    def __len__(self) -> int:
        return len(list(self.dictionary.keys()))

    def is_standard(self) -> bool:
        return self.set == list(range(self.size))

    def is_discrete(self) -> bool:
        """
        Checks whether the set partition consists in singletons.
        """
        return len(self) == abs(self)

    def __le__(self, other) -> bool:
        res = (self.set == other.set) and all(
            any(set(p).issubset(set(q)) for q in other.parts)
            for p in self.parts
        )
        return bool(res)

    @property
    def set(self) -> list[int]:
        """
        The set underlying the set partition.
        """
        res = sum([self(k) for k in range(self.length)], [])
        res.sort()
        return res

    @property
    def composition(self) -> list[int]:
        """
        The lengths of the parts of the set partition.
        """
        return [len(self(k)) for k in range(self.length)]

    @property
    def partition(self) -> IntegerPartition:
        """
        The lengths of the parts of the set partition, reordered in
        a non-increasing sequence (integer partition).
        """
        c = self.composition
        c.sort(reverse=True)
        return IntegerPartition(c)

    @property
    def parts(self) -> Iterable:
        """
        The parts of the set partition.
        """
        return (self(k) for k in range(self.length))

    def find(self, x: int) -> int:
        """
        Finds the index of the part of the set partition which contains x.
        """
        if x not in self.set:
            raise ValueError(f"{x} is not in the set partition")
        else:
            res = [x in p for p in self.parts]
            return res.index(True)


class OrderedSetPartition(SetPartition):
    def __init__(self, L: Sequence[Sequence[int]]):
        self.category = "set partition"
        self.dictionary = {}
        M = self._partial_init(L, True)
        for k in range(len(L)):
            self.dictionary[k] = M[k]
            self.dictionary[k].sort()

    def __repr__(self) -> str:
        return f"Ordered set partition {Repr(maxdict=10).repr(self.dictionary)}"

    def __le__(self, other) -> bool:
        S = self.set
        res = S == other.set
        if res:
            map_parts = -np.ones(len(self), dtype=np.int64)
            for i in range(len(self)):
                for j in range(len(other)):
                    if set(self(i)).issubset(set(other(j))):
                        map_parts[i] = j
            res *= np.all(map_parts >= 0) and np.all(np.diff(map_parts) >= 0)
        return bool(res)

    def split_part(self, P: OrderedSetPartition) -> OrderedSetPartition:
        L = list(self.parts)
        k = L.index(P.set)
        M = L[:k] + list(P.parts) + L[k + 1 :]
        return OrderedSetPartition(M)

# Conversions of CombinatorialObjects into other types

from typing import Callable

import numpy as np

FromTo = tuple[str, str]


def adjacency_to_code(A: np.ndarray) -> tuple:
    n = A.shape[0]
    return tuple(A[i, j] for i in range(n) for j in range(i + 1, n))


conversions: dict[FromTo, Callable] = {}
conversions[("partition", "code")] = lambda P: tuple(P.parts)
conversions[("partition", "dictionary")] = lambda P: P.dictionary
conversions[("set partition", "code")] = lambda P: tuple(
    tuple(p) for p in P.parts
)
conversions[("graph", "code")] = lambda G: (
    tuple(G.nodes),
    adjacency_to_code(G.adjacency),
)
conversions[("graph", "networkx")] = lambda G: G.graph
conversions[("set partition", "dictionary")] = lambda P: P.dictionary

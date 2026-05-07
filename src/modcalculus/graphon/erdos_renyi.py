import scipy.stats as scs

from ..abstraction import RandomModel
from .graph import Graph


class ErdosRenyi(RandomModel):

    def __init__(self):
        self.category = "graph"

    def __call__(self, size: int, *parameters) -> Graph:
        V = range(size)
        E = []
        p = parameters[0]
        for j in range(size):
            for i in range(j):
                if scs.bernoulli(p).rvs():
                    E.append((i, j))
        return Graph(V, E)

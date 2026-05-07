# Defines Graph and IsomorphismClassGraph

# TODO: draw_graph_function/graphon
# subgraph count = number of graph morphisms
# subgraph densities = that divided by n^k

# TODO: (HARD) express cumulant limites in the algebra of observables

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..abstraction import CombinatorialObject
from ..partition import OrderedSetPartition


class Graph(CombinatorialObject):
    def __init__(self, V: Iterable, E: Iterable):
        self.category = "graph"
        self.graph = nx.Graph()
        W = list(V)
        F = list(E)
        W.sort()
        F.sort()
        self.graph.add_nodes_from(W)
        self.graph.add_edges_from(F)

    def __abs__(self) -> int:
        return self.graph.number_of_nodes()

    def __len__(self) -> int:
        return self.graph.number_of_edges()

    @property
    def adjacency(self) -> np.ndarray:
        """
        Returns the adjacency matrix of the graph.
        """
        return nx.adjacency_matrix(self.graph).toarray()

    @property
    def nodes(self) -> list:
        """
        Returns the list of nodes of the graph.
        """
        return list(self.graph.nodes)

    @property
    def edges(self) -> list:
        """
        Returns the list of edges of the graph.
        """
        return list(self.graph.edges)

    def is_standard(self) -> bool:
        """
        Checks whether the set of nodes is [0, n-1].
        """
        return self.nodes == list(range(abs(self)))

    def degree(self, x, V: None | list = None) -> int:
        """
        Computes the global degree of the vertex x, or the relative degree
        with respect to the node set V.
        """
        if V is None:
            G = self.convert("networkx")
            return G.degree[x]
        else:
            return sum([(x, v) in self.graph.edges for v in V])

    ### MCKAY

    def reorder(self, P: OrderedSetPartition) -> Graph:
        """
        Returns an isomorphic graph, constructed by using the permutation
        associated to a discrete ordered set partition.
        """
        if not P.is_discrete():
            raise ValueError(f"{P} is not a discrete ordered set partition")
        V = self.nodes
        sigma = {i: P.find(i) for i in V}
        E = [(sigma[i], sigma[j]) for (i, j) in self.edges]
        return Graph(range(len(V)), E)

    def standardize_node_set(self) -> Graph:
        """
        Returns an isomorphic graph with node set [0, n-1].
        """
        if self.is_standard():
            return self
        else:
            P = OrderedSetPartition([[n] for n in self.nodes])
            return self.reorder(P)

    def shatters(self, P: OrderedSetPartition, i: int, j: int) -> bool:
        """
        Checks whether the j-th part of P shatters the i-th part of P relatively
        to the graph.
        """
        return not bool(
            np.all(np.diff(np.array([self.degree(v, P(j)) for v in P(i)])) == 0)
        )

    def shattering(self, Vi: list, Vj: list) -> OrderedSetPartition:
        """
        Shatters the part Vi by using the set of nodes Vj, and returns the
        corresponding ordered set partition of Vi.
        """
        d = defaultdict(list)
        for v in Vi:
            d[self.degree(v, Vj)].append(v)
        D = list(d.keys())
        D.sort()
        return OrderedSetPartition([d[k] for k in D])

    def is_equitably_partitioned(self, P: OrderedSetPartition) -> bool:
        """
        Checks whether the ordered set partition P is equitable for the graph.
        """
        L = len(P)
        return all(
            not self.shatters(P, i, j) for i in range(L) for j in range(L)
        )

    def equitable_refinement_procedure(
        self, P: OrderedSetPartition
    ) -> OrderedSetPartition:
        """
        Returns the coarsest equitable partition among ordered set partitions Q
        which are finer than P.
        """
        B = [
            (i, j)
            for i in range(len(P))
            for j in range(len(P))
            if self.shatters(P, i, j)
        ]
        if B == []:
            return P
        else:
            i, j = min(B)
            Q = self.shattering(P(i), P(j))
            Pplus = P.split_part(Q)
            return self.equitable_refinement_procedure(Pplus)

    def splitting_procedure(
        self, P: OrderedSetPartition, x: int
    ) -> OrderedSetPartition:
        """
        Extracts the element x from its part in P, and then computes the
        coarsest equitable partition finer than the new ordered ordered
        set partition.
        """
        k = P.find(x)
        if len(P(k)) == 1:
            return P
        else:
            L = list(P(k))
            L.remove(x)
            Q = OrderedSetPartition([[x], L])
            Pplus = P.split_part(Q)
            return self.equitable_refinement_procedure(Pplus)

    def mckay(self) -> Graph:
        """
        Determines a canonical representative of the isomorphism class of the
        graph.
        """
        L = [
            self.equitable_refinement_procedure(
                OrderedSetPartition([self.nodes])
            )
        ]
        Ltest = [P.is_discrete() for P in L]
        while False in Ltest:
            i = Ltest.index(False)
            _ = Ltest.pop(i)
            P = L.pop(i)
            k = 0
            while len(P(k)) == 1:
                k += 1
            for x in P(k):
                Q = self.splitting_procedure(P, x)
                L.append(Q)
                Ltest.append(Q.is_discrete())
        candidates = [self.reorder(P) for P in L]
        return max(candidates, key=lambda H: H.convert("code")[1])

    def is_isomorphic(self, other: Graph) -> bool:
        """
        Checks whether the other graph is isomorphic.
        """
        return self.mckay() == other.mckay()

    def draw(self, **parameters) -> None:
        """
        Draws the graph.
        """
        _, ax0 = plt.subplots()
        nx.draw_networkx(self.graph, ax=ax0, **parameters)
        ax0.set_axis_off()
        ax0.set_aspect(1)
        plt.show()


class IsomorphismClassGraph(Graph):
    def __init__(self, V: Iterable, E: Iterable):
        G = Graph(V, E).mckay()
        V2 = G.nodes
        E2 = G.edges
        Graph.__init__(self, V2, E2)

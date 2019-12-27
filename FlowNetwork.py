from Graph import Graph, Vertex

class NegativeCapacityException(Exception):
    pass

class Network(Graph):
    """
    A flow network. Inherits from a Graph, since there are still nodes and edges, but each edge has a corresponding
    capacity. Any "flow" pushed through this edge cannot exceed this capacity, and the maximum possible amount of flow
    that can exist at any point in the graph is the sum of all the capacities leaving the source node.

    Also includes a residual network that maps edges to "extra flow" that can be pushed through (note: residual flow
    can go backwards as well to "undo" flow that has already been pushed, if using Ford Fulkerson for max flow).
    """
    def __init__(self, source, sink, vertices=None, edges=None, capacities=None):
        if vertices is None or edges is None or capacities is None:
            self.capacities = {}
            super(Network, self).__init__({source, sink}, {}, self.capacities)
        else:
            self.capacities = capacities  # Maps u -> {v1: c1, v2: c2, ... }, ...; must be a mapping w "weighted" edges
            super(Network, self).__init__(vertices, edges, capacities)
        self.source = source  # Source node S
        self.sink = sink  # Sink node T
        self.flow = {}  # Maps u -> {v1: f(u, v1), v2: f(u, v2), ... }, ...
        self.residualNetwork = {}  # Maps u -> {v1: rf(u, v1), v2: rf(u, v2), ... }, ...
        # Residual network initialized to deep copy of capacities
        self.resetFlowAndResidualNetwork()

    def resetFlowAndResidualNetwork(self):
        """For each edge present (specified in capacities mapping), reset flow to 0 and the residual to the capacity"""
        for u in self.capacities:
            self.residualNetwork[u] = {}
            self.flow[u] = {}
            for v in self.capacities[u]:
                self.residualNetwork[u][v] = self.capacities[u][v]
                self.flow[u][v] = 0

    def checkRep(self):
        for u in self.flow:
            for v in self.flow[u]:
                # If there is flow through an edge, then the flow must be <= the capacity
                assert u in self.capacities
                assert v in self.capacities[u]
                f = self.flow[u][v]
                cp = self.capacities[u][v]
                assert 0 <= f <= cp

                # No edge in residual network if flow == capacity
                if f == cp:
                    if u in self.residualNetwork:
                        assert v not in self.residualNetwork[u]
                    assert v in self.residualNetwork and u in self.residualNetwork[v]
                    assert f == self.residualNetwork[v][u]
                else:  # Otherwise, residual flow must be <= capacity-flow, and must have a reverse edge w >= f(u,v)
                    assert u in self.residualNetwork and v in self.residualNetwork[u]
                    assert self.residualNetwork[u][v] <= self.capacities[u][v] - self.flow[u][v]
                    if f == 0:  # If 0 flow, then reverse edge shouldn't be in the residual network
                        if v in self.residualNetwork:
                            assert u not in self.residualNetwork[v]
                    else:  # Reverse edge >= f(u,v) since there could be other contributing flows through edge (u,v)
                        assert v in self.residualNetwork and u in self.residualNetwork[v]
                        assert self.residualNetwork[v][u] >= self.flow[u][v]

        assert self.capacities == self.weights  # Aliased, so should be the same (pass by reference for dictionaries)
        for u in self.capacities:
            for v in self.capacities[u]:
                # Capacities must be non-negative, and also integral (otherwise Ford Fulkerson might converge properly)
                cp = self.capacities[u][v]
                assert cp >= 0
                assert isinstance(cp, int)

        # Source and sink nodes must be present
        # Total flow out of source must be equal to total flow into sink
        sourceSum, sinkSum = 0, 0
        assert self.source in self.flow
        sinkPresent = False
        for u in self.flow:
            if self.sink in self.flow[u]:
                sinkPresent = True
                sinkSum += self.flow[u][self.sink]
        assert sinkPresent
        for f in self.flow[self.source].values():
            sourceSum += f
        assert sourceSum == sinkSum

    def addEdge(self, u, v, capacity=0):
        """
        Given two vertices and a capacity, adds the edge to the flow network.
        Throws an exception if the capacity specified is negative.
        Behavior unspecified if there exists an edge back to the source S.
        If flow values already filled in, then reset all flows and add the edge (u,v) (to prevent weird FF behavior)
        """
        if capacity < 0:
            raise NegativeCapacityException
        if any(self.flow[u][v] != 0 for u in self.flow for v in self.flow[u]):
            self.resetFlowAndResidualNetwork()

        # This will implicitly update capacities as well since it's aliased to Graph's weights mapping
        super().addEdge(u, v, capacity)
        if u in self.flow:
            self.flow[u][v] = 0
            self.residualNetwork[u][v] = capacity
        else:
            self.flow[u] = {v: 0}
            self.residualNetwork[u] = {v: capacity}

    def getAugmentingPath(self):
        """
        Gets the shortest-length augmenting path via BFS on the residual network. Uses Edmonds-Karp as the spec
        since it bounds the number of augmentations to O(VE^2) rather than O(E * |f|) where f is the max flow
        :return: list of vertices in the shortest-length augmenting path
        """
        queue, visited, parents = [self.source], {self.source}, {self.source: self.source}
        while queue:
            node = queue.pop(0)
            if node == self.sink:
                break

            for neighbor in self.residualNetwork[node]:
                if neighbor not in visited:
                    parents[neighbor] = node
                    queue.append(neighbor)
                    visited.add(neighbor)

        if self.sink not in parents:
            return None
        # Invariant at this point is that S, T \in parents set, and so \exists a path from S~~>T
        i, path = self.sink, [self.sink]
        while i != self.source:
            i = parents[i]
            path.append(i)

        return path[::-1]  # Reverse path so that it is from source to sink

    def pushAugmentingFlow(self, augPath):
        """
        Pushes augmenting flow along the specified path, and updates the residuals in the residual network
        :param augPath: input path from source to sink node of possible nonzero additional flow, must not be None
        :return: null
        """
        assert augPath is not None
        # Need to identify largest difference between any capacity and flow already being pushed through
        additionalFlow = float('inf')
        for i in range(len(augPath) - 1):
            u, v = augPath[i], augPath[i+1]
            if u in self.flow:
                additionalFlow = min(additionalFlow, self.capacities[u][v] - self.flow[u].get(v, 0))
            else:
                additionalFlow = min(additionalFlow, self.capacities[u][v])

        # If an augmenting path is specified, then just need to make the necessary changes along the augmenting path
        for i in range(len(augPath) - 1):
            u, v = augPath[i], augPath[i+1]

            # Augment flow network for f(u,v)
            if u in self.flow:
                self.flow[u][v] = self.flow[u].get(v, 0) + additionalFlow
            else:
                self.flow[u] = {v: additionalFlow}

            # Augment residual network, potentially edit edges (u,v) and (v,u) if already flow going through
            assert additionalFlow <= self.residualNetwork[u][v]
            # Subtract off flow pushed through, ie delta f(u,v)
            if v in self.residualNetwork[u] and self.residualNetwork[u][v] == additionalFlow:
                del self.residualNetwork[u][v]
            else:
                self.residualNetwork[u][v] -= additionalFlow

            # Residual flow, from v->u
            if v not in self.residualNetwork:
                self.residualNetwork[v] = {u: additionalFlow}
            else:
                self.residualNetwork[v][u] = self.residualNetwork[v].get(u, 0) + additionalFlow

    def getMaxFlow(self):
        """
        Finds the max flow (as an integer), given the current flow network. Uses the Ford Fulkerson algorithm.
        Note: Pushes flow through the network (mutates the network's flow)
        :return: int, value of the max flow

        Pseudocode (from https://www.hackerearth.com/practice/algorithms/graphs/maximum-flow/tutorial/):
        function: FordFulkerson(Graph G,Node S,Node T):
            Initialise flow in all edges to 0
            while (there exists an augmenting path(P) between S and T in residual network graph):
                Augment flow between S to T along the path P
                Update residual network graph
            return
        """
        # Decided to keep the flow mapping + source/sink nodes in the constructor of a Network
        # instead of inside a member function
        augmentingPath = self.getAugmentingPath()
        while augmentingPath is not None:
            self.pushAugmentingFlow(augmentingPath)
            augmentingPath = self.getAugmentingPath()

        maxFlow = 0
        if self.source in self.flow:
            for v in self.flow[self.source]:
                maxFlow += self.flow[self.source][v]
        return maxFlow


if __name__ == "__main__":
    a, b, c, d, e = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e")
    g = Graph()
    g.addEdge(a, b, 2)
    g.addEdge(a, c, 3)
    g.addEdge(c, b, 5)
    g.addEdge(b, d, 4)
    g.addEdge(c, e, 5)
    g.addEdge(d, e, 4)
    vertices = g.getVertices()
    edges = g.getEdges()
    weights = g.getWeights()
    N = Network(a, e, vertices, edges, weights)

    G = Network(a, e)
    G.addEdge(a, b, 2)
    G.addEdge(a, c, 3)
    G.addEdge(c, b, 5)
    G.addEdge(b, d, 4)
    G.addEdge(c, e, 5)
    G.addEdge(d, e, 4)
    # Can implement a __eq__ to see if these really match programmatically if there's more time

    N.checkRep()
    G.checkRep()
    print(N.getMaxFlow())
    print(G.getMaxFlow())
    N.checkRep()
    G.checkRep()



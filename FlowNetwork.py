from Graph import Graph, Vertex

class NegativeCapacityException(Exception):
    pass

class Network(Graph):
    def __init__(self, vertices, edges, capacities, source, sink):
        super(Network, self).__init__(vertices, edges, capacities)
        self.capacities = capacities  # Maps u -> {v1: c1, v2: c2, ... }, ...; must be a mapping w "weighted" edges
        self.source = source  # Source node S
        self.sink = sink  # Sink node T
        self.flow = {}  # Maps u -> {v1: f(u, v1), v2: f(u, v2), ... }, ...
        self.resetFlow()
        self.residualNetwork = {}  # Maps u -> {v1: rf(u, v1), v2: rf(u, v2), ... }, ...
        # Residual network initialized to deep copy of capacities
        for u in self.capacities:
            self.residualNetwork[u] = {}
            for v in self.capacities[u]:
                self.residualNetwork[u][v] = self.capacities[u][v]

    def resetFlow(self):  # modularized in case future methods need to refresh the flow network
        for u in self.capacities:
            self.flow[u] = {}
            for v in self.capacities[u]:
                self.flow[u][v] = 0

    def addEdge(self, u, v, capacity=0):
        if capacity < 0:
            raise NegativeCapacityException
        super().addEdge(u, v, capacity)

    def getAugmentingPath(self):
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

    def FordFulkerson(self):
        """
        Finds the max flow (as an integer), given the current flow network.
        Pushes flow through the network (mutates the network's flow)
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
    N = Network(vertices, edges, weights, a, e)

    print(N.FordFulkerson())


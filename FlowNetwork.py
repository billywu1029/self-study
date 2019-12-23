from Graph import *

class NegativeCapacityException(Exception):
    pass

class Network(Graph):
    def __init__(self, vertices, edges, capacities, source, sink):
        super(Network, self).__init__(vertices, edges, capacities)
        self.capacities = capacities
        self.source = source
        self.sink = sink
        self.flow = {}
        self.resetFlow()
        self.residualNetwork = {}

    def resetFlow(self):  # modularized in case future methods need to refresh the flow network
        for u in self.capacities:
            self.flow[u] = {}
            for v in self.capacities[u]:
                self.flow[u][v] = 0

    def addEdge(self, u, v, w=0):
        if w < 0:
            raise NegativeCapacityException
        self.addEdge(u, v, w)

    def getAugmentingPath(self, resNet):
        pass

    def pushAugmentingFlow(self, augPath):
        pass

    def updateResidualNetwork(self):
        pass

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
        augmentingPath = self.getAugmentingPath(self.residualNetwork)
        while augmentingPath is not None:
            self.pushAugmentingFlow(augmentingPath)
            self.updateResidualNetwork()
            augmentingPath = self.getAugmentingPath(self.residualNetwork)

        maxFlow = 0
        if self.source in self.flow:
            for v, f in self.flow[self.source]:
                maxFlow += f
        return maxFlow


if __name__ == "__main__":
    a, b, c, d, e = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e")
    g = Graph()
    g.addEdge(a, b, 1)
    g.addEdge(a, c, -1)
    g.addEdge(b, d, 4)
    g.addEdge(b, c, 2)
    g.addEdge(c, d, 5)
    g.addEdge(c, d, 5)
    g.addEdge(a, e, 10)
    g.addEdge(e, d, -7)
    vertices = g.getVertices()
    edges = g.getEdges()
    weights = g.getWeights()
    N = Network(vertices, edges, weights, a, e)
    z = 1


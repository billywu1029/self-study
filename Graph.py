class Graph:
    def __init__(self):
        self.vertices = set()
        # Adjacency set for all the edges, maps Vertex objects to sets of Edge objects
        self.edges = {}

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        return self.edges

    def addEdge(self, u, v, w=0):  # Unweighted edges by default
        if u in self.edges.keys():
            self.edges[u].add(Edge(u, v, w))
        else:
            self.edges[u] = {Edge(u, v, w)}

    def addVertex(self, x):
        self.vertices.add(Vertex(x))


class Vertex:
    def __init__(self, x):
        # Must have immutable value x
        self.val = x

    def copy(self):
        return Vertex(self.val)

    def __str__(self):
        return "Vertex with value %r" % self.val


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def copy(self):
        # All fields are immutable so this will return a copy of this Edge
        return Edge(self.u, self.v, self.w)

    def __str__(self):
        return "Edge from %r to %r with weight %r" % (str(self.u), str(self.v), self.w)



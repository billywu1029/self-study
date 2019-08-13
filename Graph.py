import Topological_Sort

class Graph:
    def __init__(self, vertices=None, edges=None, weights=None):
        self.vertices = set() if vertices is None else vertices
        # Adjacency set for all the edges, maps Vertex objects to sets of Edge objects
        self.edges = {} if edges is None else edges
        # Maps vertex to mapping of vertex to weight (can be float)
        self.weights = {} if weights is None else weights

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        return self.edges

    def getChildren(self, u):
        assert u in self.vertices
        if u in self.edges:
            return [e.v for e in self.edges[u]]
        else:
            return []

    def __getitem__(self, item):
        # Dunder method to allow notation like graph[u] to represent children of u
        return self.getChildren(item)

    def addEdge(self, u, v, w=0):  # Unweighted edges by default
        if u in self.edges.keys():
            self.edges[u].add(Edge(u, v, w))
        else:
            self.edges[u] = {Edge(u, v, w)}
        if u in self.weights.keys():
            self.weights[u][v] = w
        else:
            self.weights[u] = {v:w}

        # Add new vertices if an edge connects ones not already in the graph
        self.vertices = self.vertices.union({u, v})

    def addVertex(self, x):
        self.vertices.add(Vertex(x))


class Vertex:
    # Assume that a Vertex is immutable
    def __init__(self, x):
        # Must have immutable value x
        self.val = x

    def copy(self):
        return Vertex(self.val)

    def __str__(self):
        return "vertex %r" % self.val

    def __repr__(self):
        return "Vertex(%r)" % self.val

    def __hash__(self):
        return hash(self.val)


class Edge:
    # Edge assumed to be directed, from u to v with weight w
    # Also assumed that an Edge is immutable
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def w(self):
        return self.w

    def copy(self):
        # All fields are immutable so this will return a copy of this Edge
        return Edge(self.u, self.v, self.w)

    def __str__(self):
        return "e(%r, %r) w=%r" % (self.u, self.v, self.w)

    def __repr__(self):
        return "Edge(%r,%r,%r)" % (self.u, self.v, self.w)

    def __hash__(self):
        return hash(self.u) + hash(self.v) + hash(self.w)

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.u == other.u and self.v == other.v and self.w == other.w
        else:
            return False




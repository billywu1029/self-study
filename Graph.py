class Graph:
    def __init__(self, vertices=None, edges=None, weights=None, adjSet=None):
        # Can construct a graph via adj set (vertices mapped to set of vertices that are connected via directed edges)
        # For ease of use, the vertices are assumed to not be be of type Graph.Vertex(x)
        self.vertices = set() if vertices is None else vertices
        # Adjacency set for all the edges, maps Vertex objects to sets of Edge objects
        self.edges = {} if edges is None else edges
        # Maps vertex to mapping of vertex to weight (can be float)
        self.weights = {} if weights is None else weights
        if adjSet is not None:
            for u in adjSet:
                if isinstance(adjSet[u], set):  # Unweighted edges, truly an "adjacency set"
                    for v in adjSet[u]:
                        self.addEdge(u, v)
                elif isinstance(adjSet[u], dict):  # Weighted, adjSet[u][v] = w_{u,v}
                    for v in adjSet[u]:
                        self.addEdge(u, v, adjSet[u][v])

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        return self.edges

    def getWeights(self):
        return self.weights

    def getChildren(self, u):
        assert isinstance(u, Vertex) and u in self.vertices
        # Can instead yield from a generator for better performance, since there could be a lot of children -
        # Keep the list for now so that debugging/readability is easier
        if u in self.edges:
            return [e.v for e in self.edges[u]]
        else:
            return []

    def __getitem__(self, item):
        # Dunder method to allow notation like graph[u] to represent children of u
        return self.getChildren(item)

    def addEdge(self, u, v, w=0):  # Unweighted edges by default
        # Lazy way of making graph creation easier by specifying numbers in addEdge()
        # (instead of wrapping every number x with Vertex(x))
        if not isinstance(u, Vertex):
            u = Vertex(u)
        if not isinstance(v, Vertex):
            v = Vertex(v)
        # Adds edge (u, v) with weight w to the Graph
        # Undefined behavior if we call addEdge(u, v, w) if there is already edge (u,v)
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

    def relax(self, u, v, w, d):
        """
        If current "shortest" distance from s to v is greater than shortest distance from s to u + w(u,v), then set
        the new shortest distance from s to v to be = newly found shortest distance d(s,u)+w(u,v).
        Better explained by illustration:
                   d(s,v)
                s ~~~~~~> v
                |      /
                |     /
         d(s,u) |    /
                |   /  w(u,v)
                |  /
                | /
                u
        """
        assert u in d and v in d and u in self.weights and v in self.weights[u]
        assert w == self.weights[u][v]
        if d[v] > d[u] + w:
            d[v] = d[u] + w

    def verifyDAG(self, s):
        """
        In order for the SSSP by topological sort to work, ensure that this graph is a directed acyclic graph (DAG),
        for the nodes reachable by s
        :param s specifying source node s to make traversal start easier
        """
        # Find presence of a back edge, if none, then the nodes reachable from s + edges traversed form a DAG
        curr_nodes = set()
        def traverse(root):
            curr_nodes.add(root)
            for child in self.getChildren(root):
                if child in curr_nodes:
                    assert False
                traverse(child)
            curr_nodes.remove(root)  # Important, to keep nodes in the stack updated

        return traverse(s)

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

    def __eq__(self, other):
        return isinstance(other, Vertex) and other.val == self.val


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

if __name__ == "__main__":
    pass

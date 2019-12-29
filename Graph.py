class Graph:
    def __init__(self, vertices=None, edges=None):
        # Can construct a graph via edges adjacency set (u -> {v1: w1, v2: w2}, ...})
        # For ease of use, the vertices are assumed to not be be of type Graph.Vertex(x)
        self.vertices = set() if vertices is None else vertices
        # Adjacency set for all the edges - {u: {v1: w1, v2: w2, ...}, ...}
        self.edges = {} if edges is None else edges

    def getVertices(self):
        return self.vertices  # Consider making deep copies to prevent aliasing/rep exposure issues

    def getEdges(self):
        return self.edges

    def getChildren(self, u):
        assert isinstance(u, Vertex) and u in self.vertices
        # Can instead yield from a generator for better performance, since there could be a lot of children -
        # Keep the list for now so that debugging/readability is easier
        if u in self.edges:
            return (v for v in self.edges[u].keys())
        else:
            return ()

    def __getitem__(self, item):
        return self.edges.get(item, {})

    def __setitem__(self, key, value):
        assert isinstance(key, Vertex)
        assert isinstance(value, dict) and all(isinstance(v, Vertex) for v in value)
        self.edges[key] = value

    def getWeight(self, u, v):
        # Given vertices u and v, get the weight of the edge (u, v)
        # Returns 0 if (u, v) not in the graph
        if u not in self.edges or v not in self.edges[u]:
            return 0
        return self.edges[u][v]

    def __contains__(self, item):
        return item in self.vertices and item in self.edges

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
            self.edges[u][v] = w
        else:
            self.edges[u] = {v: w}

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
        assert u in d and v in d and u in self.edges and v in self.edges[u]
        assert w == self.edges[u][v]
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


if __name__ == "__main__":
    pass

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

    def SSSPTopologicalRelaxation(self, s):
        """
        Finds the single source shortest paths between the source s and all other vertices
        The graph must be a DAG for the algorithm to produce the correct SSSP
        :return: mapping of vertex pairs to their shortest path weight
        """
        self.verifyDAG(s)
        shortestPaths = {s:0}  # maps vertex u -> d(s, u) for all vertices u
        for v in self.vertices:
            if v != s:
                shortestPaths[v] = float('inf')

        # list of graph's vertices reachable from s in topological order
        verticesSorted = Topological_Sort.topological_sort_SS(self, s)
        for u in verticesSorted:
            if u in self.edges.keys():
                for e in self.edges[u]:
                    v, w = e.v, e.w
                    self.relax(u, v, w, shortestPaths)
        return shortestPaths

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

    def SSlongestPathDAG(self, s):
        self.verifyDAG(s)

        # Initialize all longest paths to -inf, if by the end any longest path is still -inf then it is unreachable from s
        longestPaths = {s:0}  # maps vertex u -> LD(s, u) for all vertices u, where LD -> longest distance
        for v in self.vertices:
            if v != s:
                longestPaths[v] = -float('inf')

        sortedVertices = Topological_Sort.topological_sort_SS(self, s)
        for u in sortedVertices:
            if u in self.edges.keys():
                for e in self.edges[u]:
                    v, w = e.v, e.w
                    # Do the opposite of relaxing the edge - if d[v] < d[u] + w, then set d[v] to d[u] + w
                    longestPaths[v] = max(longestPaths[v], longestPaths[u] + w)
        return longestPaths


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

if __name__ == "__main__":
    a, b, c, d, e = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e")
    g = Graph({a, b, c, d})
    g.addEdge(a, b, 1)
    g.addEdge(a, c, -1)
    g.addEdge(b, d, 4)
    g.addEdge(b, c, 2)
    g.addEdge(c, d, 5)
    g.addEdge(c, d, 5)
    g.addEdge(a, e, 10)
    g.addEdge(e, d, -7)

    print("Edges: ", g.getEdges())
    try:
        print(g.SSSPTopologicalRelaxation(a))
        print("successfully determined that graph g was a DAG")
    except AssertionError:
        print("wasn't supposed to fail...")

    g2 = Graph({a, b, c, d})
    g2.addEdge(a, b, 1)
    g2.addEdge(a, c, -1)
    g2.addEdge(d, a, 4)
    g2.addEdge(c, d, 5)

    try:
        print(g2.SSSPTopologicalRelaxation(a))
    except AssertionError:
        print("successfully detected graph g2 was not a DAG")

    print("Longest path dict: ", g.SSlongestPathDAG(a))


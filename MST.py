import Graph
import UnionFind

class MST:
    def __init__(self, graph):
        # Can assume that the graph is connected, since o/w set of trees could become a spanning forest
        # Make this support spanning forests in a later iteration
        self.graph = graph
        E = graph.getEdges()
        self.graphEdgesSorted = []
        for v in E.keys():
            for e in E[v]:
                self.graphEdgesSorted.append(e)
        self.graphEdgesSorted.sort(key=lambda x: x.w)
        self.MSTEdges = set()
        self.nodes = UnionFind.UnionFind()

        # Kruskal's algorithm to form the set of MST edges
        for v in self.graph.getVertices():
            self.nodes.make_set(v)
        for e in self.graphEdgesSorted:
            u, v = e.u, e.v
            if self.nodes.find_set(u) != self.nodes.find_set(v):
                self.MSTEdges.add(e)
                self.nodes.union(u, v)

    def get_MST_Edges(self):
        # Return a defensive copy to avoid aliasing
        result = set()
        for e in self.MSTEdges:
            result.add(e.copy())
        return result

if __name__ == "__main__":
    G = Graph.Graph()
    for i in range(1, 5):
        G.addVertex(i)
    count = 0
    for u in G.getVertices():
        for v in G.getVertices():
            if u != v:
                G.addEdge(u, v, count)
                count += 1
    print([str(v) for v in G.getVertices()])
    print(G.getEdges().items())

    M = MST(G)
    print([str(e) for e in M.get_MST_Edges()])





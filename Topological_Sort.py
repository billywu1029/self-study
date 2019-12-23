from Graph import *

"""
Topological Sort:
Use DFS subroutine to get a topological sorted order of vertices, ie for each edge (u,v), u comes before v in the
sorted ordering. Consider in future refactoring: change adjacency set to graph abstract data type
Author: Bill Wu
Date: 8/4/19
"""

def topological_sort(graph):
    """
    Conducts a topological ordering of vertices of a graph
    :param graph: graph input graph as adjacency set, assumes vertices are integers,
                  also assume for now graph is fully connected and is a DAG (directed acyclic graph)
                  must also contain all vertices present in the keys of the adjacency set
    :return: list of graph vertices in topologically sorted order
    """
    result, visited = [], set()
    unvisited = [Vertex(v.val) for v in graph.getVertices()]  # Deep copy
    while nodes_left_to_traverse(graph.getVertices(), visited) and unvisited:
        add_children_of(graph, next(iter(unvisited)), result, visited, unvisited)
    return [v.val for v in result]

def add_children_of(graph, root, result, visited, unvisited=None):
    """
    Prepends the root node before its children in the result list based on DFS ordering
    Updates visited and unvisited sets to reflect traversal through nodes under root
    :param graph: input graph
    :param root: starting node of the traversal
    :param result: list of nodes meant to be in topological order after this function call
    :param visited: set of visited nodes
    :param unvisited: optional to specify which nodes must still be traversed, potentially in a separate tree
    """
    visited.add(root)
    for child in graph[root]:
        if child not in visited:
            add_children_of(graph, child, result, visited, unvisited)

    # prepend the node to the front of the topological ordering, in front of its children
    result.insert(0, root)
    if unvisited is not None:
        unvisited.remove(root)

def nodes_left_to_traverse(all_nodes, visited_nodes):
    """
    Checks if there are nodes left to traverse, given the set of all graph nodes and the current visited set
    :param all_nodes: graph nodes set
    :param visited_nodes: visited nodes set
    :return: true if nodes left, false o/w
    """
    # Uncomment when debugging, ensure that no non-graph nodes are ever added to visited set
    # assert visitedNodes.issubset(allNodes)
    return len(all_nodes) != len(visited_nodes)

def topological_sort_SS(graph, source):
    """
    Finds a topological sort ordering on a graph given a source node. Will exclude nodes unreachable from the source.
    :param graph: input graph
    :param source: input source
    :return: list of nodes of the graph that are reachable from source in a topological ordering
    """
    result, visited = [source], {source}
    add_children_of(graph, source, result, visited)
    return result

def SSlongestPathDAG(g, s):
    g.verifyDAG(s)

    # Initialize all longest paths to -inf, if by the end any longest path is still -inf then it is unreachable from s
    longestPaths = {s:0}  # maps vertex u -> LD(s, u) for all vertices u, where LD -> longest distance
    for v in g.vertices:
        if v != s:
            longestPaths[v] = -float('inf')

    sortedVertices = topological_sort_SS(g, s)
    for u in sortedVertices:
        if u in g.edges.keys():
            for e in g.edges[u]:
                v, w = e.v, e.w
                # Do the opposite of relaxing the edge - if d[v] < d[u] + w, then set d[v] to d[u] + w
                longestPaths[v] = max(longestPaths[v], longestPaths[u] + w)
    return longestPaths

def SSSPTopologicalRelaxation(g, s):
    """
    Finds the single source shortest paths between the source s and all other vertices
    The graph must be a DAG for the algorithm to produce the correct SSSP
    :return: mapping of vertex pairs to their shortest path weight
    """
    g.verifyDAG(s)
    shortestPaths = {s:0}  # maps vertex u -> d(s, u) for all vertices u
    for v in g.vertices:
        if v != s:
            shortestPaths[v] = float('inf')

    # list of graph's vertices reachable from s in topological order
    verticesSorted = topological_sort_SS(g, s)
    for u in verticesSorted:
        if u in g.edges.keys():
            for e in g.edges[u]:
                v, w = e.v, e.w
                g.relax(u, v, w, shortestPaths)
    return shortestPaths


if __name__ == '__main__':
    ezGraph = Graph()
    ezGraph.addEdge(0, 5)
    ezGraph.addEdge(1, 3)
    ezGraph.addEdge(1, 0)
    ezGraph.addEdge(2, 4)
    ezGraph.addEdge(3, 2)

    # {0: {5}, 1:{3,0}, 2: {4}, 3:{2}, 4:{}, 5:{}}
    print(topological_sort(ezGraph))

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

    print("Edges: ", g.getEdges())
    try:
        print(SSSPTopologicalRelaxation(g, a))
        print("successfully determined that graph g was a DAG")
    except AssertionError:
        print("wasn't supposed to fail...")

    g2 = Graph()
    g2.addEdge(a, b, 1)
    g2.addEdge(a, c, -1)
    g2.addEdge(d, a, 4)
    g2.addEdge(c, d, 5)

    try:
        print(SSSPTopologicalRelaxation(g2, a))
    except AssertionError:
        print("successfully detected graph g2 was not a DAG")

    print("Longest path dict: ", SSlongestPathDAG(g, a))



"""
Solves the airline interview problem:
Given input:
1. List of airports (eg [JFK, BUD, TLV, ...]) as a list of strings
2. List of routes between source and destination airports that are one-way flights (eg [ [JFK, BUD], [DEL, TLV], ... ])
3. and a starting airport (eg SFO),

Find the minimum number of additional one-way flights that must be added before there exists a flight path
from the starting airport (3.) to every other airport in the list from (1.). Unlimited transfer flights/connecting
flights are allowed and would be considred a valid "path".

@author: Bill Wu
Date: June 4, 2020
"""

from Graph import Graph, Vertex

def process_input(airports: list, routes: list) -> Graph:
    """
    Given a list of airports (as str/vertices), a list of routes (as either tuples or lists of str/vertex, return the
    resulting directed Graph that represents the current flight options, where vertices are airports and edges are
    one-way flights.
    """
    V = set(airports)
    G = Graph(V)
    for s, d in routes:
        G.addEdge(s, d)
    return G

def min_additional_routes(G: Graph, start: Vertex) -> int:
    """
    Given a directed graph of the current airline routes, output the minimum number of additional routes needed to be
    able to have a path from the start airport to every other airport (ie G.V).
    """
    # 1. Delineate all vertices reachable from each airport/node u, stored in a map<str, int>, remove already visited
    #    nodes from the search space if re-visited during DFS since that implies that an ancestor must reach >= 1 more
    #    nodes than the visited node
    reachable = set()
    start_reachable_nodes = set()

    def dfs_reachable_nodes(root, visited):
        if root in visited:
            return
        visited.add(root)
        start_reachable_nodes.add(root)
        for child in G.getChildren(root):
            if child not in visited:
                dfs_reachable_nodes(child, visited)

    dfs_reachable_nodes(start, set())
    search_space = {v for v in G.vertices if v not in start_reachable_nodes}

    # 2. Find the u with the largest reachable set of nodes, remove all reachable nodes from search space
    # 3. Repeat step 2. until search space exhausted
    def dfs_remove(root, visited):
        # Run DFS from root and remove all child nodes from the search_space
        visited.add(root)
        # If it's no longer in the search space, just terminate right here since already DFS removed it + its children
        if root not in search_space:
            return
        search_space.remove(root)
        for child in G.getChildren(root):
            if child not in visited:
                dfs_remove(child, visited)

    def dfs(root, visited):
        if root in reachable:
            dfs_remove(root, set())
            return

        visited.add(root)
        for child in G.getChildren(root):
            if child not in visited:
                dfs(child, visited)
        reachable.add(root)

    for v in search_space.copy():
        dfs(v, set())

    # 4. Return number of iterations required
    return len(search_space)


if __name__ == "__main__":
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")
    f = Vertex("F")
    g = Vertex("G")
    h = Vertex("H")
    airports = [a, b, c, d, e, f, g, h]
    routes = [(a, c), (b, c), (d, f), (e, h), (d, e), (c, g), (a, f)]
    start = a
    G = process_input(airports, routes)
    print(G.vertices)
    print(G.edges)
    print(min_additional_routes(G, start))


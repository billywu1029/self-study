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
    result, visited, unvisited = [], set(), set(graph.keys())
    while nodes_left_to_traverse(graph.keys(), visited):
        add_children_of(graph, next(iter(unvisited)), result, visited, unvisited)
    return result

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


if __name__ == '__main__':
    g = {0: {1,2,3}, 1:{2}, 2: {3, 4}, 3:{}, 4:{}}
    g2 = {0: {5}, 1:{3,0}, 2: {4}, 3:{2}, 4:{}, 5:{}}
    print(topological_sort(g2))


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
    def add_children_of(root):
        """
        Prepends the root node before its children in the result list based on DFS ordering
        Updates visited and unvisited sets to reflect traversal through nodes under root
        :param root: starting node of the traversal
        """
        visited.add(root)
        for child in graph[root]:
            if child not in visited:
                add_children_of(child)  # recursive call may run into stack frame limit problems, consider making iterative

        # prepend the node to the front of the topological ordering, in front of its children
        result.insert(0, root)
        unvisited.remove(root)

    while nodes_left_to_traverse(graph.keys(), visited):
        add_children_of(next(iter(unvisited)))
    return result

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


if __name__ == '__main__':
    g = {0: {1,2,3}, 1:{2}, 2: {3, 4}, 3:{}, 4:{}}
    g2 = {0: {5}, 1:{3,0}, 2: {4}, 3:{2}, 4:{}, 5:{}}
    print(topological_sort(g2))


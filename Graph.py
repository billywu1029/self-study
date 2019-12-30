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

    def bfs(self, start, target):
        # Given a graph/adjacency matrix/adjacency set, (in 6.006 ex create dict of paths to all V) find SP to target
        queue, visited, parents = [start], {start}, {start: start}
        while queue:  # While there are still items in the queue (FIFO)
            # Pop off first node in the current queue; once nodes in curr lvl set popped, next lvl set will be formed
            node = queue.pop(0)
            if node == target:  # Short circuit if found the target node
                break

            # Push all neighbors for the next level set onto queue, add to seen, add parent pointers etc
            for neighbor in self.getChildren(node):
                if neighbor not in visited:  # Make sure to not visit any already visited nodes
                    parents[neighbor] = node
                    queue.append(neighbor)
                    visited.add(neighbor)

        if target not in parents:  # No path exists/target doesn't have a parent node
            return None
        # Invariant at this point is that start, target \in parents set, and so \exists a path from start~~>target
        # Now, construct path from start to target
        i, path = target, [target]
        while i != start:  # Potentially O(V) loop here
            i = parents[i]
            path.append(i)

        return path[::-1]  # Reverse path so that it is from start to target

    def dfs(self, start, target):
        # Given graph/adjacency matrix/adjacency set, return *a* path from start to target, using depth-first search
        stack, visited, parents = [start], {start}, {start: start}

        # Difference between BFS and DFS is queue vs stack -> popping off from front vs back for next node to be processed
        while stack:  # While items still on stack
            curr_node = stack.pop()  # Use last element of stack as current (ie LIFO policy)
            visited.add(curr_node)
            if curr_node == target: break  # If found the target node, short circuit
            # Loop through all neighbors of current node, add them to stack if not visit
            for next_node in self.getChildren(curr_node):
                if next_node not in visited:
                    parents[next_node] = curr_node
                    stack.append(next_node)

        if target not in parents:
            return None
        # Now found the target node, want to construct path from start to target
        i, path = target, [target]
        while i != start:  # Potentially O(V) loop here
            i = parents[i]
            path.append(i)

        return path[::-1]  # Reverse path so that it is from start to target

    # Should this be a static method or not??
    def relax(self, u, v, d):
        """
        If current "shortest" distance from s to v is greater than shortest distance from s to u + w(u,v), then set
        the new shortest distance from s to v to be = newly found shortest distance d(s,u) + w(u,v).
        Return the boolean result from the triangle inequality condition mentioned above as well.
        Better explained by illustration: d(s,v) <- d(s,u) + w(u,v) if d(s,v) > d(s,u) + w(u,v)
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
        flag = d[v] > d[u] + self.edges[u][v]
        if flag:
            d[v] = d[u] + self.edges[u][v]
        return flag

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

    @staticmethod
    def minDistVertex(pq, d):
        """
        Find the vertex with current minimum distance and update Q to reflect its removal from the data structure
        @param Q: a data structure storing the vertices ordered by minimum distance
        @param d: a mapping of vertices to their current known shortest distance from a source node
                  (source node has default distance of 0 from itself)
        @return: the vertex of minimum distance from the start/source node
        """
        minDist, minNodeInd = float('inf'), None
        for i, v in enumerate(pq):
            if d[v] <= minDist:
                minDist = d[v]
                minNodeInd = i
        assert minNodeInd is not None
        minNode = pq[minNodeInd]
        del pq[minNodeInd]
        return minNode

    def dijkstra_SSSP(self, source):
        """
        Dijkstra's algorithm for single-source shortest paths, given a start and target Vertex.
        Note: graph must not contain any cycles with negative weights (for now, just restrict the graph to be a DAG)
        @param source: source node
        @return: mapping of the shortest distances between source and every other vertex (default d(s, s) <- 0)
                 and a mapping of every node to its parent in its corresponding shortest path (see: subpaths of SP's
                 are themselves SPs, and triangle inequality for why this works)
        """
        self.verifyDAG(source)
        d = {}
        for v in self.vertices:
            d[v] = float('inf')
        d[source] = 0
        visited = set()
        priority_queue = list(self.vertices)  # This can be changed to be a heapq later
        parentMap = {source: source}

        while priority_queue:
            u = Graph.minDistVertex(priority_queue, d)
            visited.add(u)
            for v in self.getChildren(u):
                flag = self.relax(u, v, d)
                if flag:
                    parentMap[v] = u

        return d, parentMap

    def printSSSPs(self, desiredVertices=None):
        """
        Prints the SSSP from source to each vertex in desiredVertices. Uses Dijkstra's Algorithm for SSSP.
        @param desiredVertices: if None, then assume all vertices are desired
        """
        if desiredVertices is None:
            desiredVertices = self.getVertices()
        assert all(isinstance(v, Vertex) for v in desiredVertices)
        d, p = self.dijkstra_SSSP(a)
        for v in desiredVertices:
            if v not in p or v not in desiredVertices:
                continue
            i, path = v, [v]
            while i != a:  # Potentially O(V) loop here
                i = p[i]
                path.append(i)

            print("SSSP from source %r to node %r has distance %r and path %r" % (a, v, d[v], path[::-1]))


if __name__ == "__main__":
    a, b, c, d, e = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e")
    G = Graph()
    G.addEdge(a, b, 2)
    G.addEdge(a, c, 3)
    G.addEdge(c, b, 5)
    G.addEdge(b, d, 4)
    G.addEdge(c, e, 5)
    G.addEdge(d, e, 4)

    G.printSSSPs()

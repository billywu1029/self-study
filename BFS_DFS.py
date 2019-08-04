def bfs(graph, start, target):
    # Given a graph/adjacency matrix/adjacency set, (in 6.006 ex create dict of paths to all V) find SP to target
    queue, visited, parents = [start], {start}, {start: start}
    while queue:  # While there are still items in the queue (FIFO)
        # Pop off first node in the current queue; once all nodes in curr lvl set popped, next lvl set will be formed
        node = queue.pop(0)
        if node == target:  # Short circuit if found the target node
            break

        # Push all neighbors for the next level set onto queue, add to seen, add parent pointers etc
        for neighbor in graph[node]:
            if neighbor not in visited:  # Make sure to not visit any already visited nodes
                parents[neighbor] = node
                queue.append(neighbor)
                visited.add(neighbor)

    print(parents)
    if target not in parents:  # No path exists/target doesn't have a parent node
        return None
    # Now found the target node, want to construct path from start to target
    i, path = target, [target]
    while i != start:  # Potentially O(V) loop here
        i = parents[i]
        path.append(i)

    return path[::-1]  # Reverse path so that it is from start to target


G = {0: {1, 2, 3}, 1: {0, 3, 4}, 2: {0}, 3: {0, 1}, 4: {1, 5, 6}, 5: {4, 6}, 6: {4, 5}}
start, target = 0, 5
print(bfs(G, start, target))


def dfs(graph, start, target):
    # Given graph/adjacency matrix/adjacency set, return A path from start to target, using depth-first search
    stack, visited, parents = [start], {start}, {start: start}

    # Difference between BFS and DFS is queue vs stack -> popping off from front vs back for next node to be processed
    while stack:  # While items still on stack
        curr_node = stack.pop()  # Use last element of stack as current (ie LIFO policy)
        visited.add(curr_node)
        if curr_node == target: break  # If found the target node, short circuit
        for next_node in graph[curr_node]:  # Loop through all neighbors of current node, add them to stack if not visit
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


G = {0: {1, 2, 3}, 1: {0, 3, 4}, 2: {0}, 3: {0, 1}, 4: {5, 1, 7, 6}, 5: {4, 6}, 6: {4, 5}, 7: {4}}
start, target = 0, 5
print(dfs(G, start, target))


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

visited = {}
a = TreeNode(5)
visited["bruh"] = a
print(visited)

class UnionFind:
    class ElementNotFoundException(Exception):
        pass

    def __init__(self):
        # self.sets is a forest of trees (represented as a list of Node's), with the root node
        # being the set rep
        self.sets = []
        # stores all elements inside UF data structure so far, mapped to their corresponding Node
        self.elements = {}
        self.idCounter = 0

    def make_set(self, x):
        """
        Initializes a set with the element x in it, if not already present
        :param x: element of any immutable type
        :return: Nothing
        """
        if x not in self.elements:
            new_node = Node(self.idCounter, 0)
            self.sets.append(new_node)
            self.idCounter += 1
            self.elements[x] = new_node

    def find_set(self, x):
        """
        Finds the set with the element x in it, utilizes path compression
        :param x: element of any immutable type
        :return: set rep of the set containing x
        :raises ElementNotFoundException if element not contained in any set
        """
        if x not in self.elements:
            raise self.ElementNotFoundException

        # Need x's node, now path compress until reached root node
        xNode = self.elements[x]
        while not xNode.isRoot():
            prev = xNode
            xNode = xNode.parent
            prev.parent = xNode.parent
        return xNode

    def union(self, x, y):
        """
        Joins sets x and y together, utilizes union by rank
        :param x: first input element
        :param y: second input element
        :return: Nothing
        """
        xRoot = self.find_set(x)
        yRoot = self.find_set(y)
        if xRoot == yRoot:  # Assuming this is comparing references of the Nodes
            return  # return early if they are the same

        # Union by Rank trick here, guarentees that smaller rank set will always be
        # merged with larger rank set, and if equal, then rank only increases by 1
        # Here, we want xRoot to point to larger set by default after this swap
        if xRoot.rank < yRoot.rank:
            xRoot, yRoot = yRoot, xRoot

        yRoot.parent = xRoot
        if yRoot.rank == xRoot.rank:  # Only condition in which rank increases
            xRoot.rank += 1


class Node:
    def __init__(self, id: int, rank: int) -> None:
        self.id = id
        self.parent = self
        self.rank = rank

    def isRoot(self):
        return self.parent == self

    def __str__(self):
        return "Node object with id: %r, and with rank %r" % (self.id, self.rank)

if __name__ == "__main__":
    import time
    uf = UnionFind()
    overallStart = time.time()
    for i in range(10):
        uf.make_set(i)
    findStart = time.time()
    uf.find_set(2)  # 2
    findEnd = time.time()
    findTime = findEnd - findStart
    uf.union(1,3)
    uf.find_set(3)  # 1
    uf.union(4, 1)
    uf.find_set(4)  # 1
    uf.find_set(3)  # Should be same as find_set(3) earlier
    uf.union(8,9)
    uf.union(7,9)
    uf.union(3, 8)
    findStart = time.time()
    uf.find_set(9)  # 1

    # print(uf.find_set(2))  # 2
    # print(uf.union(1, 3))
    # print(uf.find_set(3))  # 1
    # print(uf.union(4, 1))
    # print(uf.find_set(4))  # 1
    # print(uf.find_set(3))  # Should be same as find_set(3) earlier
    # print(uf.union(8, 9))
    # print(uf.union(7, 9))
    # print(uf.union(3, 8))
    # print(uf.find_set(9))  # 1

    findEnd = time.time()

    uf.union(6,5)
    uf.union(4,5)
    numOps = 10000000
    for i in range(numOps):
        try:
            uf.find_set(i%10)
        except uf.ElementNotFoundException:
            print("breh")

    overallEnd = time.time()
    findHarderTime = findEnd - findStart
    overallTime = overallEnd - overallStart
    print("Easy find took: %r s\nHarder find took: %r s\n~%r operations took: %r s." %
          (findTime, findHarderTime, numOps, overallTime))





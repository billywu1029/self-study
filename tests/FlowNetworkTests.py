import unittest
from FlowNetwork import *
from tests.midnights import *

class FlowNetworkTests(unittest.TestCase):
    """
    Testing Strategy:
        - Use checkRep() to ensure that the flow network is valid and expected at all times
        - addEdge(): Edges, vertices, weights, and capacities mappings all properly updated
            - Negative capacity exception properly thrown
            - 0, >0 capacity edge
        - getAugmentingPath()
            - No path from S (source) to T (sink)
            - Cycle exists, need to ignore it
            - Path exists
        - pushAugmentingFlow(): test that the residual and flow networks are properly updated
            - augPath is None, len 2, >2
            - Residual network has a path/no path
        - getMaxFlow()
        - getMinCostMaxFlow(): (after identifying a feasible max flow, there exists: )
            - 0, 1, >1 negative cost cycles
            - 0, 1, >1 minimum capacity through cycle (if exists)
    """

    def testNegativeCapacity(self):
        a, b = Vertex("a"), Vertex("b")
        G = FlowNetwork(a, b)
        self.assertRaises(NegativeCapacityException, G.addEdge(a, b, -5))

    def testAddNetworkEdgeStartEmpty(self):
        a, b, c, d, e, f = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e"), Vertex("f")
        G = FlowNetwork(a, f)
        cp = 5
        G.addEdge(a, c, cp)
        self.assertEqual(G.capacityGraph.edges, {a: {c: cp}})
        self.assertEqual(G.residualGraph.edges, {a: {c: cp}})
        self.assertEqual(G.source, a)
        self.assertEqual(G.sink, f)

    def testAddEdgeComplex(self):
        a, b, c, d, e, f = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e"), Vertex("f")
        G = self.generateComplexNetwork(a, b, c, d, e, f)
        # TODO: Keep track of mappings before
        G.addEdge(a, e, 10)
        # Verify that mapping afterwards is same as before except just one more added w (a,e) -> 10


    def testNoAugmentingPath(self):
        a, b, c, d, e, f = Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e"), Vertex("f")
        G = FlowNetwork(a, f)
        # TODO: Construct residual network s.t. there isn't a path S~~~>T, verify that getAugmentingPath() returns None

    def testPathWithCycle(self):
        # TODO: Introduce a cycle, but BFS should ignore it so expect a return of shortest-length path given cycle
        pass

    def testPushFlowNoAugPath(self):
        # TODO: Verify that if no augmenting path, nothing changes
        pass

    def testPushFlowBasicAugPath(self):
        # TODO: path from S to T exists in residual, test flow and residual updated correctly
        pass

    def testPushFlowComplexAugPath(self):
        # TODO: S~~~~~>T longer path, test that mappings udpated correctly
        pass

    def testMaxFlow(self):
        # TODO: given some network, make sure it returns the right max flow value and check all mappings
        pass

    # TODO: create a helper function to test that all mappings are properly updated after a push flow operation

    def testMinCostFlow2Cycles(self):
        s, a, b, c, d, e, t = Vertex("S"), Vertex("a"), Vertex("b"), Vertex("c"), Vertex("d"), Vertex("e"), Vertex("T")
        G = FlowNetwork(s, t)
        G.addEdge(s, a, 20, 4)
        G.addEdge(s, c, 10, 2)
        G.addEdge(a, b, 20, 3)
        G.addEdge(b, c, 5, 1)
        G.addEdge(b, d, 25, 5)
        G.addEdge(c, e, 22, 2)
        G.addEdge(d, t, 25, 6)
        G.addEdge(b, t, 10, 20)
        G.addEdge(e, t, 20, 6)

        minCost, maxFlow = G.getMinCostMaxFlow()
        self.assertEqual(minCost, 450)
        self.assertEqual(maxFlow, 30)

    def testMidnightsMediumComplexity(self):
        inpPath = "midnights.json"
        dayToMidnights, midnightPointValues, midnightsToNumReq, people, dayPreferences, midnightPreferences, progress = extractData(inpPath)
        G = generateMidnightsFlowNetwork(dayToMidnights, midnightPointValues, midnightsToNumReq, people, dayPreferences, midnightPreferences, progress)
        cost, maxFlow = G.getMinCostMaxFlow()
        peopleMidnightMap = getMidnightAssignments(G, people)
        dayToMidnightAssignmentsMap = getPeopleMidnightsToDayAssignments(peopleMidnightMap)
        peoplePointsGain = getPeoplePointsGain(dayToMidnightAssignmentsMap, midnightPointValues)
        # TODO: assert that things are the way they are/implement a checker that reads from an answer JSON etc.

if __name__ == "__main__":
    unittest.main()

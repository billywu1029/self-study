"""
Implementation of the algorithm for ZBT midnights (AKA our system for doing chores throughout our fraternity house).
Uses the max flow code developed in this directory + input preferences + midnights structure to setup a Flow Network
and then use Ford Fulkerson to find the max flow (and obviously find the optimal midnights assignment for the week).

@author: Bill Wu
Date: 12/30/19
"""

from FlowNetwork import *
import json

POINTS_REQ = 50
PERSON_BASE_COST = 10
PREFER_DAY_WEIGHT = 20
PREFER_MIDNIGHT_WEIGHT = 5
PREFERENCE_OFFSET = 26  # To make costs positive, ie offset the potential -10 - 2 for c(boi, m)
STRONGLY_AGAINST_PENALTY = 50

def weightedPersonCost(pointsProgress: int) -> int:
    """
    Gets a weighted cost of assigning a midnight to each person, determined by:
        PERSON_BASE_COST ** (1 + person's pointsProgress / POINTS_REQ)
    Intuition: The more midnight points someone has, the less midnights they should be assigned, and vice versa.
    @param pointsProgress: number of midnight points the person has
    @return: int of max num of midnights one person should be allowed in a week
    """
    return int(round(PERSON_BASE_COST ** (1 + pointsProgress / POINTS_REQ)))

def getCostBoiToMidnight(preferDay: bool, preferMidnight: bool) -> int:
    """
    Gets the cost for an edge from a person to any corresponding midnight. Intuitively, should assign low cost for
    midnights that are more preferred, and higher cost if not preferred. Can even use different levels of preference
    so that strongly prefer -> 0 cost, strongly do not prefer -> super high cost.
    @param preferDay: True to indicate that the day is preferred, False o/w
    @param preferMidnight: True to indicate that the midnight is preferred, False o/w
    @return: int generated via formula: -1(preferDay) * PREFER_DAY_WEIGHT - 1(preferMidnight) * PREFER_MIDNIGHT_WEIGHT
    """
    # TODO: Different levels of preference to potentially create useful backdoors to guarantee midnights you want
    dayCoeff = PREFER_DAY_WEIGHT if preferDay else 1
    midnightCoeff = PREFER_MIDNIGHT_WEIGHT if preferMidnight else 1
    penalty = -STRONGLY_AGAINST_PENALTY if not preferMidnight and not preferDay else 1
    return PREFERENCE_OFFSET - (dayCoeff + midnightCoeff) * penalty

def getMidnightAssignments(G: FlowNetwork, people: list) -> dict:
    """
    Gets the mapping of midnight assignments for each person according to a Flow Network G.
    Assumes that max flow has already been found in G, behavior unspecified o/w.
    @param G: Input flow network, assumed to have optimal max flow values already filled in.
    @param people: input list of people (repr as name strings) available to do midnights for the week
    @return: dict mapping each person in people to list of midnights (with day) they should do
    """
    result = {}
    for boi in people:
        u = Vertex(boi)
        result[boi] = [m.val for m in G.capacityGraph.getChildren(u) if G.flowGraph.getWeight(u, m) > 0]
    return result

def createNewMidnight(day: str, m: str, i: int) -> str:
    """
    Create a new string that concatenates all three pieces of information together: day, midnight, and midnight number
    @param day: which day the midnight is assigned
    @param m: the midnight
    @param i: the midnight number, ie waitings 1 or waitings 2 would have i=1 and i=2 respectively
    @return: str that has all the information concatenated in a separable fashion
    """
    return "%s|%s|%r" % (day, m, i)


# Assuming that JSON file format is:
# "dayToMidnights": {M: [bathrooms, dinings, ...], T: [...], ...}  // Days mapped to which midnights are needed that day
# "midnightsToNumReq: {bathrooms: 1, dinings: 2, ...}  // Midnights mapped to number of people required for each chore
# "people": [Bill, Jack, Daniel, Eric, ...]  // List of all people available for midnights
# "dayPreferences": {Bill: [M, W, F], Jack: [F, Sa, Su], ...}  // Midnight preferences for which days are best
# "midnightPreferences": {Bill: [bathrooms, dinings, ...], Jack: [commons, dishes, ...], ...}
# "progress": {Bill: 21, Jack: 35, ...}  // Number of midnights points each person has
with open("midnights.json", "r") as infile:
    # TODO: Add point values to each midnight and let the cost generation reflect the point reward
    info = json.load(infile)
    dayToMidnights = info["dayToMidnights"]
    midnightsToNumReq = info["midnightsToNumReq"]
    people = info["people"]
    dayPreferences = info["dayPreferences"]
    midnightPreferences = info["midnightPreferences"]
    progress = info["progress"]

    S, T = Vertex("S"), Vertex("T")
    G = FlowNetwork(S, T)
    v = {}  # Stores the mapping of string to Vertex wrapped string (used to identify/add edges to/from bois in graph)

    midnightsCount = 0
    for day in dayToMidnights:
        for m in dayToMidnights[day]:
            midnightsCount += 1

    for boi in people:
        v[boi] = Vertex(boi)
        # Edges from source to people with weight: w(S, p) = ceil(floor(n/k) * (progress[p]/total_req))
        G.addEdge(S, v[boi], 5, weightedPersonCost(progress[boi]))

    for day in dayToMidnights:
        for m in dayToMidnights[day]:
            for i in range(midnightsToNumReq[m]):
                midnightWithDay = Vertex(createNewMidnight(day, m, i))
                # Edges from midnights to sink with weight 1, cost 1
                G.addEdge(midnightWithDay, T, 1, 1)
                for boi in people:
                    # Exists an edge from every boi to every midnight, different cost based on day + m preferences
                    costBoiMidnight = getCostBoiToMidnight(day in dayPreferences[boi], m in midnightPreferences[boi])
                    if day in dayPreferences[boi] or m in midnightPreferences[boi]:
                        G.addEdge(v[boi], midnightWithDay, 1, costBoiMidnight)

    # print(G.getMaxFlow())
    print(G.getMinCostMaxFlow())
    peopleMidnightMap = getMidnightAssignments(G, people)
    print(peopleMidnightMap)

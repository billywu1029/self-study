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

def weightedMidnightsCount(totalMidnights: int, numPeople: int, pointsProgress: int) -> int:
    """
    Gets an upper bound on the number of midnights to be assigned to a person, determined by:
        floor(totalMidnights/numPeople) weighted by the person's pointsProgress
    @param totalMidnights: number of required midnights for the week
    @param numPeople: number of people available to do midnights for the week
    @param pointsProgress: number of midnight points the person has
    @return: int of max num of midnights one person should be allowed in a week
    """
    return int(round(totalMidnights // numPeople * (1 - pointsProgress / POINTS_REQ))) + 1

def getMidnightAssignments(G: Network, people: list) -> dict:
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
        result[boi] = [m.val for m in G.getChildren(u) if G.flowGraph.getWeight(u, m) > 0]
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
    info = json.load(infile)
    dayToMidnights = info["dayToMidnights"]
    midnightsToNumReq = info["midnightsToNumReq"]
    people = info["people"]
    dayPreferences = info["dayPreferences"]
    midnightPreferences = info["midnightPreferences"]
    progress = info["progress"]

    S, T = Vertex("S"), Vertex("T")
    G = Network(S, T)

    midnightsCount = 0
    for day in dayToMidnights:
        for m in dayToMidnights[day]:
            midnightsCount += 1

    for boi in people:
        # Edges from source to people with weight: w(S, p) = ceil(floor(n/k) * (progress[p]/total_req))
        # G.addEdge(S, boi, weightedMidnightsCount(midnightsCount, len(people), progress[boi]))
        G.addEdge(S, boi, 100000)
        for day in dayToMidnights:
            for m in dayToMidnights[day]:
                for i in range(midnightsToNumReq[m]):
                    midnightWithDay = createNewMidnight(day, m, i)
                    # Edges from people to midnights with weight: w(p, m) = 1(m in mPref[p]) * 1(day in dayPref[p])
                    if day in dayPreferences[boi] and m in midnightPreferences[boi]:
                        G.addEdge(boi, midnightWithDay, 1)
                    # Edges from midnights to sink with weight: w(m, T) = choresToNumReq[m]
                    G.addEdge(midnightWithDay, T, 1)

    print(G.getMaxFlow())
    peopleMidnightMap = getMidnightAssignments(G, people)
    print(peopleMidnightMap)

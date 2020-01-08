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
# PREFER_DAY_PENALTY = 30
PREFER_MIDNIGHT_PENALTY = 10
STRONGLY_AGAINST_PENALTY = 50  # Could potentially be used later when implementing multiple levels of preferences

def weightedPersonCost(pointsProgress: int) -> int:
    """
    Gets a weighted cost of assigning a midnight to each person, determined by:
        PERSON_BASE_COST ** (1 + person's pointsProgress / POINTS_REQ)
    Intuition: The more midnight points someone has, the less midnights they should be assigned, and vice versa.
    @param pointsProgress: number of midnight points the person has
    @return: int of max num of midnights one person should be allowed in a week
    """
    return int(round(PERSON_BASE_COST ** (1 + pointsProgress / POINTS_REQ)))

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
        daysAssigned = (dayBoi for dayBoi in G.flowGraph.getChildren(u) if G.flowGraph.getWeight(u, dayBoi) > 0)
        result[boi] = []
        for day in daysAssigned:
            for m in G.capacityGraph.getChildren(day):
                if G.flowGraph.getWeight(day, m) > 0:
                    result[boi].append(m.val)
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

def createNewDayNode(day: str, boi: str) -> str:
    """Create a new string that concatenates day and boi together"""
    return "%s|%s" % (day, boi)

# def getDayCost(preferDay: bool) -> int:
#     """
#     Gets the cost associated with a edge from person to their day node, based on whether or not the day was preferred
#     @param preferDay: True if the day was preferred, and False o/w
#     @return: cost as an int following the formula: 1(dayPreffed) * PREFER_DAY_PENALTY
#     """
#     return PREFER_DAY_PENALTY if not preferDay else 0

def getCostBoiDayToMidnight(preferMidnight: bool, midnightWorth: int, boiProgress: int) -> int:
    """
    Gets the cost for an edge from a person to any corresponding midnight. Intuitively, should assign low cost for
    midnights that are more preferred, and higher cost if not preferred. Can even use different levels of preference
    so that strongly prefer -> 0 cost, strongly do not prefer -> super high cost.
    @param preferMidnight: True to indicate that the midnight is preferred, False o/w
    @param midnightWorth: How many points the midnight is worth
    @param boiProgress: How many points the person has
    @return: int generated via formula:
        1(preferMidnight) * PREFER_MIDNIGHT_PENALTY
    """
    # TODO: Different levels of preference to potentially create useful backdoors to guarantee midnights you want
    # TODO: point values of midnights to influence cost, dpeneding on progress made
    midnightCoeff = PREFER_MIDNIGHT_PENALTY if not preferMidnight else 1
    return midnightCoeff

def getPeopleMidnightsToDayAssignments(peopleTasksMap: dict) -> dict:
    """
    Given a mapping of people to their list of midnights, return a new map that maps each day to the corresponding
    people that are in turn mapped to whichever midnights they were assigned to do for that particular day.
    """
    result = {"M": {}, "T": {}, "W": {}, "Th": {}, "F": {}, "Sa": {}, "Su": {}}
    for boi in peopleTasksMap:
        for m in peopleTasksMap[boi]:
            day, midnight, idx = m.strip().split("|")  # Stay safe by stripping, remember that kids
            if boi in result[day]:
                result[day][boi].append(midnight)
            else:
                result[day][boi] = [midnight]
    return result

def getPeoplePointsGain(dayToAssignments: dict, pointsMap: dict) -> dict:
    """
    Given a mapping of day to midnight assignments for each person, output a mapping of each person to points gained
    @param dayToAssignments: input mapping taking the form: {M: {Jack: [bathrooms, dinings], Bill: [commons], ...}, ...}
    @param pointsMap: maps midnights to their associated point values
    @return: mapping taking the form: {Bill: 1, Jack: 2, ...}
    """
    result = {}
    for day in dayToAssignments:
        for person in dayToAssignments[day]:
            if person not in result:
                result[person] = 0
            for m in dayToAssignments[day][person]:
                result[person] += pointsMap[m]
    return result

def extractData(inPath: str) -> tuple:
    """
    Given a filename path to an input JSON file, extracts the data into a tuple of dictionaries
    @param inPath: input file str, must point to valid JSON file following the format:
        "dayToMidnights": {M: [bathrooms, dinings, ...], T: [...], ...}
        "midnightPointValues": {bathrooms: 1, dinings: 2, ...}
        "midnightsToNumReq: {bathrooms: 1, dinings: 2, ...}
        "people": [Bill, Jack, Daniel, Eric, ...]
        "dayPreferences": {Bill: [M, W, F], Jack: [F, Sa, Su], ...}
        "midnightPreferences": {Bill: [bathrooms, dinings, ...], Jack: [commons, dishes, ...], ...}
        "progress": {Bill: 21, Jack: 35, ...}
    @return: tuple of dictionaries + lists from the JSON, ordered as such:
        (dayToMidnights, midnightPointValues, midnightsToNumReq, people, dayPreferences, midnightPreferences, progress)
    """
    with open(inPath, "r") as infile:
        info = json.load(infile)
        dayToMidnights = info["dayToMidnights"]
        midnightPointValues = info["midnightPointValues"]
        midnightsToNumReq = info["midnightsToNumReq"]
        people = info["people"]
        dayPreferences = info["dayPreferences"]
        midnightPreferences = info["midnightPreferences"]
        progress = info["progress"]
    return dayToMidnights, midnightPointValues, midnightsToNumReq, people, dayPreferences, midnightPreferences, progress


def generateMidnightsFlowNetwork(dayToMidnights: dict,
                                 midnightPointValues: dict,
                                 midnightsToNumReq: dict,
                                 people: list,
                                 dayPreferences: dict,
                                 midnightPreferences: dict,
                                 progress: dict,
                                 outPath: str=None) -> FlowNetwork:
    """
    Given midnights preferences/points info, generates a Flow Network to model the ZBT midnights assignment problem
    Optionally, write the Flow Network to an output JSON file, specified with path outPath
    @param dayToMidnights: Days mapped to midnights needed that day
    @param midnightPointValues: Point values for each midnight
    @param midnightsToNumReq: Midnights mapped to number of people req for each chore
    @param people: List of all people available for midnights
    @param dayPreferences: Midnight preferences for which days are best
    @param midnightPreferences: Which midnights each person prefers
    @param progress: Number of midnights points each person has
    @param outPath: output file str, if doesn't exist, then creates the file under the tests/ directory.
        Follows format specified in FlowNetwork's serializeJSON method
    @return: Flow Network that models the midnights assignment problem
    """
    S, T = Vertex("S"), Vertex("T")
    G = FlowNetwork(S, T)
    v = {}  # Stores the mapping of string to Vertex wrapper (used to identify/add edges to/from bois in graph)

    for boi in people:
        v[boi] = Vertex(boi)
        # Edges from source to people with weight: w(S, p) = ceil(floor(n/k) * (progress[p]/total_req))
        G.addEdge(S, v[boi], 4, weightedPersonCost(progress[boi]))  # Total limit per week to be 4

    for day in dayToMidnights:
        for m in dayToMidnights[day]:
            for i in range(midnightsToNumReq[m]):
                midnightWithDay = Vertex(createNewMidnight(day, m, i))
                # Edges from midnights to sink with weight 1, cost 1
                G.addEdge(midnightWithDay, T, 1, 1)
                for boi in people:
                    for boisDay in dayToMidnights:  # all 7 days for each boi to capture midnights/day limit
                        if boisDay in dayPreferences[boi]:
                            dayWithBoi = Vertex(createNewDayNode(boisDay, boi))
                            # limit number of midnights per day to 1, and higher cost if day not preferred
                            G.addEdge(v[boi], dayWithBoi, 1, 1)
                            # Edge from every boi's day to every midnight pref'ed, cost depends on progress
                            costBoiDayToMidnight = getCostBoiDayToMidnight(
                                m in midnightPreferences[boi],
                                midnightPointValues[m],
                                progress[boi]
                            )
                            G.addEdge(dayWithBoi, midnightWithDay, 1, costBoiDayToMidnight)

    if outPath is not None:
        G.serializeToJSON(outPath)  # TODO: Make a serialize + deserialize to/from JSON for the Flow Network

    return G

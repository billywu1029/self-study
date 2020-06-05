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

import Graph

def process_input(airports: list, routes: list) -> Graph:
    """
    Given a list of airports (as strings), a list of routes (as either tuples or lists of strings, return the
    resulting directed Graph that represents the current flight options, where vertices are airports and edges are
    one-way flights.
    """
    V = set(airports)
    E = {}
    for s, d in routes:
        if s not in E:
            E[s] = {d}
        else:
            E[s].add(d)
    return Graph.Graph(V, E)

if __name__ == "__main__":
    airports = ["A", "B", "C", "D", "E", "F", "G", "H"]
    routes = [("A", "C"), ("B", "C"), ("D", "F"), ("E", "H"), ("D", "E"), ("C", "G"), ("A", "F")]
    start = "A"
    G = process_input(airports, routes)
    print(G)


import math, itertools, json

# Program to solve this problem (albeit in Python):
# https://www.notion.so/Practice-Coffee-Script-Exercise-187d9245277540898e24f6084d35d8db

class Student:
    def __init__(self, name, noisy, understands, fights_with):
        self.name = name
        self.noisy = noisy
        self.understands = understands
        self.fights_with = fights_with

def boi(n, A, k):
    if k == 1 and len(A) <= math.ceil(len(A)/k):
        return [all_combos(A, len(A))]
    result = []
    combos = all_combos(A, math.ceil(len(A)/k))
    for combo in combos:
        prev_bois = boi(n, list_without(A, combo), k-1)
        for b in prev_bois:
            b.append(combo)
        result.extend(prev_bois)  # Extend result by newly modified prev boi w our new combo
    return result

def all_combos(A, sublistSize):
    """Return all possible combinations of length sublistSize from A"""
    return list(itertools.combinations(A, sublistSize))

def list_without(A, sublist):
    """Return copy of A without any of the elements in the sublist"""
    # Note that sublist will contain Student objects in the real application, so each is unique
    result = []
    for i in range(len(A)):
        if A[i] not in sublist:
            result.append(A[i])
    return result

if __name__ == "__main__":
    with open("bruh.json", "r") as f:
        info = json.load(f)
        groups, studentsRaw = info["groups"], info["students"]
        studentNames = [s["name"] for s in studentsRaw]
        studentsMap = {s["name"]: Student(s["name"], s["noisy"], s["understands"], s["fights_with"]) for s in studentsRaw}
        # Keep a map of name to Student object for when you're actually doing the filtering
        allgroups = boi(len(studentNames), studentNames, groups)
        validSetups = []
        for classSetup in allgroups:
            subgroupsGucci = True
            for subgroup in classSetup:
                numNoisy = 0
                numUnderstands = 0
                fightPairPresent = False
                for bro in subgroup:
                    s = studentsMap[bro]
                    if s.noisy:
                        numNoisy += 1
                    if s.understands:
                        numUnderstands += 1
                    if any(boiWithBeef in subgroup for boiWithBeef in s.fights_with):
                        fightPairPresent = True
                        break
                if numNoisy > 2 or numUnderstands < 1 or fightPairPresent:
                    subgroupsGucci = False
                    break
            if subgroupsGucci:
                validSetups.append(classSetup)
        print(validSetups)


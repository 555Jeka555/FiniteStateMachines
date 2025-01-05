import csv
from collections import defaultdict, deque
import argparse

def readNFA(filename):
    nfa = {
        'states': [],
        'alphabet': [],
        'transitions': defaultdict(lambda: defaultdict(list)),
        'startState': None,
        'finalStates': []
    }

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)

        statesLine = next(reader)
        for i, cell in enumerate(statesLine):
            if cell:
                nfa['states'].append(cell)
                if headers[i] == "F":
                    nfa['finalStates'].append(cell)

        for row in reader:
            if row[0]:
                symbol = row[0]
                nfa['alphabet'].append(symbol)
                for i, cell in enumerate(row[1:], start=0):
                    if cell:
                        destinations = cell.split(',')
                        for destination in destinations:
                            nfa['transitions'][nfa['states'][i]][symbol].append(destination)

    if nfa['states']:
        nfa['startState'] = nfa['states'][0]

    return nfa


def epsilonClosure(nfa, state):
    closure = {state}
    toProcess = deque([state])

    while toProcess:
        current = toProcess.popleft()
        if current in nfa['transitions'] and "ε" in nfa['transitions'][current]:
            for nextState in nfa['transitions'][current]["ε"]:
                if nextState not in closure:
                    closure.add(nextState)
                    toProcess.append(nextState)

    return closure


def buildDFATransitionTable(nfa):
    dfa = {
        'states': set(),
        'alphabet': [],
        'transitions': {},
        'finalStates': set(),
        'startState': None
    }

    stateQueue = deque()

    startClosure = epsilonClosure(nfa, nfa['startState'])
    stateQueue.append(startClosure)

    processedStates = {frozenset(startClosure): "X0"}
    dfa['startState'] = "X0"

    alphabetDFA = [symbol for symbol in nfa['alphabet'] if symbol != 'ε']
    dfa['alphabet'] = alphabetDFA

    if any(state in nfa['finalStates'] for state in startClosure):
        dfa['finalStates'].add("X0")

    stateCounter = 1

    while stateQueue:
        currentStates = stateQueue.popleft()
        currentStateName = processedStates[frozenset(currentStates)]

        for symbol in alphabetDFA:
            reachable = set()

            for state in currentStates:
                if state in nfa['transitions'] and symbol in nfa['transitions'][state]:
                    for nextState in nfa['transitions'][state][symbol]:
                        closure = epsilonClosure(nfa, nextState)
                        reachable.update(closure)

            if reachable:
                frozenReachable = frozenset(reachable)
                if frozenReachable not in processedStates:
                    newStateName = f"X{stateCounter}"
                    processedStates[frozenReachable] = newStateName
                    stateQueue.append(reachable)

                    if any(state in nfa['finalStates'] for state in reachable):
                        dfa['finalStates'].add(newStateName)

                    stateCounter += 1

                dfa['transitions'].setdefault(currentStateName, {})[symbol] = processedStates[frozenReachable]
            else:
                dfa['transitions'].setdefault(currentStateName, {})[symbol] = ""

    return dfa


def writeDFAToFile(dfa, filename):
    with open(filename, 'w') as file:
        renamedState = {state: f"q{i}" for i, state in enumerate(dfa['transitions'].keys())}
        if (len(renamedState) == 0):
            file.write(";F\n")
            file.write(";X0")
            return
        file.write(";")
        if dfa['startState'] in dfa['finalStates']:
            file.write("F")

        for state in dfa['transitions'].keys():
            if state != dfa['startState']:
                file.write(f";{'F' if state in dfa['finalStates'] else ''}")

        file.write("\n")

        file.write(";")
        file.write(renamedState[dfa['startState']])

        for state in dfa['transitions'].keys():
            if state != dfa['startState']:
                file.write(f";{renamedState[state]}")

        file.write("\n")

        for symbol in dfa['alphabet']:
            line = [symbol]
            for state in dfa['transitions'].keys():
                nextState = dfa['transitions'][state].get(symbol, "")
                line.append(renamedState[nextState] if nextState != "" else "")
            file.write(";".join(line) + "\n")


def determineNFA(inputFile, outputFile):
    nfa = readNFA(inputFile)
    dfa = buildDFATransitionTable(nfa)
    writeDFAToFile(dfa, outputFile)

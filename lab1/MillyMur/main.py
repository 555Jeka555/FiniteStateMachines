from collections import deque, defaultdict
from typing import Set, Dict, List


class MooreTransition:
    def __init__(self, fromState: int, toStates: Set[int], inSymbol: str):
        if toStates is None:
            toStates = set()
        self.fromState = fromState
        self.toStates = toStates
        self.inSymbol = inSymbol


class MooreState:
    def __init__(self, state: str = "", outSymbol: str = "", transitions: Set[int] = None):
        if transitions is None:
            transitions = set()
        self.state = state
        self.outSymbol = outSymbol
        self.transitions = transitions


class RegexToNFA:
    def __init__(self, regularExpression: str):
        self.alphabet = {"e"}
        self.regularExpression = regularExpression
        self.states: List[MooreState] = []
        self.statesMap: Dict[str, int] = {}
        self.transitions: List[MooreTransition] = []
        self.toNfa()

    def addTransitionToNew(self, fromState: int, toState: int, ch: str = "e"):
        fromStateIdx = fromState
        self.states[fromStateIdx].transitions.add(len(self.transitions))
        self.states.append(MooreState(f"S{toState}", "", {len(self.transitions)}))
        self.transitions.append(MooreTransition(fromStateIdx, {toState}, ch))

    def addTransitionTo(self, fromState: int, toState: int, ch: str = "e"):
        self.states[fromState].transitions.add(len(self.transitions))
        self.transitions.append(MooreTransition(fromState, {toState}, ch))

    def writeToCsvFile(self, filename: str):
        with open(filename, 'w') as file:
            file.write(";".join([""] + [state.outSymbol for state in self.states]) + "\n")
            file.write(";".join([""] + [state.state for state in self.states]) + "\n")

            for inSymbol in self.alphabet:
                file.write(inSymbol)

                for state in self.states:
                    emptyTransitionsSet = set()

                    for transition in state.transitions:
                        t = self.transitions[transition]
                        if t.fromState == self.states.index(state) and t.inSymbol == inSymbol:
                            for toState in t.toStates:
                                if toState == self.states.index(state) and inSymbol == "e":
                                    continue
                                emptyTransitionsSet.add(self.states[toState].state)

                    emptyTransitions = ",".join(emptyTransitionsSet)
                    file.write(f";{emptyTransitions}")

                file.write("\n")

    def convertToNFAFormat(self):
        nfa = {
            'states': [],
            'alphabet': list(self.alphabet),
            'transitions': defaultdict(lambda: defaultdict(list)),
            'startState': None, 
            'finalStates': []
        }

        for state in self.states:
            nfa['states'].append(state.state)
            if state.outSymbol == "F":
                nfa['finalStates'].append(state.state)

        nfa['startState'] = self.states[0].state

        for transition in self.transitions:
            fromState = self.states[transition.fromState].state
            inSymbol = transition.inSymbol
            toStates = [self.states[state].state for state in transition.toStates]

            for toState in toStates:
                nfa['transitions'][fromState][inSymbol].append(toState)

        return nfa

    def toNfa(self):
        stateCounter = 0
        stateIndex = 0
        preBracketStateIndex = deque([0])
        stateIndexToBrackets = deque([set()])

        self.states.append(MooreState("S0"))
        self.transitions.append(MooreTransition(0, {0}, "e"))

        closeBracket = False
        openBracket = False

        for c in self.regularExpression:
            if c == "|":
                if closeBracket:
                    preBracketStateIndex.pop()

                stateIndexToBrackets[-1].add(stateIndex)
                stateIndex = preBracketStateIndex[-1]
                openBracket = False
                closeBracket = False
            elif c == "(":
                stateCounter += 1
                self.states.append(MooreState(f"S{stateCounter}"))
                self.addTransitionTo(stateCounter, stateCounter, "e")
                self.addTransitionTo(stateIndex, stateCounter, "e")
                stateIndex = stateCounter
                stateIndexToBrackets.append(set())
                preBracketStateIndex.append(stateCounter)

                openBracket = True
                closeBracket = False
            elif c == ")":
                stateCounter += 1
                if openBracket:
                    self.addTransitionToNew(stateIndex, stateCounter, "e")
                    stateIndex = stateCounter
                    preBracketStateIndex.pop()
                    stateIndexToBrackets.pop()
                else:
                    if closeBracket:
                        preBracketStateIndex.pop()

                    self.states.append(MooreState(f"S{stateCounter}"))
                    self.addTransitionTo(stateIndex, stateCounter, "e")
                    if stateIndexToBrackets[-1]:
                        for stateInd in stateIndexToBrackets[-1]:
                            self.addTransitionTo(stateInd, stateCounter, "e")
                    stateIndexToBrackets.pop()
                    stateIndex = stateCounter
                    closeBracket = True
                openBracket = False
            elif c == "+":
                stateCounter += 1
                if closeBracket:
                    self.addTransitionToNew(stateIndex, stateCounter, "e")
                    transition = self.transitions[
                        next(iter(self.states[preBracketStateIndex[-1]].transitions))
                    ]
                    self.addTransitionTo(stateCounter, preBracketStateIndex[-1], transition.inSymbol)
                    preBracketStateIndex.pop()
                else:
                    self.addTransitionToNew(stateIndex, stateCounter, "e")
                    transition = self.transitions[
                        next(iter(self.states[stateIndex].transitions))
                    ]
                    self.addTransitionTo(stateCounter, stateIndex, transition.inSymbol)

                stateIndex = stateCounter
                openBracket = False
                closeBracket = False
            elif c == "*":
                stateCounter += 1
                if closeBracket:
                    self.addTransitionToNew(stateIndex, stateCounter, "e")
                    transition = self.transitions[
                        next(iter(self.states[preBracketStateIndex[-1]].transitions))
                    ]
                    self.addTransitionTo(stateIndex, preBracketStateIndex[-1], transition.inSymbol)
                    self.addTransitionTo(transition.fromState, stateCounter, "e")
                    preBracketStateIndex.pop()
                else:
                    self.addTransitionToNew(stateIndex, stateCounter, "e")
                    transition = self.transitions[
                        next(iter(self.states[stateIndex].transitions))
                    ]
                    self.addTransitionTo(stateCounter, stateIndex, transition.inSymbol)
                    self.addTransitionTo(transition.fromState, stateCounter, "e")

                stateIndex = stateCounter
                openBracket = False
                closeBracket = False
            else:
                stateCounter += 1
                if closeBracket:
                    preBracketStateIndex.pop()

                self.alphabet.add(c)
                self.addTransitionToNew(stateIndex, stateCounter, c)
                stateIndex = stateCounter
                openBracket = False
                closeBracket = False

        stateCounter += 1
        self.states.append(MooreState(f"S{stateCounter}", "F"))
        if stateIndexToBrackets:
            stateIndexToBrackets[-1].add(stateIndex)

        if stateIndexToBrackets and stateIndexToBrackets[-1]:
            for stateInd in stateIndexToBrackets[-1]:
                self.addTransitionTo(stateInd, stateCounter, "e")


if __name__ == "__main__":
    import sys

    if len(sys.argv) not in {3, 4}:
        print("main.py <outputFile> regularExpression")
        sys.exit(1)

    outputFile = sys.argv[1]
    regularExpression = sys.argv[2]

    if len(sys.argv) == 4:
        outputFile = sys.argv[2]
        regularExpression = sys.argv[3]

    rtNfa = RegexToNFA(regularExpression)
    rtNfa.writeToCsvFile(outputFile)

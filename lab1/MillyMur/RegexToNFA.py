class RegexNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class State:
    def __init__(self):
        self.transitions = {}
        self.epsilonTransitions = []

    def addTransition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def addEpsilonTransition(self, state):
        self.epsilonTransitions.append(state)


class NFA:
    def __init__(self, startState, acceptState):
        self.startState = startState
        self.acceptState = acceptState


def isLiteral(value):
    return value not in "+*()|"


def parseRegex(expression):
    def parse(tokens):
        def getNext():
            return tokens.pop(0) if tokens else None

        def parsePrimary():
            token = getNext()
            if token == "\\":
                escaped = getNext()
                if isLiteral(escaped):
                    tokens.insert(0, escaped)
                else:
                    return RegexNode(escaped)
            if isLiteral(token):
                return RegexNode(token)
            elif token == "(":
                node = parseExpression()
                if getNext() != ")":
                    raise ValueError("Mismatched parentheses")
                return node
            raise ValueError(f"Unexpected token: {token}")

        def parseFactor():
            node = parsePrimary()
            while tokens and tokens[0] in ("*", "+"):
                op = "multiply" if getNext() == "*" else "add"
                node = RegexNode(op, left=node)
            return node

        def parseTerm():
            node = parseFactor()
            while tokens and tokens[0] and (isLiteral(tokens[0]) or tokens[0] == "("):
                right = parseFactor()
                node = RegexNode("concat", left=node, right=right)
            return node

        def parseExpression():
            node = parseTerm()
            while tokens and tokens[0] == "|":
                getNext()
                right = parseTerm()
                node = RegexNode("or", left=node, right=right)
            return node

        return parseExpression()

    tokens = list(expression)
    return parse(tokens)


def buildNFA(node):
    if node is None:
        return None

    if node.value not in ("concat", "or", "add", "multiply"):
        start = State()
        accept = State()
        start.addTransition(node.value, accept)
        return NFA(start, accept)
    elif node.value == "concat":
        leftNFA = buildNFA(node.left)
        rightNFA = buildNFA(node.right)
        leftNFA.acceptState.addEpsilonTransition(rightNFA.startState)
        return NFA(leftNFA.startState, rightNFA.acceptState)
    elif node.value == "or":
        start = State()
        accept = State()
        leftNFA = buildNFA(node.left)
        rightNFA = buildNFA(node.right)
        start.addEpsilonTransition(leftNFA.startState)
        start.addEpsilonTransition(rightNFA.startState)
        leftNFA.acceptState.addEpsilonTransition(accept)
        rightNFA.acceptState.addEpsilonTransition(accept)
        return NFA(start, accept)
    elif node.value == "multiply":
        start = State()
        accept = State()
        subNFA = buildNFA(node.left)
        start.addEpsilonTransition(subNFA.startState)
        start.addEpsilonTransition(accept)
        subNFA.acceptState.addEpsilonTransition(subNFA.startState)
        subNFA.acceptState.addEpsilonTransition(accept)
        return NFA(start, accept)
    elif node.value == "add":
        start = State()
        accept = State()
        subNFA = buildNFA(node.left)
        start.addEpsilonTransition(subNFA.startState)
        subNFA.acceptState.addEpsilonTransition(subNFA.startState)
        subNFA.acceptState.addEpsilonTransition(accept)
        return NFA(start, accept)

    raise ValueError(f"Unexpected node value: {node.value}")


def adaptNFA(nfa: NFA):
    stateIndex = {}
    index = 0

    def assignIndices(state):
        nonlocal index
        if state not in stateIndex:
            stateIndex[state] = f"S{index}"
            index += 1
            for symbol, states in state.transitions.items():
                for s in states:
                    assignIndices(s)
            for s in state.epsilonTransitions:
                assignIndices(s)

    assignIndices(nfa.startState)

    initState = stateIndex[nfa.startState]
    finiteState = stateIndex[nfa.acceptState]

    machine = {stateIndex[s]: {"isFinite": name == finiteState, "transitions": {}} for s, name in
               stateIndex.items()}

    for state, name in stateIndex.items():
        for symbol, states in state.transitions.items():
            machine[name]["transitions"].setdefault(symbol, set()).update(stateIndex[s] for s in states)
        for s in state.epsilonTransitions:
            machine[name]["transitions"].setdefault("ε", set()).add(stateIndex[s])

    symbols = set()
    for state in machine:
        trans = machine[state]["transitions"]
        for symbol in trans:
            symbols.add(symbol)

    for state in machine:
        for symbol in symbols:
            machine[state]["transitions"].setdefault(symbol, set())

    return initState, finiteState, machine


def processRegex(regexPattern):
    tree = parseRegex(regexPattern)
    nfa = buildNFA(tree)
    return adaptNFA(nfa)
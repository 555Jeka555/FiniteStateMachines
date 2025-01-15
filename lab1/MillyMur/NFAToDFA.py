def fillEpsilon(machine):
    epsilon = {}

    for state in machine:
        visited = set()
        stack = [state]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)

                if "ε" not in machine[vertex]["transitions"]:
                    continue
                for neighbor in machine[vertex]["transitions"]["ε"]:
                    if neighbor:
                        stack.append(neighbor)

        epsilon[state] = list(visited)

    return epsilon


def getDependencies(states, epsilon):
    dependencies = set()

    for state in states:
        dependencies.add(state)
        for transition in epsilon[state]:
            dependencies.add(transition)

    return list(dependencies)


def findKeyWithValue(dictionary, newValue):
    for key, value in dictionary.items():
        if tuple(sorted(value)) == tuple(sorted(newValue)):
            return key

    return None


def createDFA(initialState, finiteState, epsilon, machine):
    sCount = 0
    stateDependencies = {"s0": [initialState]}
    states = ["s0"]
    newMachine = {}

    for state in states:
        newMachine[state] = {
            "isFinite": finiteState in getDependencies(stateDependencies[state], epsilon),
            "transitions": {}
        }

        for symbol in filter(lambda x: x != "ε", machine[initialState]["transitions"]):
            transitions = []
            for dependency in getDependencies(stateDependencies[state], epsilon):
                transitions.extend(machine[dependency]["transitions"][symbol])
            transitions = list(set(transitions))
            key = ''
            if len(transitions) != 0:
                key = findKeyWithValue(stateDependencies, transitions)
            if key is None:
                sCount += 1
                key = f"s{sCount}"
                states.append(key)
                stateDependencies[key] = transitions
            newMachine[state]["transitions"][symbol] = key

    return newMachine


def adaptDFA(initialState, machine):
    states = machine.keys()
    inputSymbols = machine[initialState]["transitions"].keys()
    outputs = {}
    transitions = {}
    for state in states:
        outputs[state] = "F" if machine[state]["isFinite"] else ""
        transitions[state] = {}
        for symbol in inputSymbols:
            transitions[state][symbol] = machine[state]["transitions"][symbol]

    return states, inputSymbols, transitions, outputs, initialState


def processNFA(initialState, finiteState, machine):
    epsilon = fillEpsilon(machine)
    dfa = createDFA(initialState, finiteState, epsilon, machine)
    return adaptDFA("s0", dfa)
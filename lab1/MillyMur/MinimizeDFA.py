def removeUnreachableStates(states, inputSymbols, transitions, outputs, initialState):
    reachableStates = set()
    toVisit = [initialState]

    while toVisit:
        state = toVisit.pop()
        if state in reachableStates:
            continue
        reachableStates.add(state)

        for symbol in transitions[state]:
            transition = transitions[state][symbol]
            if transition:
                toVisit.append(transition)

    return list(filter(lambda x: x in reachableStates, states)), inputSymbols, transitions, outputs, initialState


def minimizeMooreMachine(states, inputSymbols, transitions, outputs, initialState):
    outputGroups = {}
    for state in states:
        output = outputs[state]
        outputGroups.setdefault(output, set()).add(state)

    partitions = list(outputGroups.values())

    def refine(partitions):
        newPartitions = []
        for group in partitions:
            subgroup = {}
            for state in group:
                key = ""
                for symbol in inputSymbols:
                    for i, s in enumerate(partitions):
                        if transitions[state][symbol] in s:
                            key += symbol + str(i)
                subgroup.setdefault(key, set()).add(state)
            newPartitions.extend(subgroup.values())
        return newPartitions

    while True:
        newPartitions = refine(partitions)
        if newPartitions == partitions:
            break
        partitions = newPartitions

    stateMap = {}
    minimizedStates = []
    minimizedTransitions = {}
    minimizedOutputs = {}

    for i, group in enumerate(partitions):
        newState = f"S{i}"
        for state in group:
            stateMap[state] = newState
        minimizedStates.append(newState)
        representative = next(iter(group))
        minimizedOutputs[newState] = outputs[representative]

    for group in partitions:
        representative = next(iter(group))
        newState = stateMap[representative]
        minimizedTransitions[newState] = {
            symbol: stateMap[transitions[representative][symbol]] if transitions[representative][symbol] else ""
            for symbol in inputSymbols
        }
    minimizedInitialState = stateMap[initialState]

    return minimizedStates, inputSymbols, minimizedTransitions, minimizedOutputs, minimizedInitialState


def processDFA(states, inputSymbols, transitions, outputs, initialState):
    return minimizeMooreMachine(
        *removeUnreachableStates(states, inputSymbols, transitions, outputs, initialState))
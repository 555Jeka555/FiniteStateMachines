import csv
import argparse

NEW_STATE_NAME = 'q'
DEFAULT_MIN_STATE_NAME = 'X'
STATE_OUTPUT_SEPARATOR = '/'
STATE_INPUT_SEPARATOR = '/'
DEFAULT_GROUP_PREFIX = "_ "
CONVERT_TYPE_MEALY_TO_MOORE = 'mealy-to-moore'
CONVERT_TYPE_MOORE_TO_MEALY = 'moore-to-mealy'
MINIMIZE_MEALY = 'mealy'
MINIMIZE_MOORE = 'moore'


def printFormattedDict(data):
    for row in data:
        formattedRow = " ".join(f"{item:<7}" for item in row)
        print(formattedRow)
    print()


def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)


def readMealyFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        mealyStates = []
        for index, state in enumerate(data[0]):
            if index == 0:
                continue
            mealyStates.append(state.strip())

        mealyStateOutputs = {}
        inputValueToTransitions = {}
        for index, transitions in enumerate(data):
            if index == 0:
                continue

            inputValue = transitions[0].strip()

            for index2, transition in enumerate(transitions[1:]):
                state = transition.strip().split(STATE_OUTPUT_SEPARATOR)[0]
                output = transition.strip().split(STATE_OUTPUT_SEPARATOR)[1]

                if state not in mealyStateOutputs:
                    mealyStateOutputs[state] = set()
                mealyStateOutputs[state].add(output)

                if inputValue not in inputValueToTransitions:
                    inputValueToTransitions[inputValue] = {}
                    inputValueToTransitions[inputValue][mealyStates[index2]] = {}

                inputValueToTransitions[inputValue][mealyStates[index2]] = state + STATE_OUTPUT_SEPARATOR + output

        return mealyStates, mealyStateOutputs, inputValueToTransitions


def readMooreFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        mooreStates = []
        mooreStateOutputs = {}
        inputValueToTransitions = {}

        inputOutputsLine = data[0][1:]
        inputStatesLine = data[1][1:]

        for output, state in zip(inputOutputsLine, inputStatesLine):
            mooreStates.append(state.strip())
            mooreStateOutputs[state.strip()] = output.strip()

        for transitions in data[2:]:
            inputValue = transitions[0].strip()

            for i, transition in enumerate(transitions[1:]):
                nextState = transition.strip()
                currentState = mooreStates[i]
                output = mooreStateOutputs[currentState]

                if inputValue not in inputValueToTransitions:
                    inputValueToTransitions[inputValue] = {}

                inputValueToTransitions[inputValue][currentState] = f"{nextState}{STATE_OUTPUT_SEPARATOR}{output}"

    return mooreStates, inputValueToTransitions


def mealyToMoore(inputFileName, outputFileName):
    mealyStates, mealyStateOutputs, inputValueToTransitions = readMealyFromCsv(inputFileName)
    mealyToMooreStates = {}

    mealyStateOutputs = dict(
        sorted(mealyStateOutputs.items(),
               key=lambda item: mealyStates.index(item[0]) if item[0] in mealyStates else float('inf')))
    for mealyState, output in mealyStateOutputs.items():
        mealyStateOutputs[mealyState] = sorted(output)

    for mealyState in mealyStates:
        if mealyState in mealyStateOutputs:
            for output in mealyStateOutputs[mealyState]:
                transition = mealyState + STATE_OUTPUT_SEPARATOR + output
                mealyToMooreStates[transition] = NEW_STATE_NAME + str(len(mealyToMooreStates))
        else:
            mealyToMooreStates[mealyState] = NEW_STATE_NAME + str(len(mealyToMooreStates))

    outputsRow = ['']
    statesRow = ['']
    for mealyState in mealyStates:
        if mealyState in mealyStateOutputs:
            for output in mealyStateOutputs[mealyState]:
                outputsRow.append(output)
                statesRow.append(mealyToMooreStates[mealyState + STATE_OUTPUT_SEPARATOR + output])
        else:
            outputsRow.append('')
            statesRow.append(mealyToMooreStates[mealyState])

    transitionsRows = []
    for inputValue, transitions in inputValueToTransitions.items():
        row = [inputValue]

        for currentState in transitions:
            nextState = inputValueToTransitions[inputValue][currentState]

            countOutputs = len(mealyStateOutputs.get(currentState, [1]))
            for i in range(countOutputs):
                row.append(mealyToMooreStates[nextState])

        transitionsRows.append(row)

    data = [outputsRow, statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    printFormattedDict(data)
    writeToCsv(outputFileName, data)


def mooreToMealy(inputFileName, outputFileName):
    mooreStateOutputs, inputValueToTransitions = readMooreFromCsv(inputFileName)

    statesRow = ['']
    for mooreState in mooreStateOutputs.keys():
        statesRow.append(mooreState)

    transitionsRows = []
    for inputValue, transitions in inputValueToTransitions.items():
        row = [inputValue]

        for currentState in transitions:
            nextState = inputValueToTransitions[inputValue][currentState]
            row.append(nextState)

        transitionsRows.append(row)

    data = [statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    printFormattedDict(data)
    writeToCsv(outputFileName, data)


def splitStates(
        groups,
        groupOutputs,
        stateToGroup,
        state,
        inputValueToTransitions,
        prevStateToGroup=None,
        groupPrefix=DEFAULT_GROUP_PREFIX,
):
    groupInputs = [groupPrefix]
    outputs = []
    for inputValue in inputValueToTransitions:
        if prevStateToGroup is None:
            groupInput = inputValueToTransitions[inputValue][state].split(STATE_INPUT_SEPARATOR)[1]

            groupInputs.append(groupInput)
            continue

        groupInput = inputValueToTransitions[inputValue][state].split(STATE_INPUT_SEPARATOR)[0]
        outputs.append(inputValueToTransitions[inputValue][state].split(STATE_INPUT_SEPARATOR)[1])

        groupName = prevStateToGroup[groupInput]
        groupNames = prevStateToGroup.values()
        unique_group_names = []
        for group in groupNames:
            if group not in unique_group_names:
                unique_group_names.append(group)
        groupInput = unique_group_names.index(groupName)
        groupInputs.append(str(groupInput))

    groupInputsStr = ' '.join(groupInputs)

    if groupInputsStr not in groups.keys():
        groups[groupInputsStr] = []
    groups[groupInputsStr].append(state)
    groupOutputs[groupInputsStr] = outputs
    stateToGroup[state] = groupInputsStr

    return groups, groupOutputs, stateToGroup


def splitStatesInGroup(states, inputValueToTransitions, prevStateToGroup=None):
    groups = {}
    groupOutputs = {}
    stateToGroup = {}

    if isinstance(states, list):
        for state in states:
            groups, groupOutputs, stateToGroup = splitStates(
                groups,
                groupOutputs,
                stateToGroup,
                state,
                inputValueToTransitions,
                prevStateToGroup,
            )
    else:
        for i, group in enumerate(states, start=1):
            for state in states[group]:
                groupPrefix = '\\' + str(i)
                groups, groupOutputs, stateToGroup = splitStates(
                    groups,
                    groupOutputs,
                    stateToGroup,
                    state,
                    inputValueToTransitions,
                    prevStateToGroup,
                    groupPrefix,
                )

    return groups, groupOutputs, stateToGroup


def groupStatesToInputs(states, inputValueToTransitions):
    groups, _, stateToGroup = splitStatesInGroup(states, inputValueToTransitions)

    groups, _, stateToGroup = splitStatesInGroup(groups, inputValueToTransitions, stateToGroup)

    while True:
        newGroups, groupOutputs, stateToGroup = splitStatesInGroup(groups, inputValueToTransitions, stateToGroup)
        groups = newGroups

        if str(newGroups) == str(groups):
            break

    return groups, groupOutputs


def minimizeMealy(inputFileName, outputFileName):
    mealyStates, mealyStateOutputs, inputValueToTransitions = readMealyFromCsv(inputFileName)
    groups, groupOutputs = groupStatesToInputs(mealyStates, inputValueToTransitions)

    statesRow = ['']
    for i in range(len(groups)):
        state = DEFAULT_MIN_STATE_NAME + str(i)
        statesRow.append(state)

    transitionsRows = []
    for i, inputValue in enumerate(inputValueToTransitions):
        row = [inputValue]

        for group in groups:
            groupStates = group.split(' ')[1:]
            state = DEFAULT_MIN_STATE_NAME + str(groupStates[i])
            output = groupOutputs[group][i]
            transition = state + STATE_INPUT_SEPARATOR + output
            row.append(transition)

        transitionsRows.append(row)

    data = [statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    printFormattedDict(data)

    writeToCsv(outputFileName, data)


def minimizeMoore(inputFileName, outputFileName):
    mooreStates, inputValueToTransitions = readMooreFromCsv(inputFileName)
    groups, groupOutputs = groupStatesToInputs(mooreStates, inputValueToTransitions)

    outputsRow = ['']
    statesRow = ['']
    for i in range(len(groups)):
        state = DEFAULT_MIN_STATE_NAME + str(i)
        statesRow.append(state)

        output = groupOutputs[list(groups.keys())[i]][0]
        outputsRow.append(output)

    transitionsRows = []
    for i, inputValue in enumerate(inputValueToTransitions):
        row = [inputValue]
        for group in groups:
            groupStates = group.split(' ')[1:]
            state = DEFAULT_MIN_STATE_NAME + str(groupStates[i])
            row.append(state)

        transitionsRows.append(row)

    data = [outputsRow, statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    printFormattedDict(data)
    writeToCsv(outputFileName, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('command', type=str, help='Input CSV file for Mealy')
    parser.add_argument('inputFileName', type=str, help='Input CSV file')
    parser.add_argument('outputFileName', type=str, help='Output CSV file')

    args = parser.parse_args()

    if args.command == CONVERT_TYPE_MEALY_TO_MOORE:
        mealyToMoore(args.inputFileName, args.outputFileName)
    elif args.command == CONVERT_TYPE_MOORE_TO_MEALY:
        mooreToMealy(args.inputFileName, args.outputFileName)
    elif args.command == MINIMIZE_MEALY:
        minimizeMealy(args.inputFileName, args.outputFileName)
    elif args.command == MINIMIZE_MOORE:
        minimizeMoore(args.inputFileName, args.outputFileName)
    else:
        print('Not found')

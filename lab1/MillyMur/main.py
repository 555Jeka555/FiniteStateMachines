import csv
import argparse

NEW_STATE_NAME = 'q'
CONVERT_TYPE_MEALY_TO_MOORE = 'mealy-to-moore'
CONVERT_TYPE_MOORE_TO_MEALY = 'moore-to-mealy'


def printFormattedDict(data):
    for row in data:
        formattedRow = " ".join(f"{item:<6}" for item in row)
        print(formattedRow)
    print()

def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)


def convertMealyToMoore(inputValues, mooreStates, millyStates, millyInputValue):
    data = []
    width = len(mooreStates.values()) + len(mooreStates) + 1
    height = len(inputValues) + 2
    remindMealyStates = millyStates.copy()

    for _ in range(height):
        tmp = []
        for _ in range(width):
            tmp.append('')
        data.append(tmp)

    i = 0
    for stateWithOutValue, newState in mooreStates.items():
        data[0][i + 1] = stateWithOutValue.split('/')[1]  # Для проверки убрать .split('/')[1]
        data[1][i + 1] = newState

        j = 0
        for inputValue in inputValues:
            data[j + 2][0] = inputValue

            statesToNewState = millyInputValue[inputValue]
            for state, newStateFromMealy in statesToNewState.items():
                millyState = stateWithOutValue.split('/')[0]
                if state == millyState:

                    if state in remindMealyStates:
                        remindMealyStates.remove(state)

                    data[j + 2][i + 1] = newStateFromMealy

            j += 1
        i += 1

    # i - сохранился с прошлого цикла, чтобы продолжить записывать дальше
    newStateCount = len(mooreStates.values()) + 2
    for remindMealyState in remindMealyStates:
        newStateNameRemind = NEW_STATE_NAME + str(newStateCount)
        newStateCount += 1

        data[1][i + 1] = newStateNameRemind

        j = 0
        for inputValue in inputValues:
            data[j + 2][0] = inputValue

            statesToNewState = millyInputValue[inputValue]
            for state, newStateFromMealy in statesToNewState.items():
                if state != remindMealyState:
                    continue

                for stateWithOutValue, newState in mooreStates.items():
                    if newState == newStateFromMealy:
                        data[j + 2][i + 1] = newStateFromMealy

            j += 1
        i += 1

    # Не подходит по формату
    # dataWithoutEmpties = []
    # for i, row in enumerate(data):
    #     tmp = []
    #     for j, cell in enumerate(row):
    #         if len(cell) != 0 or i <= 1 and j == 0:
    #             tmp.append(cell)
    #
    #     dataWithoutEmpties.append(tmp)

    return data


def readMooreFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []
        milly = []

        for row in reader:
            data.append(row)
            tmp = []
            for i in range(len(row)):
                tmp.append('')
            milly.append(tmp)

        printFormattedDict(data)

        millyStates = []
        millyStatesWithOut = {}

        i = 0
        for row in data:
            for j in range(len(row)):
                if i == 1 and j != 0:
                    millyState = data[i][j]

                    if millyState not in millyStates:
                        millyStates.append(millyState)
                        milly[1][j] = millyState

                    if j < len(data[0]):
                        millyStatesWithOut[millyState] = data[0][j]
                elif i > 1 and j == 0:
                    milly[i][j] = data[i][j]
                elif i > 1 and j > 0:
                    millyState = data[i][j]

                    milly[i][j] = millyState + '/' + millyStatesWithOut[millyState]
            i += 1

        milly.pop(0)

        return milly


def readMealyFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        for row in reader:
            data.append(row)

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
                state = transition.strip().split('/')[0]
                output = transition.strip().split('/')[1]

                if state not in mealyStateOutputs:
                    mealyStateOutputs[state] = set()
                mealyStateOutputs[state].add(output)

                if inputValue not in inputValueToTransitions:
                    inputValueToTransitions[inputValue] = {}
                    inputValueToTransitions[inputValue][mealyStates[index2]] = {}

                inputValueToTransitions[inputValue][mealyStates[index2]] = state + '/' + output

        return mealyStates, mealyStateOutputs, inputValueToTransitions


def mealyToMoore(inputFileName, outputFileName):
    mealyStates, mealyStateOutputs, inputValueToTransitions = readMealyFromCsv(inputFileName)

    pass


def mooreToMealy(inputFileName, outputFileName):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('conertType', type=str, help='Input CSV file for Mealy')
    parser.add_argument('inputFileName', type=str, help='Input CSV file')
    parser.add_argument('outputFileName', type=str, help='Output CSV file')

    args = parser.parse_args()

    if args.conertType == CONVERT_TYPE_MEALY_TO_MOORE:
        mealyToMoore(args.inputFileName, args.outputFileName)
    elif args.conertType == CONVERT_TYPE_MOORE_TO_MEALY:
        mealyToMoore(args.inputFileName, args.outputFileName)
    else:
        print('Not found')

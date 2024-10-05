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


def readMealyFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        millyStates = []
        newStates = []
        inputValues = []
        newStateCount = 0
        mooreStates = {}

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        i = 0
        for row in data:
            j = 0
            for cell in row:
                if i == 0 and j != 0:
                    millyStates.append(cell)
                elif i != 0 and j == 0:
                    inputValues.append(cell)
                elif i != 0 and j != 0:
                    newStateName = NEW_STATE_NAME + str(newStateCount)
                    newStateCount += 1

                    newStateAlreadyExist = False
                    for key in mooreStates.keys():
                        if key == cell:
                            newStateAlreadyExist = True
                    if newStateAlreadyExist:
                        continue

                    mooreStates[cell] = newStateName
                    newStates.append(newStateName)
                j += 1
            i += 1

        millyInputValue = {}
        i = 0
        for row in data:
            if i == 0:
                i += 1
                continue

            currentInputValue = ''
            j = 0
            for cell in row:
                if j == 0:
                    currentInputValue = cell
                elif j != 0:
                    currentState = millyStates[j - 1]

                    if currentInputValue not in millyInputValue:
                        millyInputValue[currentInputValue] = {}

                    millyInputValue[currentInputValue][currentState] = mooreStates[cell]

                j += 1

            i += 1

        return inputValues, mooreStates, millyStates, millyInputValue


def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)


def convertMealyToMoore(inputValues, mooreStates, millyStates, millyInputValue):
    data = []
    width = len(mooreStates.values()) + len(millyStates) + 1
    height = len(inputValues) + 2
    remindMealyStates = millyStates.copy()

    for _ in range(height):
        tmp = []
        for _ in range(width):
            tmp.append('')
        data.append(tmp)

    i = 0
    for stateWithOutValue, newState in mooreStates.items():
        data[0][i + 1] = stateWithOutValue
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
    newStateCount = -1
    for remindMealyState in remindMealyStates:
        data[0][i + 1] = remindMealyState

        newStateNameRemind = NEW_STATE_NAME + str(newStateCount)
        newStateCount -= 1

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

                    millyStatesWithOut[millyState] = data[0][j]
                elif i > 1 and j == 0:
                    milly[i][j] = data[i][j]
                elif i > 1 and j > 0:
                    millyState = data[i][j]

                    milly[i][j] = millyState + '/' + millyStatesWithOut[millyState]
            i += 1

        return milly

# @deprecated
def convertMooreToMealy(millyInputValues, inputValues):
    data = []
    width = len(millyInputValues.keys()) + 1
    height = len(inputValues) + 1

    for _ in range(height):
        tmp = []
        for _ in range(width):
            tmp.append('')
        data.append(tmp)

    k = 0
    for inputValue in inputValues:
        data[k + 1][0] = inputValue
        k += 1

    i = 0
    for millyState, inputValuesStateWithOut in millyInputValues.items():
        data[0][i + 1] = millyState

        j = 0
        for inputValue, stateWithOut in inputValuesStateWithOut.items():
            data[j + 1][i + 1] = stateWithOut
            j += 1

        i += 1

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('conertType', type=str, help='Input CSV file for Mealy')
    parser.add_argument('inputFileName', type=str, help='Input CSV file')
    parser.add_argument('outputFileName', type=str, help='Output CSV file')

    args = parser.parse_args()

    if args.conertType == CONVERT_TYPE_MEALY_TO_MOORE:
        inputValues, mooreStates, millyStates, millyInputValue = readMealyFromCsv(args.inputFileName)
        data = convertMealyToMoore(inputValues, mooreStates, millyStates, millyInputValue)
        printFormattedDict(data)
        writeToCsv(args.outputFileName, data)
    elif args.conertType == CONVERT_TYPE_MOORE_TO_MEALY:
        data = readMooreFromCsv(args.inputFileName)
        printFormattedDict(data)
        writeToCsv(args.outputFileName, data)
    else:
        print('Not found')

import csv

NEW_STATE_NAME = 'q'


def printFormattedDict(data):
    for row in data:
        formattedRow = " ".join(f"{item:<10}" for item in row)
        print(formattedRow)
    print()

def readMilyFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        states = []
        newStates = []
        inputValues = []
        newStateCount = 0
        mureStates = {}

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        i = 0
        for row in data:
            j = 0
            for cell in row:
                if i == 0 and j != 0:
                    states.append(cell)
                elif i != 0 and j == 0:
                    inputValues.append(cell)
                elif i != 0 and j != 0:
                    newStateName = NEW_STATE_NAME + str(newStateCount)
                    newStateCount += 1

                    newStateAlreadyExist = False
                    for key in mureStates.keys():
                        if key == cell:
                            newStateAlreadyExist = True
                    if newStateAlreadyExist:
                        continue

                    mureStates[cell] = newStateName
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
                    currentState = states[j - 1]

                    if currentInputValue not in millyInputValue:
                        millyInputValue[currentInputValue] = {}

                    millyInputValue[currentInputValue][currentState] = mureStates[cell]

                j += 1

            i += 1

        return inputValues, mureStates, millyInputValue


def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)

def convertMillyToMure(inputValues, mureStates, millyInputValue):
    print("inputValues: ", inputValues)
    print("mureStates: ", mureStates)
    print("millyInputValue: ", millyInputValue)

    data = []
    width = len(mureStates.values()) + 1
    height = len(inputValues) + 2

    for _ in range(height):
        tmp = []
        for _ in range(width):
            tmp.append('')

        data.append(tmp)

    i = 0
    for stateWithOutValue, newState in mureStates.items():
        data[0][i + 1] = stateWithOutValue
        data[1][i + 1] = newState

        j = 0
        for inputValue in inputValues:
            data[j + 2][0] = inputValue

            statesToNewState = millyInputValue[inputValue]
            for state, newStateFromMilly in statesToNewState.items():
                stateFromMure = stateWithOutValue.split('/')[0]
                if state == stateFromMure:
                    data[j + 2][i + 1] = newStateFromMilly

            j += 1
        i += 1

    return data


if __name__ == '__main__':
    fileNameRead = "data/read/Milly1.csv"
    fileNameWrite = "data/write/Milly1.csv"

    inputValues, mureStates, millyInputValue = readMilyFromCsv(fileNameRead)

    data = convertMillyToMure(inputValues, mureStates, millyInputValue)

    printFormattedDict(data)

    writeToCsv(fileNameWrite, data)
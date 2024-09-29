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

        millyStates = []
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
                    millyStates.append(cell)
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
                    currentState = millyStates[j - 1]

                    if currentInputValue not in millyInputValue:
                        millyInputValue[currentInputValue] = {}

                    millyInputValue[currentInputValue][currentState] = mureStates[cell]

                j += 1

            i += 1

        return inputValues, mureStates, millyStates, millyInputValue


def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)


def convertMillyToMure(inputValues, mureStates, millyStates, millyInputValue):
    data = []
    width = len(mureStates.values()) + len(millyStates) + 1
    height = len(inputValues) + 2
    remindMillyStates = millyStates.copy()

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
                millyState = stateWithOutValue.split('/')[0]
                if state == millyState:

                    if state in remindMillyStates:
                        remindMillyStates.remove(state)

                    data[j + 2][i + 1] = newStateFromMilly

            j += 1
        i += 1

    # i - сохранился с прошлого цикла, чтобы продолжить записывать дальше
    newStateCount = -1
    for remindMillyState in remindMillyStates:
        data[0][i + 1] = remindMillyState

        newStateNameRemind = NEW_STATE_NAME + str(newStateCount)
        newStateCount -= 1

        data[1][i + 1] = newStateNameRemind

        j = 0
        for inputValue in inputValues:
            data[j + 2][0] = inputValue

            statesToNewState = millyInputValue[inputValue]
            for state, newStateFromMilly in statesToNewState.items():
                if state != remindMillyState:
                    continue

                for stateWithOutValue, newState in mureStates.items():
                    if newState == newStateFromMilly:
                        data[j + 2][i + 1] = newStateFromMilly

            j += 1
        i += 1


    return data


def readMureFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        inputValues = []
        mureStates = {}

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        i = 0
        for row in data:
            j = 0

            for cell in row:
                if i > 1 and j == 0:
                    inputValues.append(cell)
                elif i > 1 and j != 0:
                    millyStateWithOut = data[0][j]
                    mureState = data[1][j]

                    if len(millyStateWithOut) == 0 and len(mureState) == 0:
                        continue

                    mureStates[mureState] = millyStateWithOut

                j += 1
            i += 1

        millyInputValues = {}
        i = 0
        for row in data:
            if i <= 1:
                i += 1
                continue

            currentInputValue = ''
            j = 0
            for cell in row:
                if j == 0:
                    currentInputValue = cell
                elif j != 0:
                    currentState = data[0][j].split('/')[0]
                    if len(currentState) == 0:
                        continue

                    if currentState not in millyInputValues:
                        millyInputValues[currentState] = {}

                    millyInputValues[currentState][currentInputValue] = mureStates[cell]

                j += 1

            i += 1

        return millyInputValues, inputValues


def convertMureToMilly(millyInputValues, inputValues):
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
    fileNameRead = "data/read/Milly2.csv"
    fileNameWrite = "data/write/Milly2.csv"

    # inputValues, mureStates, millyStates, millyInputValue = readMilyFromCsv(fileNameRead)
    # data = convertMillyToMure(inputValues, mureStates, millyStates, millyInputValue)
    # printFormattedDict(data)
    # writeToCsv(fileNameWrite, data)

    fileNameRead = "data/read/Mure1.csv"
    fileNameWrite = "data/write/Mure1.csv"

    millyInputValues, inputValues = readMureFromCsv(fileNameRead)
    data = convertMureToMilly(millyInputValues, inputValues)
    printFormattedDict(data)
    writeToCsv(fileNameWrite, data)

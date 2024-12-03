import csv
import re
import argparse

DIRECTION_PATTERN = r'<\w+>\s*[\wε]'
RIGHT_GRAMMA_PATTERN = r'^\s*<(\w+)>\s*->\s*([\wε](?:\s+<\w+>)?(?:\s*\|\s*[\wε](?:\s+<\w+>)?)*)\s*$'
LEFT_GRAMMA_PATTERN = r'^\s*<(\w+)>\s*->\s*((?:<\w+>\s+)?[\wε](?:\s*\|\s*(?:<\w+>\s+)?[\wε])*)\s*$'


def saveMooreToCSV(states, inputs, transitions, path):
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        states = sorted(states, key=lambda state: not state["isStart"])

        writer.writerow([''] + ['F' if s["isEnd"] else '' for s in states])
        writer.writerow([''] + [s["name"] for s in states])

        transition_data = {inputSymbol: [] for inputSymbol in inputs}

        for input in inputs:
            for state in states:
                next_state = transitions.get((state["name"], input), '')
                transition_data[input].append(f"{','.join(next_state)}")

        for input in inputs:
            row = [input] + transition_data[input]
            writer.writerow(row)


def addToAliases(state, aliases, index, isEnd = False, isStart = False):
    if state in aliases:
        return aliases, index
    s = 'q' + str(index)
    aliases[state] = {}
    aliases[state]["name"] = s
    aliases[state]["isEnd"] = isEnd
    aliases[state]["isStart"] = isStart
    index += 1
    return aliases, index


def prinAliases(aliases):
    for key, value in aliases.items():
        print(key, value["name"])
        
        
def listAliasesValues(aliases):
    return list(aliases.values())


def convertGrammaToMoore(isLeft, grammaTransitions):
    transitions = {}
    inputs = set()
    for transition in grammaTransitions:
        inputs.add(transition["y"])

    aliases = dict()
    index = 0

    if isLeft:
        aliases, index = addToAliases('H', aliases, index, False, True)
        aliases, index = addToAliases(grammaTransitions[0]["x1"], aliases, index, True)
    else:
        aliases, index = addToAliases('F', aliases, index, True)
        aliases, index = addToAliases(grammaTransitions[0]["x1"], aliases, index, False, True)

    for transition in grammaTransitions:
        if transition["x1"] is not None:
            aliases, index = addToAliases(transition["x1"], aliases, index)
        if transition["x2"] is not None:
            aliases, index = addToAliases(transition["x2"], aliases, index)

    for transition in grammaTransitions:
        to = None
        frm = None
        if not isLeft:
            frm = (aliases[transition["x1"]]["name"], transition["y"])
            if transition["x2"] is None:
                to = aliases.get('F')["name"]
            else:
                to = aliases[transition["x2"]]["name"]
        else:
            to = aliases[transition["x1"]]["name"]
            if transition["x2"] is None:
                frm = (aliases.get("H")["name"], transition["y"])
            else:
                frm = (aliases[transition["x2"]]["name"], transition["y"])
        if frm not in transitions:
            transitions[frm] = []
        transitions[frm].append(to)

    prinAliases(aliases)

    return listAliasesValues(aliases), inputs, transitions


def readGramma(data):
    print(data)

    isLeftPatter = re.compile(DIRECTION_PATTERN, re.MULTILINE)
    isLeft = bool(len(isLeftPatter.findall(data)) > 0)

    pattern = RIGHT_GRAMMA_PATTERN
    if isLeft:
        pattern = LEFT_GRAMMA_PATTERN

    p = re.compile(pattern, re.MULTILINE)

    grammaTransitions = []
    for transit in p.findall(data):
        x1 = transit[0]

        for t in str.split(transit[1], '|'):
            tdata = str.strip(t).split(" ")
            transition = {"x1": x1}
            yi = 0
            xi = 1
            if isLeft:
                yi, xi, = xi, yi
            if len(tdata) == 1:
                yi = 0
            transition["y"] = tdata[yi]
            if len(tdata) == 2:
                transition["x1"] = x1
                transition["x2"] = tdata[xi][1:-1]
            else:
                transition["x2"] = None
            grammaTransitions.append(transition)

    return isLeft, grammaTransitions


def readFile(path):
    with open(path) as f:
        return f.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('inputFile', type=str, help='Input txt')
    parser.add_argument('outputFile', type=str, help='Output csv')

    args = parser.parse_args()
    content = readFile(args.inputFile)
    isLeft, grammaTransitions = readGramma(content)
    states, inputs, transitions = convertGrammaToMoore(isLeft, grammaTransitions)
    saveMooreToCSV(states, inputs, transitions, args.outputFile)
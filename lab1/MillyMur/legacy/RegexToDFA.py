import RegexToNFA
import NFAToDFA
import csv
import os
import Slider

STATE_OUTPUT_SEPARATOR = '/'

def readDataFromCsv(fileName) -> list[str]:
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=";")
        data = []

        for row in reader:
            data.append(row)
    return data

class RegToDFAConverter:
    def __init__(self):
        pass

    def convert(self, expression: str) -> Slider.Slider:
        self.expression = expression
        try:
            os.remove("../data/Lexer/nfa.csv")
            os.remove("../data/Lexer/dfa.csv")
        except OSError as e:
            print(f"Error deleting files: {e}")

        regexToNFACovnerter = RegexToNFA.RegexToNFA(expression)
        regexToNFACovnerter.writeToCsvFile("./data/Lexer/nfa.csv")
        NFAToDFA.determineNFA("./data/Lexer/nfa.csv", "./data/Lexer/dfa.csv")
        return self.readDKAFromCSV("../data/Lexer/dfa.csv")

    def readDKAFromCSV(self, path: str) -> Slider.Slider:
        data = readDataFromCsv(path)

        outputs = data[0][1:]
        states = data[1][1:]
        finishStates = []

        mooreStates: list[Slider.State] = []

        for output, state in zip(outputs, states):
            mooreStates.append(Slider.State(state))
            if output == "F":
                finishStates.append(state)

        for transitions in data[2:]:
            input = transitions[0]

            for i, transition in enumerate(transitions[1:]):
                if transition != "":
                    mooreStates[i].AddTransition(input, transition)

        return Slider.Slider(mooreStates, finishStates)
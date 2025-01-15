import RegexToNFA
import NFAToDFA
import MinimizeDFA
import Slider
from typing import List


class RegToDFAConverter:
    def __init__(self):
        pass
    
    def convert(self, expression: str) -> Slider.Slider:
        nfa = RegexToNFA.processRegex(expression)
        dfa = NFAToDFA.processNFA(*nfa)
        states, input_symbols, transitions, outputs, initial_state = MinimizeDFA.processDFA(*dfa)

        sliderStates: List[Slider.State] = [Slider.State(initial_state)]
        finishStates = []

        for state in states:
            if outputs[state] == "F":
                finishStates.append(state)
            if state != initial_state:
                sliderState = Slider.State(state)
                sliderStates.append(sliderState)
            else:
                sliderState = sliderStates[0]

            stateTransaction = transitions[state]
            for input_symbol in input_symbols:
                transaction = stateTransaction[input_symbol]
                if transaction:
                    sliderState.AddTransition(input_symbol, transaction)

        return Slider.Slider(sliderStates, finishStates)

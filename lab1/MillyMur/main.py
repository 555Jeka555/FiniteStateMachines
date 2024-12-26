import re
import os
from collections import deque
from typing import Set, Dict, List, Union


class MooreTransition:
    def __init__(self, from_state: int, to_states: Set[int], in_symbol: str):
        if to_states is None:
            to_states = set()
        self.from_state = from_state
        self.to_states = to_states
        self.in_symbol = in_symbol


class MooreState:
    def __init__(self, state: str = "", out_symbol: str = "", transitions: Set[int] = None):
        if transitions is None:
            transitions = set()
        self.state = state
        self.out_symbol = out_symbol
        self.transitions = transitions


class RegexToNFA:
    def __init__(self, regular_expression: str):
        self.m_inSymbols = {"e"}  # epsilon (empty string) symbol
        self.m_regularExpression = regular_expression
        self.m_states: List[MooreState] = []
        self.m_statesMap: Dict[str, int] = {}
        self.m_transitions: List[MooreTransition] = []
        self.to_nfa()

    def add_transition_to_new(self, from_state: int, to_state: int, ch: str = "e"):
        from_state_idx = from_state
        self.m_states[from_state_idx].transitions.add(len(self.m_transitions))
        self.m_states.append(MooreState(f"S{to_state}", "", {len(self.m_transitions)}))
        self.m_transitions.append(MooreTransition(from_state_idx, {to_state}, ch))

    def add_transition_to(self, from_state: int, to_state: int, ch: str = "e"):
        self.m_states[from_state].transitions.add(len(self.m_transitions))
        self.m_transitions.append(MooreTransition(from_state, {to_state}, ch))

    def write_to_csv_file(self, filename: str):
        if not filename:
            raise ValueError(f"Can't open file {filename}")

        with open(filename, 'w') as file:
            # Write the header for the CSV
            file.write(";".join([""] + [state.out_symbol for state in self.m_states]) + "\n")
            file.write(";".join([""] + [state.state for state in self.m_states]) + "\n")

            for in_symbol in self.m_inSymbols:
                file.write(in_symbol)
                for state in self.m_states:
                    empty_transitions_set = set()

                    for transition in state.transitions:
                        t = self.m_transitions[transition]
                        if t.from_state == self.m_states.index(state) and t.in_symbol == in_symbol:
                            for to_state in t.to_states:
                                if to_state == self.m_states.index(state) and in_symbol == "e":
                                    continue
                                empty_transitions_set.add(self.m_states[to_state].state)

                    empty_transitions = ",".join(empty_transitions_set)
                    file.write(f";{empty_transitions}")
                file.write("\n")

    def to_nfa(self):
        state_counter = 0
        state_index = 0
        pre_bracket_state_index = deque([0])
        state_index_to_brackets = deque([set()])

        self.m_states.append(MooreState("S0"))
        self.m_transitions.append(MooreTransition(0, {0}, "e"))

        close_bracket = False
        open_bracket = False

        for c in self.m_regularExpression:
            if c == "(":
                state_counter += 1
                self.m_states.append(MooreState(f"S{state_counter}"))
                self.add_transition_to(state_counter, state_counter, "e")
                self.add_transition_to(state_index, state_counter, "e")
                state_index = state_counter
                state_index_to_brackets.append(set())
                pre_bracket_state_index.append(state_counter)

                open_bracket = True
                close_bracket = False
            elif c == ")":
                state_counter += 1
                if open_bracket:
                    self.add_transition_to_new(state_index, state_counter, "e")
                    state_index = state_counter
                    pre_bracket_state_index.pop()
                    state_index_to_brackets.pop()
                else:
                    if close_bracket:
                        pre_bracket_state_index.pop()

                    self.m_states.append(MooreState(f"S{state_counter}"))
                    self.add_transition_to(state_index, state_counter, "e")
                    if state_index_to_brackets[-1]:
                        for state_ind in state_index_to_brackets[-1]:
                            self.add_transition_to(state_ind, state_counter, "e")
                    state_index_to_brackets.pop()
                    state_index = state_counter
                    close_bracket = True
                open_bracket = False
            elif c == "+":
                state_counter += 1
                if close_bracket:
                    self.add_transition_to_new(state_index, state_counter, "e")
                    transition = self.m_transitions[
                        next(iter(self.m_states[pre_bracket_state_index[-1]].transitions))
                    ]
                    self.add_transition_to(state_counter, pre_bracket_state_index[-1], transition.in_symbol)
                    pre_bracket_state_index.pop()
                else:
                    self.add_transition_to_new(state_index, state_counter, "e")
                    transition = self.m_transitions[
                        next(iter(self.m_states[state_index].transitions))
                    ]
                    self.add_transition_to(state_counter, state_index, transition.in_symbol)

                state_index = state_counter
                open_bracket = False
                close_bracket = False
            elif c == "*":
                state_counter += 1
                if close_bracket:
                    self.add_transition_to_new(state_index, state_counter, "e")
                    transition = self.m_transitions[
                        next(iter(self.m_states[pre_bracket_state_index[-1]].transitions))
                    ]
                    self.add_transition_to(state_index, pre_bracket_state_index[-1], transition.in_symbol)
                    self.add_transition_to(transition.from_state, state_counter, "e")
                    pre_bracket_state_index.pop()
                else:
                    self.add_transition_to_new(state_index, state_counter, "e")
                    transition = self.m_transitions[
                        next(iter(self.m_states[state_index].transitions))
                    ]
                    self.add_transition_to(state_counter, state_index, transition.in_symbol)
                    self.add_transition_to(transition.from_state, state_counter, "e")

                state_index = state_counter
                open_bracket = False
                close_bracket = False
            elif c == "|":
                if close_bracket:
                    pre_bracket_state_index.pop()

                state_index_to_brackets[-1].add(state_index)
                state_index = pre_bracket_state_index[-1]
                open_bracket = False
                close_bracket = False
            else:
                state_counter += 1
                if close_bracket:
                    pre_bracket_state_index.pop()

                self.m_inSymbols.add(c)
                self.add_transition_to_new(state_index, state_counter, c)
                state_index = state_counter
                open_bracket = False
                close_bracket = False

        state_counter += 1
        self.m_states.append(MooreState(f"S{state_counter}", "F"))
        if state_index_to_brackets:
            state_index_to_brackets[-1].add(state_index)

        if state_index_to_brackets and state_index_to_brackets[-1]:
            for state_ind in state_index_to_brackets[-1]:
                self.add_transition_to(state_ind, state_counter, "e")


if __name__ == "__main__":
    import sys

    if len(sys.argv) not in {3, 4}:
        print("Must be program.exe <output_file> regular_expression")
        sys.exit(1)

    output_file = sys.argv[1]
    regular_expression = sys.argv[2]

    if len(sys.argv) == 4:
        output_file = sys.argv[2]
        regular_expression = sys.argv[3]

    rt_nfa = RegexToNFA(regular_expression)
    rt_nfa.write_to_csv_file(output_file)

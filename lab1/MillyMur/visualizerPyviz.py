from pyvis.network import Network


def drawMoore(inputValues, mooreStates, millyInputValue):
    states = list(mooreStates.values())
    transitions = []

    i = 0
    for stateWithOutValue, newState in mooreStates.items():

        j = 0
        for inputValue in inputValues:
            transition = []

            statesToNewState = millyInputValue[inputValue]
            for state, newStateFromMealy in statesToNewState.items():
                millyState = stateWithOutValue.split('/')[0]
                if state == millyState:
                    transition.append(newState)
                    transition.append(newStateFromMealy)
                    transition.append(inputValue)

                    transitions.append(transition)

            j += 1
        i += 1

    net = Network(height='600px', width='100%', bgcolor='white', font_color='black', notebook=True)

    for state in states:
        net.add_node(state, label=state)

    for src, dst, label in transitions:
        net.add_edge(src, dst, title=label)

    net.show('moore_automaton_graph.html')
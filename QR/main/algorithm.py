from graphviz import Digraph
from main.state import Container
from main.utils import DerivativeRules, MagnitudeRules

states = []

sink = Container()
combinations = sink.get_all_combinations()
a = 2


def generate_states(combination, row, column):
    if row > 4:
        state = Container()
        state.set_values(combination)
        states.append(state)
        return

    if column >= len(combinations[row]):
        return

    pair = combinations[row][column]
    combination[row] = pair
    generate_states(combination[:], row + 1, 0)
    generate_states(combination[:], row, column + 1)


def keep_valid_constraint_states(states):
    valid_states = []
    for state in states:
        if state.repsects_constraints():
            valid_states.append(state)
    return valid_states


def keep_valid_relations(states):
    valid_states = []
    for state in states:
        if state.respect_relations():
            valid_states.append(state)
    return valid_states


def is_transition(first, second):
    first_quantities = first.quantities
    second_quantities = second.quantities
    for i in range(0, len(first_quantities)):
        first_derivative = first_quantities[i].derivative
        first_magnitude = first_quantities[i].magnitude

        second_derivative = second_quantities[i].derivative
        second_magnitude = second_quantities[i].magnitude

        # derivative rules
        if second_derivative not in DerivativeRules.derivative_rules[first_derivative]:
            return False
        # check if magnitudes are too distant from each other
        if abs(second_magnitude - first_magnitude) > 1:
            return False
        # checking magnitude rules
        value_space_rules = MagnitudeRules.magnitude_rules[first_magnitude]
        if second_magnitude not in value_space_rules[first_derivative]:
            return False
        return True


def get_transitions(states):
    transitions = []
    for i in range(0, len(states)):
        for j in range(0, len(states)):
            if i != j:
                first = states[i]
                second = states[j]
                if is_transition(first, second):
                    edge = (str(i), str(j))
                    transitions.append(edge)
    return transitions


generate_states([0 for _ in range(len(combinations))], 0, 0)
valid_constraint_states = keep_valid_constraint_states(states)
valid_constraints_relations = keep_valid_relations(valid_constraint_states)
print(len(valid_constraints_relations))

graph = Digraph(format='png')
idx = 0
labels_values = dict()
for state in valid_constraints_relations:
    quantities = state.quantities
    label = ""
    for quantity in quantities:
        label += quantity.name + "_d: " + str(quantity.derivative) + " \n"
        label += quantity.name + "_m: " + str(quantity.magnitude) + " \n"
        labels_values[idx] = label
    graph.node(str(idx), label)
    idx += 1
transitions = get_transitions(valid_constraints_relations)
print(len(transitions))
for t in transitions:
    graph.edge(t[0], t[1])
graph.render('../states', view=True)
